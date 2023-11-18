import random


#definicao de classes
class Jogo:
    def __init__(self):
        self.existe_macrox = False
    
    def setExiste_Macrox(self):
        if(self.existe_macrox):
            self.existe_macrox = False
        else:
            self.existe_macrox = True


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


#Define variavel jogo
jogo = Jogo()

#Define das variaveis iniciais
total_simulacoes = 0        #score total das simulacoes todas
numero_simulacoes = 0       #numero simulacoes realizadas
media = 0                   #media das simulacoes
score = 0                   #score do jogo


#Definição dos scores para cada forma
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
tabuleiro = []

#cria lista de espera
lista_simbolos = []

posicao_x_uso = []
posicao_bola_uso = []
posicao_cruz_uso = []
posicao_traco_uso = []

#Posições base
#posicoes_base_bola = [(3,0), (3,1), (4,0), (4,1)]          Estão na ordem original
#posicoes_base_cruz = [(2,3), (3,2), (3,3), (3,4), (4,3)]   Estão na ordem original
posicoes_base_x = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
posicoes_base_bola = [(3,0), (4,1), (3,1), (4,0)]
posicoes_base_cruz = [(2,3), (3,2), (3,4), (4,3), (3,3)]
posicoes_base_traco = [(1, 4), (2, 4)]

#Posicoes caso macrox
posicoes_macrox_x = [(0,0), (0, 4), (1,1), (1,3), (2,2), (4,4), (3,1), (4,0), (3,3)]
posicoes_macrox_bola = [(3,0), (4,1), (3,1), (4,0)]
posicoes_macrox_cruz = [(2,3), (3,2), (3,4), (4,3), (3,3)]
posicoes_macrox_traco = [(1,4), (2,4)]




# Definição de funções
def main():
    global numero_simulacoes
    global total_simulacoes
    global score
    global tabuleiro
    global lista_simbolos
    global jogo

    #definir_simbolo_util()      será necessário para a formação de macrofiguras, mas por enquanto não


    while(numero_simulacoes < 100000):
        score = 0
        tabuleiro = [[ " " for _ in range(5)] for _ in range(5)]
        gerarFilaRandom(lista_simbolos)
        teste_ver_macrox()
        jogar()
        calcularScoreFinal()
        numero_simulacoes += 1
        total_simulacoes += score
    media = total_simulacoes / numero_simulacoes
    print(f"A media de score desta versão é de {media} | Numero de simulacoes: {numero_simulacoes}")
    return 0    



# O espaço critico refere-se ao espaço onde já não é possivel fazer figuras devido a sobreposição de uma maior
def teste_ver_macrox():
    array_x = []
    array_o = []
    isImposible = False
    continue_loop = True

    for index, i in enumerate(lista_simbolos):
        if(i.value == x):
            array_x.append(index)
        elif(i.value == bola):
            array_o.append(index)
    

    while(len(array_x) >= 9):
        
        if(len(array_o) > 0):
            contador_bola_antes_espaco_critico = 0
            contador_bola_depois_espaco_critico = 0
            
            #verifica antes do espaço critico quantas bolas tem
            while(array_x[5] > array_o[contador_bola_antes_espaco_critico]):
                contador_bola_antes_espaco_critico += 1
                #caso não existam mais bolas para verificar
                if((contador_bola_antes_espaco_critico) == len(array_o)):
                    continue_loop = False
                    break
            
            if(contador_bola_antes_espaco_critico % 4 > 2):
                isImposible = True

            #verifica se depois de entrar no espaço critico as bolas vão ultrapassar o limite    
            if(continue_loop):
                while((array_x[8] > array_o[contador_bola_antes_espaco_critico + contador_bola_depois_espaco_critico])):
                    contador_bola_depois_espaco_critico += 1
                    #caso não existam mais bolas para verificar
                    if((contador_bola_antes_espaco_critico + contador_bola_depois_espaco_critico) == (len(array_o))):
                        break

            if((contador_bola_antes_espaco_critico + contador_bola_depois_espaco_critico) > 2):
                isImposible = True


        if(isImposible):
            array_x = array_x[5:]
        else:
            lista_simbolos[array_x[0]].setInicioMacrofigura()
            lista_simbolos[array_x[8]].setFimMacrofigura()
            jogo.setExiste_Macrox()
            break


