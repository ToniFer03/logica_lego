import numpy as np
import random

# Variables
lista_simbolos = []
simbolos_disponiveis = ['X', 'O', '+', '-']
valor_simbolos = {'X': 1, 'O': 2, '+': 3, '-': 4}
tabuleiro = []

# Define the neural network architecture
num_symbols = 5  # 'X', 'O', "+", "-" and empty space 
input_size = 25 + 12 + 1  # 5x5 board + 12 next symbols + number of symbols on the list
hidden_size_1 = 60  # Number of hidden units
hidden_size_2 = 60  # Number of hidden units
hidden_size_3 = 60  # Number of hidden units
output_size = 25  # 5x5 table positions


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

main()
