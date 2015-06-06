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
                   dataset_filename,
                   network_filename,
                   training_epochs):

    network = build(input_size, hidden_size, output_size)
    ds = dataset.load_from_file("datasets/rnd_rnd_rnd.data")
    train(network, ds, training_epochs)
    save_to_file(network_filename, network)

def rnd_config():
    return {
        "input_size": 9,
        "output_size": 1,
        "hidden_size": 50,
        "network_filename": "network/rnd_net.pickle",
        "dataset_filename": "dataset/rnd_rnd_rnd.data",
        "training_epochs": 300
    }

if __name__ == '__main__':
    train_and_save(**rnd_config())

