"""
Neural Network class/

A simple feedforwards neural network where:
- Weights are evolved by the genetic algorithm (no backprop)
- Genome = flattened array of all weights and biases
- fixed topology (structure doesn't change, only weights/biases)
"""

import numpy as np
from typing import List, Tuple

class NeuralNetwork:
    """
    Neural Network class for MazeRunner.
    
    Implements:
        REQ-1.1: Feed-forward neural network with configurable topology
        REQ-1.2: Xavier weight initialization (https://www.geeksforgeeks.org/deep-learning/xavier-initialization/)
        REQ-1.3: Tanh activation function (https://www.geeksforgeeks.org/deep-learning/tanh-activation-in-neural-network/)
        REQ-1.4: Forward pass method
        REQ-1.5: get_genome() method
        REQ-1.6: set_genome() method
        REQ-1.7: mutate() method
        REQ-1.8: crossover() static method
        REQ-1.9: copy() method
    """
    def __init__(self, layer_sizes: Tuple[int, ...] = (6, 8, 2)):
        """
        Initalize neural network with random weights.

        Args:
            layer sizes: tuple of layer sizes (6, 8, 2) means:
                - 6 input neurons (e.g. sensor distances + goal angle)
                - 8 hidden neurons
                - 2 output neurons (turn angle, turn speed)

        REQ-1.1, REQ-1.2
        """         
        
        self.layer_sizes = layer_sizes
        self.num_layers = len(layer_sizes)
        #initalizes weights and biases with random values
        self.biases: List[np.ndarray] = []
        self.weights: List[np.ndarray] = []

        for i in range(self.num_layers - 1):
            # Xavier initialization (https://www.geeksforgeeks.org/deep-learning/xavier-initialization/): helps with training stability
            scale = np.sqrt(2.0 / (layer_sizes[i] + layer_sizes[i+1]))
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * scale
            b = np.zeros(layer_sizes[i+1])  # Biases start at zero

            self.weights.append(w)
            self.biases.append(b)

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        """
        Forward pass through the network (https://en.wikipedia.org/wiki/Feedforward_neural_network)
        Args:
            inputs: Input array of shape (input_size,)
        Returns:
            Output array of shape (output_size,)

        Implements: REQ-1.3, REQ-1.4
        """
        # force inputs are np array
        x = np.array(inputs, dtype=np.float32)

        for i in range(len(self.weights)):
            #linear transformation
            x = x @ self.weights[i] + self.biases[i]
            #activation function (tanh: squashes outputs between -1 and 1) (https://www.geeksforgeeks.org/deep-learning/tanh-activation-in-neural-network/)
            x = np.tanh(x)
        return x
    
    def get_genome(self) -> np.ndarray:
        """
        Flatten all weights and biases into a 1d array (genome)

        This is what the genetic algorithm will manipulate.

        Returns:
            1d numpy array of all network params

        Implements: REQ-1.5
        """
        genes = []

        for w, b in zip(self.weights, self.biases):
            genes.append(w.flatten())
            genes.append(b.flatten())

        return np.concatenate(genes)
    
    def set_genome(self, genome: np.ndarray):
        """
        Load weights and biases from 1 genome array
        
        Aegs:
            genome: 1d array from get_genome() or GA operations
        
        Implements: REQ-1.6
        """
        idx = 0

        for i in range(len(self.weights)):
            # gets weight matrix shape
            w_shape = self.weights[i].shape
            w_size = w_shape[0] * w_shape[1]

            #extract and reshape weights
            self.weights[i] = genome[idx:idx + w_size].reshape(w_shape)
            idx += w_size

            # extract biases
            b_size = self.biases[i].shape[0]
            self.biases[i] = genome[idx:idx + b_size]
            idx += b_size

    def copy(self) -> 'NeuralNetwork':
        """ 
        Create a deep copy of this network
        
        Implements: REQ-1.9
        """
        new_nn = NeuralNetwork(self.layer_sizes)
        new_nn.set_genome(self.get_genome())
        return new_nn
    
    def mutate(self, mutation_rate: float = 0.01, mutation_strength: float = 0.1):
        """
        Mutate weights in place
        Args:
            mutation_rate: probability of each gene being mutated
            mutation_strength: stdev of mutation noise
        """
        genome = self.get_genome()

        mask = np.random.random(len(genome)) < mutation_rate

        # add gaussian noise to selected genes
        mutations = np.random.randn(len(genome)) * mutation_strength
        genome[mask] += mutations[mask]

        self.set_genome(genome)

    @staticmethod
    def crossover(parent1: 'NeuralNetwork', parent2: 'NeuralNetwork') -> 'NeuralNetwork':
        """
        Create a child network by crossing over two parents
        Args:
            parent1: first parent network
            parent2: second parent network
        Returns:
            child network with mixed genome
        Implements: REQ-1.8
        """
        genome1 = parent1.get_genome()
        genome2 = parent2.get_genome()

        assert len(genome1) == len(genome2), "Genomes must be same length for crossover"

        # Uniform crossover: randomly pick a gene from either parent
        mask = np.random.random(len(genome1)) < 0.5
        child_genome = np.where(mask, genome1, genome2)

        child = NeuralNetwork(parent1.layer_sizes)
        child.set_genome(child_genome)

        return child
    
    def __repr__(self):
        return f"NeuralNetwork(layers={self.layer_sizes}), params+{len(self.get_genome())}"
    
    