#!/usr/bin/env python
# coding=utf-8

from pybrain.rl.environments.environment import Environment
from engine.game import CowboyGame
import operator
import os
import imp

class CowboyEnv(Environment):
    def __init__(self, opponent1_file, opponent2_file):
        self.opponent1_file = opponent1_file
        self.opponent2_file = opponent2_file
        self.game = None
        self.opponent1 = None
        self.opponent2 = None
        self.reset()

    # the number of action values the environment accepts
    indim = 5

    # the number of sensor values the environment produces
    outdim = 262144  # 2^18

    def getSensors(self):
        game_state = self.game.get_state()
        game_state = reduce(operator.add, game_state)
        game_state_float = 0.
        # player 0 alive
        if game_state[0]:
            game_state_float += 1
        # player 1 alive
        if game_state[1]:
            game_state_float += 2
        # player 2 alive
        if game_state[2]:
            game_state_float += 4
        # player 0 has dodged
        if game_state[6]:
            game_state_float += 8
        # player 1 has dodged
        if game_state[7]:
            game_state_float += 16
        # player 2 has dodged
        if game_state[8]:
            game_state_float += 32
        # player 0 bullet num (0 - 3) - add 64 for 0 and 512 for 3
        game_state_float += 2 ** (6 + game_state[3])
        # player 1 bullet num (0 - 3) - add 1024 for 0 and 8192 for 3
        game_state_float += 2 ** (10 + game_state[4])
        # player 2 bullet num (0 - 3) - add 16384 for 0 and 131072 for 3
        game_state_float += 2 ** (14 + game_state[5])
        print 'Game state', str(self.game.get_state())
        return [game_state_float, ]

    def performAction(self, action_float):
        action_map = {
            0.: 'DODGE',
            1.: 'LOAD',
            2.: 'SHOOT0',
            3.: 'SHOOT1',
            4.: 'SHOOT2',
        }
        action = action_map[action_float[0]]
        opp1_action = self.opponent1.strategy()
        opp2_action = self.opponent2.strategy()
        actions = [action, opp1_action, opp2_action]
        print "Actions performed: ", str(actions)
        self.game.do_turn(action, opp1_action, opp2_action)
        self.opponent1.round_result(actions)
        self.opponent2.round_result(actions)
        if not self.game.alive[0]:
            self.reset()
        if self.game.is_finished():
            self.reset()

    def getReward(self):
        print('reward: {0}'.format(self.game.get_rewards()[0]))
        return self.game.get_rewards()[0]

    def reset(self):
        print('<-- NEW GAME -->')
        self.game = CowboyGame()
        self.opponent1 = load_player_from_file(self.opponent1_file)
        self.opponent2 = load_player_from_file(self.opponent2_file)
        self.opponent1.name(1)
        self.opponent2.name(2)



def load_player_from_file(file_path):
    """
    Loads a player module and returns Player class instance that it implements
    """
    class_inst = None
    expected_class = 'Player'

    mod_name,file_ext = os.path.splitext(os.path.split(file_path)[-1])

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, file_path)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, file_path)

    if hasattr(py_mod, expected_class):
        class_inst = getattr(py_mod, expected_class)()

    return class_inst
