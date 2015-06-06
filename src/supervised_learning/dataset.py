#!/usr/bin/env python
# coding=utf-8

from pybrain.datasets import SupervisedDataSet

from src.player.utils import load_player_from_file
from src.supervised_learning.utils import CowboyRunner, BasicFilePersister


def generate(player1_filename, player2_filename, player3_filename, filename, game_count = 1000):
    player1 = load_player_from_file(player1_filename)
    player2 = load_player_from_file(player2_filename)
    player3 = load_player_from_file(player3_filename)
    persister = BasicFilePersister(filename)
    runner = CowboyRunner(player1, player2, player3, persister)
    for i in xrange(game_count):
        runner.run_game()
    persister.close()

def load_from_file(filename):
    input_size = 9
    output_size = 1
    dataset = SupervisedDataSet(input_size, output_size)
    with open(filename, 'r') as datafile:
        for line in datafile:
            data = line.strip().split(' ')
            dataset.appendLinked(
                tuple(data[:input_size]),
                tuple(data[-output_size:]))
    return dataset

if __name__ == '__main__':
    dataset = load_from_file("datasets/rnd_rnd_rnd.data")
    inp = dataset['input']
