import random

class Simbolo:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return (
            f"Valor: {self.value}, "
        )


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


# Criar um tabuleiro vazio
tabuleiro = []

# cria lista de espera
lista_simbolos = []

# Posições que serão usadas para colocar no tabuleiro
posicao_x_uso = [(0, 0) for _ in range(9)]
posicao_bola_uso = [(0, 0) for _ in range(9)]
posicao_cruz_uso = [(0, 0) for _ in range(9)]
posicao_traco_uso = [(0, 0) for _ in range(9)]

# Posições base
posicoes_base_bola = [(3,0), (3,1), (4,0), (4,1)]          
posicoes_base_cruz = [(2,3), (3,2), (3,3), (3,4), (4,3)]   
posicoes_base_x = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
posicoes_base_traco = [(1, 4), (2, 4)]


# Definição de funções
def main():
    global score
    global tabuleiro
    global lista_simbolos

    # loop das simulações
    while numero_simulacoes < 100000:
        score = 0
        tabuleiro = [[" " for _ in range(5)] for _ in range(5)]
        gerarFilaRandom(lista_simbolos)
        jogar()
        calcularScoreFinal()
        calcular_estatisticas()

    media = total_simulacoes / numero_simulacoes
    print(
        f"A media de score desta versão é de {media} | Numero de simulacoes: {numero_simulacoes} | "
    )
    print(
        f"Porcentagem de Simulações negativas {numero_simulacoes_negativas/numero_simulacoes*100}"
    )
    return 0


# Função para gerar uma lista aleatoria de simbolos
def gerarFilaRandom(lista_simbolos):
    # Gera um número aleatório entre 40 e 60 para determinar o tamanho da lista
    tamanho_lista = random.randint(40, 60)

    # Adiciona símbolos aleatórios à lista de espera
    for _ in range(tamanho_lista):
        simbolo_aleatorio = Simbolo(random.choice([cruz, x, bola, traco]))
        lista_simbolos.append(simbolo_aleatorio)


# Função que serve para copiar valores de um array para outro
# Atenção que so funciona se o array de destino for maior ou igual
# que o array de origem
def copiar_valores_array(array_origem, array_destino):
    for index, i in enumerate(array_origem):
        array_destino[index] = i


# Função que realiza a simulação do jogo em si, com o preenchimento
# do tabueleiro e verificação se ja existem figuras completas ou não
def jogar():
    contador_tabuleiro = [
        0,
        0,
        0,
        0,
        0,
    ]  # [contador_x, contador_o, contador_cruz, contador_traco, contador_lixo]

    # Define as posicoes a serem colocadas no tabuleiro
    copiar_valores_array(posicoes_base_x, posicao_x_uso)
    copiar_valores_array(posicoes_base_bola, posicao_bola_uso)
    copiar_valores_array(posicoes_base_cruz, posicao_cruz_uso)
    copiar_valores_array(posicoes_base_traco, posicao_traco_uso)

    # Para todas os simbolos da lista
    while len(lista_simbolos) > 0:
        # procedimento para colocar a peça no tabuleiro
        if lista_simbolos[0].value == x:  # No caso de ser um X
            if (
                tabuleiro[(posicao_x_uso[contador_tabuleiro[0]][0])][
                    (posicao_x_uso[contador_tabuleiro[0]][1])
                ]
                != " "
            ):
                exit(erro_colocacao_cruz)
            tabuleiro[(posicao_x_uso[contador_tabuleiro[0]][0])][
                (posicao_x_uso[contador_tabuleiro[0]][1])
            ] = x
            contador_tabuleiro[0] += 1
        elif lista_simbolos[0].value == bola:  # No caso de ser uma bola
            if (
                tabuleiro[(posicao_bola_uso[contador_tabuleiro[1]][0])][
                    (posicao_bola_uso[contador_tabuleiro[1]][1])
                ]
                != " "
            ):
                exit(erro_colocacao_bola)
            tabuleiro[(posicao_bola_uso[contador_tabuleiro[1]][0])][
                (posicao_bola_uso[contador_tabuleiro[1]][1])
            ] = bola
            contador_tabuleiro[1] += 1
        elif lista_simbolos[0].value == cruz:  # No caso de ser uma cruz
            if (
                tabuleiro[(posicao_cruz_uso[contador_tabuleiro[2]][0])][
                    (posicao_cruz_uso[contador_tabuleiro[2]][1])
                ]
                != " "
            ):
                exit(erro_colocacao_cruz)
            tabuleiro[(posicao_cruz_uso[contador_tabuleiro[2]][0])][
                (posicao_cruz_uso[contador_tabuleiro[2]][1])
            ] = cruz
            contador_tabuleiro[2] += 1
        elif lista_simbolos[0].value == traco:  # No caso de ser um traço
            if (
                tabuleiro[(posicao_traco_uso[contador_tabuleiro[3]][0])][
                    (posicao_traco_uso[contador_tabuleiro[3]][1])
                ]
                != " "
            ):
                exit(erro_colocacao_traco)
            tabuleiro[(posicao_traco_uso[contador_tabuleiro[3]][0])][
                (posicao_traco_uso[contador_tabuleiro[3]][1])
            ] = traco
            contador_tabuleiro[3] += 1


        lista_simbolos.pop(0)
        verifica_existencia_figura(contador_tabuleiro, tabuleiro)


