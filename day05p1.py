#!/usr/bin/env python

import cytoolz.curried as cc
import sys

data_input = cc.pipe(
    sys.stdin.readlines()
    , cc.map(lambda x: x.replace('\n', ''))
    , cc.map(int)
    , list
)

old_pos = None
pos = 0
steps = 0

while pos < len(data_input):
    old_pos = pos
    pos     = pos + data_input[pos]
    steps  += 1
    data_input[old_pos] += 1

print(steps)
