#!/usr/bin/env python

from collections import deque
from pprint import pprint as pp
import cytoolz.curried as cc
import itertools as it
import re
import sys


class Tree(object):
    def __init__(self, node_id, tree_dict, weight_dict, parent=None):
        self.node_id     = node_id
        self.parent      = parent
        self.children    = [Tree(c, tree_dict, weight_dict, parent=self) for c in tree_dict[node_id]]
        self.self_weight = weight_dict[node_id]
        self.weight      = self.self_weight + sum(x.weight for x in self.children)

    @property
    def siblings(self):
        if not self.parent:
            return [self]
        return self.parent.children

    @property
    def is_balanced(self):
        return self.children_are_balanced

    @property
    def root(self):
        current = self
        while current.parent is not None:
            current = current.parent
        return current

    @property
    def children_are_balanced(self):
        return len(self.grouped('children')) <= 1

    @property
    def siblings_are_balanced(self):
        return len(self.grouped('siblings')) <= 1

    def __repr__(self):
        return self.node_id

    def print(self, level=0):
        print('{}{} [{}]'.format(' '*4*level, self.node_id, self.weight))
        for child in self.children:
            child.print(level=level+1)

    def grouped(self, group, key=lambda x: x.weight):
        if group == 'siblings' and not self.parent:
            return { self.weight: [self] }
        elif group in {'siblings', 'children'}:
            agg = self.siblings if group == 'siblings' else self.children
            return cc.pipe(
                ((key(x), x) for x in agg)
                , cc.groupby(lambda x: x[0])
                , cc.valmap(lambda x: [y[1] for y in x]))
        else:
            return {}

    def dfs(self):
        yield self
        remaining = deque(self.children)
        while remaining:
            current = remaining.popleft()
            yield current
            remaining.extendleft(current.children)

    def bfs(self):
        if self.parent:
            remaining = deque(self.siblings)
        else:
            yield self
            remaining = deque(self.children)
        while remaining:
            current = remaining.popleft()
            yield current
            remaining.extend(current.children)


tree_val_re = re.compile('([a-z]{1,}).*\(([0-9]{1,})\)')
input_file = cc.pipe(
    open(r'day07_test.in')
    , list
)

data_input = cc.pipe(
    input_file
    # sys.stdin.readlines()
    , cc.map(lambda x: x.replace('\n', ''))
    , cc.map(lambda x: x.split('->'))
    , cc.map(lambda x: (x[0], [] if len(x) == 1 else cc.pipe(x[1], lambda x: x.split(','), cc.map(str.strip), list)))
    , list
)

tree_val_dict = cc.pipe(
    data_input
    , cc.map(cc.first)
    , cc.map(lambda x: [tree_val_re.match(x).group(y) for y in (1, 2)])
    , dict
    , cc.valmap(int)
)

tree_mapping_dict = cc.pipe(
    data_input
    , cc.map(lambda x: (tree_val_re.match(x[0]).group(1), x[1]))
    , dict
)

root = cc.pipe(
    tree_mapping_dict.keys()
    , cc.filter(lambda x: x not in cc.concat(tree_mapping_dict.values()))
    , cc.first
)
tree = Tree(root, tree_mapping_dict, tree_val_dict)

grouped_children = cc.pipe(
    tree.dfs()
    , cc.curry(it.dropwhile)(lambda x: x.is_balanced and all(y.is_balanced for y in x.children))
    , cc.first
    , lambda x: x.children
    , lambda x: [(y, y.weight) for y in x]
    , cc.groupby(lambda x: x[1])
)

unbalanced_child = cc.pipe(
    grouped_children
    , cc.valmap(len)
    , cc.valfilter(lambda x: x ==1)
    , lambda x: x.keys()
    , cc.first
    , lambda x: grouped_children[x][0][0]
)

balanced_children = cc.pipe(
    grouped_children
    , cc.keyfilter(lambda x: x != unbalanced_child.weight)
    , cc.valmap(lambda x: [y[0] for y in x])
    , lambda x: cc.concat(x.values())
    , list
)

weight_diff = balanced_children[0].weight - unbalanced_child.weight
unbalanced_self_weight = unbalanced_child.weight - sum(x.weight for x in unbalanced_child.children)
answer = weight_diff + unbalanced_self_weight

pp(root)
