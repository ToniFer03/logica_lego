import random
import math
import json
from datetime import datetime

# Variables
valor_simbolos = {'X': 1, 'O': 2, '+': 3, '-': 4}

input_data = []
output_data = []

# Define the neural network architecture
num_symbols = 5  # 'X', 'O', "+", "-" and empty space
input_size = 25 + 12 + 1 + 4  # 5x5 board + 12 next symbols + number of symbols on the list, number of each symbol
hidden_size_1 = 80  # Number of hidden units
hidden_size_2 = 80  # Number of hidden units
hidden_size_3 = 80  # Number of hidden units
output_size = 25  # 5x5 table positions
num_epochs = 10


random.seed(80)


# Initialize weights and biases for each layer
weights_input_hidden1 = [[random.random() for _ in range(input_size)] for _ in range(hidden_size_1)]
biases_hidden1 = [0.5] * hidden_size_1

weights_hidden1_hidden2 = [[random.random() for _ in range(hidden_size_1)] for _ in range(hidden_size_2)]
biases_hidden2 = [0.5] * hidden_size_2

weights_hidden2_hidden3 = [[random.random() for _ in range(hidden_size_2)] for _ in range(hidden_size_3)]
biases_hidden3 = [0.5] * hidden_size_3

weights_hidden3_output = [[random.random() for _ in range(hidden_size_3)] for _ in range(output_size)]
biases_output = [0.5] * output_size

output_layer = []


training_inputs = []
training_targets = []


# Activation function
def sigmoid(x):
    if isinstance(x, list):
        return [1 / (1 + math.exp(-val)) for val in x]
    else:
        return 1 / (1 + math.exp(-x))


# Activation function derivative
def sigmoid_derivative(x):
    if isinstance(x, list):
        return [sig * (1 - sig) for sig in sigmoid(x)]
    else:
        return sigmoid(x) * (1 - sigmoid(x))


# Softmax function
def softmax(x):
    exp_x = [math.exp(val - max(x)) for val in x]
    return [val / sum(exp_x) for val in exp_x]


# Softmax derivative
def softmax_derivative(x):
    s = softmax(x)
    return [s_i * (1 - s_i) for s_i in s]


# Forward propagation layer 1
def forward_propagation_hidden1(input_data, weights, biases):
    layer_input = [sum(x * w for x, w in zip(input_data, weights[i])) + biases[i] for i in range(len(weights))]
    layer_output = [sigmoid(x) for x in layer_input]
    return layer_output


# Forward propagation layer 2
def forward_propagation_hidden2(hidden1_output, weights, biases):
    layer_input = [sum(x * w for x, w in zip(hidden1_output, weights[i])) + biases[i] for i in range(len(weights))]
    layer_output = sigmoid(layer_input)
    return layer_output


# Forward propagation layer 3
def forward_propagation_hidden3(hidden2_output, weights, biases):
    layer_input = [sum(x * w for x, w in zip(hidden2_output, weights[i])) + biases[i] for i in range(len(weights))]
    layer_output = sigmoid(layer_input)
    return layer_output


# Forward propagation output layer
def forward_propagation_output(hidden3_output, weights, biases):
    output_input = [sum(x * w for x, w in zip(hidden3_output, weights[i])) + biases[i] for i in range(len(biases))]
    output_output = softmax(output_input)
    return output_output


# Calculate the output error
def calculate_output_error(predictions, targets):
    # Calculate the error for each output neuron
    output_error = [predictions[i] - target for i, target in enumerate(targets)]
    return output_error


# Calculate the error for each neuron in the hidden layer 3
def calculate_hidden3_error(output_gradient, weights_hidden3_output):
    # Calculate the error in hidden layer 3 using the chain rule
    hidden3_error = [sum(output_gradient[i] * weights_hidden3_output[j][i] for i in range(len(output_gradient))) for j in range(len(weights_hidden3_output))]
    return hidden3_error


def calculate_hidden2_error(hidden3_gradient, weights_hidden2_hidden3):
    # Calculate the error in hidden layer 2 using the chain rule
    hidden2_error = [sum(hidden3_gradient[i] * weights_hidden2_hidden3[j][i] for i in range(len(hidden3_gradient))) for j in range(len(weights_hidden2_hidden3))]
    return hidden2_error


def calculate_hidden1_error(hidden2_gradient, weights_hidden1_hidden2):
    # Calculate the error in hidden layer 1 using the chain rule
    hidden1_error = [sum(hidden2_gradient[i] * weights_hidden1_hidden2[j][i] for i in range(len(hidden2_gradient))) for j in range(len(weights_hidden1_hidden2))]
    return hidden1_error


