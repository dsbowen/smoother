<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

<link rel="stylesheet" href="https://assets.readthedocs.org/static/css/readthedocs-doc-embed.css" type="text/css" />

<style>
    a.src-href {
        float: right;
    }
    p.attr {
        margin-top: 0.5em;
        margin-left: 1em;
    }
    p.func-header {
        background-color: gainsboro;
        border-radius: 0.1em;
        padding: 0.5em;
        padding-left: 1em;
    }
    table.field-table {
        border-radius: 0.1em
    }
</style># Maximum entropy distribution

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##smoother.**MaxEntropy**



Computes a maximum entropy distribution given moment constraints. Inherits
from `Smoother`. The only difference is that the `fit` method is optimized
but more restrictive.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

####Notes

See
<https://en.wikipedia.org/wiki/Maximum_entropy_probability_distribution#Continuous_case>
for mathematical detail.

####Examples

This example approximates a standard normal distribution.

```python
import matplotlib.pyplot as plt
from smoother import MaxEntropy

dist = MaxEntropy()
mu, sigma2 = 0, 1
dist.fit(-3, 3, [lambda x: x, lambda x: (x-mu)**2], [mu, sigma2])
plt.plot(dist.x, dist.f_x)
```

####Methods



<p class="func-header">
    <i></i> <b>fit</b>(<i>self, lb, ub, moment_funcs, values, num=50</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/max_entropy.py#L36">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>lb : <i>scalar</i></b>
<p class="attr">
    Lower bound of the distribution.
</p>
<b>ub : <i>scalar</i></b>
<p class="attr">
    Upper bound of the distribution.
</p>
<b>moment_funcs : <i>list of callable</i></b>
<p class="attr">
    List of moment functions. e.g. for the mean, use <code>lambda x: x</code>.
</p>
<b>values : <i>list of scalars</i></b>
<p class="attr">
    List of values the expected value of the moment functions should evaluate to.
</p>
<b>num : <i>int, default=50</i></b>
<p class="attr">
    Number of points on the distribution used for approximation.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i></i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

