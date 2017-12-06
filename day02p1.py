#!/usr/bin/env python

import cytoolz.curried as cc
from pprint import pprint as pp
import sys

data_input = cc.pipe(
    sys.stdin.readlines()
    , cc.map(lambda x: x.replace('\n', ''))
)

answer = cc.pipe(
    data_input
    , cc.map(str.split)
    , lambda x: (cc.map(int, row) for row in x)
    , cc.map(list)
    , cc.map(lambda x: max(x) - min(x))
    , sum
)

pp(answer)
