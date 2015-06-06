#!/usr/bin/env python
# coding=utf-8

from src.engine.game import CowboyGame
import copy

DATA_DIR = "datasets/"

class CowboyRunner(object):
    def __init__(self, player1, player2, player3, persister = None):
        self.players = [player1, player2, player3]
        self.game = None
        self.last_strategies = []
        self.persister = persister
        self.state = None
        self.last_score = 0.0
        self.score = 0.0
        self.init_players()

    def run_game(self):
        self.game = CowboyGame()
        while not self.game.is_finished():
            self.state = copy.deepcopy(self.game.get_state())

            try:
                self.players[0].set_state(self.state)
            except:
                pass
            self.last_strategies = [player.strategy() for player in self.players]
            self.game.do_turn(*self.last_strategies)
            if self.persister:
                self.persist_round()
            for player in self.players:
                player.round_result(self.last_strategies)

        if self.game.alive[0]:
            self.last_score = 1.0 / self.game.players_alive
        else:
            self.last_score = 0.0
        self.score += self.last_score

    def is_game_finished(self):
        return self.game.is_finished() or not self.game.alive[0]

    def persist_round(self):
        rewards = self.game.get_rewards()
        self.persister.persist_round(self.last_strategies, self.state, rewards)

    def init_players(self):
        for i, player in enumerate(self.players):
            player.name(i)


class BasicFilePersister(object):

    def __init__(self, filename):
        self.filename = filename
        try:
            self.outfile = open(DATA_DIR + self.filename, 'a')
        except IOError:
            raise(ValueError("Could not open file {0}".format(self.filename)))

    def persist_round(self, strategies, state, rewards):
        state_format = format_state(prepare_state(state, strategies[0]))
        line = "{0} {1}\n".format(
            state_format,
            rewards[0])
        self.outfile.write(line)

    def close(self):
        self.outfile.close()

class ConsolePersister(object):
    def persist_round(self, strategies, state, rewards):
        print strategies
        state_format = format_state(prepare_state(state, strategies[0]))
        line = "{0} {1}\n".format(
            state_format,
            rewards[0])

value_map = {
    'True'  : 0.,
    'False' : 1.,
    'DODGE'  : 0.,
    'LOAD'  : 1.,
    'SHOOT0': 2.,
    'SHOOT1': 3.,
    'SHOOT2': 4.
}

def prepare_state(state, strategy):
    state_merged = []
    for l in state:
        state_merged += l
    state_merged.append(strategy)
    state_merged = map(map_value, state_merged)
    return state_merged[1:]


def map_value(value):
    if isinstance(value, basestring):
        return value_map[value]
    try:
        float_value = float(value)
    except TypeError:
        float_value = value_map[value]
    return float_value

def format_state(state):
    state_format = str(state[0])
    for state_element in state[1:]:
        state_format += ' ' + str(state_element)
    return state_format
