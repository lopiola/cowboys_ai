#!/usr/bin/env python
# coding=utf-8
from docutils.writers.latex2e import Babel

from src.engine.game import CowboyGame


DATA_DIR = "datasets/"

class CowboyRunner(object):
    def __init__(self, player1, player2, player3, persister):
        self.players = [player1, player2, player3]
        self.game = None
        self.last_strategies = []
        self.persister = persister
        self.state = None
        self.init_players()

    def run_game(self):
        self.game = CowboyGame()
        while not self.game.is_finished():
            self.state = self.game.get_state()
            self.last_strategies = [player.strategy() for player in self.players]
            self.game.do_turn(*self.last_strategies)
            self.persist_round()

    def persist_round(self):
        rewards = self.game.get_rewards()
        self.persister.persist_round(self.last_strategies, self.state, rewards)

    def init_players(self):
        for i, player in enumerate(self.players):
            player.name(i)

class BasicFilePersister(object):

    value_map = {
        'True'  : 0.,
        'False' : 1.,
        'DODGE'  : 0.,
        'LOAD'  : 1.,
        'SHOOT0': 2.,
        'SHOOT1': 3.,
        'SHOOT2': 4.
    }

    def __init__(self, filename):
        self.filename = filename
        try:
            self.outfile = open(DATA_DIR + self.filename, 'a')
        except IOError:
            raise(ValueError("Could not open file {0}".format(self.filename)))

    def persist_round(self, strategies, state, rewards):
        state_format = self.format_state(state)
        line = "{1} {0} {2}\n".format(
            self.map_value(strategies[0]),
            state_format,
            rewards[0])
        self.outfile.write(line)

    def format_state(self, state):
        state_merged = []
        for l in state:
            state_merged += l
        state_merged = map(self.map_value, state_merged)
        state_format = str(state_merged[0])
        for state_element in state_merged[1:]:
            state_format += ' ' + str(state_element)
        return state_format

    def map_value(self, value):
        if isinstance(value, basestring):
            return BasicFilePersister.value_map[value]
        try:
            float_value = float(value)
        except TypeError:
            float_value = BasicFilePersister.value_map[value]
        return float_value

    def close(self):
        self.outfile.close()
