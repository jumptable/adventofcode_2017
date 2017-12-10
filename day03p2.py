#!/usr/bin/env python

import cytoolz.curried as cc
import itertools as it

from pprint import pprint as pp
from math import sqrt, floor, modf
import sys

def is_odd_square(n):
    if n < 0 or not isinstance(n, (float, int)):
        return False

    return modf(sqrt(n))[0] == 0.0 and sqrt(n) % 2 == 1


def neighbors_8(point):
    x, y = point
    return (
        (x-1, y+1), (x, y+1), (x+1, y+1),
        (x-1, y)  ,           (x+1, y),
        (x-1, y-1), (x, y-1), (x+1, y-1)
    )


def neighbors_sum(pos, sum_dict):
    if pos == (0, 0):
        return 1

    return cc.pipe(
        pos
        , lambda x: neighbors_8(x)
        , cc.map(lambda x: sum_dict.get(x, 0))
        , sum
    )


def sum_path():
    n = 1
    pos = (0, 0)
    side_length = 1

    sum_dict = {(0, 0) : 1}

    step_fns = it.cycle([
        lambda x:   (x[0] + 1, x[1]    )
        , lambda x: (x[0]    , x[1] + 1)
        , lambda x: (x[0] - 1, x[1]    )
        , lambda x: (x[0]    , x[1] - 1)
    ])

    step_fn = next(step_fns)
    rotation_break_seq = set()

    while True:
        if is_odd_square(n - 1):
            step_fn      = next(step_fns)
            side_length += 2
            delta_seq    = [side_length - 2, side_length - 2 + 1, side_length - 2 + 1]

            rotation_break_seq = cc.pipe(it.accumulate([n] + delta_seq), cc.drop(1), set)
        elif n in rotation_break_seq:
            step_fn = next(step_fns)

        sum_dict[pos] = neighbors_sum(pos, sum_dict)

        yield (pos, sum_dict[pos])

        pos = step_fn(pos)
        n += 1


answer = cc.pipe(
    sum_path()
    , cc.curry(it.dropwhile)(lambda x: x[1] <= int(sys.argv[1]))
    , cc.take(1)
    , list
    , lambda x: x[0][1]
)

pp(answer)
