import random
import math
import pickle # Para guardar os pesos
from datetime import datetime

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

best_score = float('-inf')  # Initialize the best score to negative infinity
all_scores = []  # List to store all scores obtained during training
num_simulacoes_ate_agora = 0


# Estatisticas
micro_x_formados = 0
micro_cruz_formados = 0
micro_bola_formados = 0
micro_traco_formados = 0
macro_x_formados = 0
macro_cruz_formados = 0
macro_bola_formados = 0
macro_traco_formados = 0


# Initialize weights and biases for each layer
random.seed(80)
weights_input_hidden1 = [[random.random() for _ in range(hidden_size_1)] for _ in range(input_size)]
biases_hidden1 = [0.5] * hidden_size_1

weights_hidden1_hidden2 = [[random.random() for _ in range(hidden_size_2)] for _ in range(hidden_size_1)]
biases_hidden2 = [0.5] * hidden_size_2

weights_hidden2_hidden3 = [[random.random() for _ in range(hidden_size_3)] for _ in range(hidden_size_2)]
biases_hidden3 = [0.5] * hidden_size_3

weights_hidden3_output = [[random.random() for _ in range(output_size)] for _ in range(hidden_size_3)]
biases_output = [0.5] * output_size


# Posicoes
# ----------------------------------------------------------------------------------------------------------
# Todos posições posiveis fazendo um x num tabuleiro 5x5
posicoes_x = [
    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (0, 4), (1, 3), (3, 1), (4, 0)],
    [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
    [(0, 1), (0, 3), (1, 2), (2, 1), (2, 3)],
    [(0, 2), (0, 4), (1, 3), (2, 2), (2, 4)],
    [(1, 0), (1, 2), (2, 1), (3, 0), (3, 2)],
    [(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)],
    [(1, 2), (1, 4), (2, 3), (3, 2), (3, 4)],
    [(2, 0), (2, 2), (3, 1), (4, 0), (4, 2)],
    [(2, 1), (2, 3), (3, 2), (4, 1), (4, 3)],
    [(2, 2), (2, 4), (3, 3), (4, 2), (4, 4)],
]

# Todos posições posiveis fazendo uma cruz num tabuleiro 5x5
posicoes_cruz = [
    [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 2), (4, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 2), (1, 1), (1, 2), (1, 3), (2, 2)],
    [(0, 3), (1, 2), (1, 3), (1, 4), (2, 3)],
    [(1, 1), (2, 0), (2, 1), (2, 2), (3, 1)],
    [(1, 2), (2, 1), (2, 2), (2, 3), (3, 2)],
    [(1, 3), (2, 2), (2, 3), (2, 4), (3, 3)],
    [(2, 1), (3, 0), (3, 1), (3, 2), (4, 1)],
    [(2, 2), (3, 1), (3, 2), (3, 3), (4, 2)],
    [(2, 3), (3, 2), (3, 3), (3, 4), (4, 3)],
]


# Todos posições posiveis fazendo uma bola num tabuleiro 5x5
posicoes_bola = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
    [(0, 1), (0, 2), (0, 3), (1, 1), (1, 3), (2, 1), (2, 2), (2, 3)],
    [(0, 2), (0, 3), (0, 4), (1, 2), (1, 4), (2, 2), (2, 3), (2, 4)],
    [(1, 0), (1, 1), (1, 2), (2, 0), (2, 2), (3, 0), (3, 1), (3, 2)],
    [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)],
    [(1, 2), (1, 3), (1, 4), (2, 2), (2, 4), (3, 2), (3, 3), (3, 4)],
    [(2, 0), (2, 1), (2, 2), (3, 0), (3, 2), (4, 0), (4, 1), (4, 2)],
    [(2, 1), (2, 2), (2, 3), (3, 1), (3, 3), (4, 1), (4, 2), (4, 3)],
    [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 1), (0, 2), (1, 1), (1, 2)],
    [(0, 2), (0, 3), (1, 2), (1, 3)],
    [(0, 3), (0, 4), (1, 3), (1, 4)],
    [(1, 0), (1, 1), (2, 0), (2, 1)],
    [(1, 1), (1, 2), (2, 1), (2, 2)],
    [(1, 2), (1, 3), (2, 2), (2, 3)],
    [(1, 3), (1, 4), (2, 3), (2, 4)],
    [(2, 0), (2, 1), (3, 0), (3, 1)],
    [(2, 1), (2, 2), (3, 1), (3, 2)],
    [(2, 2), (2, 3), (3, 2), (3, 3)],
    [(2, 3), (2, 4), (3, 3), (3, 4)],
    [(3, 0), (3, 1), (4, 0), (4, 1)],
    [(3, 1), (3, 2), (4, 1), (4, 2)],
    [(3, 2), (3, 3), (4, 2), (4, 3)],
    [(3, 3), (3, 4), (4, 3), (4, 4)],
]


