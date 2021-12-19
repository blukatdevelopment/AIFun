#!/usr/bin/python3
import random

def int_to_bitstring(int_val):
    """
    little-endian 4-bit int with a leading negative bit
    """
    prefix = ""
    if int_val < 0:
        prefix += "1"
        int_val *= -1
    else:
        prefix += "0" 
    return prefix + "{0:04b}".format(int_val)

def bitstring_to_int(bitstring):
    """ Converts four binary digits and multiplies by leading negative bit"""
    output = 1 if bitstring[4] == "1" else 0
    output += 2 if bitstring[3] == "1" else 0
    output += 4 if bitstring[2] == "1" else 0
    output += 8 if bitstring[1] == "1" else 0
    output *= -1 if bitstring[0] == "1" else 1
    return output

def bitstring_to_int_array(bitstring):
    """ Convert a bunch of bitstrings into an int array"""
    ints = []
    chunks = len(bitstring)
    for i in range(0, chunks, 5):
        ints.append(bitstring_to_int(bitstring[i:i+5]))
    return ints
    
def int_array_to_bitstring(int_array):
    """ Convert a list of ints to a bitstring """
    output = ""
    for i in int_array:
        output += int_to_bitstring(i)
    return output    
        

class NeuralNet():

    """
    A simple feed-forward neural network lines up neurons in layers and allows
    input from the previous layer to flow into the activation function of
    each neuron in the next layer to create a new activation function.
    
    Each neuron needs a number of weights equalling the number of inputs it
    will receive.
    """
    def __init__(self, layers_neuron_counts, bitstring = None, thresholds=None, weights=None):
        """
        Picks a constructor.
        """
        if bitstring != None:
            self.bitstring_constructor(layers_neuron_counts, bitstring)
        else:
            self.default_constructor(layers_neuron_counts, thresholds, weights)

    def default_constructor(self, layers_neuron_counts, thresholds=None, weights=None):
        """
        layers_neuron_counts contains the number of neurons that will be found
        in each of the layers.
        Accepts a list of thresholds and weights.
        If the thresholds and weights are None, they will be randomly generated.
        
        """
        if thresholds == None:
            thresholds = self.random_thresholds(layers_neuron_counts)
        if weights == None:
            weights = self.random_weights(layers_neuron_counts)
        self.layers = []
        last_layer = layers_neuron_counts[0]
        for i in range(len(layers_neuron_counts)-1):
            layer_neuron_count = layers_neuron_counts[i + 1]
            neuron_weights = []
            new_layer = []
            for j in range(last_layer):
                neuron_weights.append(weights.pop(0))
            for k in range(layer_neuron_count):
                new_layer.append(Neuron(thresholds.pop(0), neuron_weights))
            self.layers.append(new_layer)
            last_layer = len(new_layer)

    def bitstring_constructor(self, layers_neuron_counts, bitstring):
        """
        layers_neuron_counts contains the number of neurons that will be found
        in each of the layers.
        Constructor building from a bitstring
        """
        ints = bitstring_to_int_array(bitstring)
        self.layers = []
        last_layer = layers_neuron_counts[0]
        for i in range(len(layers_neuron_counts)-1):
            layer_neuron_count = layer_neuron_counts[i + 1]
            new_layer = []
            for j in range(layer_neuron_Count):
                
                threshold = ints.pop(0)
                weights = []
                for k in range(last_layer):
                    weights += ints.pop(0)
                new_layer.append(Neuron(threshold, weights))
            last_layer = layers_neuron_count
    
    def int_array(self):
        output = []
        for layer in self.layers:
            for neuron in layer:
                output.append(neuron.threshold)
                output = output + neuron.weights
        return output
    
    def random_thresholds(self, layers_neuron_counts):
        out = []
        for i in range(len(layers_neuron_counts)):
            for j in range(i):
                out.append(random.randrange(-10, 10, 1))
        return out
    
    def random_weights(self, layers_neuron_counts):
        out = []
        for i in range(len(layers_neuron_counts)):
            for j in range(layers_neuron_counts[i]):
                out.append(random.randrange(-10, 10, 1))
        return out

    def __str__(self):
        """
        Human-readible string representation of Neural Net.
        """
        out = "Neural Net: ["
        for i in range(len(self.layers)):
            out += str(len(self.layers[i]))
            if i < len(self.layers[i]):
                out += ","
        out += "]"
        
        out += "\n#--  Layers  --#"
        for i in range(len(self.layers)):
            out += "\nLayer {} [".format(i)
            for j in range(len(self.layers[i])):
                out += "\n\t" + str(self.layers[i][j])
            out += "\n]"
        return out
        
    def activate(self, input_signal):
        """
        Propagate the input signal throughout the network, one layer at a time.
        """
        for i in range(len(self.layers)):
            current_layer = self.layers[i]
            output_signal = []
            
            for j in range(len(current_layer)):
                neuron = current_layer[j]
                output_signal.append(neuron.activate(input_signal))
            input_signal = output_signal
        return input_signal
    
    def get_bitstring(self):
        out = ""
        for layer in self.layers:
            for neuron in layer:
                out += neuron.get_bitstring()
        return out
    
    def get_int_array(self):
        out = []
        for layer in self.layers:
            for neuron in layer:
                out = out + neuron.get_int_array()
        return out

