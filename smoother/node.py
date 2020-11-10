"""# Node"""

import numpy as np

import random

def sort_nodes(nodes, shuffle=False, presort=False, reverse=False):
    """
    Sorts nodes in an order in which they should be estimated. i.e. all of
    node N's in-nodes should be estimated before estimating node N.

    Parameters
    ----------
    nodes : list of `Node`s
        Nodes to sort.

    shuffle : bool, default=False
        Indicates that nodes should be shuffled before presorting.

    presort : bool, default=False
        Indicates that nodes should be presorted by number of in-nodes.

    reverse : bool, default=False
        Indicates that nodes should be presorted by number of in-nodes from
        greatest to least. If `False`, presorting will sort nodes by in-nodes
        from least to greatest.

    Returns
    -------
    sorted_nodes : list of `Node`s
    """
    def presort_nodes(nodes):
        nodes = [node for node in nodes if not node.added]
        if shuffle:
            random.shuffle(nodes)
        if presort:
            key = (
                lambda node: -len(node.in_nodes) if reverse
                else lambda node: len(node.in_nodes)
            )
            nodes = sorted(nodes, key=key)
        return nodes

    def sort_nodes_(nodes):
        nodes = presort_nodes(nodes)
        sorted_nodes = []
        for node in nodes:
            if not node.added:
                if not all([n.added for n in node.in_nodes]):
                    sorted_nodes += sort_nodes_(node.in_nodes)
                node.added = True
                sorted_nodes.append(node)
        return sorted_nodes
    
    for node in nodes:
        node.added = False
    sorted_nodes = sort_nodes_(nodes)
    for node in nodes:
        del node.added
    return sorted_nodes


class Node():
    """Node in Bayesian network

    Parameters and attributes
    -------------------------
    in_nodes : list of `Node`s
        Nodes on which this node depends

    distribution : distribution, default=None
        Distribution of the variable associated with this node. If this node
        has `in_nodes`, this should be a `ConditionalDistribution` where the
        given features correspond to the `in_nodes`. You may also fix this
        node's value by setting `distribution` to a `float` or `int`.

    name : str or None, default=None
        For debugging.

    Additional attributes
    ---------------------
    frozen_rvs : np.array
        Frozen sampling of random values from this node's distribution.
    """
    def __init__(self, in_nodes=[], distribution=None, name=None):
        self.in_nodes = in_nodes
        self.distribution = distribution
        self.name = name
        self.frozen_rvs = None
        
    def rvs(self, size=1):
        """
        Sample random values from this node's distribution. If this node has
        `frozen_rvs`, `frozen_rvs` will be returned. If this node has 
        `in_nodes`, it will sample from these to draw from conditional 
        distributions.

        Parameters
        ----------
        size : int, default=1
            Number of random values to sample.

        Returns
        -------
        random_values : (size,) np.array
        """
        if isinstance(self.distribution, (int, float)):
            self.frozen_rvs = np.array([self.distribution]*size)
        if self.frozen_rvs is not None:
            return self.frozen_rvs
        assert self.distribution is not None
        if self.in_nodes:
            given = self.given_rvs(size)
            conditional_dists = self.distribution.predict(given)
            self.frozen_rvs = np.array([d.rvs() for d in conditional_dists])
        else:
            self.frozen_rvs = self.distribution.rvs(size)
        return self.frozen_rvs
    
    def given_rvs(self, size=1):
        """
        Sample random values from the distributions of this node's `in_nodes`.

        Parameters
        ----------
        size : int, default=1

        Returns
        -------
        random_values : (size x # in nodes) np.array
        """
        assert self.in_nodes
        return np.array([node.rvs(size) for node in self.in_nodes]).T
    
    def clear_rvs(self):
        """
        Clear `frozen_rvs`.

        Returns
        -------
        self
        """
        if self.frozen_rvs is not None:
            self.frozen_rvs = None
            [node.clear_rvs() for node in self.in_nodes]
        return self