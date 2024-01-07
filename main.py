import numpy as np
import random

# Variables
lista_simbolos = []
simbolos_disponiveis = ['X', 'O', '+', '-']
valor_simbolos = {'X': 1, 'O': 2, '+': 3, '-': 4}
tabuleiro = []
score = 0

input_data = []
output_data = []

# Define the neural network architecture
num_symbols = 5  # 'X', 'O', "+", "-" and empty space 
input_size = 25 + 12 + 1  # 5x5 board + 12 next symbols + number of symbols on the list
hidden_size_1 = 60  # Number of hidden units
hidden_size_2 = 60  # Number of hidden units
hidden_size_3 = 60  # Number of hidden units
output_size = 25  # 5x5 table positions
learning_rate = 0.01
num_epochs = 1000


# Initialize weights and biases for each layer
np.random.seed(42)
weights_input_hidden1 = np.random.rand(input_size, hidden_size_1)
biases_hidden1 = np.zeros((1, hidden_size_1))

weights_hidden1_hidden2 = np.random.rand(hidden_size_1, hidden_size_2)
biases_hidden2 = np.zeros((1, hidden_size_2))

weights_hidden2_hidden3 = np.random.rand(hidden_size_2, hidden_size_3)
biases_hidden3 = np.zeros((1, hidden_size_3))

weights_hidden3_output = np.random.rand(hidden_size_3, output_size)
biases_output = np.zeros((1, output_size))


def main():
    global tabuleiro
    global score
    global lista_simbolos

    tabuleiro = [[" " for _ in range(5)] for _ in range(5)]
    gerar_fila_simbolos()
    return 0



# Gerar fila random de simbolos
def gerar_fila_simbolos():
    global lista_simbolos
    global simbolos_disponiveis
    global valor_simbolos

    num_iterations = random.randrange(20, 40)
    for i in range(num_iterations):
        lista_simbolos.append(simbolos_disponiveis[np.random.randint(0, 4)])




# Activation function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# Activation function derivative
def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))


# Função para dar update no input data
def update_inputData():
    global input_data
    global tabuleiro
    global lista_simbolos
    global valor_simbolos

    input_data = []

    # Update os primeiros 25 valores do input data com o tabuleiro
    for i in range(5):
        for j in range(5):
            if tabuleiro[i][j] == " ":
                input_data.append(0)
            else:
                input_data.append(valor_simbolos[tabuleiro[i][j]])

    # Update os 12 valores seguintes com os simbolos da lista
    for i in range(12):
        if i < len(lista_simbolos):
            input_data.append(valor_simbolos[lista_simbolos[i]])
        else:
            input_data.append(0)

    input_data.append(len(lista_simbolos))


# Forward propagation layer 1
def forward_propagation_hidden1(input_data, weights, biases):
    layer_input = np.dot(input_data, weights) + biases
    layer_output = sigmoid(layer_input)
    return layer_output

# Forward propagation layer 2
def forward_propagation_hidden2(hidden1_output, weights, biases):
    layer_input = np.dot(hidden1_output, weights) + biases
    layer_output = sigmoid(layer_input)
    return layer_output

# Forward propagation layer 3
def forward_propagation_hidden3(hidden2_output, weights, biases):
    layer_input = np.dot(hidden2_output, weights) + biases
    layer_output = sigmoid(layer_input)
    return layer_output

# Softmax function
def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

# Forward propagation output layer
def forward_propagation_output(hidden3_output, weights, biases):
    output_input = np.dot(hidden3_output, weights) + biases
    output_output = softmax(output_input)
    return output_output

main()
