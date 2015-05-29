#!/usr/bin/env python
# coding=utf-8


from pybrain.rl.environments.task import Task

class CowboyTask(Task):
    """ A task is associating a purpose with an environment. It decides how to evaluate the observations, potentially returning reinforcement rewards or fitness values.
    Furthermore it is a filter for what should be visible to the agent.
    Also, it can potentially act as a filter on how actions are transmitted to the environment. """

    def __init__(self, environment):
        """ All tasks are coupled to an environment. """
        self.env = environment

    def performAction(self, action):
        """ A filtered mapping towards performAction of the underlying environment. """               
        self.env.performAction(action)
       
    def getObservation(self):
        """ A filtered mapping to getSample of the underlying environment. """
        return self.env.getSensors()

    def getReward(self):
        """ Compute and return the current reward (i.e. corresponding to the last action performed) """
        return self.env.get_reward()

    @property
    def indim(self):
        return self.env.indim
   
    @property
    def outdim(self):
        return self.env.outdim
