#!/usr/bin/env python
# coding=utf-8

import rl_test
import numpy
import sys
import threading
from multiprocessing import Pool

player1_file = 'player/good_rnd.py'
player2_file = 'player/good_rnd.py'
alpha = 0.92
beta = 0.81
gamma = 0.06

result = rl_test.run(
    learning_rounds=500000,
    test_rounds=100,
    player1_file=player1_file,
    player2_file=player2_file,
    alpha=alpha,
    gamma=beta,
    epsilon=gamma,
    logs=True,
    interactive_test=True)

print(result)

