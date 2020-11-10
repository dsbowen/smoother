"""# Conditional distribution

A `ConditionalDistribution` estimates the conditional distribution p(y|x) for
any x using known conditional distributions for a sample of x's.

The known conditional distributions are objects with the following methods, as
defined in `scipy.stats`:

- `pdf`
- `cdf`
- `ppf`
"""

from .distribution import Distribution

import numpy as np
from sklearn.metrics.pairwise import pairwise_kernels

import json


def linspace(distributions, num=50):
    """
    Parameters
    ----------
    distributions : list of distribution objects
        
    num : int, default=50
        Number of points to sample in the linear space.
    """
    def get_lb(dist):
        lb = dist.ppf(0)
        return lb if lb != -np.inf else dist.ppf(.01)

    def get_ub(dist):
        ub = dist.ppf(1)
        return ub if ub != np.inf else dist.ppf(.99)

    start = min([get_lb(dist) for dist in distributions])
    stop = max([get_ub(dist) for dist in distributions])
    return np.linspace(start, stop, num)
    
def wasserstein(true_dist, estimated_dist, num=50):
    """
    Parameters
    ----------
    true_dist : distribution

    estimated_dist : distribution
    
    num : int, default=50
    
    Returns
    -------
    distance : float
        Negative Wasserstein distance between the true and estimated 
        distributions.
    """
    x = linspace([true_dist, estimated_dist], num)
    true_cdf, estimated_cdf = true_dist.cdf(x), estimated_dist.cdf(x)
    return -abs(true_cdf - estimated_cdf).sum() * (x[-1] - x[0]) / num
    
metrics = dict(
    wasserstein=wasserstein
)


class ConditionalDistribution():
    """
    Parameters and attributes
    -------------------------
    metric : str
        Type of kernel to use. See `sklearn.pairwise.pairwise_kernels`

    gamma : float, default=1
        `gamma` parameter for the kernel.

    coef0 : float, default=1
        `coef0` parameter for the kernel.

    feature_scale : float or (# conditional features,) np.array
        Scaling parameters for the features on which the distribution is 
        conditional.

    eval_metric : str or callable, default='wasserstein'
        Metric to use for scoring the conditional distribution. Currently,
        only `'wasserstein'` is implemented.

    Additional attributes
    ---------------------
    given : (# known distributions x # conditional features) np.array
        Each row are the values of the features on which the distribution is 
        conditioned. This is set during `fit`.

    x : np.array
        Linearly spaced over the support of the conditional distribution. Set
        during `fit`.

    f_x : (# known distributions x shape of `x`) np.array
        PDF of the known distributions for the points in `x`. Set during 
        `fit`.
    """
    def __init__(
            self, metric='linear', gamma=1, coef0=1, feature_scale=1, 
            eval_metric='wasserstein'
        ):
        self.metric = metric
        self.gamma = gamma
        self.coef0 = coef0
        self.feature_scale = feature_scale
        self.eval_metric = eval_metric
        self.given, self.x, self.f_x = None, None, None
        
    def fit(self, given, distributions, num=50):
        """
        Fit the conditional distribution using know conditional distributions.

        Parameters
        ----------
        given : (# known distributions x # conditional features) np.array
            Sets the `given` attribute.

        distributions : list of distribution objects
            Known conditional distributions.

        num : int, default=50
            Number of points used to approximate conditional distributions.

        Returns
        -------
        self
        """
        self.given = given
        self.x = linspace(distributions, num)
        self.f_x = np.array([dist.pdf(self.x) for dist in distributions])
        return self
    
    def predict(self, given):
        """
        Predict a conditional distribution.

        Parameters
        ----------
        given : (# estimated distributions x # conditional features) np.array
            Values of features on which to condition.

        Returns
        -------
        conditional distributions : list of smoother.Distribution
            Estimated conditional distributions.
        """
        given = given.reshape(1, -1) if len(given.shape) == 1 else given
        kwargs = {}
        if self.metric in ('poly', 'sigmoid', 'rbf', 'laplacian', 'chi2'):
            kwargs['gamma'] = self.gamma
        if self.metric in ('poly', 'sigmoid'):
            kwargs['coef0'] = self.coef0
        weight = pairwise_kernels(
            self.feature_scale*given, self.feature_scale*self.given, 
            metric=self.metric, **kwargs
        )
        f_x = weight @ self.f_x
        distributions = [Distribution(self.x, f_x_i) for f_x_i in f_x]
        return distributions
    
    def score(self, given, distributions):
        """
        Evaluate performance.

        Parameters
        ----------
        given : (# distributions x # conditional feautres) np.array
            Values of features on which to condition.

        distributions : list of distribution objects
            Known conditional distributions against which to evaluate 
            predictions.

        Returns
        -------
        score : float
        """
        estimates = self.predict(given)
        metric = (
            metrics[self.eval_metric] if isinstance(self.eval_metric, str) 
            else self.eval_metric
        )
        return sum([
            metric(true, estimated) for true, estimated in zip(distributions, estimates)
        ]) / len(distributions)
    
    def get_params(self, deep=False):
        """
        Returns
        -------
        parameters : dict
        """
        return dict(
            metric=self.metric, 
            gamma=self.gamma, 
            coef0=self.coef0, 
            feature_scale=self.feature_scale
        )
    
    def set_params(
            self, metric=None, gamma=None, coef0=None, feature_scale=None
        ):
        """Used for cross validation"""
        if metric is not None:
            self.metric = metric
        if gamma is not None:
            self.gamma = gamma
        if coef0 is not None:
            self.coef0 = coef0
        if feature_scale is not None:
            self.feature_scale = feature_scale
        return self
    
    def dump(self):
        """
        Returns
        -------
        JSON dict : str
            JSON dictionary of conditional distribution state.
        """
        return json.dumps(dict(
            metric=self.metric,
            gamma=self.gamma,
            coef0=self.coef0,
            feature_scale=self.feature_scale.tolist(),
            eval_metric=self.eval_metric,
            given=self.given.tolist(),
            x=self.x.tolist(),
            f_x=self.f_x.tolist()
        ))
    
    @classmethod
    def load(cls, state_dict):
        """
        Parameters
        ----------
        state_dict : str (JSON)
            Output of `cls.dump`.

        Returns
        -------
        conditional distribution : cls
        """
        state = json.loads(state_dict)
        dist = cls(
            metric=state['metric'], 
            gamma=state['gamma'], 
            coef0=state['coef0'],
            feature_scale=state['feature_scale'],
            eval_metric=state['eval_metric']
        )
        dist.given = np.array(state['given'])
        dist.x = np.array(state['x'])
        dist.f_x = np.array(state['f_x'])
        return dist