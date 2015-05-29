#!/usr/bin/env python
# coding=utf-8

from cowboy_task import CowboyTask
from cowboy_env import CowboyEnv
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import EpsilonGreedyExplorer
import sys


def run(learning_rounds, test_rounds, player1_file, player2_file, alpha, gamma, epsilon, logs, interactive_test):
    """
    Run a learning process with given parameters, than tests agent's performance
    by playing given amount of test games and returns the percent of won games.
    """

    # define the environment
    env = CowboyEnv(player1_file, player2_file)

    # define the task
    task = CowboyTask(env)

    av_table = ActionValueTable(env.outdim, env.indim)
    av_table.initialize(0.)

    # define Q-learning agent
    learner = Q(alpha, gamma)
    learner._setExplorer(EpsilonGreedyExplorer(epsilon))
    agent = LearningAgent(av_table, learner)

    # finally, define experiment
    experiment = Experiment(task, agent)

    def play_one_game(learn):
        """
        Orders the agent to play a single game and learn from it.
        Returns number of rounds played
        """
        # Do interactions until the game finishes
        rounds_played = 0
        while not env.game_finished():
            experiment.doInteractions(1)
            if learn:
                agent.learn()
                agent.reset()
            rounds_played += 1
        env.reset()
        return rounds_played

    env.toggle_logs(False)

    round_counter = 0
    # Learn for given number of rounds
    while round_counter < learning_rounds:
        round_counter += play_one_game(True)
        if logs:
            sys.stdout.write("Learning progress: %d%%   \r" %
                             (round_counter * 100.0 / learning_rounds))
            sys.stdout.flush()

    round_counter = 0
    score = 0
    env.toggle_logs(True)
    # Test for given number of rounds
    while round_counter < test_rounds:
        round_counter += play_one_game(False)
        score = env.agent_score()
        if interactive_test:
            print(sys.stdout.write("Testing progress: %d%%" % (round_counter * 100.0 / learning_rounds)))
            raw_input('Score: {0} ->'.format(score))
        elif logs:
            sys.stdout.write("Testing progress: %d%%   \r" %
                             (round_counter * 100.0 / learning_rounds))
            sys.stdout.flush()

    sys.stdout.write("                                                  \r")
    sys.stdout.flush()
    return score * 100.0 / test_rounds
