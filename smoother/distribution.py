import numpy as np
from scipy.stats import entropy

import json
import random


class Distribution():
    def __init__(self, x=None, f_x=None):
        self.x = np.linspace(0, 1) if x is None else x
        self.f_x = np.ones(self.x.shape) if f_x is None else f_x

    @property
    def f_x(self):
        return self._f_x

    @f_x.setter
    def f_x(self, f_x):
        s = (f_x * (self.x[-1] - self.x[0]) / self.x.shape[0]).sum()
        self._f_x = f_x / s
    
    @property
    def F_x(self):
        """
        Explanation of expression:
        
        F_x[1] = integral_0^d f_x[0] + (f_x[1]-f_x[0])/d * x dx
        = [f_x[0]*x + (f_x[1]-f_x[0])/d * x^2]_0^d
        = 1/2 * (f_x[0] + f_x[1]) * d
        This is f_x[:-1] + f_x[1:]
        We normalize in the end, so we can leave off 1/2 and d.

        F_x[0] = 0
        This is np.insert(f_x, 0, 0)
        """
        f_x = np.insert(self._f_x[:-1] + self._f_x[1:], 0, 0)
        a = np.cumsum(f_x)
        return a / a[-1]

    def rvs(self, size=1):
        """
        Parameters
        ----------
        size : int, default=1
            Size of the output vector.

        Returns
        -------
        sample : np.array or scalar
            Vector of random samples from the distribution. If `size` is 1,
            return a scalar.
        """
        x = [self.ppf(random.random()) for _ in range(size)]
        return x[0] if size == 1 else np.array(x)
    
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
        def pdf(x):
            if x < self.x[0] or self.x[-1] < x:
                return 0
            lb, w_lb, ub, w_ub = self._get_weights(x)
            return w_lb * self.f_x[lb] + w_ub * self.f_x[ub]

        if isinstance(x, (int, float)):
            return pdf(x)
        if isinstance(x, list):
            return [pdf(x_i) for x_i in x]
        if isinstance(x, np.ndarray):
            return np.array([pdf(x_i) for x_i in x])
    
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
        def cdf(x):
            if x <= self.x[0]:
                return 0
            if self.x[-1] <= x:
                return 1
            lb, w_lb, ub, w_ub = self._get_weights(x)
            return w_lb * self.F_x[lb] + w_ub * self.F_x[ub]

        if isinstance(x, (int, float)):
            return cdf(x)
        if isinstance(x, list):
            return [cdf(x_i) for x_i in x]
        if isinstance(x, np.ndarray):
            return np.array([cdf(x_i) for x_i in x])
        
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
        def ppf(q):
            def get_ppf(x, i, max_iter=1e2):
                delta = self.cdf(x) - q
                if abs(delta) < 1e-4 or i > max_iter:
                    return x
                step_size = (self.x[-1] - self.x[0]) / 2**(i+1)
                x += step_size if delta < 0 else -step_size
                return get_ppf(x, i+1)

            if q == 0:
                return self.x[0]
            if q == 1:
                return self.x[-1]
            return get_ppf((self.x[0] + self.x[-1])/2, 0)

        if isinstance(q, (int, float)):
            return ppf(q)
        if isinstance(q, list):
            return [ppf(q_i) for q_i in q]
        if isinstance(q, np.ndarray):
            return np.array([ppf(q_i) for q_i in q])
    
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
            val = self.x
        elif type_ == 'central':
            val = self.x - self.mean()
        elif type_ == 'standardized':
            val = (self.x - self.mean()) / self.std()
        val = (val**degree * self._f_x).mean()
        return val**(1/degree) if norm else val

    def dump(self):
        """
        Returns
        -------
        state_dict : dict
            JSON dump of the state dictionary.
        """
        return json.dumps({
            'x': list(self.x),
            'f_x': list(self.f_x)
        })

    @classmethod
    def load(cls, state_dict):
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
        instance = cls(
            np.array(state_dict['x']), 
            np.array(state_dict['f_x'])
        )
        return instance