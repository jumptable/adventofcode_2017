#!/usr/bin/env python

import cytoolz.curried as cc
import itertools as it
import sys
import re
from pprint import pprint as pp

tree_val_re = re.compile('([a-z]{1,}).*\(([0-9]{1,})\)')

data_input = cc.pipe(
    sys.stdin.readlines()
    , cc.map(lambda x: x.replace('\n', ''))
    , cc.map(lambda x: x.split('->'))
    , cc.map(lambda x: (x[0], []) if len(x) == 1 else (x[0], list(cc.map(str.strip, x[1].split(',')))))
    , list
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

pp(root)
