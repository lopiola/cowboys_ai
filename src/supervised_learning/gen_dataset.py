#!/usr/bin/env python
# coding=utf-8

from src.supervised_learning.dataset import generate

def rnd_config():
    return {
        "player1_filename": 'src/player/rnd.py',
        "player2_filename": 'src/player/rnd.py',
        "player3_filename": 'src/player/rnd.py',
        "filename": 'rnd_rnd_rnd.data',
        "game_count": 5000
    }

if __name__ == '__main__':
    generate(**rnd_config())

