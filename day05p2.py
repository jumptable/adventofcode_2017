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

while 0 <= pos < len(data_input):
    old_pos = pos
    pos     = pos + data_input[pos]
    steps  += 1
    offset  = 1 if data_input[old_pos] < 3 else -1
    data_input[old_pos] += offset


print(steps)
