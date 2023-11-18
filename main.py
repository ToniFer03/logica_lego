import random


#definicao de classes
class Celula:
    def __init__(self, reservedValue, isReserved, isTrash):
        self.value = " "
        self.reservedValue = reservedValue
        self.isReserved = isReserved
        self.isTrash = isTrash
        self.isBlocked = False

    def __str__(self):
        return (
        f"Valor: {self.value}, "
        f"Valor Reservado: {self.reservedValue}, "
        f"Reservada: {self.isReserved}, "
        f"Lixo: {self.isTrash}, "
        f"Bloqueada: {self.isBlocked}"
        )


class Simbolo:
    def __init__(self, value):
        self.value = value
        self.isTrash = False
        self.inicioMacrofigura = False
        self.fimMacrofigura = False

    def setTrashTrue(self):
        if(self.isTrash):
            self.isTrash = False
        else:
            self.isTrash = True

    def setInicioMacrofigura(self):
        self.inicioMacrofigura = True
    
    def setFimMacrofigura(self):
        self.fimMacrofigura = True


    def __str__(self):
        return (
        f"Valor: {self.value}, "
        f"Lixo: {self.isTrash}, "
        f"Inicio Macrofigura: {self.inicioMacrofigura}, "
        f"Fim Macrofigura: {self.fimMacrofigura}"
        )
    


#Define das variaveis iniciais
total_simulacoes = 0        #score total das simulacoes todas
numero_simulacoes = 0       #numero simulacoes realizadas
media = 0                   #media das simulacoes
score = 0                   #score do jogo
score_micro_bola = 16       #score por completar uma bola
score_micro_x = 32          #score por completar uma x
score_micro_cruz = 32       #score por completar uma cruz
score_micro_traco = 4       #score por completar um traco
score_macro_x = 512         #score para completar macro x


#define simbolos a utilizar
cruz = "+"
x = "x"
bola = "o"
traco = "-"


#define tamanho microfiguras (quantos simbolos são necessários para formar uma figura)
micro_forma_x = 5
micro_forma_0 = 4
micro_forma_cruz = 5
micro_forma_traco = 2


#define tamanho das macrofiguras
macro_forma_x = 9


# Criar um tabuleiro vazio
tabuleiro = [[' ' for _ in range(5)] for _ in range(5)]
tabuleiro_macrox = [[' ' for _ in range(5)] for _ in range(5)]

#cria lista de espera
lista_simbolos = []

#definir posicoes microfiguras
posicoes_microfigura_x = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
posicoes_microfigura_o = [(3, 0), (3, 1), (4, 0), (4, 1)]
posicoes_microfigura_cruz = [(2, 3), (3, 2), (3, 3), (3, 4), (4, 3)]
posicoes_microfigura_traco = [(1, 4), (2, 4)]
posicoes_lixo = [(0, 1), (0, 3), (0, 4), (1, 0), (1, 2), (1, 3), (2, 1), (4, 2), (4, 4)]


#definir posicoes macrofigura_X
posicoes_macrox_x = [(0,0), (0, 4), (1,1), (1,3), (2,2), (4,4), (3,1), (4,0), (3,3)]
posicoes_macrox_cruz = [(2,3), (3,2), (3,4), (4,3), (3,3)]
posicoes_macrox_bola = [(3,0), (4,1), (3,1), (4,0)]
posicoes_macrox_traco = [(1,4), (2,4)]




#definicao de funcoes
def main():
    global numero_simulacoes
    global total_simulacoes
    global score
    global tabuleiro
    global tabuleiro_macrox
    global lista_simbolos

    #gerarFilaRandom()
    #verifica_macrofigura_x()
    #iniciar_tabuleiro_microfiguras()
    #iniciar_tabuleiro_macrox()
    #jogar()
    #exibir_tabuleiro(tabuleiro)
    #copiar_valores_tabuleiro(tabuleiro, tabuleiro_macrox)
    #exibir_tabuleiro(tabuleiro_macrox)

    #definir_simbolo_util()      será necessário para a formação de macrofiguras, mas por enquanto não


    while(numero_simulacoes < 100000):
        score = 0
        iniciar_tabuleiro(tabuleiro, posicoes_microfigura_x, posicoes_microfigura_o, posicoes_microfigura_cruz, posicoes_microfigura_traco)
        iniciar_tabuleiro(tabuleiro_macrox, posicoes_macrox_x, posicoes_macrox_bola, posicoes_macrox_cruz, posicoes_macrox_traco)
        gerarFilaRandom(lista_simbolos) 
        verifica_possiblidade_macrofigura_x()
        jogar()
        exibir_tabuleiro(tabuleiro)
        calcularScoreFinal()
        print(f"Score: {score} ---- Numero simulações: {numero_simulacoes}")
        numero_simulacoes += 1
        total_simulacoes += score
    media = total_simulacoes / numero_simulacoes
    print(f"A media de score desta versão é de {media}")
    return 0    



