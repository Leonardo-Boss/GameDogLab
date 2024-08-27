from BitDogLib import *
# Conhecimentos necessários
# - funções
# - while
# - if
# - variaveis
# - escopo global e local
# - tipos de dados
# - lógica booleana
# - listas

TOTAL_COLUNAS = 5
TOTAL_LINHAS = 5
HIGHSCORE_FILE = 'highscore.txt'

# criamos uma variaveis para guardar as core
AZUL = [0, 0, 1]
VERMELHO = [1, 0, 0]
VERDE = [0, 1, 0]

# função para ligar uma linha inteira no tela led
def ligar_linha(buraco, arvore_y):
    coluna = 0
    while coluna < TOTAL_COLUNAS:
    # usamos um loop para ligar cada led da linha
        # usamos essa verificação para pular o led do buraco
        if coluna != buraco:
            ligar_led(coluna, arvore_y, VERDE)
        # aumentamos o i para 
        coluna = coluna + 1

# função para desligar uma linha inteira no tela led
def apagar_linha(buraco, y):
    coluna = 0
    while coluna < TOTAL_COLUNAS:
    # usamos um loop para desligar cada led da linha
        if coluna != buraco:
        # usamos essa verificação para pular o led do buraco pois o jogador pode estar nele
            apagar_led(coluna, y)
        coluna = coluna + 1

# inicializar jogador
# definimos a posição inicial do jogador
jogador_x = 2
jogador_y = 0
# ligamos o led com a posição do jogador
ligar_led(jogador_x, jogador_y, AZUL) 
# inicializamos a pontuação
pontos = 0
# essa variavel define se o jogador está morto ou não
morreu = False
# lemos o highscore
texto_arquivo = ler_arquivo(HIGHSCORE_FILE)
if texto_arquivo == '':
    highscore = 0
else:
    highscore = int(texto_arquivo)

# inicializar arvore
# esolhemos um número aleatório para o buraco
buraco = numero_aleatorio(0,4)
# definimos a posição inicial das arvores
arvore_y = 4.999999 # começar com 4 mostrar porque precisa .999999
# ligamos os leds das arvores
ligar_linha(buraco, int(arvore_y))

# função para apagar todos os leds
def limpar_leds():
    coluna = 0
    while coluna < TOTAL_COLUNAS:
        # fazemos um loop para as colunas
        linha = 0
        while linha < TOTAL_LINHAS:
            # e um loop para as colunas
            apagar_led(coluna,linha)
            linha = linha + 1
        coluna = coluna + 1

# função para mover o jogador para a esquerda
def jogador_esq():
    global jogador_x
    # primeiro verificamos se o jogador não está no canto esquerdo
    if jogador_x <= 0:
        return
    # apagamos o led da posição atual do jogador
    apagar_led(jogador_x, jogador_y)
    # mudamos a posição para a esquerda
    jogador_x = jogador_x - 1
    # ligamos o led da nova posição do jogador
    ligar_led(jogador_x, jogador_y, AZUL)

# função para mover o jogador para a direita
def jogador_direita():
    global jogador_x
    # primeiro verificamos se o jogador não está no canto direito
    if jogador_x >= TOTAL_COLUNAS - 1:
        return
    # apagamos o led da posição atual do jogador
    apagar_led(jogador_x, jogador_y)
    # mudamos a posição para a direita
    jogador_x = jogador_x + 1
    # ligamos o led da nova posição do jogador
    ligar_led(jogador_x,jogador_y, AZUL)


# reseta os valores da arvore
def resetar_arvore():
    global buraco
    global arvore_y
    global pontos
    global highscore
    # escolhemos um novo buraco aleatório
    buraco = numero_aleatorio(0,4)
    # retornamos as arvores para a parte de baixo da tela
    arvore_y = 4.999999
    # pontuamos o jogador por ter passado por uma fileira de arvores
    pontos = pontos + 1
    if pontos > highscore:
        highscore = pontos

# reseta os valores do jogador quando ele morrer
def resetar_jogador():
    global jogador_x
    global jogador_y
    global pontos
    # ligamos o led na posição inicial
    ligar_led(2,0,AZUL)
    jogador_x = 2
    jogador_y = 0
    # resetamos os pontos
    pontos = 0


def mover_arvore(tempo):
    global arvore_y
    global buraco
    # calculamos a distancia que as arvores vão mover
    # velocidade = distância / tempo
    # então podemos calcular a distância movida em certo tempo fazendo
    # tempo * velocidade = distância
    dist = tempo/250_000
    # apagamos a linha atual
    # usamos a função int para transformar o número quebrado da arvore_y em um inteiro
    apagar_linha(buraco, int(arvore_y))
    # calculamos a nova posição da arvore
    # subtraindo a posição atual da distância movida
    arvore_y = arvore_y - dist
    # verificamos se a arvore ainda está nos leds
    if arvore_y < 0:
        # se a arvore já saiu dos leds vamos 
        resetar_arvore()
        return
    # se a arvore não saiu dos leds ligamos os leds na nova posição
    ligar_linha(buraco, int(arvore_y))


# verifica se o jogador está morto
def morto():
    # se o jogador estiver na mesma linha das arvores e não estiver na coluna do burco ele morreu
    if jogador_x != buraco and jogador_y == int(arvore_y):
        return True
    # caso contrario ele sobreviveu
    else:
        return False

# verifica se o jogador deve ganhar pontos
def pontuou():
    # o jogador pontua se estiver na mesma linha da arvore
    if jogador_y == int(arvore_y):
        return True
    return False

# função que define o que deve ser feito em cada loop do jogo
def jogo(delta):
    global pontos
    global morreu
    global arvore_y
    global buraco
    # primeiro verificamos se o jogador morreu
    if morto():
        # trocamos a cor do led para mostrar que o jogador morreu
        ligar_led(jogador_x, jogador_y, VERMELHO)
        # esta verificação é para tocar o som apenas na primeira vez que o loop rodar e o jogador estiver morto
        if not morreu:
            # tocamos o som
            som_morreu()
            # salvamos o novo highscore transformando o numero inteiro em texto (string)
            escrever_arquivo(HIGHSCORE_FILE, str(highscore))
        # trocamos está variável para na próxima iteração não tocar o som de novo
        morreu = True
        # verificamos se o jogador pressionou um botão para voltar ao jogo
        if botao_A_pressionado() or botao_B_pressionado():
            # mudamos o valor de morreu para falso assim vai tocar o som e salvar o pontuação novamente
            morreu = False
            limpar_leds()
            resetar_arvore()
            resetar_jogador()
        # retornamos a função para não executar as partes da arvore
        return
    # se ele não morreu limpamos a tela
    limpar_tela()
    # escrevemos novamente a pontuação para caso ela ter mudado
    escrever_tela("score: " + str(pontos),0,0)
    escrever_tela("hiscore: " + str(highscore),0,10)
    mostrar_tela()
    # movemos a arvore passando o tempo decorrido desde o última iteração
    mover_arvore(delta)
    # verificamos se o jogador pressionou algum botão
    if botao_A_pressionado():
        # se ele pressionou o botão A movemos para a equerda
        jogador_esq()
    if botao_B_pressionado():
        # se ele pressionou o botão B movemos para a direita
        jogador_direita()

# passamos a função jogo que criamos como variavel da função loop
loop(jogo)