#funcao para gerar uma lista ao calhas de simbolos
def gerarFilaRandom(lista_simbolos):
    # Gera um número aleatório entre 40 e 60 para determinar o tamanho da lista
    tamanho_lista = random.randint(40, 60)

    # Adiciona símbolos aleatórios à lista de espera
    for _ in range(tamanho_lista):
        simbolo_aleatorio = Simbolo(random.choice([cruz, x, bola, traco]))
        lista_simbolos.append(simbolo_aleatorio)


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


def jogar_macrofigurax(contador_tabuleiro):

    while(lista_simbolos[0].fimMacrofigura != True):
        #procedimento normal para macrofigura_x
        if lista_simbolos[0].value == x:
            if(tabuleiro[(posicoes_macrox_x[contador_tabuleiro[0]][0])][(posicoes_macrox_x[contador_tabuleiro[0]][1])] != " "):
                exit("Erro, jogo normal, colocação do x onde já existia uma peça")
            tabuleiro[(posicoes_macrox_x[contador_tabuleiro[0]][0])][(posicoes_macrox_x[contador_tabuleiro[0]][1])] = x
            contador_tabuleiro[0] += 1
        elif lista_simbolos[0].value == bola:
            if(tabuleiro[(posicoes_macrox_bola[contador_tabuleiro[1]][0])][(posicoes_macrox_bola[contador_tabuleiro[1]][1])] != " "):
                exit("Erro, jogo normal, colocação da bola onde já existia uma peça")
            tabuleiro[(posicoes_macrox_bola[contador_tabuleiro[1]][0])][(posicoes_macrox_bola[contador_tabuleiro[1]][1])] = bola
            contador_tabuleiro[1] += 1
        elif lista_simbolos[0].value == cruz:
            if(tabuleiro[(posicoes_macrox_cruz[contador_tabuleiro[2]][0])][(posicoes_macrox_cruz[contador_tabuleiro[2]][1])] != " "):
                exit("Erro, jogo normal, colocação da cruz onde já existia uma peça")
            tabuleiro[(posicoes_macrox_cruz[contador_tabuleiro[2]][0])][(posicoes_macrox_cruz[contador_tabuleiro[2]][1])] = cruz
            contador_tabuleiro[2] += 1
        elif lista_simbolos[0].value == traco:
            if(tabuleiro[(posicoes_macrox_traco[contador_tabuleiro[3]][0])][(posicoes_macrox_traco[contador_tabuleiro[3]][1])] != " "):
                exit("Erro, jogo normal, colocação do traco onde já existia uma peça")
            tabuleiro[(posicoes_macrox_traco[contador_tabuleiro[3]][0])][(posicoes_macrox_traco[contador_tabuleiro[3]][1])] = traco
            contador_tabuleiro[3] += 1
        
        lista_simbolos.pop(0)
        verificaFigura(contador_tabuleiro, tabuleiro, False)
    
    contador_tabuleiro[0] += 1
    lista_simbolos.pop(0)
    verifica_figura_macrox(contador_tabuleiro, tabuleiro)


