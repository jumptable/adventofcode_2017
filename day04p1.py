#!/usr/bin/env python

import cytoolz.curried as cc
from pprint import pprint as pp
import sys

data_input = cc.pipe(
    sys.stdin.readlines()
    , cc.map(lambda x: x.replace('\n', ''))
    , list
)


def has_no_duplicate(x):
    return len(set(x)) == len(x)


answer = cc.pipe(
    data_input
    , cc.map(str.split)
    , cc.filter(has_no_duplicate)
    , list
    , len
)

pp(answer)
