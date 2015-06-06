#!/usr/bin/env python
# coding=utf-8

import random
from src.supervised_learning.utils import prepare_state

class Player:
    def __init__(self, network):
        self._name = None
        self.strategies = ["LOAD", "DODGE", "SHOOT0", "SHOOT1", "SHOOT2"]
        self.network = network
        self.state = None

    def name(self, name):
        self._name = name

    def start(self):
        pass

    def strategy(self):
        scores = {}
        for s in self.strategies:
            current_state = prepare_state(self.state, s)
            scores[s] = self.network.activate(current_state)
        sorted_strategies = sorted(scores.keys(), key=scores.get, reverse=True)
        max_score = scores[sorted_strategies[0]]
        strategies_with_max_score = []
        for s in sorted_strategies:
            if scores[s] == max_score:
                strategies_with_max_score.append(s)
            else:
                break
        # for s in sorted_strategies:
        #     print s, scores[s]
        strategy = random.choice(strategies_with_max_score)
        return strategy

    def preround_info(self, alive, bullets, dodged):
        pass

    def round_result(self, s):
        pass

    def die(self):
        pass

    def game_over(self, x):
        pass

    def set_state(self, state):
        self.state = state

