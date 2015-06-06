#!/usr/bin/env python
# coding=utf-8
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from src.supervised_learning import dataset
from math import sqrt

import cPickle as pickle


def build(input_size, hidden_size, target_size):
    return buildNetwork(input_size, hidden_size, target_size, bias=True)

def train(network, dataset, epochs):
    trainer = BackpropTrainer(network, dataset)
    # trainer.trainUntilConvergence(verbose=True)
    #
    for i in range(epochs):
        mse = trainer.train()
        rmse = sqrt(mse)
        print "training RMSE, epoch {}: {}".format(i + 1, rmse)

def load_from_file(filename):
    network = None
    with open(filename, 'r') as pickle_file:
        network = pickle.load(pickle_file)
    return network

def save_to_file(filename, network):
    pickle.dump(network, open(filename, 'wb'))

def train_and_save(input_size,
                   output_size,
                   hidden_size,
                   training_epochs,
                   network_filename,
                   dataset_filename):

    network = build(input_size, hidden_size, output_size)
    ds = dataset.load_from_file(dataset_filename)
    train(network, ds, training_epochs)
    save_to_file(network_filename, network)

def rnd_config():
    return {
        "network_filename": "network/rnd_net.pickle",
        "dataset_filename": "datasets/rnd.data",
    }

def best_avg_config():
    return {
        "network_filename": "network/best_avg_net.pickle",
        "dataset_filename": "datasets/best_avg.data",
    }

def thinking_config():
    return {
        "network_filename": "network/thinking_net.pickle",
        "dataset_filename": "datasets/thinking.data",
    }

def mixed_config():
    return {
        "network_filename": "network/mixed_net.pickle",
        "dataset_filename": "datasets/mixed.data",
    }

if __name__ == '__main__':
    input_size = 9
    output_size = 1
    hidden_size = 15
    training_epochs = 200
    train_and_save(
        input_size,
        output_size,
        hidden_size,
        training_epochs,
        **mixed_config())

