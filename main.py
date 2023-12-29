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
resultado_jogo = 0  # score do jogo


# Definição dos scores para cada forma
score_micro_bola = 16  # score por completar uma bola
score_micro_x = 32  # score por completar uma x
score_micro_cruz = 32  # score por completar uma cruz
score_micro_traco = 4  # score por completar um traco
score_macro_x = 512  # score para completar macro x
score_macro_cruz = 512  # score para completar macro cruz
score_macro_bola = 256  # score para completar macro bola
score_macro_traco = 64  # score para completar macro traco


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
profundidade = 2

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
        jogar()
        calcularScoreFinal()

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
def verificarMacroX():
    temp = lista_simbolos[20:]
    if temp.count(x) >= 9:
        print("Macro X")
        return True
    else:
        return False


# Função que ve as proximas 20 figuras na lista e retorna true se existirem 9 cruzes
def verificarMacroCruz():
    temp = lista_simbolos[20:]
    if temp.count(cruz) >= 9:
        print("Macro Cruz")
        return True
    else:
        return False


# Função que ve as proximas 20 figuras na lista e retorna true se existirem 8 bolas
def verificarMacroBola():
    temp = lista_simbolos[20:]
    if temp.count(bola) >= 8:
        print("Macro Bola")
        return True
    else:
        return False


# Função que ve as proximas 20 figuras na lista e retorna true se existirem 3 tracos
def verificarMacroTraco():
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
    temp_posicao = posicoes_x[:1]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == x:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 9:
                print("Existe X")
                return True

    return False


# Função que verifica se existe uma macrofigura cruz no tabuleiro
def verifica_existencia_macro_cruz(tabuleiro_temp):
    temp_posicao = posicoes_cruz[:1]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == cruz:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 9:
                print("Existe Cruz")
                return True

    return False


# Função que verifica se existe uma macrofigura bola no tabuleiro
def verifica_existencia_macro_bola(tabuleiro_temp):
    temp_posicao = posicoes_cruz[:9]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == bola:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 8:
                print("Existe bola")
                return True

    return False


# Função que verifica se existe uma macrofigura traco no tabuleiro
def verifica_existencia_macro_traco(tabuleiro_temp):
    temp_posicao = posicoes_traco[:15]

    for lista_posicao in temp_posicao:
        num_correspondecias = 0
        for posicao in lista_posicao:
            if tabuleiro_temp[posicao[0]][posicao[1]] == traco:
                num_correspondecias += 1
            else:
                break
        
            if num_correspondecias == 3:
                print("Existe traco")
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
        for lista_posicoes in posicoes_x[1:]:
            if posicao in lista_posicoes:
                return True
        else:
            return False
    
    elif figura == cruz:
        for lista_posicoes in posicoes_cruz[1:]:
            if posicao in lista_posicoes:
                return True
        else:
            return False
    
    elif figura == bola:
        for lista_posicoes in posicoes_bola[9:]:
            if posicao in lista_posicoes:
                return True
        else:
            return False
    
    elif figura == traco:
        for lista_posicoes in posicoes_traco[15:]:
            if posicao in lista_posicoes:
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


# Função para copiar tabuleiro
def copiarTabuleiro(tabuleiro_temp):
    tabuleiro_copia = [linha[:] for linha in tabuleiro_temp]
    return tabuleiro_copia


# Função para copiar lista
def copiarLista(lista_temp):
    lista_copia = []
    for i in lista_temp:
        lista_copia.append(i)
    return lista_copia
# --------------------------------------------------------------------------------------------------------



# Itera pelas posições possiveis da figura a procura da melhor jogada
def procurarJogadas():
    camada_temporaria = []
    posicoes_temp = []
    
    lista_simbolos_temp = copiarLista(lista_simbolos)
    primeira_camada = get_best_moves(lista_simbolos_temp[0], tabuleiro)
    segunda_camada = []
    terceira_camada = []
    
    for jogada in primeira_camada:
        segunda_camada.append(get_best_moves(lista_simbolos_temp[1], jogada[1]))

    # Somar os scores das jogadas da segunda camada com as da primeira camada,
    # guardar os 30 melhores scores, tabuleiros e posicoes (da primeira e segunda camada)
    for i, jogada in enumerate(segunda_camada):
        for j in jogada:
            score = primeira_camada[i][0] + j[0]
            tabuleiros = j[1]
            posicoes_temp.append(primeira_camada[i][2])
            posicoes_temp.append(j[2])
            camada_temporaria.append((score, tabuleiros, posicoes_temp))
            posicoes_temp = []

    # Ordenar array por score
    camada_temporaria.sort(key=lambda tup: tup[0], reverse=True)
    segunda_camada = camada_temporaria[:30]
    
    # Iterar pelas jogadas da segunda camada e procurar as melhores jogadas para a terceira camada
    for jogada in segunda_camada:
        terceira_camada.append(get_best_moves(lista_simbolos_temp[2], jogada[1]))
    
    # Somar os scores das jogadas da terceira camada com as da segunda camada,
    # retornar as posições do melhor score
    camada_temporaria = []
    for i, jogada in enumerate(terceira_camada):
        for j in jogada:
            score = segunda_camada[i][0] + j[0]
            tabuleiros = j[1]

            for c in segunda_camada[i][2]:
                posicoes_temp.append(c)

            posicoes_temp.append(j[2])
            camada_temporaria.append((score, tabuleiros, posicoes_temp))
            posicoes_temp = []

    # Ordenar array por score
    camada_temporaria.sort(key=lambda tup: tup[0], reverse=True)

    terceira_camada = camada_temporaria[:1]

    print(terceira_camada)
    return terceira_camada[0][2]





