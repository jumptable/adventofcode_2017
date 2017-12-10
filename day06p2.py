#!/usr/bin/env python

import cytoolz.curried as cc
import sys

def argmax(seq):
    max_seen = None
    max_seen_index = None
    for i, value in enumerate(seq):
        if max_seen is None or value > max_seen:
            max_seen = value
            max_seen_index = i
    return max_seen_index


data_input = cc.pipe(
    sys.stdin.readline()
    , str.split
    , cc.map(int)
    , list
)

selected_bin = 0
dist = data_input
seen_dists_dict = {}
cycle_len_dict = {}

while not cc.valfilter(lambda x: x >= 2, seen_dists_dict):
    dist_tuple = tuple(dist)
    if dist_tuple not in seen_dists_dict:
        seen_dists_dict[dist_tuple] = 1
    else:
        seen_dists_dict[dist_tuple] += 1

    if dist_tuple not in cycle_len_dict:
        cycle_len_dict[dist_tuple] = 0
    cycle_len_dict = cc.valmap(lambda x: x + 1, cycle_len_dict)

    selected_bin = argmax(dist)
    selected_bin_val = dist[selected_bin]
    dist[selected_bin] = 0

    while selected_bin_val > 0:
        selected_bin = (selected_bin + 1) % len(data_input)
        dist[selected_bin] += 1
        selected_bin_val -= 1

cycle_len_dict = cc.valmap(lambda x: x - 1, cycle_len_dict)
cycles = cc.valfilter(lambda x: x >= 2, seen_dists_dict)
key = tuple(cycles.keys())[0]

print(key)
print(cycle_len_dict[key])
