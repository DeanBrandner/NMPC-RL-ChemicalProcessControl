"""Convert trained Keras NARX models into do-mpc symbolic models.

The helpers in this module rebuild a trained surrogate as a do-mpc ``Model``
so it can be embedded in simulation or optimization workflows. The conversion
preserves the NARX shift-register structure encoded by the Keras model inputs
and optionally adds reinforcement-learning corrective terms.
"""

import os, pickle
from narx_functions import Hyperparameters
from keras.saving import load_model

from _model_for_rl import RL_Model as do_mpc_Model
import casadi as cd

def cdf_gauss(x):
    """Return the standard normal cumulative distribution function."""
    return 0.5 * (1.0 + cd.erf(x / cd.sqrt(2.0)))

def gelu(x):
    """Return the Gaussian error linear unit activation."""
    return x * cdf_gauss(x)

def transform_keras_to_do_mpc(keras_model, scaler_x, scaler_u, hyperparameters: Hyperparameters):
    """Convert a trained NARX Keras model into a plain do-mpc model.

    Parameters
    ----------
    keras_model : keras.Model
        Trained Keras model whose inputs follow the ``input_x_t-*`` and
        ``input_u_t-*`` naming convention.
    scaler_x : object
        Feature scaler for state inputs. Must expose ``scale_`` and ``min_``.
    scaler_u : object
        Feature scaler for control inputs. Must expose ``scale_`` and ``min_``.
    hyperparameters : Hyperparameters
        NARX configuration object. ``total_number_of_steps`` defines the shift
        register depth.

    Returns
    -------
    RL_Model
        do-mpc model that reproduces the trained surrogate dynamics.
    """

    do_mpc_model = do_mpc_Model(model_type="discrete")

    x_states = {}
    u_inputs = {}
    for input_item in keras_model.inputs:
        if "x_t" in input_item.name:
            state_name = input_item.name.split("input_")[1]
            x_states[state_name] = do_mpc_model.set_variable(var_type="_x", var_name=state_name, shape=(input_item.shape[1], 1))
        elif "u_t" in input_item.name:
            if input_item.name == "input_u_t-1":
                input_name = input_item.name.split("input_")[1]
                u_inputs[input_name] = do_mpc_model.set_variable(var_type="_u", var_name=input_name, shape=(input_item.shape[1], 1))
            else:
                state_name = input_item.name.split("input_")[1]
                x_states[state_name] = do_mpc_model.set_variable(var_type="_x", var_name=state_name, shape=(input_item.shape[1], 1))


    # First do the nice NARX dynamics
    for idx in range(hyperparameters.total_number_of_steps, 1, -1):
        state_name = f"x_t-{idx}"
        do_mpc_model.set_rhs(var_name = state_name, expr = x_states[f"x_t-{idx-1}"])

        state_name = f"u_t-{idx}"
        if idx == 2:
            do_mpc_model.set_rhs(var_name = state_name, expr = u_inputs[f"u_t-{idx-1}"])
        else:
            do_mpc_model.set_rhs(var_name = state_name, expr = x_states[f"u_t-{idx-1}"])


    x_scaled = {}
    for state_name, x_state in x_states.items():
        if "x" in state_name:
            x_state_scaled = scaler_x.scale_.reshape(-1, 1) * x_state + scaler_x.min_.reshape(-1, 1)
            x_scaled[state_name] = x_state_scaled
        elif "u" in state_name:
            u_state_scaled = scaler_u.scale_.reshape(-1, 1) * x_state + scaler_u.min_.reshape(-1, 1)
            x_scaled[state_name] = u_state_scaled
        else:
            pass

    u_scaled = {}
    for input_name, u_input in u_inputs.items():
        u_input_scaled = scaler_u.scale_.reshape(-1, 1) * u_input + scaler_u.min_.reshape(-1, 1)
        u_scaled[input_name] = u_input_scaled


    stacked_nn_input_scaled = []
    for input_item in keras_model.inputs:
        if "x_t" in input_item.name or "u_t" in input_item.name:
            state_name = input_item.name.split("input_")[1]
            if state_name in x_scaled.keys():
                stacked_nn_input_scaled.append(x_scaled[state_name])
            elif state_name in u_scaled.keys():
                stacked_nn_input_scaled.append(u_scaled[state_name])

    nn_input_concatenated = cd.vertcat(*stacked_nn_input_scaled)


    nn_output_scaled = nn_input_concatenated
    for layer in keras_model.layers:
        if "input" in layer.name:
            continue
        
        weights, biases = layer.get_weights()
        weights_casadi = weights.T
        biases_casadi = biases.reshape(-1, 1)
        nn_output_scaled = weights_casadi @ nn_output_scaled + biases_casadi
        if layer.activation.__name__ == "relu":
            nn_output_scaled = cd.fmax(nn_output_scaled, 0)
        elif layer.activation.__name__ == "linear":
            pass
        elif layer.activation.__name__ == "tanh":
            nn_output_scaled = cd.tanh(nn_output_scaled)
        elif layer.activation.__name__ == "gelu":
            nn_output_scaled = gelu(nn_output_scaled)
        else:
            raise NotImplementedError(f"Activation {layer.activation.__name__} not implemented in do-mpc transformation.")

    nn_output = (nn_output_scaled - scaler_x.min_.reshape(-1, 1)) / scaler_x.scale_.reshape(-1, 1)

    do_mpc_model.set_rhs(var_name = "x_t-1", expr = nn_output)

    # Transform the Keras model to a do-mpc model
    return do_mpc_model


