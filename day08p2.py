#!/usr/bin/env python

from collections import defaultdict
from operator import lt, gt, eq, ne, add, sub
import cytoolz.curried as cc
import itertools as it
import sys

lte = lambda x, y: x < y or x == y
gte = lambda x, y: x > y or x == y

pred_map = {
    '<'  : lt,
    '==' : eq,
    '<=' : lte,
    '>'  : gt,
    '>=' : gte,
    '!=' : ne,
}

op_map = {
    'inc' : add,
    'dec' : sub,
}

regs = defaultdict(lambda: 0)
max_seen = -sys.maxsize - 1

for line in sys.stdin.readlines():
    sp = line.split()
    reg, op, val, pred, pred_larg, pred_rarg = sp[0], sp[1], int(sp[2]), pred_map[sp[5]], sp[4], int(sp[6])
    if pred(regs[pred_larg], pred_rarg):
        value = op_map[op](regs[reg], val)
        max_seen = value if value > max_seen else max_seen
        regs[reg] = value

print(max_seen)