#funcao para preencher celulas
def jogar():
    contador_tabuleiro = [0, 0, 0, 0, 0]  # [contador_x, contador_o, contador_cruz, contador_traco, contador_lixo]

    while(len(lista_simbolos) > 0):
        if(jogo.existe_macrox): #se existir macrox jogar este
            jogar_macrofigurax(contador_tabuleiro)
        else:
            #procedimento normal para microfiguras
            if lista_simbolos[0].value == x:
                if(tabuleiro[(posicoes_base_x[contador_tabuleiro[0]][0])][(posicoes_base_x[contador_tabuleiro[0]][1])] != " "):
                    exit("Erro, jogo normal, colocação do x onde já existia uma peça")
                tabuleiro[(posicoes_base_x[contador_tabuleiro[0]][0])][(posicoes_base_x[contador_tabuleiro[0]][1])] = x
                contador_tabuleiro[0] += 1
            elif lista_simbolos[0].value == bola:
                if(tabuleiro[(posicoes_base_bola[contador_tabuleiro[1]][0])][(posicoes_base_bola[contador_tabuleiro[1]][1])] != " "):
                    exit("Erro, jogo normal, colocação da bola onde já existia uma peça")
                tabuleiro[(posicoes_base_bola[contador_tabuleiro[1]][0])][(posicoes_base_bola[contador_tabuleiro[1]][1])] = bola
                contador_tabuleiro[1] += 1
            elif lista_simbolos[0].value == cruz:
                if(tabuleiro[(posicoes_base_cruz[contador_tabuleiro[2]][0])][(posicoes_base_cruz[contador_tabuleiro[2]][1])] != " "):
                    exit("Erro, jogo normal, colocação da cruz onde já existia uma peça")
                tabuleiro[(posicoes_base_cruz[contador_tabuleiro[2]][0])][(posicoes_base_cruz[contador_tabuleiro[2]][1])] = cruz
                contador_tabuleiro[2] += 1
            elif lista_simbolos[0].value == traco:
                if(tabuleiro[(posicoes_base_traco[contador_tabuleiro[3]][0])][(posicoes_base_traco[contador_tabuleiro[3]][1])] != " "):
                    exit("Erro, jogo normal, colocação do traço onde já existia uma peça")
                tabuleiro[(posicoes_base_traco[contador_tabuleiro[3]][0])][(posicoes_base_traco[contador_tabuleiro[3]][1])] = traco
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
                tabuleiro[(posicoes_base_x[lista_contadores[0]][0])][(posicoes_base_x[lista_contadores[0]][1])] = " "

    if(lista_contadores[1] == micro_forma_0):
        score += score_micro_bola
        while(lista_contadores[1] != 0):
            lista_contadores[1] -= 1
            tabuleiro[(posicoes_base_bola[lista_contadores[1]][0])][(posicoes_base_bola[lista_contadores[1]][1])] = " "


    if(lista_contadores[2] == micro_forma_cruz):
        score += score_micro_cruz
        while(lista_contadores[2] != 0):
            lista_contadores[2] -= 1
            tabuleiro[(posicoes_base_cruz[lista_contadores[2]][0])][(posicoes_base_cruz[lista_contadores[2]][1])] = " "


    if(lista_contadores[3] == micro_forma_traco):
        score += score_micro_traco
        while(lista_contadores[3] != 0):
                lista_contadores[3] -= 1
                tabuleiro[(posicoes_base_traco[lista_contadores[3]][0])][(posicoes_base_traco[lista_contadores[3]][1])] = " "


#verifica se existe uma figura macro_x no tabuleiro
def verifica_figura_macrox(lista_contadores, tabuleiro):
    global score

    if(lista_contadores[0] == macro_forma_x):
        score += score_macro_x
        while(lista_contadores[0] != 0):
                lista_contadores[0] -= 1
                tabuleiro[(posicoes_macrox_x[lista_contadores[0]][0])][(posicoes_macrox_x[lista_contadores[0]][1])] = " "
        
        jogo.setExiste_Macrox()


#funcao para retirar o score das pecas ainda no tabuleiro
def calcularScoreFinal():
    global score
    numeroPecasRestantes = 0
    for linha in tabuleiro:
        for celula in linha:
            if(celula != " "):
                numeroPecasRestantes += 1

    score -= 2**numeroPecasRestantes


# Função para exibir o tabuleiro
def exibir_tabuleiro(tabuleiro_exibir):
    print('-' * 9)
    for linha in tabuleiro_exibir:
        print('|'.join(celula for celula in linha))
        print('-' * 9)





main()
