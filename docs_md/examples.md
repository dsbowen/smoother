# Examples

Find the [full code for these examples here](https://github.com/dsbowen/smoother/blob/master.examples.ipynb).

## Moments constraints

In this example, we compute a smooth distribution given moments constraints.

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

The result should look like a standard normal distribution.

We begin by defining the lower and upper bounds of the distribution along with two moments constraints. The first constrains the mean (the first moment, `degree=1`), to be 0. The second constrains the standard deviation (the norm of the second central moment) to be 1. By default, `Smoother` computes a maximum entropy distribution subject to the upper and lower bound and constraints.

## Masses constraints

In this example, we compute a smooth distribution given masses constraints.

```python
from smoother import Smoother, DerivativeObjective, MassConstraint

import numpy as np
import matplotlib.pyplot as plt

# fit a smooth distribution given masses constraints
lower_bound, upper_bound = -3, 3
p25_const = MassConstraint(lower_bound, -.67, mass=.25)
p50_const = MassConstraint(-.67, 0, mass=.25)
p75_const = MassConstraint(0, .67, mass=.25)
p100_const = MassConstraint(.67, upper_bound, mass=.25)
smoother = Smoother().fit(
    lower_bound, 
    upper_bound,
    [p25_const, p50_const, p75_const, p100_const],
    objective=DerivativeObjective(1)
)

# plot smoother pdf
x = np.linspace(lower_bound, upper_bound, num=100)
f_x = np.array([smoother.pdf(x_i) for x_i in x])
plt.plot(x, f_x)
```

The result should look like a standard normal distribution.

We begin by defining the upper and lower bounds of the distribution, along with masses constraints. Masses constraints require that a certain mass of the distribution be within a given range. For example, `MassConstraint(-.67, 0, mass=.25)` means that 25% of the mass of the distribution must be between -.67 and 0.

The `DerivativeObjective` is a different smoothing function from the default, which maximizes entropy. The derivative objective smoothing function minimizes the mean square of a derivative; in this case the first derivative, since we passed in `1` to the constructor.