def transform_keras_to_do_mpc_for_rl(keras_model, scaler_x, scaler_u, hyperparameters: Hyperparameters):
    """Convert a trained NARX Keras model into an RL-aware do-mpc model.

    This variant adds reinforcement-learning parameters for corrective matrices
    and backoff terms while preserving the base NARX shift-register dynamics.
    """

    do_mpc_model = do_mpc_Model(model_type="discrete")

    x_states = {}
    u_inputs = {}
    for input_item in keras_model.inputs:
        if "x_t" in input_item.name:
            state_name = input_item.name.split("input_")[1]
            x_states[state_name] = do_mpc_model.set_variable(var_type="_x", var_name=state_name, shape=(input_item.shape[1], 1))
        elif "u_t" in input_item.name:
            if input_item.name == "input_u_t-1":
                input_name = input_item.name.split("input_")[1]
                u_inputs[input_name] = do_mpc_model.set_variable(var_type="_u", var_name=input_name, shape=(input_item.shape[1], 1))
            else:
                state_name = input_item.name.split("input_")[1]
                x_states[state_name] = do_mpc_model.set_variable(var_type="_x", var_name=state_name, shape=(input_item.shape[1], 1))


    # First do the nice NARX dynamics
    for idx in range(hyperparameters.total_number_of_steps, 1, -1):
        state_name = f"x_t-{idx}"
        do_mpc_model.set_rhs(var_name = state_name, expr = x_states[f"x_t-{idx-1}"])

        state_name = f"u_t-{idx}"
        if idx == 2:
            do_mpc_model.set_rhs(var_name = state_name, expr = u_inputs[f"u_t-{idx-1}"])
        else:
            do_mpc_model.set_rhs(var_name = state_name, expr = x_states[f"u_t-{idx-1}"])


    x_scaled = {}
    for state_name, x_state in x_states.items():
        if "x" in state_name:
            x_state_scaled = scaler_x.scale_.reshape(-1, 1) * x_state + scaler_x.min_.reshape(-1, 1)
            x_scaled[state_name] = x_state_scaled
        elif "u" in state_name:
            u_state_scaled = scaler_u.scale_.reshape(-1, 1) * x_state + scaler_u.min_.reshape(-1, 1)
            x_scaled[state_name] = u_state_scaled
        else:
            pass

    u_scaled = {}
    for input_name, u_input in u_inputs.items():
        u_input_scaled = scaler_u.scale_.reshape(-1, 1) * u_input + scaler_u.min_.reshape(-1, 1)
        u_scaled[input_name] = u_input_scaled


    stacked_nn_input_scaled = []
    for input_item in keras_model.inputs:
        if "x_t" in input_item.name or "u_t" in input_item.name:
            state_name = input_item.name.split("input_")[1]
            if state_name in x_scaled.keys():
                stacked_nn_input_scaled.append(x_scaled[state_name])
            elif state_name in u_scaled.keys():
                stacked_nn_input_scaled.append(u_scaled[state_name])

    nn_input_concatenated = cd.vertcat(*stacked_nn_input_scaled)


    nn_output_scaled = nn_input_concatenated
    for idx, layer in enumerate(keras_model.layers):
        if "input" in layer.name:
            continue
        
        weights, biases = layer.get_weights()
        weights_casadi = weights.T
        biases_casadi = biases.reshape(-1, 1)
        if idx == len(keras_model.layers) - 1:
            last_layer_weights_parameters= cd.DM.zeros(weights_casadi.shape)
            last_layer_biases_parameters = cd.DM.zeros(biases_casadi.shape)
            
            nn_output_scaled = (weights_casadi + last_layer_weights_parameters) @ nn_output_scaled + (biases_casadi + last_layer_biases_parameters)
        else:
            nn_output_scaled = weights_casadi @ nn_output_scaled + biases_casadi
        if layer.activation.__name__ == "relu":
            nn_output_scaled = cd.fmax(nn_output_scaled, 0)
        elif layer.activation.__name__ == "linear":
            pass
        elif layer.activation.__name__ == "tanh":
            nn_output_scaled = cd.tanh(nn_output_scaled)
        elif layer.activation.__name__ == "gelu":
            nn_output_scaled = gelu(nn_output_scaled)
        else:
            raise NotImplementedError(f"Activation {layer.activation.__name__} not implemented in do-mpc transformation.")
        
    corrective_A_mat = do_mpc_model.set_variable(var_type="_rlp", var_name="corrective_A_mat", shape=(nn_output_scaled.shape[0], nn_output_scaled.shape[0]))
    corrective_B_mat = do_mpc_model.set_variable(var_type="_rlp", var_name="corrective_B_mat", shape=(nn_output_scaled.shape[0], u_scaled["u_t-1"].shape[0]))
    
    nn_output_scaled = nn_output_scaled + corrective_A_mat @ x_scaled["x_t-1"] + corrective_B_mat @ u_scaled["u_t-1"]

    nn_output = (nn_output_scaled - scaler_x.min_.reshape(-1, 1)) / scaler_x.scale_.reshape(-1, 1)

    x_B_backoff = do_mpc_model.set_variable(var_type="_rlp", var_name="x_B_backoff", shape=(1,1))
    distillate_mass_backoff = do_mpc_model.set_variable(var_type="_rlp", var_name="distillate_mass_backoff", shape=(1,1))


    do_mpc_model.set_rhs(var_name = "x_t-1", expr = nn_output)

    

    # Transform the Keras model to a do-mpc model
    return do_mpc_model

