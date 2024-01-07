import random
import math

# Variables
lista_simbolos = []
simbolos_disponiveis = ['X', 'O', '+', '-']
valor_simbolos = {'X': 1, 'O': 2, '+': 3, '-': 4}
tabuleiro = []

input_data = []
output_data = []

# Define the neural network architecture
num_symbols = 5  # 'X', 'O', "+", "-" and empty space
input_size = 25 + 12 + 1  # 5x5 board + 12 next symbols + number of symbols on the list
hidden_size_1 = 80  # Number of hidden units
hidden_size_2 = 80  # Number of hidden units
hidden_size_3 = 80  # Number of hidden units
output_size = 25  # 5x5 table positions
learning_rate = 0.01
num_episodes = 1000


# Initialize weights and biases for each layer
random.seed(80)
weights_input_hidden1 = [[random.random() for _ in range(hidden_size_1)] for _ in range(input_size)]
biases_hidden1 = [0] * hidden_size_1

weights_hidden1_hidden2 = [[random.random() for _ in range(hidden_size_2)] for _ in range(hidden_size_1)]
biases_hidden2 = [0] * hidden_size_2

weights_hidden2_hidden3 = [[random.random() for _ in range(hidden_size_3)] for _ in range(hidden_size_2)]
biases_hidden3 = [0] * hidden_size_3

weights_hidden3_output = [[random.random() for _ in range(output_size)] for _ in range(hidden_size_3)]
biases_output = [0] * output_size


def main():
    global tabuleiro
    global lista_simbolos

    tabuleiro = [[" " for _ in range(5)] for _ in range(5)]
    gerar_fila_simbolos()
    simulate_game()
    return 0


# Gerar fila random de simbolos
def gerar_fila_simbolos():
    global lista_simbolos
    global simbolos_disponiveis

    num_iterations = random.randrange(20, 40)
    for i in range(num_iterations):
        lista_simbolos.append(simbolos_disponiveis[random.randint(0, 3)])


# Activation function
def sigmoid(x):
    return 1 / (1 + math.exp(-x))


# Activation function derivative
def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))


# Função para dar update no input data
def update_input_data():
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
    layer_input = [sum(x * w for x, w in zip(input_data, weights[i])) + biases[i] for i in range(len(weights))]
    layer_output = [sigmoid(x) for x in layer_input]
    return layer_output


# Forward propagation layer 2
def forward_propagation_hidden2(hidden1_output, weights, biases):
    layer_input = [sum(x * w for x, w in zip(hidden1_output, weights[i])) + biases[i] for i in range(len(weights))]
    layer_output = [sigmoid(x) for x in layer_input]
    return layer_output


# Forward propagation layer 3
def forward_propagation_hidden3(hidden2_output, weights, biases):
    layer_input = [sum(x * w for x, w in zip(hidden2_output, weights[i])) + biases[i] for i in range(len(weights))]
    layer_output = [sigmoid(x) for x in layer_input]
    return layer_output


# Softmax function
def softmax(x):
    exp_x = [math.exp(val - max(x)) for val in x]
    return [val / sum(exp_x) for val in exp_x]


# Forward propagation output layer
def forward_propagation_output(hidden3_output, weights, biases):
    output_input = [sum(x * w for x, w in zip(hidden3_output, weights[i])) + biases[i] for i in range(len(biases))]
    output_output = softmax(output_input)
    return output_output


# Define the loss function (cross-entropy)
def calculate_loss(predictions, targets):
    return -sum(t * math.log(p) for t, p in zip(targets, predictions)) / len(predictions)


# Turn an index into a the coordinate of the board
def index_to_2d(index, num_columns):
    row = index // num_columns
    col = index % num_columns
    return row, col


