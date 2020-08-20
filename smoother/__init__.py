"""# Smoother"""

from .utils import DerivativeObjective, MassConstraint, MomentConstraint

import numpy as np
from scipy.stats import entropy
from scipy.optimize import Bounds, LinearConstraint, minimize

import json
import math

class Smoother():
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
    def __init__(self, lb=0, ub=1, num=50):
        self.x = np.linspace(lb, ub, num=num)
        self._f_x = np.ones(num)
        
    @property
    def f_x(self):
        return 1 / (self.x[-1]-self.x[0]) * self._f_x
    
    @property
    def F_x(self):
        a = np.cumsum(self._f_x)
        a /= a[-1]
        return a
        # a = np.cumsum(self._f_x[1:])
        # a /= a[-1]
        # return np.insert(a, 0, 0)
    
    def mean(self):
        """
        Returns
        -------
        mean : float
        """
        return self.moment(1)
    
    def var(self):
        """
        Returns
        -------
        variance : float
        """
        return self.moment(2, 'central')
    
    def std(self):
        """
        Returns
        -------
        standard deviation : float
        """
        return self.moment(2, 'central', True)
    
    def median(self):
        """
        Returns
        -------
        median : float
        """
        return self.ppf(.5)
    
    def entropy(self):
        """
        Returns
        -------
        entropy : float
        """
        return entropy(self._f_x)
    
    def pdf(self, x):
        """
        Parameters
        ----------
        x : float

        Returns
        -------
        pdf(x) : float
            Probability density function of `x`.
        """
        if x < self.x[0] or self.x[-1] < x:
            return 0
        lb, w_lb, ub, w_ub = self._get_weights(x)
        return w_lb * self.f_x[lb] + w_ub * self.f_x[ub]
    
    def cdf(self, x):
        """
        Parameters
        ----------
        x : float

        Returns
        -------
        cdf(x) : float between 0. and 1.
            Cumulative distribution function of `x`.
        """
        if x <= self.x[0]:
            return 0
        if self.x[-1] <= x:
            return 1
        lb, w_lb, ub, w_ub = self._get_weights(x)
        # self.F_x is off by a small margin due to numerical approximation
        # this is a hacky fix which helps performance
        lb = max(0, lb-1)
        return w_lb * self.F_x[lb] + w_ub * self.F_x[ub]
        
    def _get_weights(self, x):
        """
        Computes the indices and weights of points on either side of `x`.

        Returns
        -------
        lb, w_lb, ub, w_ub : int, float, int, float
            Index of the 'lower bound', weight on the lower bound, index of 
            the 'upper bound', weight on the upper bound. The weights on the 
            boundary points are based on the linear distance of the points 
            from `x`.
        """
        # lb = arg max_i {self.x[i] : self.x[i] < x}
        # ub = arg min_i {self.x[i] : self.x[i] > x}
        lb, ub  = np.where(self.x<=x)[0][-1], np.where(self.x>=x)[0][0]
        delta = self.x[ub] - self.x[lb]
        return (
            (lb, .5, ub, .5) if delta == 0 
            else (lb, 1 - (x-self.x[lb])/delta, ub, 1 - (self.x[ub]-x)/delta)
        )
    
    def ppf(self, q):
        """
        Parameters
        ----------
        q : float between 0. and 1.
            Quantile.

        Returns
        -------
        ppf(q) : float
            Percent point function; inverse of `self.cdf`.
        """
        def get_ppf(x, i, max_iter=1e2):
            delta = self.cdf(x) - q
            if abs(delta) < 1e-4 or i > max_iter:
                return x
            step_size = (self.x[-1] - self.x[0]) / 2**(i+1)
            x += step_size if delta < 0 else -step_size
            return get_ppf(x, i+1)

        return get_ppf((self.x[0] + self.x[-1])/2, 0)
    
    def sf(self, x):
        """
        Parameters
        ----------
        x : float

        Returns
        -------
        sf(x) : float between 0. and 1.
            Survival function; `1-self.cdf`.
        """
        return 1-self.cdf(x)
    
    def isf(self, q):
        """
        Parameters
        ----------
        q : float between 0. and 1.

        Returns
        -------
        isf(x) : float
            Inverse survival function.
        """
        return self.ppf(1-q)
    
    def moment(self, degree=1, type_='raw', norm=False):
        """
        Parameters
        ----------
        degree : int, default=1
            The degree of the moment, e.g. first (mean), second (var).
        type_ : str, default='raw'
            Type of moment; `'raw'`, `'central'`, or `'standardized'`.
        norm : bool, default=False
            Indicates whether to return the norm of the moment. If `True`, 
            return `moment**(1/degree)`.

        Returns
        -------
        moment : float
        """
        if type_ == 'raw':
            val = (self.x**degree * self._f_x).mean()
        elif type_ == 'central':
            val = ((self.x - self.mean())**degree * self._f_x).mean()
        elif type_ == 'standardized':
            val = (
                ((self.x - self.mean())/self.std())**degree * self._f_x
            ).mean()
        return val**(1/degree) if norm else val
    
    def fit(
            self, lb, ub, constraints, 
            objective=lambda self: self.entropy(), num=50
        ):
        """
        Parameters
        ----------
        lb : float
            Lower bound of the distribution.

        ub : float
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

    def dump(self):
        """
        Returns
        -------
        state_dict : dict
            JSON dump of the state dictionary.
        """
        return json.dumps({
            'x': list(self.x),
            '_f_x': list(self._f_x)
        })

    def load(state_dict):
        """
        Parameters
        ----------
        state_dict : dict
            Output of `Smoother.dump`.

        Returns
        -------
        smoother : Smoother
            Smoother with the specified state dictionary.
        """
        state_dict = json.loads(state_dict)
        smoother = Smoother()
        smoother.x = np.array(state_dict['x'])
        smoother._f_x = np.array(state_dict['_f_x'])
        return smoother