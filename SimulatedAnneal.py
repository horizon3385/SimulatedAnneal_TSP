#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from random import sample


class NewPath(object):
    """NewPath class includes:

    1. Generate a neighbour path from the old path;
    2. Return the difference between new and old path;
    3. A static method to return the total length of one path.
    """
    
    def __init__(self, old, cnt):
        new = old[:]
        self.old = old
        self.loc0, self.loc1 = sample(range(1, cnt), 2)
        new[self.loc0], new[self.loc1] = new[self.loc1], new[self.loc0]
        self.new = new

    def diff(self, matrix):
        """return the difference between new and old path:
        diff = old_length - new _length
        """
        old_sum = 0
        new_sum = 0
        for index in [self.loc0, self.loc1]:
            for sub_index in [-1, 1]:
                old_sum += matrix[self.old[index + sub_index]][self.old[index]]
                new_sum += matrix[self.new[index + sub_index]][self.new[index]]
        return old_sum - new_sum

    @staticmethod
    def length_total(path, matrix):
        total = 0
        for i in range(len(path) - 1):
            total += matrix[path[i]][path[i + 1]]
        return total

    @staticmethod
    def revert_part(path, index1, index2):
        to_revert = path[index1: index2]
        to_revert.reverse()
        new = path[:index1]
        new = new + to_revert
        new = new + path[index2:]
        return new


def main():

    import sys
    import json
    import logging
    import argparse

    from random import random
    from math import sqrt, exp

    #---- configurate log ----#
    logging.basicConfig(
    	filemode='w',
    	format='[%(asctime)s][%(levelname)s]%(message)s', 
    	datefmt='%Y-%m-%dT%H:%M:%S',
    	level=logging.DEBUG
    	)

    #---- import cities coordinate ----#
    cities = json.load(sys.stdin)
    x = cities.get('x')
    y = cities.get('y')
    cnt = len(x)
    if not cnt == len(y):
        print >> sys.stderr, "check cities coordinate"
        sys.exit(2)

    #---- distance matrix ----#
    dis_matrix = []
    for i in range(cnt):
        row = []
        for k in range(cnt):
            row.append(sqrt((x[i] - x[k])**2 + (y[i] - y[k])**2))
        dis_matrix.append(row)  
         
    #---- arguments ----#
    parser = argparse.ArgumentParser(
        description="""
        Travelling Salesman's Problem (TSP)
        with simulated annealing (SA) algorithm

        Input cities' coordinate from JSON file.
        Input JSON file should be like:
        {
            "x": [52.66, ...],
            "y": [10.19, ...]
        }""", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--maxIterations', type=int, default=10**8, help='Maximum iteration steps')
    parser.add_argument('--maxTemperature', type=float, default=30.0, help='Initiate temperature')
    parser.add_argument('--minTemperature', type=float, default=0.001, help='Minimum temperature')
    parser.add_argument('--pho', type=float, default=0.99, help='schedule temperature structure')
    parser.add_argument('--length', type=int, default=100, help='initiate length in each specified temperature')
    parser.add_argument('--length_increment', type=int, default=100, help='increment in step length in each specified temperature')
    args = parser.parse_args()
    
    #---- initiate algorithm ----#
    path = sample(range(cnt), cnt)
    path.append(path[0])
    iteration = 0
    temperature = args.maxTemperature
    schedule_length = 0
    while iteration < args.maxIterations and temperature > args.minTemperature:
        try:
            schedule_length += 1
            iteration += 1            
            new_path = NewPath(path, cnt)
            difference = new_path.diff(matrix=dis_matrix)
            if difference > 0 or random() < exp(difference / temperature):
                path = new_path.new
            if schedule_length % args.length == 0:
                temperature *= args.pho
                args.length += args.length_increment
                schedule_length = 0
                logging.info('[iterations: %.2E  temperature: %4.2f  length: %8.4f]', iteration, temperature, NewPath.length_total(path, matrix=dis_matrix))
        except KeyboardInterrupt:
            break

    output = {}
    output.update({'intermedium': {'path': path, 'length': NewPath.length_total(path, matrix=dis_matrix)}})
    
    #path = [94, 99, 91, 45, 0, 87, 79, 63, 46, 82, 55, 40, 37, 23, 59, 3, 10, 49, 24, 17, 36, 71, 95, 52, 22, 76, 70, 90, 88, 6, 28, 73, 61, 39, 43, 32, 20, 16, 89, 97, 54, 75, 38, 65, 9, 58, 51, 47, 4, 30, 50, 78, 96, 35, 48, 69, 25, 7, 21, 15, 57, 12, 2, 98, 5, 77, 29, 44, 84, 62, 8, 86, 93, 27, 33, 83, 14, 18, 42, 31, 34, 13, 60, 64, 26, 68, 72, 80, 19, 81, 11, 41, 85, 67, 92, 53, 66, 1, 74, 56, 94]
    #---- solve cross path ----#
    length = len(path)       
    def one_step_more(path):
    	orig = path[:]
    	orig_length = NewPath.length_total(path, matrix=dis_matrix)
    	for i in range(1, length - 4):
    		for k in range(i + 3, length - 1):
    			temp = NewPath.revert_part(path, i, k)
    			curr_length = NewPath.length_total(temp, matrix=dis_matrix)
    			if curr_length < orig_length:
    				path = temp
    				orig_length = curr_length
    	if not path == orig:
            return one_step_more(path)
        return path
    path = one_step_more(path)    

    output.update({'final': {'path': path, 'length': NewPath.length_total(path, matrix=dis_matrix)}})
    json.dump(output, sys.stdout, encoding='utf-8')


if __name__ == '__main__':
    main()
