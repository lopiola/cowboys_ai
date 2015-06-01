#!/usr/bin/env python
# coding=utf-8

import rl_test
import numpy
from multiprocessing import Pool

SAME_TEST_RETRIES = 5

player1_learn_file = 'player/lopiola.py'
player2_learn_file = 'player/lopiola.py'
player1_test_file = 'player/rnd.py'
player2_test_file = 'player/rnd.py'


def run((alpha, gamma, epsilon)):
    res = 0.0
    for i in range(SAME_TEST_RETRIES):
        res += rl_test.run(
            learning_rounds=1000,
            test_rounds=200,
            player1_learn_file=player1_learn_file,
            player2_learn_file=player2_learn_file,
            player1_test_file=player1_test_file,
            player2_test_file=player2_test_file,
            alpha=alpha,
            gamma=gamma,
            epsilon=epsilon,
            logs=False,
            interactive_test=False)

    res = res * 1.0 / SAME_TEST_RETRIES
    print('OK {0}'.format(alpha))
    return (res, alpha, gamma, epsilon)

# number of concurrent threads to process all the stuff
thread_pool = Pool(8)

arg_sets = []
for a in numpy.arange(0.0, 1.01, 0.1):
    for g in numpy.arange(0.0, 1.01, 0.1):
        for e in numpy.arange(0.0, 1.01, 0.1):
            arg_sets.append((a, g, e))

# for a in numpy.arange(0.2, 0.61, 0.025):
#     for g in numpy.arange(0.4, 1.01, 0.025):
#         for e in numpy.arange(0.0, 0.26, 0.02):
#             arg_sets.append((a, g, e))

print('To process: {0}'.format(len(arg_sets)))
results = thread_pool.map(run, arg_sets)

results.sort(key=lambda tup: tup[0])

for (result, alpha, gamma, epsilon) in results:
    print('''
alpha: {0}
gamma: {1}
epsilon: {2}
result: {3}
'''.format(
        alpha, gamma, epsilon, result))

