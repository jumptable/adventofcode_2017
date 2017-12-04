#!/usr/bin/env python

import cytoolz.curried as cc
import itertools as it
from pprint import pprint as pp
import sys

data_input = sys.stdin.read().replace('\n', '')
data_input_midpt = cc.pipe(
    data_input
    , it.cycle
    , cc.drop(int(len(data_input) / 2))
)

answer = cc.pipe(
    zip(data_input, data_input_midpt)
    , cc.filter(lambda x: x[0] == x[1])
    , cc.map(lambda x: int(x[0]))
    , sum
)

pp(answer)