# Retorna as 10 melhores jogadas para uma camada de profundidade
def get_best_moves(simbolo, tabuleiro):
    score_array = []
    tabuleiro_array = []
    posicao_array = []
    moves_array = []

    for i in range(5):
        for l in range(5):
            if tabuleiro[i][l] == " ":
                posicao = (i, l)
                score, tabuleiro_temp = calculate_score(simbolo, tabuleiro, posicao)
                score_array.append(score)
                tabuleiro_array.append(tabuleiro_temp)
                posicao_array.append(posicao)

    for i, score in enumerate(score_array):
        moves_array.append((score, tabuleiro_array[i], posicao_array[i]))

    # Ordenar array por score
    moves_array.sort(key=lambda tup: tup[0], reverse=True)

    moves_array = moves_array[:10]
    
    return moves_array
                
                



# Calcular score da jogada (esta tabuleiro já possui a peça colocada)
def calculate_score(figura, tabuleiro, posicao):
    score = 0
    tabuleiro_temp = copiarTabuleiro(tabuleiro)
    tabuleiro_temp[posicao[0]][posicao[1]] = figura


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

    
    # Se colocou uma peça ao lado de outra diferente diminiu o score por 4
    #if posicao[0] != 0 and tabuleiro_temp[posicao[0] - 1][posicao[1]] != figura:
    #    score -= 4
    
    # Se colocou uma peça a distancia de 2 de outra diferente diminiu o score por 3
    #if posicao[0] != 0 and tabuleiro_temp[posicao[0] - 2][posicao[1]] != figura:
    #    score -= 3
    
    # Se colocou uma peça a distancia de 3 de outra diferente diminiu o score por 1
    #if posicao[0] != 0 and tabuleiro_temp[posicao[0] - 3][posicao[1]] != figura:
    #    score -= 1


    # Verifica se o tabuleiro possui celulas vazias, tabuleiro é array de array, caso não exista nenhum -1000
    for linha in tabuleiro_temp:
        for celula in linha:
            if celula == " ":
                return score, tabuleiro_temp
        
        score -= 1000
        break


    return score, tabuleiro_temp



# Função que será responsável por fazer as jogadas no array proximas_jogadas
def jogar():
    jogadas = []
    global possivel_macro_cruz
    global possivel_macro_x
    global possivel_macro_bola
    global possivel_macro_traco
    global resultado_jogo

    possivel_macro_cruz = verificarMacroCruz()
    possivel_macro_x = verificarMacroX()
    possivel_macro_bola = verificarMacroBola()
    possivel_macro_traco = verificarMacroTraco()

    while len(lista_simbolos) > 0:
        jogadas = procurarJogadas()

        # Colocar jogadas no tabueleiro
        for i, jogada in enumerate(jogadas):
            tabuleiro[jogada[0]][jogada[1]] = lista_simbolos[i]

            # Verificar se formou uma macrofigura
            if(verificar_macrofiguras(lista_simbolos[i], tabuleiro)):
                limparMacroFigura(lista_simbolos[i], tabuleiro)
                print("Formou macrofigura")

                if lista_simbolos[i] == x:
                    resultado_jogo += score_macro_x
                    possivel_macro_x = False
                elif lista_simbolos[i] == cruz:
                    resultado_jogo += score_macro_cruz
                    possivel_macro_cruz = False
                elif lista_simbolos[i] == bola:
                    resultado_jogo += score_macro_bola
                    possivel_macro_bola = False
                elif lista_simbolos[i] == traco:
                    resultado_jogo += score_macro_traco
                    possivel_macro_traco = False

            # Verificar se formou uma microfigura
            if(verificar_microfiguras(lista_simbolos[i], tabuleiro)):
                limparMicroFigura(lista_simbolos[i], tabuleiro)
                print("Formou microfigura")

                if lista_simbolos[i] == x:
                    resultado_jogo += score_micro_x
                elif lista_simbolos[i] == cruz:
                    resultado_jogo += score_micro_cruz
                elif lista_simbolos[i] == bola:
                    resultado_jogo += score_micro_bola
                elif lista_simbolos[i] == traco:
                    resultado_jogo += score_micro_traco
                
                possivel_macro_cruz = verificarMacroCruz()
                possivel_macro_x = verificarMacroX()
                possivel_macro_bola = verificarMacroBola()
                possivel_macro_traco = verificarMacroTraco()


            lista_simbolos.pop(i)
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
    global resultado_jogo
    numeroPecasRestantes = 0
    for linha in tabuleiro:
        for celula in linha:
            if celula != " ":
                numeroPecasRestantes += 1

    resultado_jogo -= 2**numeroPecasRestantes


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

