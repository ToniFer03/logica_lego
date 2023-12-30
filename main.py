import random


class Simbolo:
    def __init__(self, value):
        self.value = value
        self.inicioMacroX = False
        self.fimMacroX = False
        self.inicioMacroCruz = False
        self.fimMacroCruz = False
        self.inicioMacroBola = False
        self.fimMacroBola = False
    

modo_macro_x = False  # Define se o modo macro_x está ativo ou não
modo_macro_bola = False  # Define se o modo macro_bola está ativo ou não
modo_macro_cruz = False  # Define se o modo macro_cruz está ativo ou não


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
score_macro_cruz = 512  # score para completar macro cruz
score_macro_bola = 256  # score para completar macro bola


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


# define tamanho das macrofiguras
macro_forma_x = 9
macro_forma_cruz = 9
macro_forma_bola = 8


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

# Posições no conflict caso macrox
posicoes_NoConflictX_bola = [(3, 0), (4, 1), (3, 1), (4, 0)]
posicoes_NoConflictX_cruz = [(2, 3), (3, 2), (3, 4), (4, 3), (3, 3)]


# Posições no conflict caso macrocruz
posicoes_NoConflictCruz_x = [(0, 0), (1, 1), (0, 2), (2, 0), (2, 2)]
posicoes_NoConflictCruz_traco = [(0, 4), (1, 4)]


# Posições no conflict caso macrobola
posicoes_NoConflictBola_x = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
posicoes_NoConflictBola_cruz = [(2, 3), (3, 3), (3, 4), (4, 3), (3, 2)]


# Posicoes caso macrox
posicoes_macrox_x = [
    (0, 0),
    (0, 4),
    (1, 1),
    (1, 3),
    (2, 2),
    (4, 4),
    (3, 1),
    (4, 0),
    (3, 3),
]

posicoes_macro_cruz = [
    (2, 3),
    (2, 4),
    (3, 2),
    (4, 2),
    (1, 2),
    (2, 1),
    (2, 0),
    (0, 2),
    (2, 2)
]

posicoes_macro_bola = [
    (4, 0),
    (4, 1),
    (4, 2),
    (3, 0),
    (2, 1),
    (2, 2),
    (2, 0),
    (3, 2)
]



# Definição de funções
def main():
    global score
    global tabuleiro
    global lista_simbolos

    global modo_macro_bola
    global modo_macro_cruz
    global modo_macro_x

    # loop das simulações
    while numero_simulacoes < 100000:
        # Reset nas variaveis
        score = 0
        tabuleiro = [[" " for _ in range(5)] for _ in range(5)]
        modo_macro_bola = False
        modo_macro_cruz = False
        modo_macro_x = False

        gerarFilaRandom(lista_simbolos)
        
        if(not verifica_possiblidade_macrocruz(0)):
            if(not verifica_possiblidade_macrox(0)):
                verifica_possiblidade_macrobola(0)
        
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


# Função responsavel por contar quantas peças de um determinado tipo estão no tabuleiro
def conta_pecas_tabuleiro(simbolo):
    simbolos_tabuleiro = 0
    for i in tabuleiro:
        for j in i:
            if j == simbolo:
                simbolos_tabuleiro += 1

    return simbolos_tabuleiro


# Função responsavel por verificar se não existira interferencia entre a formação do simbolo bola e do macro_x
def condicao_x_macroBola(num_x_tabuleiro, array_bola, array_x):
    continue_loop = True

    if len(array_x) > 0:
        contador_x_antes_espaco_critico = 0
        contador_x_depois_espaco_critico = 0

        # verifica antes do espaço critico quantas x tem
        while array_bola[4] > array_x[contador_x_antes_espaco_critico]:
            contador_x_antes_espaco_critico += 1
            # caso não existam mais x para verificar
            if (contador_x_antes_espaco_critico) == len(array_x):
                continue_loop = False
                break

        if (contador_x_antes_espaco_critico + num_x_tabuleiro) % 5 > 3:
            return False

        # verifica se depois de entrar no espaço critico as x vão ultrapassar o limite
        if continue_loop:
            while (
                array_bola[7]
                > array_x[contador_x_antes_espaco_critico + contador_x_depois_espaco_critico]
            ):
                contador_x_depois_espaco_critico += 1
                # caso não existam mais x para verificar
                if (
                    contador_x_antes_espaco_critico + contador_x_depois_espaco_critico
                ) == (len(array_x)):
                    break

        if (
            ((contador_x_antes_espaco_critico + num_x_tabuleiro) % 5)
            + contador_x_depois_espaco_critico
        ) > 3:
            return False
        
    return True


