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


def odd_square_lower_bound_and_ring(num):
    if num < 1:
        return (None, None)

    ring = it.count(start=1)
    odd_squares = (x for x in it.count() if is_odd_square(x))
    odd_squares_lower, odd_squares_upper = it.tee(odd_squares)
    odd_squares_upper = cc.drop(1, odd_squares_upper)

    for square_tuple in zip(odd_squares_lower, odd_squares_upper, ring):
        if square_tuple[0] <= num <= square_tuple[1]:
            return (square_tuple[0], square_tuple[2])


def get_position(num):
    odd_square_lower_bound, ring = odd_square_lower_bound_and_ring(num)

    if odd_square_lower_bound is None:
        return (None, None)
    if num == 1:
        return (0, 0)
    if is_odd_square(num):
        mag = int(sqrt(odd_square_lower_bound)) - ring + 1
        return (mag, -mag)

    base_position = get_position(odd_square_lower_bound)
    base_position = (base_position[0] + 1, base_position[1])

    base_seq    = odd_square_lower_bound + 1
    side_length = base_position[0]*2 + 1

    step_fns = [
        lambda x:   (x[0]    , x[1] + 1)
        , lambda x: (x[0] - 1, x[1]    )
        , lambda x: (x[0]    , x[1] - 1)
        , lambda x: (x[0] + 1, x[1]    )
    ]

    delta_seq = [
        side_length - 2
        , side_length - 2 + 1
        , side_length - 2 + 1
    ]

    rotation_break_seq = cc.pipe(
        it.accumulate([base_seq] + delta_seq)
        , cc.drop(1)
        , set
    )

    position = base_position
    while base_seq < num:
        position = step_fns[0](position)
        base_seq += 1

        if base_seq in rotation_break_seq:
            step_fns = step_fns[1:]

    return position


get_manhattan_distance = lambda x: cc.pipe(
    x
    , cc.map(abs)
    , sum
)


answer = cc.pipe(
    int(sys.argv[1])
    , get_position
    , get_manhattan_distance
)

pp(answer)
