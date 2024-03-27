import numpy as np
import game
from sklearn import preprocessing


def mutate_layer(weights, biases, prob):
    for row in range(np.size(weights, 0)):
        for col in range(np.size(weights, 1)):
            if np.random.rand() < prob:
                weights[row][col] = np.random.randn() * 2 - 1

    for cell in range(len(biases)):
        if np.random.rand() < prob:
            biases[cell] = np.random.randn() * 2 - 1


def crossover_layer(weights_a, weights_b, bias_a, bias_b, prob):
    for row in range(np.size(weights_a, 0)):
        for col in range(np.size(weights_a, 1)):
            if np.random.rand() < prob:
                weights_a[row][col] = weights_b[row][col]

    for cell in range(len(bias_a)):
        if np.random.rand() < prob:
            bias_a[cell] = bias_b[cell]


class Agent:

    def __init__(self):
        self.cell_input = 16

        self.layer_1_nodes = 10
        self.FC1_layer_weights = np.random.randn(self.cell_input, self.layer_1_nodes)
        self.FC1_layer_bias = np.random.randn(self.layer_1_nodes)

        self.layer_2_nodes = 15
        self.FC2_layer_weights = np.random.randn(self.layer_1_nodes, self.layer_2_nodes)
        self.FC2_layer_bias = np.random.randn(self.layer_2_nodes)

        self.layer_3_nodes = 4
        self.FC3_layer_weights = np.random.randn(self.layer_2_nodes, self.layer_3_nodes)
        self.FC3_layer_bias = np.random.randn(self.layer_3_nodes)

        self.game_score = 0
        self.fitness_score = 0

    def run(self, mat):  #

        # pre-process the vector to be log 2 of itself
        input_vector = np.array(mat).reshape(-1, 16).squeeze()
        input_vector[input_vector != 0] = np.log2(input_vector[input_vector != 0])
        preprocessed_vector = preprocessing.normalize([input_vector]).reshape(-1, 16).squeeze()

        # calculate NN output
        layer_1 = np.maximum(np.dot(preprocessed_vector, self.FC1_layer_weights) + self.FC1_layer_bias, 0)
        layer_2 = np.maximum(np.dot(layer_1, self.FC2_layer_weights) + self.FC2_layer_bias, 0)
        layer_3 = np.maximum(np.dot(layer_2, self.FC3_layer_weights) + self.FC3_layer_bias, 0)

        # create list of the best action and the values they got
        op = [(layer_3[i], i) for i in range(4)]
        op = sorted(op, key=lambda x: x[0], reverse=True)
        return op

    def mutate(self, prob):
        mutate_layer(self.FC1_layer_weights, self.FC1_layer_bias, prob)
        mutate_layer(self.FC2_layer_weights, self.FC2_layer_bias, prob)
        mutate_layer(self.FC3_layer_weights, self.FC3_layer_bias, prob)

    def crossover(self, other_chrom, prob):
        crossover_layer(self.FC1_layer_weights, other_chrom.FC1_layer_weights,
                        self.FC1_layer_bias, other_chrom.FC1_layer_bias, prob)
        crossover_layer(self.FC2_layer_weights, other_chrom.FC2_layer_weights,
                        self.FC2_layer_bias, other_chrom.FC2_layer_bias, prob)
        crossover_layer(self.FC3_layer_weights, other_chrom.FC3_layer_weights,
                        self.FC3_layer_bias, other_chrom.FC3_layer_bias, prob)

    def fitness(self):
        avg_fitness_score = 0
        avg_game_score = 0
        for _ in range(10):
            fitness_score, game_score = game.play(self)
            avg_fitness_score += fitness_score
            avg_game_score += game_score
        avg_fitness_score /= 10
        avg_game_score /= 10
        self.fitness_score = avg_fitness_score
        self.game_score = avg_game_score
