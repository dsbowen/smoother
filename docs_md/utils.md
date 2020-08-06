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
</style># Objective functions and constraints

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##smoother.**DerivativeObjective**

<p class="func-header">
    <i>class</i> smoother.<b>DerivativeObjective</b>(<i>d=1, weight=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/utils.py#L6">[source]</a>
</p>

A `Smoother` objective function which minimizes the sum of a square
derivative.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters and attributes:</b></td>
    <td class="field-body" width="100%"><b>d : <i>int, default=1</i></b>
<p class="attr">
    e.g. <code>1</code> means first derivative, <code>2</code> means second derivative.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>__call__</b>(<i>self, smoother</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/utils.py#L20">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>smoother : <i><code>Smoother</code></i></b>
<p class="attr">
    The smoother to which this objective function applies.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>value : <i>float</i></b>
<p class="attr">
    Approximate mean square derivative over all points of the distribution.
</p></td>
</tr>
    </tbody>
</table>



##smoother.**MassConstraint**

<p class="func-header">
    <i>class</i> smoother.<b>MassConstraint</b>(<i>lb, ub, mass, weight=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/utils.py#L39">[source]</a>
</p>

A `Smoother` constraint that forces a certain amount of probability mass
to be within a given range.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters and attributes:</b></td>
    <td class="field-body" width="100%"><b>lb : <i>float</i></b>
<p class="attr">
    Lower bound of the range within which the probability mass must be.
</p>
<b>ub : <i>float</i></b>
<p class="attr">
    Upper bound of the range within which the probability mass must be.
</p>
<b>mass : <i>float between 0. and 1.</i></b>
<p class="attr">
    Amount of probability mass between <code>lb</code> and <code>ub</code>.
</p>
<b>weight : <i>float or None, default=None</i></b>
<p class="attr">
    Weight to place on the constraint. If <code>None</code> the weight will be set automatically when the constraint is called based on the smoother.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>__call__</b>(<i>self, smoother</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/utils.py#L64">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>smoother : <i>Smoother</i></b>
<p class="attr">
    Smoother to which this constraint applies.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>loss : <i>float</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##smoother.**MomentConstraint**

<p class="func-header">
    <i>class</i> smoother.<b>MomentConstraint</b>(<i>value, degree, type_='raw', norm=False, weight=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/utils.py#L80">[source]</a>
</p>

A `Smoother` constraint that forces a moment condition to hold.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters and attributes:</b></td>
    <td class="field-body" width="100%"><b>value : <i>float</i></b>
<p class="attr">
    The target value of the moment.
</p>
<b>degree : <i>int</i></b>
<p class="attr">
    The degree of the moment; e.g. the 1st moment is the mean.
</p>
<b>type_ : <i>str, default='raw'</i></b>
<p class="attr">
    Type of moment: <code>'raw'</code>, <code>'central'</code> or <code>'standardized'</code>.
</p>
<b>norm : <i>bool, default=False</i></b>
<p class="attr">
    Indicates whether to apply a norm to the moment.
</p>
<b>weight : <i>float or None, default=None</i></b>
<p class="attr">
    Weight to place on the constraint. If <code>None</code> the weight will be set automatically when the constraint is called based on the smoother.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>__call__</b>(<i>self, smoother</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/smoother/blob/master/smoother/utils.py#L109">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>smoother : <i>Smoother</i></b>
<p class="attr">
    Smoother to which this constraint applies.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>loss : <i>float</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

