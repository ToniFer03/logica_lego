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


# Variaveis que vão guardar se é possivel formar uma macrofigura
possivel_macro_x = False
possivel_macro_cruz = False
possivel_macro_bola = False
possivel_macro_traco = False


# Lista com todas as figuras
figuras = [x, cruz, bola, traco]


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
        temp_init_tabuleiro()
        limparMicroFigura(cruz, tabuleiro)

        numero_simulacoes += 1

    return 0



def temp_init_tabuleiro():
    tabuleiro[0][2] = cruz
    tabuleiro[1][1] = cruz
    tabuleiro[1][2] = cruz
    tabuleiro[1][3] = cruz
    tabuleiro[2][2] = cruz
    tabuleiro[0][0] = bola


#--------------------------------------------------------------------------------------------------------
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


# Função que ve as proximas 20 figuras na lista e retorna true se existirem 3 tracos
def verificarMacroTraco(lista_simbolos):
    temp = lista_simbolos[20:]
    if temp.count(traco) >= 3:
        print("Macro Traco")
        return True
    else:
        return False
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# Função que verifica se existe uma microfigura x no tabuleiro
def verifica_existencia_micro_x(tabuleiro_temp):
    temp_posicao = posicoes_x[1:]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == x:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 5:
                print("Existe X")
                return True

    return False


# Função que verifica se existe uma microfigura cruz no tabuleiro
def verifica_existencia_micro_cruz(tabuleiro_temp):
    temp_posicao = posicoes_cruz[1:]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == cruz:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 5:
                print("Existe Cruz")
                return True

    return False


# Função que verifica se existe uma microfigura bola no tabuleiro
def verifica_existencia_micro_bola(tabuleiro_temp):
    temp_posicao = posicoes_bola[9:]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == bola:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 4:
                print("Existe bola")
                return True

    return False


# Função que verifica se existe uma microfigura traco no tabuleiro
def verifica_existencia_micro_traco(tabuleiro_temp):
    temp_posicao = posicoes_traco[15:]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == traco:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 2:
                print("Existe traco")
                return True

    return False
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# Função que verifica se existe uma macrofigura x no tabuleiro
def verifica_existencia_macro_x(tabuleiro_temp):
    temp_posicao = posicoes_x[0]

    num_correspondecias = 0
    for posicao in temp_posicao:
        if tabuleiro_temp[posicao[0]][posicao[1]] == x:
            num_correspondecias += 1
        else:
            break
    
        if num_correspondecias == 9:
            print("Existe Macro X")
            return True

    return False


# Função que verifica se existe uma macrofigura cruz no tabuleiro
def verifica_existencia_macro_cruz(tabuleiro_temp):
    temp_posicao = posicoes_cruz[0]

    num_correspondecias = 0
    for posicao in temp_posicao:
        if tabuleiro_temp[posicao[0]][posicao[1]] == cruz:
            num_correspondecias += 1
        else:
            break
    
        if num_correspondecias == 9:
            print("Existe Macro Cruz")
            return True

    return False


# Função que verifica se existe uma macrofigura bola no tabuleiro
def verifica_existencia_macro_bola(tabuleiro_temp):
    temp_posicao = posicoes_bola[:9]

    num_correspondecias = 0
    for posicao in temp_posicao:
        if tabuleiro_temp[posicao[0]][posicao[1]] == bola:
            num_correspondecias += 1
        else:
            break
    
        if num_correspondecias == 8:
            print("Existe Macro Bola")
            return True

    return False


# Função que verifica se existe uma macrofigura traco no tabuleiro
def verifica_existencia_macro_traco(tabuleiro_temp):
    temp_posicao = posicoes_traco[:15]

    num_correspondecias = 0
    for posicao in temp_posicao:
        if tabuleiro_temp[posicao[0]][posicao[1]] == traco:
            num_correspondecias += 1
        else:
            break
    
        if num_correspondecias == 3:
            print("Existe Macro Traco")
            return True

    return False
#--------------------------------------------------------------------------------------------------------


# Funções ajudante
# --------------------------------------------------------------------------------------------------------
# Função que retorna se uma certa macrofigura é possivel
def macro_possivel(figura):
    if figura == x:
        return possivel_macro_x
    elif figura == cruz:
        return possivel_macro_cruz
    elif figura == bola:
        return possivel_macro_bola
    elif figura == traco:
        return possivel_macro_traco


def verificar_microfiguras(figura, tabuleiro_temp):
    if figura == x:
        return verifica_existencia_micro_x(tabuleiro_temp)
    elif figura == cruz:
        return verifica_existencia_micro_cruz(tabuleiro_temp)
    elif figura == bola:
        return verifica_existencia_micro_bola(tabuleiro_temp)
    elif figura == traco:
        return verifica_existencia_micro_traco(tabuleiro_temp)


