import random
import math
import json
from datetime import datetime

# Specify the file path to load weights from
#load_weights_path = 'load_test.json'
#keystoload_weights = ['weights_input_hidden1',
#              'weights_hidden1_hidden2',
#              'weights_hidden2_hidden3',
#              'weights_hidden3_output']

# Open the file and load JSON data
#with open(load_weights_path, 'r') as file:
#    loaded_data = json.load(file)

# Create a new dictionary with only the selected keys
# filtered_data = {key: loaded_data[key] for key in keystoload_weights}
# weights_input_hidden1 = filtered_data['weights_input_hidden1']
#weights_hidden1_hidden2 = filtered_data['weights_hidden1_hidden2']
#weights_hidden2_hidden3 = filtered_data['weights_hidden2_hidden3']
#weights_hidden3_output = filtered_data['weights_hidden3_output']



# Variables
lista_simbolos = []
simbolos_disponiveis = ['X', 'O', '+', '-']
valor_simbolos = {'X': 1, 'O': 2, '+': 3, '-': 4}
tabuleiro = []

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

best_score = float('-inf') 
all_scores = []  # List to store all scores obtained during training


# Estatisticas
micro_x_formados = 0
micro_cruz_formados = 0
micro_bola_formados = 0
micro_traco_formados = 0
macro_x_formados = 0
macro_cruz_formados = 0
macro_bola_formados = 0
macro_traco_formados = 0


random.seed(80)
# Initialize weights and biases for each layer
# The weights are initialized wit a value for each 
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
    global training_score

    temp_posicao = posicoes_x[:1]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == simbolos_disponiveis[0]:
                num_correspondecias += 1
                training_score += 50
            else:
                training_score -= 100
                break
        
            if num_correspondecias == 9:
                training_score += 1000
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
    global micro_x_formados
    global micro_cruz_formados
    global micro_bola_formados
    global micro_traco_formados

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
    global macro_x_formados
    global macro_cruz_formados
    global macro_bola_formados
    global macro_traco_formados

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


# Função para dar update no input data (FALTA NUMERO DE CADA SIMBOLO NA FILA)
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
    layer_output = sigmoid(layer_input)
    return layer_output


# Forward propagation layer 3
def forward_propagation_hidden3(hidden2_output, weights, biases):
    layer_input = [sum(x * w for x, w in zip(hidden2_output, weights[i])) + biases[i] for i in range(len(weights))]
    layer_output = sigmoid(layer_input)
    return layer_output


# Softmax function
def softmax(x):
    exp_x = [math.exp(val - max(x)) for val in x]
    return [val / sum(exp_x) for val in exp_x]


# Softmax derivative
def softmax_derivative(x):
    s = softmax(x)
    return [s_i * (1 - s_i) for s_i in s]


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
    global hidden1_output
    global hidden2_output
    global hidden3_output
    global training_score

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
            training_score -= 10
            i += 1

        if i == 25:
            # Game over
            return (score - 2**25) 
        # Verificar simbolo, update no score e retirar simbolo da lista
        
        score += verificar_macrofiguras(lista_simbolos[0], tabuleiro)
        score += verificar_microfiguras(lista_simbolos[0], tabuleiro)

        if lista_simbolos[0] == simbolos_disponiveis[0]:
            posicoes_macro_x_1d = [0, 4, 6, 8, 16, 18, 20, 24, 12]
            #backpropagation(posicoes_macro_x_1d, output_layer, input_data)
        
        lista_simbolos.pop(0)


    
    cont = 0
    for i in range(5):
        for j in range(5):
            if tabuleiro[i][j] != " ":
                cont += 1


    return (score - 2**cont)





def main_alternative():
    global tabuleiro
    global lista_simbolos
    global all_scores
    global macro_x_formados
    global macro_cruz_formados
    global macro_bola_formados
    global macro_traco_formados
    global micro_x_formados
    global micro_cruz_formados
    global micro_bola_formados
    global micro_traco_formados
    global input_data
    global weights_input_hidden1
    global biases_hidden1
    global weights_hidden1_hidden2
    global biases_hidden2
    global weights_hidden2_hidden3
    global biases_hidden3
    global weights_hidden3_output
    global biases_output
    global best_score
    global training_score

    


    all_iterations_data = []
    i = 0
    while i < 100:
        tabuleiro = [[" " for _ in range(5)] for _ in range(5)]
        #gerar_fila_simbolos()
        
        lista_simbolos = ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']

        score = simulate_game()
        all_scores.append(score)

        if (score >= best_score):
            print(f'Iteration {i} - Score: {score}')
            data = {
            'macro_x_formados': macro_x_formados,
            'macro_cruz_formados': macro_cruz_formados,
            'macro_bola_formados': macro_bola_formados,
            'macro_traco_formados': macro_traco_formados,
            'micro_x_formados': micro_x_formados,
            'micro_cruz_formados': micro_cruz_formados,
            'micro_bola_formados': micro_bola_formados,
            'micro_traco_formados': micro_traco_formados,
            'score': score,
            'training_score': training_score,
            'weights_input_hidden1': weights_input_hidden1,
            'biases_hidden1': biases_hidden1,
            'weights_hidden1_hidden2': weights_hidden1_hidden2,
            'biases_hidden2': biases_hidden2,
            'weights_hidden2_hidden3': weights_hidden2_hidden3,
            'biases_hidden3': biases_hidden3,
            'weights_hidden3_output': weights_hidden3_output,
            'biases_output': biases_output,
            }
            all_iterations_data.append(data)
        
        if score > best_score:
            best_score = score

        macro_x_formados = 0
        macro_cruz_formados = 0
        macro_bola_formados = 0
        macro_traco_formados = 0
        micro_x_formados = 0
        micro_cruz_formados = 0
        micro_bola_formados = 0
        micro_traco_formados = 0
        training_score = 0
        i += 1

    
    #for iteration_data in all_iterations_data:
    #    Save data to the file
    #    with open(file_path, 'a') as file:
    #        json.dump(iteration_data, file)
    #        file.write('\n')  # Add a newline for better readability between iterations

    print(f'Average score: {sum(all_scores) / len(all_scores)}')

    return 0


