#!/usr/bin/env python

import cytoolz.curried as cc

from pprint import pprint as pp
import sys

data_input = cc.pipe(
    sys.stdin.readlines()
    , cc.map(lambda x: x.replace('\n', ''))
    , list
)


def has_anagram(seq):
    set_of_sets = set(cc.map(frozenset, seq))
    return len(seq) != len(set_of_sets)


answer = cc.pipe(
    data_input
    , cc.map(str.split)
    , cc.filter(lambda x: not(has_anagram(x)))
    , list
    , len
)

pp(answer)