# Função que retorna se formou uma macrofigura
def verificar_macrofiguras(figura, tabuleiro_temp):
    if figura == x:
        return verifica_existencia_macro_x(tabuleiro_temp)
    elif figura == cruz:
        return verifica_existencia_macro_cruz(tabuleiro_temp)
    elif figura == bola:
        return verifica_existencia_macro_bola(tabuleiro_temp)
    elif figura == traco:
        return verifica_existencia_macro_traco(tabuleiro_temp)


# Função que verifica se peça foi colocada numa macrofigura
def verifica_colocar_figura_macro(figura, posicao):
    if figura == x:
        if posicao in posicoes_x[0]:
            return True
        else:
            return False
    elif figura == cruz:
        if posicao in posicoes_cruz[0]:
            return True
        else:
            return False
    elif figura == bola:
        if posicao in posicoes_bola[:9]:
            return True
        else:
            return False
    elif figura == traco:
        if posicao in posicoes_traco[:15]:
            return True
        else:
            return False


# Função que verifica se peça foi colocada numa microfigura
def verifica_colocar_figura_micro(figura, posicao):
    if figura == x:
        if posicao in posicoes_x[1:]:
            return True
        else:
            return False
    elif figura == cruz:
        if posicao in posicoes_cruz[1:]:
            return True
        else:
            return False
    elif figura == bola:
        if posicao in posicoes_bola[9:]:
            return True
        else:
            return False
    elif figura == traco:
        if posicao in posicoes_traco[15:]:
            return True
        else:
            return False


# Função para retirar peças do tabuleiro apos formar uma macrofigura
def limparMacroFigura(figura, tabuleiro_temp):
    temp_posicao = []
    num_correspondecias = 0

    if figura == x:
        lista_posicoes = posicoes_x[0]
        for posicao in lista_posicoes:
            temp_posicao.append(posicao)
    
    elif figura == cruz:
        lista_posicoes = posicoes_cruz[0]
        for posicao in lista_posicoes:
            temp_posicao.append(posicao)
    

    elif figura == bola:
        temp_todas_posicoes = posicoes_bola[:9]
        for lista_posicoes in temp_todas_posicoes:
            for posicao in lista_posicoes:
                if tabuleiro_temp[posicao[0]][posicao[1]] == bola:
                    temp_posicao.append(posicao)
                    num_correspondecias += 1
                else:
                    num_correspondecias = 0
                    temp_posicao = []
                    break
                
            if(num_correspondecias == 8):
                break
    

    elif figura == traco:
        temp_todas_posicoes = posicoes_traco[:15]
        for lista_posicoes in temp_todas_posicoes:
            for posicao in lista_posicoes:
                if tabuleiro_temp[posicao[0]][posicao[1]] == traco:
                    temp_posicao.append(posicao)
                    num_correspondecias += 1
                else:
                    num_correspondecias = 0
                    temp_posicao = []
                    break
                
            if(num_correspondecias == 3):
                break

    for posicao in temp_posicao:
        tabuleiro_temp[posicao[0]][posicao[1]] = " "


# Função para retirar peças do tabuleiro apos formar uma microfigura
def limparMicroFigura(figura, tabuleiro_temp):
    temp_posicao = []
    num_correspondecias = 0

    if figura == x:
        temp_todas_posicoes = posicoes_x[1:]
        for lista_posicoes in temp_todas_posicoes:
            for posicao in lista_posicoes:
                if tabuleiro_temp[posicao[0]][posicao[1]] == x:
                    temp_posicao.append(posicao)
                    num_correspondecias += 1
                else:
                    num_correspondecias = 0
                    temp_posicao = []
                    break
                
            if(num_correspondecias == 5):
                break
    
    elif figura == cruz:
        temp_todas_posicoes = posicoes_cruz[1:]
        for lista_posicoes in temp_todas_posicoes:
            for posicao in lista_posicoes:
                if tabuleiro_temp[posicao[0]][posicao[1]] == cruz:
                    temp_posicao.append(posicao)
                    num_correspondecias += 1
                else:
                    num_correspondecias = 0
                    temp_posicao = []
                    break
                
            if(num_correspondecias == 5):
                break
    

    elif figura == bola:
        temp_todas_posicoes = posicoes_bola[9:]
        for lista_posicoes in temp_todas_posicoes:
            for posicao in lista_posicoes:
                if tabuleiro_temp[posicao[0]][posicao[1]] == bola:
                    temp_posicao.append(posicao)
                    num_correspondecias += 1
                else:
                    num_correspondecias = 0
                    temp_posicao = []
                    break
                
            if(num_correspondecias == 4):
                break
    

    elif figura == traco:
        temp_todas_posicoes = posicoes_traco[15:]
        for lista_posicoes in temp_todas_posicoes:
            for posicao in lista_posicoes:
                if tabuleiro_temp[posicao[0]][posicao[1]] == traco:
                    temp_posicao.append(posicao)
                    num_correspondecias += 1
                else:
                    num_correspondecias = 0
                    temp_posicao = []
                    break
    
            if(num_correspondecias == 2):
                break

    for posicao in temp_posicao:
        tabuleiro_temp[posicao[0]][posicao[1]] = " "