# Função que verifica se existe uma figura completa no tabueiro
# Caso exista, limpa as posições do tabueiro que foram usadas
# e adiciona o score a que corresponde
def verifica_existencia_figura(lista_contadores, tabuleiro):
    global score

    # Caso em que existe uma microfigura x no tabuleiro
    if lista_contadores[0] == micro_forma_x:
        score += score_micro_x
        while lista_contadores[0] != 0:
            lista_contadores[0] -= 1

            if (
                tabuleiro[(posicoes_base_x[lista_contadores[0]][0])][
                    (posicoes_base_x[lista_contadores[0]][1])
                ]
                != x
            ):
                exit(erro_limpeza_x)

            tabuleiro[(posicoes_base_x[lista_contadores[0]][0])][
                (posicoes_base_x[lista_contadores[0]][1])
            ] = " "

    # Caso em que existe uma microfigura bola no tabuleiro
    if lista_contadores[1] == micro_forma_0:
        score += score_micro_bola
        while lista_contadores[1] != 0:
            lista_contadores[1] -= 1

            if (
                tabuleiro[(posicoes_base_bola[lista_contadores[1]][0])][
                    (posicoes_base_bola[lista_contadores[1]][1])
                ]
                != bola
            ):
                exit(erro_colocacao_bola)

            tabuleiro[(posicoes_base_bola[lista_contadores[1]][0])][
                (posicoes_base_bola[lista_contadores[1]][1])
            ] = " "

    # Caso em que existe uma microfigura cruz no tabuleiro
    if lista_contadores[2] == micro_forma_cruz:
        score += score_micro_cruz
        while lista_contadores[2] != 0:
            lista_contadores[2] -= 1

            if (
                tabuleiro[(posicoes_base_cruz[lista_contadores[2]][0])][
                    (posicoes_base_cruz[lista_contadores[2]][1])
                ]
                != cruz
            ):
                exit(erro_limpeza_cruz)

            tabuleiro[(posicoes_base_cruz[lista_contadores[2]][0])][
                (posicoes_base_cruz[lista_contadores[2]][1])
            ] = " "

    # Caso em que existe uma microfigura traço
    if lista_contadores[3] == micro_forma_traco:
        score += score_micro_traco
        while lista_contadores[3] != 0:
            lista_contadores[3] -= 1

            if (
                tabuleiro[(posicoes_base_traco[lista_contadores[3]][0])][
                    (posicoes_base_traco[lista_contadores[3]][1])
                ]
                != traco
            ):
                exit(erro_colocacao_traco)

            tabuleiro[(posicoes_base_traco[lista_contadores[3]][0])][
                (posicoes_base_traco[lista_contadores[3]][1])
            ] = " "


# Função para retirar o score das pecas ainda no tabuleiro
def calcularScoreFinal():
    global score
    numeroPecasRestantes = 0
    for linha in tabuleiro:
        for celula in linha:
            if celula != " ":
                numeroPecasRestantes += 1

    score -= 2**numeroPecasRestantes


def calcular_estatisticas():
    global numero_simulacoes
    global numero_simulacoes_negativas
    global total_simulacoes

    numero_simulacoes += 1
    total_simulacoes += score
    if score < 0:
        numero_simulacoes_negativas += 1


main()
