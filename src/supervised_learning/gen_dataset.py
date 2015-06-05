#!/usr/bin/env python
# coding=utf-8
from src.engine.game import CowboyGame
from src.player.utils import load_player_from_file

DATA_DIR = "datasets/"

def generate(player1_filename, player2_filename, player3_filename, filename, game_count = 1000):
    player1 = load_player_from_file(player1_filename)
    player2 = load_player_from_file(player2_filename)
    player3 = load_player_from_file(player3_filename)
    persister = BasicFilePersister(filename)
    runner = CowboyRunner(player1, player2, player3, persister)
    for i in xrange(game_count):
        runner.run_game()
    persister.close()


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
    def __init__(self, filename):
        self.filename = filename
        try:
            self.outfile = open(DATA_DIR + self.filename, 'a')
        except IOError:
            raise(ValueError("Could not open file {0}".format(self.filename)))

    def persist_round(self, strategies, state, rewards):
        state_format = self.format_state(state)
        for i, s in enumerate(strategies):
            line = "{1} {0} {2}\n".format(s, state_format, rewards[i])
            self.outfile.write(line)

    def format_state(self, state):
        state_merged = []
        for l in state:
            state_merged += l
        state_format = str(state_merged[0])
        for state_element in state_merged[1:]:
            state_format += ' ' + str(state_element)

        return state_format

    def close(self):
        self.outfile.close()


if __name__ == '__main__':
    generate(
        'src/player/rnd.py',
        'src/player/rnd.py',
        'src/player/rnd.py',
        'rnd_rnd_rnd.data')

