#!/usr/bin/env python
# coding=utf-8

import sys
from pybrain.rl.environments.environment import Environment
try:
    from engine.game import CowboyGame
except ImportError:
    print('Don\'t forget to add the src dir to PYTHONPATH!')
    sys.exit(1)
import operator
import os
import imp


class CowboyEnv(Environment):
    def __init__(self, player1_learn_file, player2_learn_file, player1_test_file, player2_test_file):
        self.should_log = False
        self.player1_learn_file = player1_learn_file
        self.player2_learn_file = player2_learn_file
        self.player1_test_file = player1_test_file
        self.player2_test_file = player2_test_file
        self.game = None
        self.opponent1 = None
        self.opponent2 = None
        self.testing_phase = False
        self.reset()
        self.should_log = True
        self.last_score = 0.0

    # the number of action values the environment accepts
    indim = 5

    # the number of sensor values the environment produces
    outdim = 512

    def toggle_logs(self, flag):
        self.should_log = flag

    def toggle_test(self, flag):
        self.testing_phase = flag

    def log(self, msg):
        if self.should_log:
            print(msg)

    def game_finished(self):
        return not self.game.alive[0] or self.game.is_finished()

    def agent_score(self):
        return self.last_score

    def getSensors(self):
        # Reset the game if it has ended or the agent died
        if not self.game.alive[0]:
            self.reset()
        if self.game.is_finished():
            self.reset()
        game_state = self.game.get_state()
        game_state = reduce(operator.add, game_state)
        game_state_float = 0.
        # player 1 alive
        if game_state[1]:
            game_state_float += 1
        # player 2 alive
        if game_state[2]:
            game_state_float += 2
        # player 0 bullet num
        if game_state[3] > 0:
            game_state_float += 4
        # player 1 bullet num
        if game_state[4] > 0:
            game_state_float += 8
        # player 2 bullet num
        if game_state[5] > 0:
            game_state_float += 16
        # player 0 has dodged
        if game_state[6]:
            game_state_float += 32
        # player 1 has dodged
        if game_state[7]:
            game_state_float += 64
        # player 2 has dodged
        if game_state[8]:
            game_state_float += 128
        # player 0 has max bullets in the barrel
        if game_state[3] == 3:
            game_state_float += 256
        self.log('Game state [{0}]: {1}'.format(int(game_state_float), self.game.get_state()))
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
        self.log('Actions performed: {0}'.format(actions))
        self.game.do_turn(action, opp1_action, opp2_action)
        self.opponent1.round_result(actions)
        self.opponent2.round_result(actions)

    def get_reward(self):
        self.log('reward: {0}'.format(self.game.get_rewards()[0]))
        return self.game.get_rewards()[0]

    def reset(self):
        if self.game is not None:
            if self.game.alive[0]:
                self.last_score = 1.0 / self.game.players_alive
            else:
                self.last_score = 0.0
        self.log('----------------')
        self.log('')
        self.log('NEW GAME:')
        self.game = CowboyGame()
        if self.testing_phase:
            self.opponent1 = load_player_from_file(self.player1_test_file)
            self.opponent2 = load_player_from_file(self.player2_test_file)
        else:
            self.opponent1 = load_player_from_file(self.player1_learn_file)
            self.opponent2 = load_player_from_file(self.player2_learn_file)
        self.opponent1.name(1)
        self.opponent2.name(2)


def load_player_from_file(file_path):
    """
    Loads a player module and returns Player class instance that it implements
    """
    class_inst = None
    expected_class = 'Player'

    mod_name, file_ext = os.path.splitext(os.path.split(file_path)[-1])

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, file_path)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, file_path)

    if hasattr(py_mod, expected_class):
        class_inst = getattr(py_mod, expected_class)()

    return class_inst
