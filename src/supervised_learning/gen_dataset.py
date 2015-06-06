#!/usr/bin/env python
# coding=utf-8

from src.supervised_learning.dataset import generate

def rnd_config():
    return {
        "player1_filename": 'src/player/rnd.py',
        "player2_filename": 'src/player/rnd.py',
        "player3_filename": 'src/player/rnd.py',
        "filename": 'rnd.data',
        "game_count": 5000
    }


def best_avg_config():
    return {
        "player1_filename": 'src/player/best_avg.py',
        "player2_filename": 'src/player/good_rnd.py',
        "player3_filename": 'src/player/good_rnd.py',
        "filename": 'best_avg.data',
        "game_count": 5000
    }


def thinking_config():
    return {
        "player1_filename": 'src/player/lopiola.py',
        "player2_filename": 'src/player/lopiola.py',
        "player3_filename": 'src/player/lopiola.py',
        "filename": 'thinking.data',
        "game_count": 1000
    }

if __name__ == '__main__':
    generate(**thinking_config())

