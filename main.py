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

    def setTrashTrue(self):
        self.isTrash = True

    def __str__(self):
        return (
        f"Valor: {self.value}, "
        f"Lixo: {self.isTrash}, "
        )
    
        
#define variavel Score
score = 0
score_micro_bola = 16
score_micro_x = 32
score_micro_cruz = 32
score_micro_traco = 4


#define simbolos a utilizar
cruz = "+"
x = "x"
bola = "o"
traco = "-"

#define tamanho microfiguras
micro_forma_x = 5
micro_forma_0 = 4
micro_forma_cruz = 5
micro_forma_traco = 2

# Criar um tabuleiro vazio
tabuleiro = [[' ' for _ in range(5)] for _ in range(5)]

#cria lista de espera
lista_simbolos = []

#definir posicoes
posicoes_x = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
posicoes_o = [(3, 0), (3, 1), (4, 0), (4, 1)]
posicoes_cruz = [(2, 3), (3, 2), (3, 3), (3, 4), (4, 3)]
posicoes_traco = [(1, 4), (2, 4)]
posicoes_lixo = [(0, 1), (0, 3), (0, 4), (1, 0), (1, 2), (1, 3), (2, 1), (4, 2), (4, 4)]


#definicao de funcoes
def main():
    iniciarTabuleiro()
    gerarFilaRandom() 
    #definir_simbolo_util()      será necessário para a formação de macrofiguras, mas por enquanto não
    jogar()
    exibir_tabuleiro()
    calcularScoreFinal()
    print(f"Score: {score}")
    return 0    


#funcao para gerar uma lista ao calhas de simbolos
def gerarFilaRandom():
    # Gera um número aleatório entre 40 e 60 para determinar o tamanho da lista
    tamanho_lista = random.randint(40, 60)

    # Adiciona símbolos aleatórios à lista de espera
    for _ in range(tamanho_lista):
        simbolo_aleatorio = Simbolo(random.choice([cruz, x, bola, traco]))
        lista_simbolos.append(simbolo_aleatorio)


#funcao para iniciar o tabuleiro
def iniciarTabuleiro():
    iniciacao_x = [x, True, False]
    iniciacao_o = [bola, True, False]
    iniciacao_cruz = [cruz, True, False]
    iniciacao_traco = [traco, True, False]
    iniciacao_lixo = [" ", False, True]


    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro[i])):
            if (i, j) in posicoes_x:
                tabuleiro[i][j] = Celula(iniciacao_x[0], iniciacao_x[1], iniciacao_x[2])
            elif (i, j) in posicoes_o:
                tabuleiro[i][j] = Celula(iniciacao_o[0], iniciacao_o[1], iniciacao_o[2])
            elif (i, j) in posicoes_cruz:
                tabuleiro[i][j] = Celula(iniciacao_cruz[0], iniciacao_cruz[1], iniciacao_cruz[2])
            elif (i, j) in posicoes_traco:
                tabuleiro[i][j] = Celula(iniciacao_traco[0], iniciacao_traco[1], iniciacao_traco[2])
            elif (i, j) in posicoes_lixo:
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


#funcao para preencher celulas
def jogar():
    contadores_tabuleiro = [0, 0, 0, 0, 0]  # [contador_x, contador_o, contador_cruz, contador_traco, contador_lixo]

    while(len(lista_simbolos) > 0):
        #if not lista_simbolos[0].isTrash:
        if lista_simbolos[0].value == x:
            tabuleiro[(posicoes_x[contadores_tabuleiro[0]][0])][(posicoes_x[contadores_tabuleiro[0]][1])].value = x
            contadores_tabuleiro[0] += 1
        elif lista_simbolos[0].value == bola:
            tabuleiro[(posicoes_o[contadores_tabuleiro[1]][0])][(posicoes_o[contadores_tabuleiro[1]][1])].value = bola
            contadores_tabuleiro[1] += 1
        elif lista_simbolos[0].value == cruz:
            tabuleiro[(posicoes_cruz[contadores_tabuleiro[2]][0])][(posicoes_cruz[contadores_tabuleiro[2]][1])].value = cruz
            contadores_tabuleiro[2] += 1
        elif lista_simbolos[0].value == traco:
            tabuleiro[(posicoes_traco[contadores_tabuleiro[3]][0])][(posicoes_traco[contadores_tabuleiro[3]][1])].value = traco
            contadores_tabuleiro[3] += 1
        #else:
        #    tabuleiro[(posicoes_lixo[contadores_tabuleiro[4]][0])][(posicoes_lixo[contadores_tabuleiro[4]][1])].value = lista_simbolos[0].value
        #    contadores_tabuleiro[4] += 1

        lista_simbolos.pop(0)
        verificaFigura(contadores_tabuleiro)


#funcao para limpar figuras completas
def verificaFigura(lista_contadores):
    global score

    if(lista_contadores[0] == micro_forma_x):
        score += score_micro_x
        while(lista_contadores[0] != 0):
                lista_contadores[0] -= 1
                tabuleiro[(posicoes_x[lista_contadores[0]][0])][(posicoes_x[lista_contadores[0]][1])].value = " "

    if(lista_contadores[1] == micro_forma_0):
        score += score_micro_bola
        while(lista_contadores[1] != 0):
            lista_contadores[1] -= 1
            tabuleiro[(posicoes_o[lista_contadores[1]][0])][(posicoes_o[lista_contadores[1]][1])].value = " "


    if(lista_contadores[2] == micro_forma_cruz):
        score += score_micro_cruz
        while(lista_contadores[2] != 0):
            lista_contadores[2] -= 1
            tabuleiro[(posicoes_cruz[lista_contadores[2]][0])][(posicoes_cruz[lista_contadores[2]][1])].value = " "


    if(lista_contadores[3] == micro_forma_traco):
        score += score_micro_traco
        while(lista_contadores[3] != 0):
                lista_contadores[3] -= 1
                tabuleiro[(posicoes_traco[lista_contadores[3]][0])][(posicoes_traco[lista_contadores[3]][1])].value = " "


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
def exibir_tabuleiro():
    print('-' * 9)
    for linha in tabuleiro:
        print('|'.join(celula.value for celula in linha))
        print('-' * 9)


main()