# Todas as posicoes para fazer um traco num tabuleiro 5x5
posicoes_traco = [
    [(0, 0), (0, 1), (0, 2)],
    [(0, 1), (0, 2), (0, 3)],
    [(0, 2), (0, 3), (0, 4)],
    [(1, 0), (1, 1), (1, 2)],
    [(1, 1), (1, 2), (1, 3)],
    [(1, 2), (1, 3), (1, 4)],
    [(2, 0), (2, 1), (2, 2)],
    [(2, 1), (2, 2), (2, 3)],
    [(2, 2), (2, 3), (2, 4)],
    [(3, 0), (3, 1), (3, 2)],
    [(3, 1), (3, 2), (3, 3)],
    [(3, 2), (3, 3), (3, 4)],
    [(4, 0), (4, 1), (4, 2)],
    [(4, 1), (4, 2), (4, 3)],
    [(4, 2), (4, 3), (4, 4)],
    [(0, 0), (0, 1)],
    [(0, 1), (0, 2)],
    [(0, 2), (0, 3)],
    [(0, 3), (0, 4)],
    [(1, 0), (1, 1)],
    [(1, 1), (1, 2)],
    [(1, 2), (1, 3)],
    [(1, 3), (1, 4)],
    [(2, 0), (2, 1)],
    [(2, 1), (2, 2)],
    [(2, 2), (2, 3)],
    [(2, 3), (2, 4)],
    [(3, 0), (3, 1)],
    [(3, 1), (3, 2)],
    [(3, 2), (3, 3)],
    [(3, 3), (3, 4)],
    [(4, 0), (4, 1)],
    [(4, 1), (4, 2)],
    [(4, 2), (4, 3)],
    [(4, 3), (4, 4)]]


# Função que verifica se existe uma microfigura x no tabuleiro
def verifica_existencia_micro_x(tabuleiro_temp):
    temp_posicao = posicoes_x[1:]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[0]:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 5:
                return True

    return False


# Função que verifica se existe uma microfigura cruz no tabuleiro
def verifica_existencia_micro_cruz(tabuleiro_temp):
    temp_posicao = posicoes_cruz[1:]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[2]:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 5:
                return True

    return False


# Função que verifica se existe uma microfigura bola no tabuleiro
def verifica_existencia_micro_bola(tabuleiro_temp):
    temp_posicao = posicoes_bola[9:]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[1]:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 4:
                return True

    return False


# Função que verifica se existe uma microfigura traco no tabuleiro
def verifica_existencia_micro_traco(tabuleiro_temp):
    temp_posicao = posicoes_traco[15:]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[3]:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 2:
                return True

    return False


# Função que verifica se existe uma macrofigura x no tabuleiro
def verifica_existencia_macro_x(tabuleiro_temp):
    temp_posicao = posicoes_x[:1]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[0]:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 9:
                return True

    return False


# Função que verifica se existe uma macrofigura cruz no tabuleiro
def verifica_existencia_macro_cruz(tabuleiro_temp):
    temp_posicao = posicoes_cruz[:1]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[2]:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 9:
                return True

    return False


# Função que verifica se existe uma macrofigura bola no tabuleiro
def verifica_existencia_macro_bola(tabuleiro_temp):
    temp_posicao = posicoes_cruz[:9]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[1]:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 8:
                return True

    return False


# Função que verifica se existe uma macrofigura traco no tabuleiro
def verifica_existencia_macro_traco(tabuleiro_temp):
    temp_posicao = posicoes_traco[:15]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[3]:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 3:
                return True

    return False


