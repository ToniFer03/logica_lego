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
        f"Valor: {self.valor}, "
        f"Valor Reservado: {self.reservedValue}, "
        f"Reservada: {self.isReserved}, "
        f"Lixo: {self.isTrash}, "
        f"Bloqueada: {self.isBlocked}"
        )

#define simbolos a utilizar
cruz = "+"
x = "x"
bola = "o"
traco = "-"

# Criar um tabuleiro vazio
tabuleiro = [[' ' for _ in range(5)] for _ in range(5)]

#cria lista de espera
lista_simbolos = []


#definicao de funcoes
def main():
    gerarFilaRandom() 
    iniciarTabuleiro()
    exibir_tabuleiro(tabuleiro)
    return 0    


#funcao para gerar uma lista ao calhas de simbolos
def gerarFilaRandom():
    # Gera um número aleatório entre 40 e 60 para determinar o tamanho da lista
    tamanho_lista = random.randint(40, 60)

    # Adiciona símbolos aleatórios à lista de espera
    for _ in range(tamanho_lista):
        simbolo_aleatorio = random.choice([cruz, x, bola, traco])
        lista_simbolos.append(simbolo_aleatorio)


#funcao para iniciar o tabuleiro
def iniciarTabuleiro():
    iniciacao_x = ["x", True, False]
    iniciacao_o = ["o", True, False]
    iniciacao_cruz = ["+", True, False]
    iniciacao_traco = ["-", True, False]
    iniciacao_lixo = [" ", False, True]

    posicoes_x = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
    posicoes_o = [(3, 0), (3, 1), (4, 0), (4, 1)]
    posicoes_cruz = [(2, 3), (3, 2), (3, 3), (3, 4), (4, 3)]
    posicoes_traco = [(1, 4), (2, 4)]

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
            else:
                # Inicialização padrão para outras posições
                tabuleiro[i][j] = Celula(iniciacao_lixo[0], iniciacao_lixo[1], iniciacao_lixo[2])


# Função para exibir o tabuleiro
def exibir_tabuleiro(tabuleiro):
    print('-' * 9)
    for linha in tabuleiro:
        print('|'.join(celula.value for celula in linha))
        print('-' * 9)


main()