# Receives the inputs, the desired target, and the inputs of all layers
def backward_propagation(inputs, targets, hidden1_output, hidden2_output, hidden3_output, predictions):
    global weights_input_hidden1
    global weights_hidden1_hidden2
    global weights_hidden2_hidden3
    global weights_hidden3_output
    global biases_hidden1
    global biases_hidden2
    global biases_hidden3
    global biases_output
    
    softmax_target = softmax(targets)
    
    output_error = calculate_output_error(predictions, softmax_target)
    # Initialize an empty list to store the output gradients
    output_gradient = []
    softmax_derivative_predictions = softmax_derivative(predictions)

    # Iterate over each output neuron's index and its corresponding output value
    for i, prediction in enumerate(softmax_derivative_predictions):
        # Calculate the gradient for the current output neuron
        current_output_gradient = output_error[i] * prediction
        # Append the current output gradient to the list
        output_gradient.append(current_output_gradient)


    # Calculate hidden layer 3 error and gradient
    hidden3_error = calculate_hidden3_error(output_gradient, weights_hidden3_output)
    hidden3_gradient = []
    sigmoid_derivative_hidden3_output = sigmoid_derivative(hidden3_output)

    for i, hidden3_value in enumerate(sigmoid_derivative_hidden3_output):
        current_hidden3_gradients = hidden3_error[i] * hidden3_value
        hidden3_gradient.append(current_hidden3_gradients)


    # Calculate hidden layer 2 error and gradient
    hidden2_error = calculate_hidden2_error(hidden3_gradient, weights_hidden2_hidden3)
    hidden2_gradient = []
    sigmoid_derivative_hidden2_output = sigmoid_derivative(hidden2_output)
    for i, hidden2_value in enumerate(sigmoid_derivative_hidden2_output):
        current_hidden2_gradient = hidden2_error[i] * hidden2_value
        hidden2_gradient.append(current_hidden2_gradient)

    
    # Calculate hidden layer 1 error and gradient
    hidden1_error = calculate_hidden1_error(hidden2_gradient, weights_hidden1_hidden2)
    hidden1_gradient = []
    sigmoid_derivative_hidden1_output = sigmoid_derivative(hidden1_output)
    for i, hidden1_value in enumerate(sigmoid_derivative_hidden1_output):
        current_hidden1_gradient = hidden1_error[i] * hidden1_value
        hidden1_gradient.append(current_hidden1_gradient)
    

    # Update weights and biases for each layer
    update_weight_input_layer1(inputs, hidden1_gradient)
    update_weight_hidden1_layer2(hidden1_output, hidden2_gradient)
    update_weight_hidden2_layer3(hidden2_output, hidden3_gradient)
    update_weight_hidden3_output(hidden3_output, output_gradient)
    update_bias_output(output_error)
    update_bias_hidden3(hidden3_error)
    update_bias_hidden2(hidden2_error)
    update_bias_hidden1(hidden1_error)




def update_weight_input_layer1(inputs, gradients, learning_rate=0.01):
    global weights_input_hidden1
    global biases_hidden1

    for i, row in enumerate(weights_input_hidden1):
        for j, weight in enumerate(row):
            weights_input_hidden1[i][j] -= learning_rate * gradients[i] * inputs[i]


def update_bias_hidden1(gradients, learning_rate=0.01):
    global biases_hidden1

    for i, bias in enumerate(biases_hidden1):
        biases_hidden1[i] -= learning_rate * gradients[i]


def update_weight_hidden1_layer2(hidden1_output, gradients, learning_rate=0.01):
    global weights_hidden1_hidden2
    global biases_hidden2

    for i, row in enumerate(weights_hidden1_hidden2):
        for j, weight in enumerate(row):
            weights_hidden1_hidden2[i][j] -= learning_rate * gradients[i] * hidden1_output[i]
    

def update_bias_hidden2(gradients, learning_rate=0.01):
    global biases_hidden2

    for i, bias in enumerate(biases_hidden2):
        biases_hidden2[i] -= learning_rate * gradients[i]


def update_weight_hidden2_layer3(hidden2_output, gradients, learning_rate=0.01):
    global weights_hidden2_hidden3
    global biases_hidden3

    for i, row in enumerate(weights_hidden2_hidden3):
        for j, weight in enumerate(row):
            weights_hidden2_hidden3[i][j] -= learning_rate * gradients[i] * hidden2_output[i]


def update_bias_hidden3(gradients, learning_rate=0.01):
    global biases_hidden3

    for i, bias in enumerate(biases_hidden3):
        biases_hidden3[i] -= learning_rate * gradients[i]


def update_weight_hidden3_output(hidden3_output, gradients, learning_rate=0.01):
    global weights_hidden3_output
    global biases_output

    for i, row in enumerate(weights_hidden3_output):
        for j, weight in enumerate(row):
            weights_hidden3_output[i][j] -= learning_rate * gradients[i] * hidden3_output[i]


def update_bias_output(gradients, learning_rate=0.01):
    global biases_output

    for i, bias in enumerate(biases_output):
        biases_output[i] -= learning_rate * gradients[i]


def load_training_data():
    global training_inputs
    global training_targets

    with open('training_data.json', 'r') as file:
        training_data_list = json.load(file)

    # Extract inputs and targets from the list of objects
    training_inputs = [obj['inputs'] for obj in training_data_list]
    training_targets = [obj['targets'] for obj in training_data_list]



def main():
    global num_epochs
    global training_inputs
    global training_targets


    load_training_data()
    # An epoch represent a full iteration over the training data
    # Train the neural network
    for epoch in range(num_epochs):
        global weights_input_hidden1
        global biases_hidden1
        global weights_hidden1_hidden2
        global biases_hidden2
        global weights_hidden2_hidden3
        global biases_hidden3
        global weights_hidden3_output
        global biases_output


        for input_data, target in zip(training_inputs, training_targets):
            # Forward propagation
            hidden1_output = forward_propagation_hidden1(input_data, weights_input_hidden1, biases_hidden1)
            hidden2_output = forward_propagation_hidden2(hidden1_output, weights_hidden1_hidden2, biases_hidden2)
            hidden3_output = forward_propagation_hidden3(hidden2_output, weights_hidden2_hidden3, biases_hidden3)
            predictions = forward_propagation_output(hidden3_output, weights_hidden3_output, biases_output)

            # Backpropagation
            backward_propagation(input_data, target, hidden1_output, hidden2_output, hidden3_output, predictions)




main()