#!/usr/bin/python3

class NeuralNet():
    """
    A simple feed-forward neural network lines up neurons in layers and allows
    input from the previous layer to flow into the activation function of
    each neuron in the next layer to create a new activation function.
    
    Each neuron needs a number of weights equalling the number of inputs it
    will receive.
    """
    def __init__(self, layers_neuron_counts):
        """
        layers_neuron_counts contains the number of neurons that will be found
        in each of the layers. The first element is assumed to be the number
        of inputs.
        """
        self.layers = []
        last_layer = layers_neuron_counts[0]
        for i in range(len(layers_neuron_counts)-1):
            layer_neuron_count = layers_neuron_counts[i + 1]
            # FIXME: Hardcoding threshold
            threshold = 1
            weights = []
            new_layer = []
            for j in range(last_layer):
                # FIXME: Hardcoding all weights as 1
                weights.append(1)
            for k in range(layer_neuron_count):
                new_layer.append(Neuron(threshold, weights))
            self.layers.append(new_layer)
            last_layer = len(new_layer)

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

def main():
    print("Hello, world!")
    ann = NeuralNet([2, 2, 3, 3, 2])
    print(ann)
    input_signal = [2, 2]
    output_signal = ann.activate(input_signal)
    print("#--  Activation --#\nInput: {}\noutput: {}".format(input_signal, output_signal))

main()