# Backpropagation to update weights and biases
def backward_propagation(targets, output_layer, hidden3_output, hidden2_output, hidden1_output, input_data):
    global weights_hidden3_output
    global biases_output
    global weights_hidden2_hidden3
    global biases_hidden3
    global weights_hidden1_hidden2
    global biases_hidden2
    global weights_input_hidden1
    global biases_hidden1

    output_error = [o - t for o, t in zip(output_layer, targets)]

    # Calculate gradients for output layer
    d_weights_hidden3_output = [[h * e for h in hidden3_output] for e in output_error]
    d_biases_output = [sum(output_error)]

    # Backpropagate errors to hidden layers
    hidden3_error = [sum(w * e for w, e in zip(weights_hidden3_output[i], output_error)) * sigmoid_derivative(h)
                     for i, h in enumerate(hidden2_output)]

    hidden2_error = [sum(w * e for w, e in zip(weights_hidden2_hidden3[i], hidden3_error)) * sigmoid_derivative(h)
                     for i, h in enumerate(hidden1_output)]

    hidden1_error = [sum(w * e for w, e in zip(weights_hidden1_hidden2[i], hidden2_error)) * sigmoid_derivative(h)
                     for i, h in enumerate(input_data)]

    # Calculate gradients for hidden layers
    d_weights_hidden2_hidden3 = [[h * e for h in hidden2_output] for e in hidden3_error]
    d_biases_hidden3 = [sum(hidden3_error)]

    d_weights_hidden1_hidden2 = [[h * e for h in hidden1_output] for e in hidden2_error]
    d_biases_hidden2 = [sum(hidden2_error)]

    d_weights_input_hidden1 = [[h * e for h in input_data] for e in hidden1_error]
    d_biases_hidden1 = [sum(hidden1_error)]

    # Update weights and biases
    weights_input_hidden1 = [[w - learning_rate * d for w, d in zip(weights_input_hidden1[i], d_weights_input_hidden1[j])]
                              for i, j in enumerate(range(len(weights_input_hidden1)))]

    biases_hidden1 = [b - learning_rate * d for b, d in zip(biases_hidden1, d_biases_hidden1)]

    weights_hidden1_hidden2 = [[w - learning_rate * d for w, d in zip(weights_hidden1_hidden2[i], d_weights_hidden1_hidden2[j])]
                               for i, j in enumerate(range(len(weights_hidden1_hidden2)))]

    biases_hidden2 = [b - learning_rate * d for b, d in zip(biases_hidden2, d_biases_hidden2)]

    weights_hidden2_hidden3 = [[w - learning_rate * d for w, d in zip(weights_hidden2_hidden3[i], d_weights_hidden2_hidden3[j])]
                               for i, j in enumerate(range(len(weights_hidden2_hidden3)))]

    biases_hidden3 = [b - learning_rate * d for b, d in zip(biases_hidden3, d_biases_hidden3)]

    weights_hidden3_output = [[w - learning_rate * d for w, d in zip(weights_hidden3_output[i], d_weights_hidden3_output[j])]
                              for i, j in enumerate(range(len(weights_hidden3_output)))]

    biases_output = [b - learning_rate * d for b, d in zip(biases_output, d_biases_output)]


# Define a function to simulate the game and obtain the action (reward)
def simulate_game():
    # Replace this with your actual game logic to simulate the game and obtain the action (reward)
    # Choose an action based on the output layer probabilities
    global tabuleiro
    global lista_simbolos
    global input_data
    global weights_input_hidden1
    global biases_hidden1
    global weights_hidden1_hidden2
    global biases_hidden2
    global weights_hidden2_hidden3
    global biases_hidden3
    global weights_hidden3_output
    global biases_output

    score = 0
    while len(lista_simbolos) > 0:
        # Update input data based on the current game state
        update_input_data()

        # Forward propagation
        hidden1_output = forward_propagation_hidden1(input_data, weights_input_hidden1, biases_hidden1)
        hidden2_output = forward_propagation_hidden2(hidden1_output, weights_hidden1_hidden2, biases_hidden2)
        hidden3_output = forward_propagation_hidden3(hidden2_output, weights_hidden2_hidden3, biases_hidden3)
        output_layer = forward_propagation_output(hidden3_output, weights_hidden3_output, biases_output)
        sorted_actions = sorted(range(len(output_layer)), key=lambda k: output_layer[k], reverse=True)

        i = 0
        for action in sorted_actions:
            row, col = index_to_2d(action, 5)
            if tabuleiro[row][col] == " ":
                tabuleiro[row][col] = lista_simbolos[0]
                break
            i += 1

        if i == 25:
            # Game over
            return (score - 2**25) 

        lista_simbolos.pop(0)
        # Verificar simbolo, update no score e retirar simbolo da lista

    return score


# Define a function to update neural network weights based on the total reward obtained during the episode
def update_weights_based_on_score(total_reward):
    # Replace this with your logic to update neural network weights based on the total reward obtained during the episode
    # You might want to adjust the learning rate or use a different update strategy
    pass


# ... (call train_neural_network or other functions as needed)

main()