def transform_keras_to_do_mpc_for_rl_with_num_time(keras_model, scaler_x, scaler_u, hyperparameters: Hyperparameters):
    """Convert a trained NARX Keras model into an RL-aware do-mpc model.

    Compared with :func:`transform_keras_to_do_mpc_for_rl`, this version also
    tracks the previous control action and an explicit numerical time state in
    the do-mpc model.
    """

    do_mpc_model = do_mpc_Model(model_type="discrete")

    x_states = {}
    u_inputs = {}
    for input_item in keras_model.inputs:
        if "x_t" in input_item.name:
            state_name = input_item.name.split("input_")[1]
            x_states[state_name] = do_mpc_model.set_variable(var_type="_x", var_name=state_name, shape=(input_item.shape[1], 1))
        elif "u_t" in input_item.name:
            if input_item.name == "input_u_t-1":
                input_name = input_item.name.split("input_")[1]
                u_inputs[input_name] = do_mpc_model.set_variable(var_type="_u", var_name=input_name, shape=(input_item.shape[1], 1))
            else:
                state_name = input_item.name.split("input_")[1]
                x_states[state_name] = do_mpc_model.set_variable(var_type="_x", var_name=state_name, shape=(input_item.shape[1], 1))


    # First do the nice NARX dynamics
    for idx in range(hyperparameters.total_number_of_steps, 1, -1):
        state_name = f"x_t-{idx}"
        do_mpc_model.set_rhs(var_name = state_name, expr = x_states[f"x_t-{idx-1}"])

        state_name = f"u_t-{idx}"
        if idx == 2:
            do_mpc_model.set_rhs(var_name = state_name, expr = u_inputs[f"u_t-{idx-1}"])
        else:
            do_mpc_model.set_rhs(var_name = state_name, expr = x_states[f"u_t-{idx-1}"])


    x_scaled = {}
    for state_name, x_state in x_states.items():
        if "x" in state_name:
            x_state_scaled = scaler_x.scale_.reshape(-1, 1) * x_state + scaler_x.min_.reshape(-1, 1)
            x_scaled[state_name] = x_state_scaled
        elif "u" in state_name:
            u_state_scaled = scaler_u.scale_.reshape(-1, 1) * x_state + scaler_u.min_.reshape(-1, 1)
            x_scaled[state_name] = u_state_scaled
        else:
            pass

    u_scaled = {}
    for input_name, u_input in u_inputs.items():
        u_input_scaled = scaler_u.scale_.reshape(-1, 1) * u_input + scaler_u.min_.reshape(-1, 1)
        u_scaled[input_name] = u_input_scaled


    stacked_nn_input_scaled = []
    for input_item in keras_model.inputs:
        if "x_t" in input_item.name or "u_t" in input_item.name:
            state_name = input_item.name.split("input_")[1]
            if state_name in x_scaled.keys():
                stacked_nn_input_scaled.append(x_scaled[state_name])
            elif state_name in u_scaled.keys():
                stacked_nn_input_scaled.append(u_scaled[state_name])

    nn_input_concatenated = cd.vertcat(*stacked_nn_input_scaled)


    nn_output_scaled = nn_input_concatenated
    for idx, layer in enumerate(keras_model.layers):
        if "input" in layer.name:
            continue
        
        weights, biases = layer.get_weights()
        weights_casadi = weights.T
        biases_casadi = biases.reshape(-1, 1)
        if idx == len(keras_model.layers) - 1:
            last_layer_weights_parameters= cd.DM.zeros(weights_casadi.shape)
            last_layer_biases_parameters = cd.DM.zeros(biases_casadi.shape)
            
            nn_output_scaled = (weights_casadi + last_layer_weights_parameters) @ nn_output_scaled + (biases_casadi + last_layer_biases_parameters)
        else:
            nn_output_scaled = weights_casadi @ nn_output_scaled + biases_casadi
        if layer.activation.__name__ == "relu":
            nn_output_scaled = cd.fmax(nn_output_scaled, 0)
        elif layer.activation.__name__ == "linear":
            pass
        elif layer.activation.__name__ == "tanh":
            nn_output_scaled = cd.tanh(nn_output_scaled)
        elif layer.activation.__name__ == "gelu":
            nn_output_scaled = gelu(nn_output_scaled)
        else:
            raise NotImplementedError(f"Activation {layer.activation.__name__} not implemented in do-mpc transformation.")
        
    corrective_A_mat = do_mpc_model.set_variable(var_type="_rlp", var_name="corrective_A_mat", shape=(nn_output_scaled.shape[0], nn_output_scaled.shape[0]))
    corrective_B_mat = do_mpc_model.set_variable(var_type="_rlp", var_name="corrective_B_mat", shape=(nn_output_scaled.shape[0], u_scaled["u_t-1"].shape[0]))
    
    nn_output_scaled = nn_output_scaled + corrective_A_mat @ x_scaled["x_t-1"] + corrective_B_mat @ u_scaled["u_t-1"]

    nn_output = (nn_output_scaled - scaler_x.min_.reshape(-1, 1)) / scaler_x.scale_.reshape(-1, 1)

    x_B_backoff = do_mpc_model.set_variable(var_type="_rlp", var_name="x_B_backoff", shape=(1,1))
    distillate_mass_backoff = do_mpc_model.set_variable(var_type="_rlp", var_name="distillate_mass_backoff", shape=(1,1))


    do_mpc_model.set_rhs(var_name = "x_t-1", expr = nn_output)

    do_mpc_model.set_variable(var_type="_x", var_name = "u_prev", shape=(u_scaled["u_t-1"].shape[0], 1))
    do_mpc_model.set_rhs(var_name = "u_prev", expr = u_inputs["u_t-1"])

    numerical_time = do_mpc_model.set_variable(var_type="_x", var_name="numerical_time", shape=(1,1))
    delta_t = do_mpc_model.set_variable(var_type="_p", var_name="delta_t", shape=(1,1))
    do_mpc_model.set_rhs(var_name="numerical_time", expr = numerical_time + delta_t)

    # Transform the Keras model to a do-mpc model
    return do_mpc_model




