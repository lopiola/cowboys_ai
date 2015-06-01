#!/usr/bin/env python
# coding=utf-8

import rl_test
from multiprocessing import Pool

player1_learn_file = 'player/best_avg.py'
player2_learn_file = 'player/best_avg.py'
player1_test_file = 'player/best_avg.py'
player2_test_file = 'player/best_avg.py'
alpha = 0.92
gamma = 0.86
epsilon = 0.09

# learning_rounds_list = [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]
learning_rounds_list = [100000, 200000, 500000]
test_rounds = 500
single_test_repeats = 30


def run_test(learning_rounds_arg):
    return rl_test.run(
        learning_rounds=learning_rounds_arg,
        test_rounds=test_rounds,
        player1_learn_file=player1_learn_file,
        player2_learn_file=player2_learn_file,
        player1_test_file=player1_test_file,
        player2_test_file=player2_test_file,
        alpha=alpha,
        gamma=gamma,
        epsilon=epsilon,
        logs=False,
        interactive_test=False)


# number of concurrent threads to process all the stuff
thread_pool = Pool(6)
for learning_rounds in learning_rounds_list:
    results = thread_pool.map(run_test, [learning_rounds] * single_test_repeats)
    print('{0}\t{1}'.format(learning_rounds, sum(results) / single_test_repeats).replace('.', ','))
