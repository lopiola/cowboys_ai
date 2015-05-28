from random import *
import traceback

max_bullets = 3
num_players = 3


class Player:
    def name(self, name):
        self.name = name
        self.player_states = [PlayerState(0), PlayerState(1), PlayerState(2)]

    def message(self, s):
        pass

    #        print 'Player %i: %s' % (self.name, s)

    def start(self):
        self.player_states = [PlayerState(0), PlayerState(1), PlayerState(2)]

    def strategy(self):
        return choice(self.player_states[self.name].get_valid_strategies())

    def preround_info(self, alive, bullets, dodged):
        pass

    def round_result(self, s):
        died = [False, False, False]

        # Update states, check if sb dies because of stupidity
        for i in range(num_players):
            died[i] = self.player_states[i].update(s)

        # Check shooting results
        for pl_a in range(num_players):
            for pl_b in range(num_players):
                if pl_b != pl_a:
                    if s[pl_b] == 'SHOOT' + str(pl_a):
                        # Can be equal as we have lowered the bullet num in update()
                        if self.player_states[pl_b].num_bullets >= 0:
                            if s[pl_a] != 'DODGE' and s[pl_a] != 'SHOOT' + str(pl_b):
                                # Getting shot - death
                                died[pl_a] = True

        # Update lists of players
        for player in range(num_players):
            if died[player]:
                for i in range(num_players):
                    self.player_states[i].report_player_death(player)

    def die(self):
        self.message('died')

    def game_over(self, x):
        self.message('game over --> %f' % x)


class PlayerState:
    def __init__(self, player_number):
        self.number = player_number
        self.alive = True
        self.num_bullets = 0
        self.can_evade = True
        self.shooting_strategies = []
        for i in range(num_players):
            if i != player_number:
                self.shooting_strategies += ['SHOOT%d' % i]

    # Returns true if the player dies because of a disallowed decision
    def update(self, strategies):
        dies = False
        strategy = strategies[self.number]
        # The player plays DODGE
        if strategy == 'DODGE':
            if self.can_evade:
                # The player cannot evade in the next round
                self.can_evade = False
            else:
                # Second evasion in a row = death
                dies = True
        # The player plays sth else than DODGE
        else:
            self.can_evade = True
            if strategy == 'LOAD':
                self.num_bullets += 1
                if self.num_bullets > max_bullets:
                    # ing too much - death
                    dies = True
            if strategy.startswith('SHOOT'):
                self.num_bullets -= 1
                if self.num_bullets < 0:
                    # Shooting without bullets - death
                    dies = True
        self.alive = dies
        return dies

    def report_player_death(self, dead_player_number):
        self.shooting_strategies = []
        for i in range(num_players):
            if i != self.number and i != dead_player_number:
                self.shooting_strategies += ['SHOOT%d' % i]

    def get_valid_strategies(self):
        strategies = []
        if self.can_evade:
            strategies += ['DODGE']
        if self.num_bullets < max_bullets:
            strategies += ['LOAD']
        if self.num_bullets > 0:
            strategies += self.shooting_strategies
        return strategies
