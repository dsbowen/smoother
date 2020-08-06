# Smoother

Smoother is a statistical tool for computing non-parametric distributions by optimizing a constrained smoothing function.

## Why smoother?

We often want to estimate a distribution given limited information, such as its mean and standard deviation. Rather than impose parametric assumptions, smoother uses non-parametric techniques to infer an entire distribution given limited information.

## Installation

```
$ pip install smoother
```

## Quickstart

```python
from smoother import Smoother, MomentConstraint

import matplotlib.pyplot as plt
import numpy as np

# fit a smooth distribution with given mean and standard deviation
lower_bound, upper_bound = -3, 3
mean_const = MomentConstraint(0, degree=1)
std_const = MomentConstraint(1, degree=2, type_='central', norm=True)
smoother = Smoother().fit(lower_bound, upper_bound, [mean_const, std_const])

# plot smoother pdf
x = np.linspace(lower_bound, upper_bound, num=100)
f_x = np.array([smoother.pdf(x_i) for x_i in x])
plt.plot(x, f_x)
```

The result should look like a normal distribution.

## Citation

```
@software{bowen2020smoother,
  author = {Dillon Bowen},
  title = {Smoother: a statistical package for computing smooth, non-parametric distributions},
  url = {https://dsbowen.github.io/smoother/},
  date = {2020-08-06},
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the MIT [License](https://github.com/dsbowen/smoother/blob/master/LICENSE).