if __name__ == "__main__":
    model_path = os.path.join("surr_models", "260506_141325_Sampling_1000", "narx_1step")
    print("You want to load the keras model at ", model_path)
    hyperparams = Hyperparameters.load(os.path.join(model_path, "hyperparams.pkl"))

    with open(os.path.join(model_path, "scaler_x.pkl"), "rb") as f:
        scaler_x = pickle.load(f)
    with open(os.path.join(model_path, "scaler_u.pkl"), "rb") as f:
        scaler_u = pickle.load(f)

    keras_model = load_model(os.path.join(model_path, "narx_model.keras"))
    keras_model.load_weights(os.path.join(model_path, "best_weights.weights.h5"))

    print("Successfully loaded Keras model and scalers. Now transforming to do-mpc model...")
    do_mpc_model = transform_keras_to_do_mpc(keras_model, scaler_x, scaler_u, hyperparams)
    do_mpc_model.setup()

    with open(os.path.join(model_path, "do_mpc_model.pkl"), "wb") as f:
        pickle.dump(do_mpc_model, f)

    print("Successfully transformed to do-mpc model and saved. Now transforming to RL-aware do-mpc model...")
    do_mpc_model_rl = transform_keras_to_do_mpc_for_rl(keras_model, scaler_x, scaler_u, hyperparams)

    do_mpc_model_rl.setup()
    with open(os.path.join(model_path, "do_mpc_model_rl.pkl"), "wb") as f:
        pickle.dump(do_mpc_model_rl, f)


    print("Successfully transformed to RL-aware do-mpc model and saved. Now transforming to RL-aware do-mpc model with numerical time...")
    do_mpc_model_rl_with_num_time = transform_keras_to_do_mpc_for_rl_with_num_time(keras_model, scaler_x, scaler_u, hyperparams)
    do_mpc_model_rl_with_num_time.setup()
    with open(os.path.join(model_path, "do_mpc_model_rl_with_num_time.pkl"), "wb") as f:
        pickle.dump(do_mpc_model_rl_with_num_time, f)