def verificar_microfiguras(figura, tabuleiro_temp):
    temp_posicao = []
    temp_score = 0
    num_correspondecias = 0

    # X
    if figura == simbolos_disponiveis[0]:
        if verifica_existencia_micro_x(tabuleiro_temp):
            micro_x_formados += 1
            temp_todas_posicoes = posicoes_x[1:]
            for lista_posicoes in temp_todas_posicoes:
                for posicao in lista_posicoes:
                    if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[0]:
                        temp_posicao.append(posicao)
                        num_correspondecias += 1
                    else:
                        num_correspondecias = 0
                        temp_posicao = []
                        break
                    
                if(num_correspondecias == 5):
                    break           

            temp_score = 32


    # Cruz
    elif figura == simbolos_disponiveis[2]:
        if verifica_existencia_micro_cruz(tabuleiro_temp):
            temp_todas_posicoes = posicoes_cruz[1:]
            micro_cruz_formados += 1
            for lista_posicoes in temp_todas_posicoes:
                for posicao in lista_posicoes:
                    if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[2]:
                        temp_posicao.append(posicao)
                        num_correspondecias += 1
                    else:
                        num_correspondecias = 0
                        temp_posicao = []
                        break
                    
                if(num_correspondecias == 5):
                    break
            
            temp_score = 32


    # Bola
    elif figura == simbolos_disponiveis[1]:
        if verifica_existencia_micro_bola(tabuleiro_temp):
            micro_bola_formados += 1
            temp_todas_posicoes = posicoes_bola[9:]
            for lista_posicoes in temp_todas_posicoes:
                for posicao in lista_posicoes:
                    if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[1]:
                        temp_posicao.append(posicao)
                        num_correspondecias += 1
                    else:
                        num_correspondecias = 0
                        temp_posicao = []
                        break
                    
                if(num_correspondecias == 4):
                    break
            
            temp_score = 16  

    

    elif figura == simbolos_disponiveis[3]:
        if verifica_existencia_micro_traco(tabuleiro_temp):
            micro_traco_formados += 1
            temp_todas_posicoes = posicoes_traco[15:]
            for lista_posicoes in temp_todas_posicoes:
                for posicao in lista_posicoes:
                    if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[3]:
                        temp_posicao.append(posicao)
                        num_correspondecias += 1
                    else:
                        num_correspondecias = 0
                        temp_posicao = []
                        break
                    
                if(num_correspondecias == 2):
                    break
            
            temp_score = 2
        
    for posicao in temp_posicao:
        tabuleiro_temp[posicao[0]][posicao[1]] = " "

    return temp_score


# Função que retorna se formou uma macrofigura
def verificar_macrofiguras(figura, tabuleiro_temp):
    temp_posicao = []
    temp_score = 0
    num_correspondecias = 0

    # X
    if figura == simbolos_disponiveis[0]: 
        if verifica_existencia_macro_x(tabuleiro_temp):
            macro_x_formados += 1
            lista_posicoes = posicoes_x[0]
            for posicao in lista_posicoes:
                temp_posicao.append(posicao)
            temp_score = 512


    # Cruz
    elif figura == simbolos_disponiveis[2]:
        if verifica_existencia_macro_cruz(tabuleiro_temp):
            macro_cruz_formados += 1
            lista_posicoes = posicoes_cruz[0]
            for posicao in lista_posicoes:
                temp_posicao.append(posicao)
            temp_score = 512


    # Bola
    elif figura == simbolos_disponiveis[1]:
        if verifica_existencia_macro_bola(tabuleiro_temp):
            macro_bola_formados += 1
            temp_todas_posicoes = posicoes_bola[:9]
            for lista_posicoes in temp_todas_posicoes:
                for posicao in lista_posicoes:
                    if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[1]:
                        temp_posicao.append(posicao)
                        num_correspondecias += 1
                    else:
                        num_correspondecias = 0
                        temp_posicao = []
                        break
                
                if(num_correspondecias == 8):
                    break
            
            temp_score = 256


    # Traco
    elif figura == simbolos_disponiveis[3]:
        if verifica_existencia_macro_traco(tabuleiro_temp):
            macro_traco_formados += 1
            temp_todas_posicoes = posicoes_traco[:15]
            for lista_posicoes in temp_todas_posicoes:
                for posicao in lista_posicoes:
                    if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[3]:
                        temp_posicao.append(posicao)
                        num_correspondecias += 1
                    else:
                        num_correspondecias = 0
                        temp_posicao = []
                        break
                
                if(num_correspondecias == 3):
                    break
            temp_score = 8

    for posicao in temp_posicao:
        tabuleiro_temp[posicao[0]][posicao[1]] = " "

    return temp_score

# ----------------------------------------------------------------------------------------------------------


