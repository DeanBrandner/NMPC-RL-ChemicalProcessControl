"""Gradient-ascent optimizers for RL parameter updates.

The classes in this module provide the small optimizer interface used by the
RL-MPC agents. Each optimizer receives a gradient and returns an ascent update
with any optimizer state that is useful for logging.
"""

import numpy as np

class StochasticGradientAscent:
    """Plain stochastic gradient-ascent update rule."""

    def __init__(self, learning_rate: float):
        """Initialize the optimizer.

        Parameters
        ----------
        learning_rate : float
            Scalar step size applied to each gradient update.
        """
        self.learning_rate = learning_rate
        self.step_counter = 0

    def __repr__(self):
        return f"StochasticGradientAscent(lr={self.learning_rate})"

    def compute_update(self, grad: np.ndarray) -> np.ndarray:
        """Compute one ascent update from a gradient.

        Parameters
        ----------
        grad : numpy.ndarray
            Gradient of the objective with respect to the optimized
            parameters.

        Returns
        -------
        update : numpy.ndarray
            Parameter update to add to the current parameters.
        m_hat : numpy.ndarray
            Raw gradient, returned for a consistent optimizer interface.
        v_hat : None
            Placeholder for optimizers that maintain a second-moment estimate.
        """
        if not isinstance(grad, np.ndarray):
            raise TypeError(f"Expected numpy array, got {type(grad)}")
        update = self.learning_rate * grad
        self.step_counter += 1
        return update, grad, None

class Adam:
    """Adam-style ascent optimizer for RL parameter updates."""

    def __init__(self, learning_rate: float, beta1: float = 0.9, beta2: float = 0.999, epsilon: float = 1e-8):
        """Initialize the optimizer state.

        Parameters
        ----------
        learning_rate : float
            Scalar step size applied to normalized updates.
        beta1 : float, optional
            First-moment smoothing coefficient.
        beta2 : float, optional
            Second-moment smoothing coefficient.
        epsilon : float, optional
            Small positive value used in the denominator for numerical
            stability.
        """
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = None
        self.v = None
        self.step_counter = 0

    def __repr__(self):
        return f"AdamOptimizer(lr={self.learning_rate}, beta1={self.beta1}, beta2={self.beta2}, epsilon={self.epsilon})"

    def compute_update(self, grad: np.ndarray) -> np.ndarray:
        """Compute one ascent update from a gradient.

        Parameters
        ----------
        grad : numpy.ndarray
            Gradient of the objective with respect to the optimized
            parameters.

        Returns
        -------
        update : numpy.ndarray
            Parameter update to add to the current parameters.
        m_hat : numpy.ndarray
            Bias-corrected first-moment estimate.
        v_hat : numpy.ndarray
            Bias-corrected second-moment estimate.
        """
        if not isinstance(grad, np.ndarray):
            raise TypeError(f"Expected numpy array, got {type(grad)}")
        if self.m is None:
            self.m = np.zeros_like(grad)
            self.v = np.zeros_like(grad)

        self.m = self.beta1 * self.m + (1 - self.beta1) * grad
        self.v = self.beta2 * self.v + (1 - self.beta2) * (grad ** 2)

        m_hat = self.m / (1 - self.beta1 ** (self.step_counter + 1))
        v_hat = self.v / (1 - self.beta2 ** (self.step_counter + 1))

        update = self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)
        self.step_counter += 1
        return update, m_hat, v_hat
