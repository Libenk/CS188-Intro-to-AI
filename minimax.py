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

def minimax(node, myagent = True):
    '''
    >>> t = TreeNode(1, [TreeNode(2,[TreeNode(1),TreeNode(2)]),TreeNode(3,[TreeNode(0)])])
    >>> print(t)
    1, [2, [1, 2], 3, [0]]
    >>> minimax(t)
    1
    '''
    if node.isleaf:
        return node.val
    if myagent:
        return maxvalue(node, myagent)
    else:
        return minvalue(node, myagent)

def maxvalue(node, myagent):
    return max([minimax(child, not myagent) for child in node.branches])

def minvalue(node, myagent):
    return min([minimax(child, not myagent) for child in node.branches])
