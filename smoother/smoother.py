"""# Smoother"""

from .distribution import Distribution

import numpy as np
from scipy.stats import entropy
from scipy.optimize import Bounds, LinearConstraint, minimize

import json
import math
from random import random

class Smoother(Distribution):
    """
    The smoother computes a distribution by maximizing an objective function
    (i.e. a smoothness function) given constraints.

    Attributes
    ----------
    x : np.array
        A linearly spaced (`self.num`,) array of points between the lower and 
        upper bounds of the distribution.

    f_x : np.array
        The probability density function of `self.x`.

    F_x : np.array
        The cumulative distribution function of `self.x`.
    """    
    def fit(
            self, lb, ub, constraints, 
            objective=lambda self: self.entropy(), num=50
        ):
        """
        Parameters
        ----------
        lb : scalar
            Lower bound of the distribution.

        ub : scalar
            Upper bound of the distribution.

        constraints : list of callables
            Constraints take in a `Smoother` and return a float. Lower values
            indicate that the constraints are satisfied.

        objective : callable, default=lambda self: self.entropy()
            The objective or smoothing function. The objective function takes 
            a `Smoother` and returns a float. This objective function is
            maximized subject to constraints. By default, it maximizes 
            entropy.

        num : int, default=50
            Number of points on the distribution used for approximation.

        Returns
        -------
        self
        """
        self.x = np.linspace(lb, ub, num=num)
        self._f_x = np.ones(num) / (ub-lb)
        self._constraints = constraints
        self._objective = objective
        bounds = Bounds([0]*num, [np.inf]*num)
        integral_cons = LinearConstraint(1/num * np.ones((1, num)), [1], [1])
        minimize(
            self._loss, 
            self._f_x, 
            constraints=[integral_cons], 
            bounds=bounds,
            options={'disp': False}
        )
        del self._constraints, self._objective
        return self

    def _loss(self, f_x=None):
        """
        Parameters
        ----------
        f_x : np.array or None, default=None
            Resets `self._f_x`; users should avoid passing this parameter.

        Returns
        -------
        loss : float
            Loss is the negative of the objective function plus loss from
            constraints.
        """
        self._f_x = self._f_x if f_x is None else f_x
        constraint_loss = sum([constraint(self) for constraint in self._constraints])
        return -self._objective(self) + constraint_loss