class Neuron():
    """
    A neuron receives a list of inputs, applies weights to them,
    and then compares the sum to the threshold.
        
    """
    def __init__(self, threshold, weights):
        self.threshold = threshold
        self.weights = weights
    
    def activate(self, inputs):
        weighted_input_sum = 0
        for i in range(len(inputs)):
            input_value = inputs[i]
            weight = self.weights[i]
            weighted_input_value = weight * input_value
            weighted_input_sum += weighted_input_value
        if weighted_input_sum >= self.threshold:
            return 1
        return 0

    def __str__(self):
        return "NEURON[Threshold = {}, Weights = {}]".format(self.threshold, self.weights)        
    
    def get_int_array(self):
        output = []
        output.append(self.threshold)
        for weight in self.weights:
            output.append(weight)
        return output
    
    def get_bitstring(self):
        output = int_to_bitstring(self.threshold)
        for weight in self.weights:
            output += int_to_bitstring(weight)
        return output



def bitstring_demo():
    """
    Debuggging function
    """
    test_set = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    bitstring = ""
    for i in test_set:
        bits = int_to_bitstring(i)
        int_again = bitstring_to_int(bits)
        print("i: {}, bit: {}, converted back: {}".format(i, bits, int_again))
        bitstring += bits
    int_array = bitstring_to_int_array(bitstring)
    print("Bitstring: {} \n Int array: {}".format(bitstring, int_array))

def ann_bits_demo():
    layers_neuron_counts = [3, 1, 2]
    int_array = [1, 1, 1, 1, 1, 1, 1, 1]
    print("Before {}".format(int_array))
    bitstring = int_array_to_bitstring(int_array)
    ann = NeuralNet(layers_neuron_counts, bitstring)
    ann_int_array = ann.get_int_array()
    
    print("Start: {}\nEnd: {}".format(int_array, ann_int_array))
    print(ann)

def main():
    random.seed()
    print("Hello, world!")
    layers_neuron_counts = [2, 2, 3, 3, 2]
    ann = NeuralNet(layers_neuron_counts)
    #print(ann)
    input_signal = [1, 0]
    output_signal = ann.activate(input_signal)
    #print("#--  Activation --#\nInput: {}\noutput: {}".format(input_signal, output_signal))
    bitstring = ann.get_bitstring()
    #print("Bitstring: " + bitstring)
    int_array = bitstring_to_int_array(bitstring)
    #print("As int array: {}".format(int_array))
    parsed_ann = NeuralNet(layers_neuron_counts, int_array)
    #print(parsed_ann)
    ann_array = ann.int_array()
    parsed_ann_array = parsed_ann.int_array()
    print("First: {}\n Second: {}".format(ann.get_bitstring(), parsed_ann.get_bitstring()))
    
ann_bits_demo()
#main()