#----------------------------------------------------------------------------------------------------
def verifica_condicoes_macrofigura_x(num_bola):
    if(num_bola % micro_forma_0 > 2 and num_bola != 3):
        return False

    return True


def verifica_possiblidade_macrofigura_x():
    numero_x = 0

    #conta o número de ocorrências de x na lista
    for i in lista_simbolos:
        if (i.value == x):
            numero_x += 1

    #caso seja maior que 9 pode continuar a verificar
    if(numero_x < 9):
        return

    #enquanto do primeiro x ao ulitmo ainda existam x possiveis para formar uma macrofigura
    while(numero_x >= 9):
        condicao_completa = False
        numero_bola = 0
        contador_x_ate_final = 0
        posicao_x_inicial = -1 #posição do primeiro x da macrofigura
        posicao_x_final = -1 #posicao do x final da macro figura
        posicao_temp = -1 #posicao do seguinte a ser inicial caso o primeiro falhe

        for index, i in enumerate(lista_simbolos):
            if i.value == x:
                contador_x_ate_final += 1
                if(posicao_x_inicial == -1):
                    posicao_x_inicial = index
                if (contador_x_ate_final % 6 == 0):
                    posicao_temp = index  # Store the current index

            if i.value == bola:
                numero_bola += 1


            # If at least 9 figures have passed since the first x
            if contador_x_ate_final == 9:
                posicao_x_final = index
                if (verifica_condicoes_macrofigura_x(numero_bola)):
                    lista_simbolos[posicao_x_inicial].setInicioMacrofigura()
                    lista_simbolos[posicao_x_final].setFimMacrofigura()
                    condicao_completa = True
                    break
                else:
                    posicao_x_inicial = posicao_temp
                    contador_x_ate_final -= micro_forma_x
                    numero_x -= micro_forma_x
        
        if(condicao_completa):
            break


#verifica se existe uma figura macro_x no tabuleiro
def verifica_figura_macrox(lista_contadores, tabuleiro):
    global score

    if(lista_contadores[0] == macro_forma_x):
        score += score_macro_x
        while(lista_contadores[0] != 0):
                lista_contadores[0] -= 1
                tabuleiro[(posicoes_macrox_x[lista_contadores[0]][0])][(posicoes_macrox_x[lista_contadores[0]][1])].value = " "

#---------------------------------------------------------------------------------------------



#funcao para gerar uma lista ao calhas de simbolos
def gerarFilaRandom(lista_simbolos):
    # Gera um número aleatório entre 40 e 60 para determinar o tamanho da lista
    tamanho_lista = random.randint(40, 60)

    # Adiciona símbolos aleatórios à lista de espera
    for _ in range(tamanho_lista):
        simbolo_aleatorio = Simbolo(random.choice([cruz, x, bola, traco]))
        lista_simbolos.append(simbolo_aleatorio)


#funcao para iniciar o tabuleiro
def iniciar_tabuleiro(tabuleiro, posicoes_x, posicoes_o, posicoes_cruz, posicoes_traco):
    iniciacao_x = [x, True, False]
    iniciacao_o = [bola, True, False]
    iniciacao_cruz = [cruz, True, False]
    iniciacao_traco = [traco, True, False]
    iniciacao_lixo = [" ", False, True]


    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro[i])):
            #Iniciação das posições x
            if (i, j) in posicoes_x:
                tabuleiro[i][j] = Celula(iniciacao_x[0], iniciacao_x[1], iniciacao_x[2])

            #Iniciação das posições o
            elif (i, j) in posicoes_o:
                tabuleiro[i][j] = Celula(iniciacao_o[0], iniciacao_o[1], iniciacao_o[2])

            #Iniciação das posicoes cruz
            elif (i, j) in posicoes_cruz:
                tabuleiro[i][j] = Celula(iniciacao_cruz[0], iniciacao_cruz[1], iniciacao_cruz[2])

            #Iniciação das posicoes traco
            elif (i, j) in posicoes_traco:
                tabuleiro[i][j] = Celula(iniciacao_traco[0], iniciacao_traco[1], iniciacao_traco[2])

            #Iniciação do resto das posicoes
            else:
                tabuleiro[i][j] = Celula(iniciacao_lixo[0], iniciacao_lixo[1], iniciacao_lixo[2])


