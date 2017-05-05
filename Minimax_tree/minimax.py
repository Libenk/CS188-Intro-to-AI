class TreeNode:
    empty = []
    def __init__(self, val, branches = empty):
        self.val = val
        for branch in branches:
            assert isinstance(branch, TreeNode)
        self.branches = branches

    def __repr__(self):
        if self.branches:
            return "{0}, {1}".format(self.val, self.branches)
        else:
            return "{0}".format(self.val)

    @property
    def isleaf(self):
        return self.branches == self.empty

def minimax(node, myagent = True, best_max = float('-inf'), best_min = float('inf')):
    '''
    >>> t = TreeNode(1, [TreeNode(2,[TreeNode(1),TreeNode(2)]),TreeNode(3,[TreeNode(0),TreeNode(3)])])
    >>> print(t)
    1, [2, [1, 2], 3, [0, 3]]
    >>> minimax(t)
    1
    '''
    if node.isleaf:
        return node.val
    if myagent:
        return maxvalue(node, myagent, best_max, best_min)
    else:
        return minvalue(node, myagent, best_max, best_min)

def maxvalue(node, myagent, best_max, best_min):
    max_candidate = float('-inf')
    for child in node.branches:
        max_candidate = max(max_candidate, minimax(child, not myagent))
        if max_candidate >= best_min:
            return max_candidate
        best_max = max(best_max, max_candidate)
    return max_candidate

def minvalue(node, myagent, best_max, best_min):
    min_candidate = float('inf')
    for child in node.branches:
        min_candidate = min(min_candidate, minimax(child, not myagent))
        if min_candidate <= best_max:
            return min_candidate
        best_min = min(best_min, min_candidate)
    return min_candidate
