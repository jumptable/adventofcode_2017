#!/usr/bin/env python

import cytoolz.curried as cc
import itertools as it
from pprint import pprint as pp
import sys
import operator as op

data_input = cc.pipe(
    sys.stdin.readlines()
    , cc.map(lambda x: x.replace('\n', ''))
    , list
)

def evenly_divisible_pair(num_line):
    for (n1, n2) in it.product(num_line, num_line):
        if n1 != n2:
            if n1 % n2 == 0:
                return (n1, n2)
            elif n2 % n1 == 0:
                return (n2, n1)


answer = cc.pipe(
    data_input
    , cc.map(str.split)
    , lambda x: (cc.map(int, row) for row in x)
    , cc.map(list)
    , cc.map(evenly_divisible_pair)
    , cc.map(lambda x: op.ifloordiv(*x))
    , sum
)

pp(answer)
