"""Utilities for preparing and storing NARX surrogate-model training setup.

This module contains helper functionality used by the NARX training workflow:

- :func:`create_narx_trajectory` converts one simulated trajectory into
  aligned lagged state/action inputs and next-state targets.
- :class:`Hyperparameters` stores model, data, augmentation, and output-path
  settings and provides convenience methods for creating result directories
  and persisting the configuration.
"""

import numpy as np
import os, pickle, csv
from dataclasses import dataclass

def create_narx_trajectory(trajectory_x: np.ndarray, trajectory_u: np.ndarray, total_number_of_steps: int):
    """Create lagged NARX input/output arrays from one trajectory.

    Parameters
    ----------
    trajectory_x : numpy.ndarray
        State trajectory with shape ``(n_samples, n_x)``. Rows are ordered in
        time.
    trajectory_u : numpy.ndarray
        Input trajectory with shape ``(n_samples, n_u)``. It must have the same
        number of rows as ``trajectory_x``.
    total_number_of_steps : int
        Number of lagged time steps used as NARX inputs. For example, a value
        of ``10`` returns ten state-history arrays and ten input-history arrays.

    Returns
    -------
    narx_input_x : list[numpy.ndarray]
        List of length ``total_number_of_steps``. Entry ``t`` contains the
        state samples shifted by ``t`` steps and truncated so all entries align
        with the same prediction targets.
    narx_input_u : list[numpy.ndarray]
        List of length ``total_number_of_steps`` with action samples aligned to
        ``narx_input_x``.
    narx_output : numpy.ndarray
        Prediction targets with shape ``(n_samples - total_number_of_steps,
        n_x)``. Each row is the state following the corresponding lag window.

    Notes
    -----
    The returned lists are intended to be passed directly to a multi-input
    Keras NARX model after stacking trajectories across the dataset.
    """

    narx_input_x = []
    narx_input_u = []

    for t in range(total_number_of_steps):
        narx_input_x.append(trajectory_x[t:-(total_number_of_steps - t), :])
        narx_input_u.append(trajectory_u[t:-(total_number_of_steps - t), :])

    narx_output = trajectory_x[total_number_of_steps:, :]

    return narx_input_x, narx_input_u, narx_output

@dataclass
class Hyperparameters:
    """Container for NARX training and dataset configuration.

    Attributes
    ----------
    total_number_of_steps : int
        Number of lagged state/action steps used as model inputs.
    n_dense_layers : int
        Number of hidden dense layers in the NARX neural network.
    n_neurons_per_layer : int
        Number of neurons in each hidden dense layer.
    learning_rate : float
        Optimizer learning rate.
    loss : str
        Training loss identifier passed to the model compilation step.
    regularization_l2 : float
        L2 regularization coefficient for trainable model weights.
    n_epochs : int
        Maximum number of training epochs.
    batch_size : int
        Batch size used during model fitting.
    data_path : str
        Path to the pickled dataset used for training.
    model_path : str
        Directory where model artifacts, figures, and hyperparameters are
        stored.
    x_features : list
        Names of state features selected for training.
    u_features : list
        Names of input features selected for training.
    nx : int
        Number of selected state features.
    nu : int
        Number of selected input features.
    train_test_split_ratio : float
        Validation/test split fraction used by the training workflow.
    train_test_split_seed : int
        Random seed for deterministic dataset splitting.
    noise_on_states : numpy.ndarray
        Optional per-state noise magnitudes used for data augmentation.
    n_augmentation : int
        Number of augmented copies generated per trajectory.
    t_step_of_unmodified_data : float
        Sampling time of the original simulated trajectories in seconds.
    t_step_for_model : float
        Effective sampling time of the data used for model training in seconds.
    flags : dict
        Runtime bookkeeping flags. Currently tracks whether :meth:`make_dirs`
        has already been called.
    """

    total_number_of_steps: int = 10
    n_dense_layers: int = 2
    n_neurons_per_layer: int = 256
    learning_rate: float = 0.001
    loss: str = "mse"
    regularization_l2: float = 0.0
    n_epochs: int = 10
    batch_size: int = 2048
    data_path: str = "data.pkl"
    model_path: str = "models"
    x_features: list = None
    u_features: list = None
    nx: int = 0
    nu: int = 0
    train_test_split_ratio: float = 0.2
    train_test_split_seed: int = 42
    noise_on_states: np.ndarray = None
    n_augmentation: int = 0
    t_step_of_unmodified_data: float = 30.0
    t_step_for_model: float = 30.0

    def __init__(self, **kwargs):
        """Initialize the hyperparameter container.

        Parameters
        ----------
        **kwargs
            Keyword overrides for dataclass fields.

        Notes
        -----
        The method also initializes the internal ``flags`` dictionary used by
        :meth:`make_dirs`.
        """

        super().__init__(**kwargs)
        self.flags = {
            "make_dirs_called": False
        }

    def make_dirs(self, overwrite: bool = False):
        """Create the output directory structure for a training run.

        Parameters
        ----------
        overwrite : bool, optional
            If true, keep ``model_path`` even when it already exists and allow
            later artifacts to overwrite existing files. If false and
            ``model_path`` exists, append ``_v<count>`` until an unused path is
            found.

        Notes
        -----
        This method always creates a ``figs`` subdirectory inside the final
        ``model_path`` and sets ``flags["make_dirs_called"]`` to true.
        """

        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path, exist_ok=True)
        else:
            print(f"Directory {self.model_path} already exists.")
            print("Overwrite:", overwrite)
            if overwrite:
                print("Results will be overwritten.")

            else:
                print("Path is renamed to avoid overwriting.")
                print("Old path:", self.model_path)
                old_path = self.model_path
                count = 1
                while os.path.exists(self.model_path) and not self.flags["make_dirs_called"]:
                    self.model_path = f"{old_path}_v{count}"
                    count += 1
                print("New path:", self.model_path)
                os.makedirs(self.model_path, exist_ok=True)
        os.makedirs(os.path.join(self.model_path, "figs"), exist_ok=True)

        self.flags["make_dirs_called"] = True

    def save(self):
        """Persist the hyperparameters to the model directory.

        Writes two files:

        - ``hyperparams.pkl`` contains a pickle dump of this object.
        - ``hyperparams.txt`` contains a line-based human-readable summary of
          dataclass fields.
        """

        with open(os.path.join(self.model_path, "hyperparams.pkl"), "wb") as f:
            pickle.dump(self, f)
        with open(os.path.join(self.model_path, "hyperparams.txt"), "w", newline='') as f:
            writer = csv.writer(f)
            for arg in self.__match_args__:
                if arg != "flags":
                    writer.writerow([f"{arg} = {getattr(self, arg)}"])

    @staticmethod
    def load(filepath: str):
        """Load a previously saved hyperparameter object.

        Parameters
        ----------
        filepath : str
            Path to a ``hyperparams.pkl`` file created by :meth:`save`.

        Returns
        -------
        Hyperparameters
            Deserialized hyperparameter object.
        """

        with open(filepath, "rb") as f:
            hyperparams = pickle.load(f)
        return hyperparams