# Função responsavel por verificar se não existira interferencia entre a formação do simbolo x e do macro_cruz
def condicao_x_macroCruz(num_x_tabuleiro, array_cruz, array_x):
    continue_loop = True

    if len(array_x) > 0:
        contador_x_antes_espaco_critico = 0
        contador_x_depois_espaco_critico = 0

        # verifica antes do espaço critico quantas x tem
        while array_cruz[5] > array_x[contador_x_antes_espaco_critico]:
            contador_x_antes_espaco_critico += 1
            # caso não existam mais x para verificar
            if (contador_x_antes_espaco_critico) == len(array_x):
                continue_loop = False
                break

        if (contador_x_antes_espaco_critico + num_x_tabuleiro) % 5 > 2:
            return False

        # verifica se depois de entrar no espaço critico as x vão ultrapassar o limite
        if continue_loop:
            while (
                array_cruz[8]
                > array_x[
                    contador_x_antes_espaco_critico + contador_x_depois_espaco_critico
                ]
            ):
                contador_x_depois_espaco_critico += 1
                # caso não existam mais x para verificar
                if (
                    contador_x_antes_espaco_critico + contador_x_depois_espaco_critico
                ) == (len(array_x)):
                    break

        if (
            ((contador_x_antes_espaco_critico + num_x_tabuleiro) % 5)
            + contador_x_depois_espaco_critico
        ) > 2:
            return False
        
    return True


# Função responsavel por verificar se não existira interferencia entre a formação do simbolo bola e do macro_x
def condição_bola_macroX(num_bolas_tabuleiro, array_x, array_bola):
    continue_loop = True

    if len(array_bola) > 0:
        contador_bola_antes_espaco_critico = 0
        contador_bola_depois_espaco_critico = 0

        # verifica antes do espaço critico quantas bolas tem
        while array_x[5] > array_bola[contador_bola_antes_espaco_critico]:
            contador_bola_antes_espaco_critico += 1
            # caso não existam mais bolas para verificar
            if (contador_bola_antes_espaco_critico) == len(array_bola):
                continue_loop = False
                break

        if (contador_bola_antes_espaco_critico + num_bolas_tabuleiro) % 4 > 2:
            return False

        # verifica se depois de entrar no espaço critico as bolas vão ultrapassar o limite
        if continue_loop:
            while (
                array_x[8]
                > array_bola[
                    contador_bola_antes_espaco_critico
                    + contador_bola_depois_espaco_critico
                ]
            ):
                contador_bola_depois_espaco_critico += 1
                # caso não existam mais bolas para verificar
                if (
                    contador_bola_antes_espaco_critico
                    + contador_bola_depois_espaco_critico
                ) == (len(array_bola)):
                    break

        if (
            ((contador_bola_antes_espaco_critico + num_bolas_tabuleiro) % 4)
            + contador_bola_depois_espaco_critico
        ) > 2:
            return False

    return True


# Função que verifica se é possível ou não fazer uma macrofigura bola, recebe o número de bolas atualmente no tabuleiro
def verifica_possiblidade_macrobola(num_bolas_tabuleiro):
    global modo_macro_bola
    array_bola = []
    array_x = []

    for index, i in enumerate(lista_simbolos):
        if i.value == bola:
            array_bola.append(index)
        elif i.value == x:
            array_x.append(index)

    while len(array_bola) >= 8:
        if condicao_x_macroBola(num_bolas_tabuleiro, array_bola, array_x):
            lista_simbolos[array_bola[0]].inicioMacroBola = True
            lista_simbolos[array_bola[7]].fimMacroBola = True
            modo_macro_bola = True
            return True
        else:
            array_bola = array_bola[4:]
    
    return False


