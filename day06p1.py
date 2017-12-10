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
dists_seen = set()

while tuple(dist) not in dists_seen:
    selected_bin = argmax(dist)
    selected_bin_val = dist[selected_bin]
    dists_seen.add(tuple(dist))
    dist[selected_bin] = 0

    while selected_bin_val > 0:
        selected_bin = (selected_bin + 1) % len(data_input)
        dist[selected_bin] += 1
        selected_bin_val -= 1

print(len(dists_seen))
