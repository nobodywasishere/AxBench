#!/bin/usr/python

# Amir Yazdanbakhsh
# Jan. 7, 2015

import sys
import json
import pyinputplus as pyip

def printUsage():
    print("python comm_to_json.py <func name>")
    exit(1)

def main():    
    args = {}
    print("------------------ Compiler Parameters ------------------")
    args['learning_rate'] = pyip.inputFloat('Learning rate [0.1-1.0]: ', min = 0.1, max = 1.0)
    args['epoch_number'] = pyip.inputInt('Epoch number [1-10000]: ', min=1, max=10000)
    args['sampling_rate'] = pyip.inputFloat('Sampling rate [0.1-1.0]: ', min=0.1, max=1.0)
    args['test_data_fraction'] = pyip.inputFloat('Test data fraction [0.1-1.0]: ', min=0.1, max=1.0)
    args['max_layer_num'] = pyip.inputInt('Maximum number of layers [3|4]: ', min=3, max=4)
    args['max_neuron_num_per_layer'] = pyip.inputInt('Maximum number of neurons per layer [2-64]: ', min=2, max=64)
    print("---------------------------------------------------------")
    
    with open(sys.argv[1] + '.json', 'w+') as outfile:
        json.dump(args, outfile)

if __name__ == "__main__":
    main()
