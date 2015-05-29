#!/usr/bin/env python
# coding=utf-8


allowed_strategies = ['DODGE', 'LOAD', 'SHOOT0', 'SHOOT1', 'SHOOT2']

GUN_SIZE = 3
MAX_ROUNDS = 50

REWARD_KILL = 2
REWARD_DIE = -2
REWARD_SUICIDE = -3
REWARD_LOAD = 1
REWARD_DODGE_SUCCESSFUL = 1
REWARD_DODGE_UNSUCCESSFUL = 0
REWARD_SHOOT_A_CORPSE = -1
REWARD_NEGATE_SHOTS = 1
REWARD_SHOOT_DODGER = 0

class CowboyGame(object):
    def __init__(self):
        self.players = []
        self.finished = False
        self.round = 0

        self.bullets = [0, 0, 0]
        self.players_alive = 3
        self.alive = [True, True, True]
        self.hide_prev = [False, False, False]  # did player dodge in last round
        self.hide_now = [False, False, False]  # is player dodging now
        self.shoots = [False, False, False]  # is player shooting someone
        self.dies_now = [False, False, False]  # is player dying now
        self.reason = ['', '', '']  # reason of death
        self.shoots_at = [-1, -1, -1]  # who is shooting who
        self.rewards = [0, 0, 0]  # rewards for the last move

    def is_finished(self):
        return self.finished

    def get_rewards(self):
        return self.rewards

    def get_state(self):
        return self.alive, self.bullets, self.hide_now

    def do_turn(self, player1_move, player2_move, player3_move):
        if self.finished:
            raise ValueError('The game has finished!')

        for i in range(3):
            self.hide_prev[i] = self.hide_now[i]
            self.dies_now[i] = False
            self.shoots[i] = False

        strategy = [player1_move, player2_move, player3_move]
        for i in range(3):
            if strategy[i] not in allowed_strategies:
                raise ValueError('{0} - strategy must be one of: {1}'
                                 .format(strategy[i], allowed_strategies))
            if not self.alive[i]:
                strategy[i] = ''

        # Parse strategies
        for i in range(3):
            if self.alive[i]:
                if strategy[i] == 'LOAD':
                    self.bullets[i] += 1

                self.hide_now[i] = False
                if strategy[i] == 'DODGE':
                    self.hide_now[i] = True

                self.shoots[i] = False
                if strategy[i][0:5] == 'SHOOT':
                    self.shoots[i] = True
                    self.shoots_at[i] = int(strategy[i][5:])

        # Calculate round effects
        for i in range(3):
            if self.bullets[i] > GUN_SIZE:
                self.dies_now[i] = True
                self.reason[i] = "loading bullet above the limit"

            if self.hide_now[i] and self.hide_prev[i]:
                self.dies_now[i] = True
                self.reason[i] = "hiding two times in a row"

            if self.shoots[i]:
                if self.bullets[i] == 0:
                    self.dies_now[i] = True
                    self.reason[i] = "shooting without bullets"
                    continue

                self.bullets[i] -= 1

                if self.hide_now[self.shoots_at[i]]:
                    continue
                # If the cowboy shoots at sb that shoots at him at the same time, both live.
                # BUT if it shoots himself, he dies.
                if self.shoots[self.shoots_at[i]] and \
                                self.shoots_at[self.shoots_at[i]] == i and \
                                self.shoots_at[i] != i:
                    continue
                # if the target is already dead, no effect
                if not self.alive[self.shoots_at[i]]:
                    continue
                self.dies_now[self.shoots_at[i]] = True
                self.reason[self.shoots_at[i]] = ("shot by %i" % i)

        # check for deaths
        for i in range(3):
            if self.dies_now[i]:
                self.alive[i] = False
        self.players_alive = int(self.alive[0]) + int(self.alive[1]) + int(self.alive[2])
        if self.players_alive <= 1:
            self.finished = True

        # check if max rounds has been reached
        self.round += 1
        if self.round >= MAX_ROUNDS:
            self.finished = True

        # calculate rewards
        for i in range(3):
            shoot_me = 'SHOOT{who}'.format(who=i)
            # if the player dies, negative reward
            if self.dies_now[i]:
                if strategy[i] == shoot_me:
                    # and shot himself, he gets -3 for being a retard
                    self.rewards[i] = REWARD_SUICIDE
                else:
                    self.rewards[i] = REWARD_DIE
            # if the player is already dead, whatever
            elif not self.alive[i]:
                self.rewards[i] = 0
            else:
                # if the player has loaded a bullet and is still alive, positive reward
                if strategy[i] == 'LOAD':
                    self.rewards[i] = REWARD_LOAD
                # if the player has dodged
                elif strategy[i] == 'DODGE':
                    # and dodged successfully, positive reward
                    if strategy[(i + 1) % 3] == shoot_me or strategy[(i + 2) % 3] == shoot_me:
                        self.rewards[i] = REWARD_DODGE_SUCCESSFUL
                    # and dodged unsuccessfully, no reward
                    else:
                        self.rewards[i] = REWARD_DODGE_UNSUCCESSFUL
                # if the player has shot
                elif strategy[i][0:5] == 'SHOOT':
                    target = int(strategy[i][5:6])
                    # nice reward for killing
                    if self.dies_now[target]:
                        self.rewards[i] = REWARD_KILL
                    else:
                        # minus reward for shooting a dead man
                        if not self.alive[target]:
                            self.rewards[i] = REWARD_SHOOT_A_CORPSE
                        else:
                            # reward for shooting a cowboy that shot at him
                            if self.shoots_at[target] == i:
                                self.rewards[i] = REWARD_NEGATE_SHOTS
                            # no reward for shooting at a dodging player
                            else:
                                self.rewards[i] = REWARD_SHOOT_DODGER

