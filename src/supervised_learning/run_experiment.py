#!/usr/bin/env python
# coding=utf-8
from src import player
from src.supervised_learning import network
from src.supervised_learning.net_player import Player
from src.supervised_learning.utils import CowboyRunner, ConsolePersister


def run(network_filename, player2_filename, player3_filename, game_count):
    net = network.load_from_file(network_filename)
    player1 = Player(net)
    player2 = player.utils.load_player_from_file(player2_filename)
    player3 = player.utils.load_player_from_file(player3_filename)
    runner = CowboyRunner(player1, player2, player3, ConsolePersister())
    for i in xrange(game_count):
        runner.run_game()
        # print runner.game.alive
    print runner.score

def rnd_config():
    return {
        "player2_filename": 'src/player/rnd.py',
        "player3_filename": 'src/player/rnd.py',
        "game_count": 100
    }

def good_rnd_config():
    return {
        "player2_filename": 'src/player/good_rnd.py',
        "player3_filename": 'src/player/good_rnd.py',
        "game_count": 100
    }


def best_avg_config():
    return {
        "player2_filename": 'src/player/best_avg.py',
        "player3_filename": 'src/player/best_avg.py',
        "game_count": 100
    }

if __name__ == '__main__':
    network_filename = 'network/rnd_net.pickle'
    run(network_filename, **good_rnd_config())
