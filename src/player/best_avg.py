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
        p0_s = self.player_states[0].get_valid_strategies()
        p1_s = self.player_states[1].get_valid_strategies()
        p2_s = self.player_states[2].get_valid_strategies()
        return choice(best_avg_strategy(self.name, [p0_s, p1_s, p2_s], self.player_states))

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


# Encapsulates relevant information about player state
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
                    # Loading too much - death
                    dies = True
            if strategy.startswith('SHOOT'):
                self.num_bullets -= 1
                if self.num_bullets < 0:
                    # Shooting without bullets - death
                    dies = True
        if dies:
            self.alive = False
        return dies

    def report_player_death(self, dead_player_number):
        if self.number == dead_player_number:
            self.alive = False
        self.shooting_strategies = []
        for i in range(num_players):
            if i != self.number and i != dead_player_number:
                self.shooting_strategies += ['SHOOT%d' % i]

    def get_valid_strategies(self):
        strategies = []
        if self.alive:
            if self.can_evade:
                strategies += ['DODGE']
            if self.num_bullets < max_bullets:
                strategies += ['LOAD']
            if self.num_bullets > 0:
                strategies += self.shooting_strategies
        else:
            strategies = ['DODGE']  # dead, return whatever
        return strategies


def best_avg_strategy(subject_number, player_strats, player_states):
    my_strats = player_strats[subject_number]
    my_state = player_states[subject_number]
    other_strats = []
    other_states = []
    for i in range(len(player_strats)):
        if i != subject_number:
            other_states += [player_states[i]]
            other_strats += [player_strats[i]]
    max_gain = -999999
    best_strats = []
    for i in range(len(my_strats)):
        current_strat = calc_avg_gain(my_strats[i], other_strats[0], other_strats[1], my_state, other_states[0],
                                      other_states[1])
        if current_strat >= max_gain:
            if current_strat == max_gain:
                best_strats += [my_strats[i]]
            else:
                best_strats = [my_strats[i]]
            max_gain = current_strat
    return best_strats


# Calculates average gain when playing a certain strategy vs. all combinations of strategies
def calc_avg_gain(subject_s, opp_1_s, opp_2_s, subject_state, opp_1_state, opp_2_state):
    gain = 0
    for i1 in range(len(opp_1_s)):
        for i2 in range(len(opp_2_s)):
            gain += calc_gain(subject_s, opp_1_s[i1], subject_state, opp_1_state)
            gain += calc_gain(subject_s, opp_2_s[i2], subject_state, opp_2_state)
    return gain * 1.0 / (len(opp_1_s) * len(opp_2_s))


# Calculates gain of playing a certain strategy vs other strategy
def calc_gain(p1_s, p2_s, p1_state, p2_state):
    if p2_s is None:
        return 0

    shoot_me = 'SHOOT' + str(p1_state.number)
    shoot_him = 'SHOOT' + str(p2_state.number)

    if p1_s == 'DODGE':
        if p2_s == 'DODGE':
            return 0
        elif p2_s == 'LOAD':
            return -1
        elif p2_s == shoot_me:
            return 2
        else:
            return 0  # p2 shoots sb else

    elif p1_s == 'LOAD':
        if p2_s == 'DODGE':
            return 1
        elif p2_s == 'LOAD':
            return 0
        elif p2_s == shoot_me:
            return -4
        else:
            return 2  # p2 shoots sb else

    elif p1_s == shoot_him:
        if p2_s == 'DODGE':
            return -1.5
        elif p2_s == 'LOAD':
            return 2
        elif p2_s == shoot_me:
            return 0
        else:
            return 4  # p2 shoots sb else

    else:  # p1 shoots sb else
        if p2_s == 'DODGE':
            return 1
        elif p2_s == 'LOAD':
            return 0
        elif p2_s == shoot_me:
            return -4
        else:
            return -1  # p2 shoots sb else