# Gerar fila random de simbolos
def gerar_fila_simbolos():
    global lista_simbolos
    global simbolos_disponiveis

    num_iterations = random.randrange(20, 25)
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
        # Verificar simbolo, update no score e retirar simbolo da lista
        
        score += verificar_macrofiguras(lista_simbolos[0], tabuleiro)
        score += verificar_microfiguras(lista_simbolos[0], tabuleiro)
        lista_simbolos.pop(0)

    return score


# Define a function to train the neural network based on the total reward obtained during the episode
def train_neural_network(score):
    global best_score
    global weights_input_hidden1
    global biases_hidden1
    global weights_hidden1_hidden2
    global biases_hidden2
    global weights_hidden2_hidden3
    global biases_hidden3
    global weights_hidden3_output
    global biases_output

    if score > best_score:
        # If the current score is better than the best score, update the best score and the weights
        best_score = score
        update_weights_based_on_score(score)


def update_weights_based_on_score(score):
    global best_score
    global weights_input_hidden1
    global biases_hidden1
    global weights_hidden1_hidden2
    global biases_hidden2
    global weights_hidden2_hidden3
    global biases_hidden3
    global weights_hidden3_output
    global biases_output


    learning_rate_multiplier = 1.2 if score > best_score else 0.8

    # Update weights and biases with the learning rate multiplier
    weights_input_hidden1 = [[w * learning_rate_multiplier for w in weights_input_hidden1_row] for weights_input_hidden1_row in weights_input_hidden1]
    biases_hidden1 = [b * learning_rate_multiplier for b in biases_hidden1]

    weights_hidden1_hidden2 = [[w * learning_rate_multiplier for w in weights_hidden1_hidden2_row] for weights_hidden1_hidden2_row in weights_hidden1_hidden2]
    biases_hidden2 = [b * learning_rate_multiplier for b in biases_hidden2]

    weights_hidden2_hidden3 = [[w * learning_rate_multiplier for w in weights_hidden2_hidden3_row] for weights_hidden2_hidden3_row in weights_hidden2_hidden3]
    biases_hidden3 = [b * learning_rate_multiplier for b in biases_hidden3]

    weights_hidden3_output = [[w * learning_rate_multiplier for w in weights_hidden3_output_row] for weights_hidden3_output_row in weights_hidden3_output]
    biases_output = [b * learning_rate_multiplier for b in biases_output]



def main():
    global tabuleiro
    global lista_simbolos
    global macro_x_formados
    global macro_cruz_formados
    global macro_bola_formados
    global macro_traco_formados
    global micro_x_formados
    global micro_cruz_formados
    global micro_bola_formados
    global micro_traco_formados

    all_iterations_data = []
    i = 0
    while i < 10000:
        tabuleiro = [[" " for _ in range(5)] for _ in range(5)]
        gerar_fila_simbolos()
        score = simulate_game()
        print("Score: " + str(score))
        train_neural_network(score)

        data = {
        'macro_x_formados': macro_x_formados,
        'macro_cruz_formados': macro_cruz_formados,
        'macro_bola_formados': macro_bola_formados,
        'macro_traco_formados': macro_traco_formados,
        'micro_x_formados': micro_x_formados,
        'micro_cruz_formados': micro_cruz_formados,
        'micro_bola_formados': micro_bola_formados,
        'micro_traco_formados': micro_traco_formados,
        # ... (other variables)
        
        'weights_input_hidden1': weights_input_hidden1,
        'biases_hidden1': biases_hidden1,
        'weights_hidden1_hidden2': weights_hidden1_hidden2,
        'biases_hidden2': biases_hidden2,
        'weights_hidden2_hidden3': weights_hidden2_hidden3,
        'biases_hidden3': biases_hidden3,
        'weights_hidden3_output': weights_hidden3_output,
        'biases_output': biases_output,
        # ... (other global variables)
        }
        all_iterations_data.append(data)

        macro_x_formados = 0
        macro_cruz_formados = 0
        macro_bola_formados = 0
        macro_traco_formados = 0
        micro_x_formados = 0
        micro_cruz_formados = 0
        micro_bola_formados = 0
        micro_traco_formados = 0
        i += 1

    # Get the current date and time
    current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Save all iterations to a file with the current date in the filename
    with open(f'iterations_data_{current_date}.pkl', 'wb') as file:
        pickle.dump(all_iterations_data, file)
    
    return 0



main()
