import random

# Para não ter de fazer 25 combinções para cada figura, apenas testar as combinações,
# que aparecem em tuplas na com esssa posição. Assim se diminui o numero de combinações
# a testar podendo aumentar a profundidade possivel da busca


# Define mensagens de erros
erro_colocacao_x = "Colocação do x num espaço ainda ocupado"
erro_colocacao_bola = "Colocação da bola num espaço ainda ocupado"
erro_colocacao_cruz = "Colocação da cruz num espaço ainda ocupado"
erro_colocacao_traco = "Colocação do traço num espaço ainda ocupado"

erro_limpeza_x = "Foi limpado uma figura X numa quadricula que não possuia X"
erro_limpeza_bola = "Foi limpada uma figura bola numa quadricula que não possuia bola"
erro_limpeza_cruz = "Foi limpada uma figura cruz numa quadricula que não possuia cruz"
erro_limpeza_traco = (
    "Foi limpada uma figura traco numa quadricula que não possuia traco"
)

# Define das variaveis iniciais
total_simulacoes = 0  # score total das simulacoes todas
numero_simulacoes = 0  # numero simulações realizadas
numero_simulacoes_negativas = 0  # numero de simulações negativas
media = 0  # media das simulacoes
score = 0  # score do jogo


# Definição dos scores para cada forma
score_micro_bola = 16  # score por completar uma bola
score_micro_x = 32  # score por completar uma x
score_micro_cruz = 32  # score por completar uma cruz
score_micro_traco = 4  # score por completar um traco
score_macro_x = 512  # score para completar macro x


# define simbolos a utilizar
cruz = "+"
x = "x"
bola = "o"
traco = "-"


# define tamanho microfiguras (quantos simbolos são necessários para formar uma figura)
micro_forma_x = 5
micro_forma_0 = 4
micro_forma_cruz = 5
micro_forma_traco = 2


# Profundidade de procura
profundidade = 3

# Criar um tabuleiro vazio
tabuleiro = []

# cria lista de espera
lista_simbolos = []


# Lista que vai conter proximas jogadas a serem feitas
proximas_jogadas = []


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



# Definição de funções
def main():
    global score
    global tabuleiro
    global lista_simbolos

    numero_simulacoes = 0
    # loop das simulações
    while numero_simulacoes < 1:
        score = 0
        tabuleiro = [[" " for _ in range(5)] for _ in range(5)]
        lista_simbolos = []

        gerarFilaRandom(lista_simbolos)
        temp_tabuleiro()
        verifica_existencia_micro_x()

        numero_simulacoes += 1

    return 0


def temp_tabuleiro():
    # Define the positions of the micro_x
    micro_x_positions = [(2, 2), (2, 4), (3, 3), (4, 2), (4, 4)]

    # Place the micro_x on the tabuleiro
    for pos in micro_x_positions:
        tabuleiro[pos[0]][pos[1]] = 'x'


# Função que ve as proximas 20 figuras na lista e retorna true se existirem 9 x's
def verificarMacroX(lista_simbolos):
    temp = lista_simbolos[20:]
    if temp.count(x) >= 9:
        print("Macro X")
        return True
    else:
        return False


# Função que ve as proximas 20 figuras na lista e retorna true se existirem 9 cruzes
def verificarMacroCruz(lista_simbolos):
    temp = lista_simbolos[20:]
    if temp.count(cruz) >= 9:
        print("Macro Cruz")
        return True
    else:
        return False


# Função que ve as proximas 20 figuras na lista e retorna true se existirem 8 bolas
def verificarMacroBola(lista_simbolos):
    temp = lista_simbolos[20:]
    if temp.count(bola) >= 8:
        print("Macro Bola")
        return True
    else:
        return False


# Função que verifica se existe uma microfigura x no tabuleiro
def verifica_existencia_micro_x():
    num_total_microfiguras = 9
    
    temp_posicao = posicoes_x[1:]

    for lista_posicao in temp_posicao:
        for posicao in lista_posicao:
            if tabuleiro[posicao[0]][posicao[1]] != 'x':
                num_total_microfiguras -= 1
                break  # Inner loop

    
    if num_total_microfiguras == 0:
        print("False")
        return False
    else:
        print("True")
        return True


# Função que verifica se existe uma microfigura cruz no tabuleiro
def verifica_existencia_micro_cruz():
    num_total_microfiguras = 9

    temp_posicao = posicoes_cruz[1:]

    for lista_posicao in temp_posicao:
        for posicao in lista_posicao:
            if tabuleiro[posicao[0]][posicao[1]] != cruz:
                num_total_microfiguras -= 1
                break  # Inner loop

    if num_total_microfiguras == 0:
        print("False")
        return False
    else:
        print("True")
        return True


# Itera pelas posições possiveis da figura a procura da melhor jogada
def procurarJogadas():
    return

# Função que será responsável por calcular o score de uma certa jogada
def calculateScore():
    return





# Função para gerar uma lista aleatoria de simbolos
def gerarFilaRandom(lista_simbolos):
    # Gera um número aleatório entre 40 e 60 para determinar o tamanho da lista
    tamanho_lista = random.randint(40, 60)

    # Adiciona símbolos aleatórios à lista de espera
    for _ in range(tamanho_lista):
        lista_simbolos.append(random.choice([cruz, x, bola]))


# Função para retirar o score das pecas ainda no tabuleiro
def calcularScoreFinal():
    global score
    numeroPecasRestantes = 0
    for linha in tabuleiro:
        for celula in linha:
            if celula != " ":
                numeroPecasRestantes += 1

    score -= 2**numeroPecasRestantes


# Função para exibir o tabuleiro
def exibir_tabuleiro(tabuleiro_exibir):
    print("-" * 9)
    for linha in tabuleiro_exibir:
        print("|".join(celula for celula in linha))
        print("-" * 9)


def calcular_estatisticas():
    global numero_simulacoes
    global numero_simulacoes_negativas
    global total_simulacoes

    numero_simulacoes += 1
    total_simulacoes += score
    if score < 0:
        numero_simulacoes_negativas += 1


main()