# Função que verifica se é possível ou não fazer uma macrofigura cruz, recebe o número de x atualmente no tabuleiro
def verifica_possiblidade_macrocruz(num_x_tabuleiro):
    global modo_macro_cruz
    array_cruz = []
    array_x = []

    for index, i in enumerate(lista_simbolos):
        if i.value == cruz:
            array_cruz.append(index)
        elif i.value == x:
            array_x.append(index)

    while len(array_cruz) >= 9:
        if condicao_x_macroCruz(num_x_tabuleiro, array_cruz, array_x):
            lista_simbolos[array_cruz[0]].inicioMacroCruz = True
            lista_simbolos[array_cruz[8]].fimMacroCruz = True
            modo_macro_cruz = True
            return True
        else:
            array_cruz = array_cruz[5:]
    
    return False


# Função que verifica se é possível ou não fazer uma macrofigura x, recebe o número de bolas atualmente no tabuleiro
# O espaço critico refere-se ao espaço onde já não é possivel fazer figuras devido a sobreposição de uma maior
def verifica_possiblidade_macrox(bolas_tabuleiro):
    global modo_macro_x
    array_x = []
    array_bola = []

    for index, i in enumerate(lista_simbolos):
        if i.value == x:
            array_x.append(index)
        elif i.value == bola:
            array_bola.append(index)

    while len(array_x) >= 9:
        if condição_bola_macroX(bolas_tabuleiro, array_x, array_bola):
            lista_simbolos[array_x[0]].inicioMacroX = True
            lista_simbolos[array_x[8]].fimMacroX = True
            modo_macro_x = True
            return True
        else:
            array_x = array_x[5:]
    
    return False



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
    ]  # [contador_x, contador_o, contador_cruz, contador_traco]


    micro_x_permitido = True  # Define se existe um macro_x a ser formado ou não
    micro_cruz_permitido = True  # Define se existe um macro_cruz a ser formado ou não
    micro_bola_permitido = True  # Define se existe um macro_bola a ser formado ou não


    if(modo_macro_x):
        copiar_valores_array(posicoes_base_x, posicao_x_uso)
        copiar_valores_array(posicoes_NoConflictX_bola, posicao_bola_uso)
        copiar_valores_array(posicoes_NoConflictX_cruz, posicao_cruz_uso)
        copiar_valores_array(posicoes_base_traco, posicao_traco_uso)
    elif(modo_macro_cruz):
        copiar_valores_array(posicoes_NoConflictCruz_x, posicao_x_uso)
        copiar_valores_array(posicoes_base_bola, posicao_bola_uso)
        copiar_valores_array(posicoes_base_cruz, posicao_cruz_uso)
        copiar_valores_array(posicoes_NoConflictCruz_traco, posicao_traco_uso)
    elif(modo_macro_bola):
        copiar_valores_array(posicoes_NoConflictBola_x, posicao_x_uso)
        copiar_valores_array(posicoes_base_bola, posicao_bola_uso)
        copiar_valores_array(posicoes_NoConflictBola_cruz, posicao_cruz_uso)
        copiar_valores_array(posicoes_base_traco, posicao_traco_uso)
    else:
        copiar_valores_array(posicoes_base_x, posicao_x_uso) 
        copiar_valores_array(posicoes_base_bola, posicao_bola_uso)
        copiar_valores_array(posicoes_base_cruz, posicao_cruz_uso)
        copiar_valores_array(posicoes_base_traco, posicao_traco_uso)       


    # Para todas os simbolos da lista
    while len(lista_simbolos) > 0:
        # Caso detete o inicio do macro_x
        if lista_simbolos[0].inicioMacroX:
            micro_x_permitido = False
            copiar_valores_array(posicoes_macrox_x, posicao_x_uso)
        
        # Caso detete o inicio do macro_cruz
        if lista_simbolos[0].inicioMacroCruz:
            micro_cruz_permitido = False
            copiar_valores_array(posicoes_macro_cruz, posicao_cruz_uso)
        
        # Caso detete o inicio do macro_bola
        if lista_simbolos[0].inicioMacroBola:
            micro_bola_permitido = False
            copiar_valores_array(posicoes_macro_bola, posicao_bola_uso)


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

        if lista_simbolos[0].fimMacroX:  # Caso chegue ao fim da macrofigura
            micro_x_permitido = True
            copiar_valores_array(posicoes_base_x, posicao_x_uso)
        
        if lista_simbolos[0].fimMacroCruz:  # Caso chegue ao fim da macrofigura
            micro_cruz_permitido = True
            copiar_valores_array(posicoes_base_cruz, posicao_cruz_uso)
        
        if lista_simbolos[0].fimMacroBola:  # Caso chegue ao fim da macrofigura
            micro_bola_permitido = True
            copiar_valores_array(posicoes_base_bola, posicao_bola_uso)


        lista_simbolos.pop(0)
        verifica_existencia_figura(contador_tabuleiro, tabuleiro, micro_x_permitido, micro_cruz_permitido, micro_bola_permitido)


