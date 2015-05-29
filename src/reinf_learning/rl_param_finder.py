#!/usr/bin/env python
# coding=utf-8

import rl_test
import numpy
import sys
import threading
from multiprocessing import Pool

player1_file = 'player/good_rnd.py'
player2_file = 'player/good_rnd.py'


def run((alpha, beta, gamma)):
    result = rl_test.run(
        learning_rounds=50000,
        test_rounds=500,
        player1_file=player1_file,
        player2_file=player2_file,
        alpha=alpha,
        gamma=beta,
        epsilon=gamma,
        logs=False,
        interactive_test=False)

    print('OK {0}'.format(alpha))
    return (result, alpha, beta, gamma)


thread_pool = Pool(8)

arg_sets = []
for a in numpy.arange(0.92, 0.95, 0.01):
    for g in numpy.arange(0.8, 0.85, 0.01):
        for e in numpy.arange(0.0, 0.2, 0.03):
            arg_sets.append((a, g, e))

print('To process: {0}'.format(len(arg_sets)))
results = thread_pool.map(run, arg_sets)

results.sort(key=lambda tup: tup[0])

for (result, alpha, beta, gamma) in results:
    print('''
alpha: {0}
gamma: {1}
epsilon: {2}
result: {3}
'''.format(
        alpha, beta, gamma, result))
