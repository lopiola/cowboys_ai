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

if len(sys.argv) < 3:
    print "Invocation:"
    print "   ./reinf_learning player1 player2"
    exit()
names = sys.argv[1:3]

# define action-value table
# number of states is:
#
#    current value: 1-21
#
# number of actions:
#
#    Stand=0, Hit=1
#    Stand=0, Hit=1
av_table = ActionValueTable(262144, 5)
av_table.initialize(0.)

# define Q-learning agent
learner = Q(0.5, 0.0)
learner._setExplorer(EpsilonGreedyExplorer(0.0))
agent = LearningAgent(av_table, learner)

# define the environment
env = CowboyEnv(names[0], names[1])

# define the task
task = CowboyTask(env)

# finally, define experiment
experiment = Experiment(task, agent)

# ready to go, start the process
# experiment.doInteractions(10000)
while True:
    experiment.doInteractions(1)
    agent.learn()
    agent.reset()
    raw_input("->")
