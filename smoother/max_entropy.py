"""# Maximum entropy distribution"""

from .smoother import Smoother

import numpy as np
from scipy.optimize import minimize
from scipy.integrate import quad


class MaxEntropy(Smoother):
    """
    Computes a maximum entropy distribution given moment constraints. Inherits 
    from `Smoother`. The only difference is that the `fit` method is optimized 
    but more restrictive.

    Examples
    --------
    This example approximates a standard normal distribution.

    ```python
    import matplotlib.pyplot as plt
    from smoother import MaxEntropy

    dist = MaxEntropy()
    mu, sigma2 = 0, 1
    dist.fit(-3, 3, [lambda x: x, lambda x: (x-mu)**2], [mu, sigma2])
    plt.plot(dist.x, dist.f_x)
    ```

    Notes
    -----
    See 
    <https://en.wikipedia.org/wiki/Maximum_entropy_probability_distribution#Continuous_case>
    for mathematical detail.
    """
    def fit(self, lb, ub, moment_funcs, values, num=50):
        """
        Parameters
        ----------
        lb : scalar
            Lower bound of the distribution.

        ub : scalar
            Upper bound of the distribution.

        moment_funcs : list of callable
            List of moment functions. e.g. for the mean, use `lambda x: x`.

        values : list of scalars
            List of values the expected value of the moment functions should 
            evaluate to.

        num : int, default=50
            Number of points on the distribution used for approximation.

        Returns
        -------
        self
        """
        self.x = np.linspace(lb, ub, num)
        self._moment_funcs = moment_funcs + [lambda x: 1]
        self._values = values + [1]
        res = minimize(self._loss, [0]*(len(moment_funcs)+1))
        self._f_x = (ub - lb) * self._pdf(self.x, res.x)
        del self._moment_funcs, self._values
        return self
        
    def _pdf(self, x, params):
        return np.exp(
            sum([param*f(x) for param, f in zip(params, self._moment_funcs)])
        )
    
    def _loss(self, params):
        constraint_loss = sum(
            [param*val for param, val in zip(params, self._values)]
        )
        integral = quad(self._pdf, self.x[0], self.x[-1], params)[0]
        return integral - constraint_loss