#funcao para definir se simbolo e util ou nao
def definir_simbolo_util():
    contador_ocorrencias_x = 0
    contador_ocorrencias_o = 0
    contador_ocorrencias_cruz = 0
    contador_ocorrencias_traco = 0

    for simbolo in lista_simbolos:
        if (simbolo.value == x):
            contador_ocorrencias_x += 1
        if (simbolo.value == bola):
            contador_ocorrencias_o += 1
        if (simbolo.value == cruz):
            contador_ocorrencias_cruz += 1
        if (simbolo.value == traco):
            contador_ocorrencias_traco += 1

    numero_lixo_x = contador_ocorrencias_x % micro_forma_x
    numero_lixo_o = contador_ocorrencias_o % micro_forma_0
    numero_lixo_cruz = contador_ocorrencias_cruz % micro_forma_cruz
    numero_lixo_traco = contador_ocorrencias_traco % micro_forma_traco

    for simbolo in reversed(lista_simbolos):
        if (simbolo.value == "x" and numero_lixo_x > 0):
            simbolo.setTrashTrue()
            numero_lixo_x -= 1
        if (simbolo.value == "o" and numero_lixo_o > 0):
            simbolo.setTrashTrue()
            numero_lixo_o -= 1
        if (simbolo.value == "+" and numero_lixo_cruz > 0):
            simbolo.setTrashTrue()
            numero_lixo_cruz -= 1
        if (simbolo.value == "-" and numero_lixo_traco):
            simbolo.setTrashTrue()
            numero_lixo_traco -= 1
        if(numero_lixo_traco + numero_lixo_o + numero_lixo_cruz + numero_lixo_x == 0):
            break


def jogar_macrofigurax(tabuleiro_Origem, tabuleiro_Destino, contador_tabuleiro):
    copiar_valores_tabuleiro(tabuleiro_Origem, tabuleiro_Destino)

    while(lista_simbolos[0].fimMacrofigura != True):
        #procedimento normal para macrofigura_x
        if lista_simbolos[0].value == x:
            if(tabuleiro_Destino[(posicoes_macrox_x[contador_tabuleiro[0]][0])][(posicoes_macrox_x[contador_tabuleiro[0]][1])].value != " "):
                exit(1)
            tabuleiro_Destino[(posicoes_macrox_x[contador_tabuleiro[0]][0])][(posicoes_macrox_x[contador_tabuleiro[0]][1])].value = x
            contador_tabuleiro[0] += 1
        elif lista_simbolos[0].value == bola:
            if(tabuleiro_Destino[(posicoes_macrox_x[contador_tabuleiro[0]][0])][(posicoes_macrox_x[contador_tabuleiro[0]][1])].value != " "):
                exit(1)
            tabuleiro_Destino[(posicoes_macrox_bola[contador_tabuleiro[1]][0])][(posicoes_macrox_bola[contador_tabuleiro[1]][1])].value = bola
            contador_tabuleiro[1] += 1
        elif lista_simbolos[0].value == cruz:
            if(tabuleiro_Destino[(posicoes_macrox_x[contador_tabuleiro[0]][0])][(posicoes_macrox_x[contador_tabuleiro[0]][1])].value != " "):
                exit(1)
            tabuleiro_Destino[(posicoes_macrox_cruz[contador_tabuleiro[2]][0])][(posicoes_macrox_cruz[contador_tabuleiro[2]][1])].value = cruz
            contador_tabuleiro[2] += 1
        elif lista_simbolos[0].value == traco:
            if(tabuleiro_Destino[(posicoes_macrox_x[contador_tabuleiro[0]][0])][(posicoes_macrox_x[contador_tabuleiro[0]][1])].value != " "):
                exit(1)
            tabuleiro_Destino[(posicoes_macrox_traco[contador_tabuleiro[3]][0])][(posicoes_macrox_traco[contador_tabuleiro[3]][1])].value = traco
            contador_tabuleiro[3] += 1
        
        lista_simbolos.pop(0)
        verificaFigura(contador_tabuleiro, tabuleiro_Destino, False)
    
    tabuleiro_Destino[(posicoes_macrox_x[contador_tabuleiro[0]][0])][(posicoes_macrox_x[contador_tabuleiro[0]][1])].value = x
    contador_tabuleiro[0] += 1
    lista_simbolos.pop(0)
    verifica_figura_macrox(contador_tabuleiro, tabuleiro_Destino)
    copiar_valores_tabuleiro(tabuleiro_Destino, tabuleiro_Origem)


