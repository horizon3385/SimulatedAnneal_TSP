#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import json

x = list()
y = list()
m = 1
n = 1
for i in range(int(sys.argv[1])**2):
    i += 1
    x.append(m)
    y.append(n)
    if i % 10 == 0:
        m += 1
        n = 0
    n += 1 

print json.dumps({'x': x, 'y': y})