# Update as listas com os moves possiveis
def update_possiveis_x(possiveis_x, colocacao, macro_possivel):
    if macro_possivel:
        possiveis_x = posicoes_x[0]
    
    for lista_posicoes in posicoes_x[1:]:
        if colocacao in lista_posicoes:
            possiveis_x = lista_posicoes
            break

    return possiveis_x


def update_possiveis_cruz(possiveis_cruz, colocacao, macro_possivel):
    if macro_possivel:
        possiveis_cruz = posicoes_cruz[0]
    
    for lista_posicoes in posicoes_cruz[1:]:
        if colocacao in lista_posicoes:
            possiveis_cruz = lista_posicoes
            break

    return possiveis_cruz


def update_possiveis_bola(possiveis_bola, colocacao, macro_possivel):
    if macro_possivel:
        possiveis_bola = posicoes_bola[:9]
    
    for lista_posicoes in posicoes_bola[9:]:
        if colocacao in lista_posicoes:
            possiveis_bola = lista_posicoes
            break

    return possiveis_bola


def update_possiveis_traco(possiveis_traco, colocacao, macro_possivel):
    if macro_possivel:
        possiveis_traco = posicoes_traco[:15]
    
    for lista_posicoes in posicoes_traco[15:]:
        if colocacao in lista_posicoes:
            possiveis_traco = lista_posicoes
            break

    return possiveis_traco


def update_possiveis(possiveis, colocacao, macro_possivel, figura):
    if figura == x:
        possiveis = update_possiveis_x(possiveis, colocacao, macro_possivel)
    elif figura == cruz:
        possiveis = update_possiveis_cruz(possiveis, colocacao, macro_possivel)
    elif figura == bola:
        possiveis = update_possiveis_bola(possiveis, colocacao, macro_possivel)
    elif figura == traco:
        possiveis = update_possiveis_traco(possiveis, colocacao, macro_possivel)

    return possiveis
# --------------------------------------------------------------------------------------------------------



# Itera pelas posições possiveis da figura a procura da melhor jogada
def procurarJogadas():
    tabuleiro_temp = tabuleiro.copy() # Tabuleiro original
    lista_simbolos_temp = lista_simbolos.copy() # Lista de simbolos original

    lista_tabelas = [] # Lista que vai conter tabelas necessarias para a procura de jogadas
    lista_jogadas = [] # Lista que vai conter todas as jogadas ja testadas

    # Arrays com lista de posicoes possiveis para colocar uma peça
    posicoes_possiveis_x = []
    posicoes_possiveis_cruz = []
    posicoes_possiveis_bola = []
    posicoes_possiveis_traco = []

    # Pela profundidade da busca
    for i in range(profundidade):
        break
    
    return



# Calcular score da jogada (esta tabuleiro já possui a peça colocada)
def calculate_score(figura, tabuleiro, posicao):
    score = 0
    tabuleiro_temp = tabuleiro.copy()

    # Faço uma copia da lista de figuras para poder remover a figura que foi colocada
    temp_lista_figuras = figuras.copy()
    temp_lista_figuras.remove(figura)


    # Verifica se formou uma macrofigura, ou microfigura
    if macro_possivel(figura):
        if verificar_microfiguras(figura, tabuleiro_temp):
            limparMicroFigura(figura, tabuleiro_temp)
            score -= 100
        elif verificar_macrofiguras(figura, tabuleiro_temp):
            limparMacroFigura(figura, tabuleiro_temp)
            score += 500
    else:
        if verificar_microfiguras(figura, tabuleiro_temp):
            limparMicroFigura(figura, tabuleiro_temp)
            score += 60

    
    # Colocar peça em macro quando macro é possivel
    if macro_possivel(figura):
        if verifica_colocar_figura_macro(figura, posicao):
            score += 8
        elif verifica_colocar_figura_micro(figura, posicao):
            score -= 6
    else:
        if verifica_colocar_figura_micro(figura, posicao):
            score += 4

    
    # Se colocou uma peça ao lado de outra diferente diminiu o score por 3
    if posicao[0] != 0 and tabuleiro_temp[posicao[0] - 1][posicao[1]] != figura:
        score -= 3


    # Verifica se o tabuleiro possui celulas vazias (tem de ser a ultima a verificar)
    if " " not in tabuleiro_temp:
        score -= 1000


    return score, tabuleiro_temp



# Função que será responsável por fazer as jogadas no array proximas_jogadas
def jogar():
    return




# Função para gerar uma lista aleatoria de simbolos
def gerarFilaRandom(lista_simbolos):
    # Gera um número aleatório entre 40 e 60 para determinar o tamanho da lista
    tamanho_lista = random.randint(40, 60)

    # Adiciona símbolos aleatórios à lista de espera
    for _ in range(tamanho_lista):
        lista_simbolos.append(random.choice([cruz, x, bola, traco]))


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