#funcao para preencher celulas
def jogar():
    contador_tabuleiro = [0, 0, 0, 0, 0]  # [contador_x, contador_o, contador_cruz, contador_traco, contador_lixo]

    while(len(lista_simbolos) > 0):
        if(lista_simbolos[0].inicioMacrofigura):
            jogar_macrofigurax(tabuleiro, tabuleiro_macrox, contador_tabuleiro)
        else:
            #procedimento normal para microfiguras
            if lista_simbolos[0].value == x:
                tabuleiro[(posicoes_microfigura_x[contador_tabuleiro[0]][0])][(posicoes_microfigura_x[contador_tabuleiro[0]][1])].value = x
                contador_tabuleiro[0] += 1
            elif lista_simbolos[0].value == bola:
                tabuleiro[(posicoes_microfigura_o[contador_tabuleiro[1]][0])][(posicoes_microfigura_o[contador_tabuleiro[1]][1])].value = bola
                contador_tabuleiro[1] += 1
            elif lista_simbolos[0].value == cruz:
                tabuleiro[(posicoes_microfigura_cruz[contador_tabuleiro[2]][0])][(posicoes_microfigura_cruz[contador_tabuleiro[2]][1])].value = cruz
                contador_tabuleiro[2] += 1
            elif lista_simbolos[0].value == traco:
                tabuleiro[(posicoes_microfigura_traco[contador_tabuleiro[3]][0])][(posicoes_microfigura_traco[contador_tabuleiro[3]][1])].value = traco
                contador_tabuleiro[3] += 1
            
            lista_simbolos.pop(0)
            verificaFigura(contador_tabuleiro, tabuleiro, True)


#funcao para limpar figuras completas
def verificaFigura(lista_contadores, tabuleiro, run_x):
    global score

    if(lista_contadores[0] == micro_forma_x and run_x):
        score += score_micro_x
        while(lista_contadores[0] != 0):
                lista_contadores[0] -= 1
                tabuleiro[(posicoes_microfigura_x[lista_contadores[0]][0])][(posicoes_microfigura_x[lista_contadores[0]][1])].value = " "

    if(lista_contadores[1] == micro_forma_0):
        score += score_micro_bola
        while(lista_contadores[1] != 0):
            lista_contadores[1] -= 1
            tabuleiro[(posicoes_microfigura_o[lista_contadores[1]][0])][(posicoes_microfigura_o[lista_contadores[1]][1])].value = " "


    if(lista_contadores[2] == micro_forma_cruz):
        score += score_micro_cruz
        while(lista_contadores[2] != 0):
            lista_contadores[2] -= 1
            tabuleiro[(posicoes_microfigura_cruz[lista_contadores[2]][0])][(posicoes_microfigura_cruz[lista_contadores[2]][1])].value = " "


    if(lista_contadores[3] == micro_forma_traco):
        score += score_micro_traco
        while(lista_contadores[3] != 0):
                lista_contadores[3] -= 1
                tabuleiro[(posicoes_microfigura_traco[lista_contadores[3]][0])][(posicoes_microfigura_traco[lista_contadores[3]][1])].value = " "


#funcao para retirar o score das pecas ainda no tabuleiro
def calcularScoreFinal():
    global score
    numeroPecasRestantes = 0
    for linha in tabuleiro:
        for celula in linha:
            if(not celula.value == " "):
                numeroPecasRestantes += 1

    score -= 2**numeroPecasRestantes


# Função para exibir o tabuleiro
def exibir_tabuleiro(tabuleiro_exibir):
    print('-' * 9)
    for linha in tabuleiro_exibir:
        print('|'.join(celula.value for celula in linha))
        print('-' * 9)


def copiar_valores_tabuleiro(tabuleiro_origem, tabuleiro_destino):
    for i in range(len(tabuleiro_origem)):
        for j in range(len(tabuleiro_origem[i])):
                # Copy attributes if it's a Celula instance
                tabuleiro_destino[i][j].value = tabuleiro_origem[i][j].value




main()