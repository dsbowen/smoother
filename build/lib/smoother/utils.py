"""# Objective functions and constraints"""

import numpy as np


class DerivativeObjective():
    """
    A `Smoother` objective function which minimizes the sum of a square
    derivative.

    Parameters and attributes
    -------------------------
    d : int, default=1
        e.g. `1` means first derivative, `2` means second derivative.
    """
    def __init__(self, d=1, weight=None):
        self.d = d
        self.weight = weight
        
    def __call__(self, smoother):
        """
        Parameters
        ----------
        smoother : `Smoother`
            The smoother to which this objective function applies.

        Returns
        -------
        value : float
            Approximate mean square derivative over all points of the
            distribution.
        """
        weight = 1e-3/self.d**2 if self.weight is None else self.weight
        delta = 1 / smoother.x.shape[0]
        deriv = np.diff(smoother._f_x, n=self.d) / delta**self.d
        return -weight*(deriv**2).mean()


class MassConstraint():
    """
    A `Smoother` constraint that forces a certain amount of probability mass
    to be within a given range.

    Parameters and attributes
    -------------------------
    lb : float
        Lower bound of the range within which the probability mass must be.

    ub : float
        Upper bound of the range within which the probability mass must be.

    mass : float between 0. and 1.
        Amount of probability mass between `lb` and `ub`.

    weight : float or None, default=None
        Weight to place on the constraint. If `None` the weight will be set
        automatically when the constraint is called based on the smoother.
    """
    def __init__(self, lb, ub, mass, weight=None):
        self.lb, self.ub = lb, ub
        self.mass = mass
        self.weight = weight
        
    def __call__(self, smoother):
        """
        Parameters
        ----------
        smoother : Smoother
            Smoother to which this constraint applies.

        Returns
        -------
        loss : float
        """
        weight = 5e2 if self.weight is None else self.weight
        curr_mass = smoother.cdf(self.ub) - smoother.cdf(self.lb)
        return weight * (curr_mass - self.mass)**2


class MomentConstraint():
    """
    A `Smoother` constraint that forces a moment condition to hold.

    Parameters and attributes
    -------------------------
    value : float
        The target value of the moment.

    degree : int
        The degree of the moment; e.g. the 1st moment is the mean.

    type_ : str, default='raw'
        Type of moment: `'raw'`, `'central'` or `'standardized'`.

    norm : bool, default=False
        Indicates whether to apply a norm to the moment.

    weight : float or None, default=None
        Weight to place on the constraint. If `None` the weight will be set
        automatically when the constraint is called based on the smoother.
    """
    def __init__(self, value, degree, type_='raw', norm=False, weight=None):
        self.value = value
        self.degree = degree
        self.type_ = type_
        self.norm = norm
        self.weight = weight
        
    def __call__(self, smoother):
        """
        Parameters
        ----------
        smoother : Smoother
            Smoother to which this constraint applies.

        Returns
        -------
        loss : float
        """
        weight = (
            5e2 / (smoother.x[-1] - smoother.x[0])**2 if self.weight is None
            else self.weight
        )
        moment = smoother.moment(self.degree, self.type_, self.norm)
        return weight * (moment - self.value)**2