"""
Created on Jul 26, 2012

@author: hadianeh
"""

from JsonCloak.JsonCloak import JsonCloak
from NeuralParrot.NeuralNet import NeuralNet
import re


class FannNet(object):
    def __init__(self):
        self.params = JsonCloak()

        self.nNeurons = []

    def load(self, path):
        try:
            f = open(path)
        except:
            print("Error: Oops! Cannot open " + path + "!")
            return False

        for i, l in enumerate(f):
            l = l.replace("\n", "")
            l = l.replace("\r", "")

            if i == 0:
                self.params.put("version", l)
                continue

            e = l.split("=")

            self.params.put(e[0], e[1])

        self.extract()

        f.close()

    def extract(self):
        layers = self.params.get("layer_sizes")
        layers = re.sub("\s*$", "", layers)
        layers = layers.split(" ")

        self.nNeurons = [(int(l) - 1) for l in layers]

        self.nn = NeuralNet(self.nNeurons)

        nnStr = self.params.get(
            "neurons (num_inputs, activation_function, activation_steepness)"
        )
        neurons = []
        m = re.match("\s*(\([^\)]+\))(.+)", nnStr)
        while m != None:
            nnStr = m.group(2)
            p = re.match("\((.+),(.+),(.+)\)", m.group(1))
            neurons.append((int(p.group(1)), int(p.group(2)), float(p.group(3))))
            m = re.match("\s*(\([^\)]+\))(.+)", nnStr)

        j = 0
        i = 0
        for n in neurons:
            if n[0] == 0:
                continue
            self.nn.neurons[j][i].__init__(n[0] - 1, self.activation[n[1]], n[2])

            i += 1
            if i == len(self.nn.neurons[j]):
                i = 0
                j += 1

        sStr = self.params.get("connections (connected_to_neuron, weight)")
        synapses = []
        m = re.match("\s*(\([^\)]+\))(.+)", sStr)
        while m != None:
            sStr = m.group(2)
            p = re.match("\((.+),(.+)\)", m.group(1))
            synapses.append((int(p.group(1)), float(p.group(2))))
            m = re.match("\s*(\([^\)]+\))(.+)", sStr)

        i = 0
        for l in self.nn.neurons:
            for n in l:
                for j in range(len(n.w)):
                    print(synapses[i])
                    n.w[j] = synapses[i][1]
                    i += 1

    def saveJson(self, path):
        self.params.save(path)

    def saveEssence(self, path):
        try:
            f = open(path, "w")
        except:
            print("Error: Oops! Cannot open " + path + "!")
            return False

        f.write(str(self.nn))

        f.close()

    activation = [
        "LINEAR",
        "THRESHOLD",
        "THRESHOLD_SYMMETRIC",
        "SIGMOID",
        "SIGMOID_STEPWISE",
        "SIGMOID_SYMMETRIC",
        "SIGMOID_SYMMETRIC_STEPWISE",
        "GAUSSIAN",
        "GAUSSIAN_SYMMETRIC",
        "GAUSSIAN_STEPWISE",
        "ELLIOT",
        "ELLIOT_SYMMETRIC",
        "LINEAR_PIECE",
        "LINEAR_PIECE_SYMMETRIC",
        "SIN_SYMMETRIC",
        "COS_SYMMETRIC",
    ]

    # ERRORFUNC_LINEAR = _libfann.ERRORFUNC_LINEAR
    # ERRORFUNC_TANH = _libfann.ERRORFUNC_TANH

    # STOPFUNC_MSE = _libfann.STOPFUNC_MSE
    # STOPFUNC_BIT = _libfann.STOPFUNC_BIT

    # TRAIN_INCREMENTAL = _libfann.TRAIN_INCREMENTAL
    # TRAIN_BATCH = _libfann.TRAIN_BATCH
    # TRAIN_RPROP = _libfann.TRAIN_RPROP
    # TRAIN_QUICKPROP = _libfann.TRAIN_QUICKPROP

    # LAYER = _libfann.LAYER
    # SHORTCUT = _libfann.SHORTCUT


if __name__ == "__main__":
    fannNet = FannNet()

    app = "xor_float"

    app = "sobel"
    app = "inversek2j"
    app = "jmeint"
    app = "jpeg"
    app = "fft"
    app = "kmeans"

    fannNet.load("./" + app + ".nn")
    fannNet.saveJson("./" + app + ".params.json")
    fannNet.saveEssence("./" + app + ".essence.json")

    exit()
    x = [-1, -1]
    y = fannNet.nn.compute(x)
    print(x, y)

    x = [-1, 1]
    y = fannNet.nn.compute(x)
    print(x, y)

    x = [1, -1]
    y = fannNet.nn.compute(x)
    print(x, y)

    x = [1, 1]
    y = fannNet.nn.compute(x)
    print(x, y)

    exit(0)
