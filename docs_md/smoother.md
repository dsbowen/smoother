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
</style># Smoother

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##smoother.**Smoother**

<p class="func-header">
    <i>class</i> smoother.<b>Smoother</b>(<i>lb=0, ub=1, num=50</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L10">[source]</a>
</p>

The smoother computes a distribution by maximizing an objective function
(i.e. a smoothness function) given constraints.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>x : <i>np.array</i></b>
<p class="attr">
    A linearly spaced (<code>self.num</code>,) array of points between the lower and upper bounds of the distribution.
</p>
<b>f_x : <i>np.array</i></b>
<p class="attr">
    The probability density function of <code>self.x</code>.
</p>
<b>F_x : <i>np.array</i></b>
<p class="attr">
    The cumulative distribution function of <code>self.x</code>.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>mean</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L54">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>mean : <i>float</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>var</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L62">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>variance : <i>float</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>std</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L70">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>standard deviation : <i>float</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>median</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L78">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>median : <i>float</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>entropy</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L86">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>entropy : <i>float</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>pdf</b>(<i>self, x</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L94">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>x : <i>float</i></b>
<p class="attr">
    
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>pdf(x) : <i>float</i></b>
<p class="attr">
    Probability density function of <code>x</code>.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>cdf</b>(<i>self, x</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L110">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>x : <i>float</i></b>
<p class="attr">
    
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>cdf(x) : <i>float between 0. and 1.</i></b>
<p class="attr">
    Cumulative distribution function of <code>x</code>.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>ppf</b>(<i>self, q</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L149">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>q : <i>float between 0. and 1.</i></b>
<p class="attr">
    Quantile.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>ppf(q) : <i>float</i></b>
<p class="attr">
    Percent point function; inverse of <code>self.cdf</code>.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>sf</b>(<i>self, x</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L171">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>x : <i>float</i></b>
<p class="attr">
    
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>sf(x) : <i>float between 0. and 1.</i></b>
<p class="attr">
    Survival function; <code>1-self.cdf</code>.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>isf</b>(<i>self, q</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L184">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>q : <i>float between 0. and 1.</i></b>
<p class="attr">
    
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>isf(x) : <i>float</i></b>
<p class="attr">
    Inverse survival function.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>moment</b>(<i>self, degree=1, type_='raw', norm=False</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L197">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>degree : <i>int, default=1</i></b>
<p class="attr">
    The degree of the moment, e.g. first (mean), second (var). type_ : str, default='raw' Type of moment; <code>'raw'</code>, <code>'central'</code>, or <code>'standardized'</code>. norm : bool, default=False Indicates whether to return the norm of the moment. If <code>True</code>, return <code>moment**(1/degree)</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>moment : <i>float</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>fit</b>(<i>self, lb, ub, constraints, objective=lambda self: self.entropy(), num=50</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L222">[source]</a>
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
<b>constraints : <i>list of callables</i></b>
<p class="attr">
    Constraints take in a <code>Smoother</code> and return a float. Lower values indicate that the constraints are satisfied.
</p>
<b>objective : <i></i></b>
<p class="attr">
    The objective or smoothing function. The objective function takes a <code>Smoother</code> and returns a float. This objective function is maximized subject to constraints. By default, it maximizes entropy.
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





<p class="func-header">
    <i></i> <b>dump</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L285">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>state_dict : <i>dict</i></b>
<p class="attr">
    JSON dump of the state dictionary.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>load</b>(<i>state_dict</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/smoother.py#L297">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>state_dict : <i>dict</i></b>
<p class="attr">
    Output of <code>Smoother.dump</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>smoother : <i>Smoother</i></b>
<p class="attr">
    Smoother with the specified state dictionary.
</p></td>
</tr>
    </tbody>
</table>

