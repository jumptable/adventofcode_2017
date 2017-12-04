#!/usr/bin/env python

import cytoolz.curried as cc
from pprint import pprint as pp
import sys

data_input = sys.stdin.read().replace('\n', '')
data_input += data_input[0]

answer = cc.pipe(
    ((x for x in data_input), (x for x in cc.drop(1, data_input)))
    , lambda x: zip(*x)
    , cc.filter(lambda x: x[0] == x[1])
    , cc.map(lambda x: int(x[0]))
    , sum
)

pp(answer)