# Função que verifica se existe uma figura completa no tabueiro
# Caso exista, limpa as posições do tabueiro que foram usadas
# e adiciona o score a que corresponde
def verifica_existencia_figura(lista_contadores, tabuleiro, run_micro_x, run_micro_cruz, run_micro_bola):
    global score

    # Caso em que existe macrofigura x no tabueiro
    if lista_contadores[0] == macro_forma_x:
        score += score_macro_x
        while lista_contadores[0] != 0:
            lista_contadores[0] -= 1

            if (
                tabuleiro[(posicoes_macrox_x[lista_contadores[0]][0])][
                    (posicoes_macrox_x[lista_contadores[0]][1])
                ]
                != x
            ):
                exit(erro_limpeza_x)

            tabuleiro[(posicoes_macrox_x[lista_contadores[0]][0])][
                (posicoes_macrox_x[lista_contadores[0]][1])
            ] = " "

        num_bolas_tabuleiro = conta_pecas_tabuleiro(bola)
        verifica_possiblidade_macrox(num_bolas_tabuleiro)

    # Caso em que existe uma microfigura x no tabuleiro
    elif lista_contadores[0] == micro_forma_x and run_micro_x:
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


    # Caso em que existe uma macrofigura bola no tabuleiro
    if lista_contadores[1] == macro_forma_bola:
        score += score_macro_bola
        while lista_contadores[1] != 0:
            lista_contadores[1] -= 1

            if (
                tabuleiro[(posicoes_macro_bola[lista_contadores[1]][0])][
                    (posicoes_macro_bola[lista_contadores[1]][1])
                ]
                != bola
            ):
                exit(erro_limpeza_bola)

            tabuleiro[(posicoes_macro_bola[lista_contadores[1]][0])][
                (posicoes_macro_bola[lista_contadores[1]][1])
            ] = " "

        num_x_tabuleiro = conta_pecas_tabuleiro(x)
        verifica_possiblidade_macrobola(num_x_tabuleiro)

    # Caso em que existe uma microfigura bola no tabuleiro
    elif lista_contadores[1] == micro_forma_0 and run_micro_bola:
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


    # Caso em que existe uma macrofigura cruz no tabuleiro
    if lista_contadores[2] == macro_forma_cruz:
        score += score_macro_cruz
        while lista_contadores[2] != 0:
            lista_contadores[2] -= 1

            if (
                tabuleiro[(posicoes_macro_cruz[lista_contadores[2]][0])][
                    (posicoes_macro_cruz[lista_contadores[2]][1])
                ]
                != cruz
            ):
                exit(erro_limpeza_cruz)

            tabuleiro[(posicoes_macro_cruz[lista_contadores[2]][0])][
                (posicoes_macro_cruz[lista_contadores[2]][1])
            ] = " "

        num_x_tabuleiro = conta_pecas_tabuleiro(x)
        verifica_possiblidade_macrocruz(num_x_tabuleiro)

    # Caso em que existe uma microfigura cruz no tabuleiro
    elif lista_contadores[2] == micro_forma_cruz and run_micro_cruz:
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
                tabuleiro[(posicao_traco_uso[lista_contadores[3]][0])][
                    (posicao_traco_uso[lista_contadores[3]][1])
                ]
                != traco
            ):
                exit(erro_colocacao_traco)

            tabuleiro[(posicao_traco_uso[lista_contadores[3]][0])][
                (posicao_traco_uso[lista_contadores[3]][1])
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


# Função para exibir o tabuleiro
def exibir_tabuleiro(tabuleiro_exibir):
    print("-" * 9)
    for linha in tabuleiro_exibir:
        print("|".join(celula for celula in linha))
        print("-" * 9)


# Função para calcular as estatisticas
def calcular_estatisticas():
    global numero_simulacoes
    global numero_simulacoes_negativas
    global total_simulacoes

    numero_simulacoes += 1
    total_simulacoes += score
    if score < 0:
        numero_simulacoes_negativas += 1


main()
