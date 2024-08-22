from BitDogLib import *

# TODO: trocar jogador_pos por jogador_x e jogador_y
# TODO: remover += -= e outros sugar syntax se tiver

# Conhecimentos necessários
# - funções
# - while
# - if
# - variaveis
# - escopo global e local
# - tipos de dados
# - lógica booleana
# - listas

TAMANHO_LINHA = 5
HIGHSCORE_FILE = 'highscore.txt'

def ligar_linha(buraco, arvore_y):
    i = 0
    while i < TAMANHO_LINHA:
        if i != buraco:
            ligar_led(i, arvore_y, [0,1,0])
        i = i + 1

def apagar_linha(buraco, y):
    i = 0
    while i < TAMANHO_LINHA:
        if i != buraco:
            apagar_led(i, y)
        i = i + 1

# inicializar jogador
ligar_led(2,0,[0,0,1])
jogador_pos = [2,0]
score = 0
morto = False
texto_arquivo = ler_arquivo(HIGHSCORE_FILE)
if texto_arquivo == '':
    hiscore = 0
else:
    hiscore = int(texto_arquivo)

# inicializar arvore
arvore_gap = numero_aleatorio(0,4)
arvore_y = 4.999999 # começar com 4 mostrar porque precisa .999999
ligar_linha(arvore_gap, int(arvore_y))

def limpar_tela():
    i = 0
    while i < 5:
        j = 0
        while j < 5:
            apagar_led(i,j)
            j = j + 1
        i = i + 1

def jogador_esq():
    x, y = jogador_pos
    if x <= 0:
        return
    apagar_led(x, y)
    jogador_pos[0] -= 1
    x, y = jogador_pos
    ligar_led(x,y,[0,0,1])

def jogador_direita():
    x, y = jogador_pos
    if x >= TAMANHO_LINHA - 1:
        return
    apagar_led(x, y)
    jogador_pos[0] += 1
    x, y = jogador_pos
    ligar_led(x,y,[0,0,1])


def inicializar_arvore():
    global arvore_gap
    global arvore_y
    global score
    global hiscore
    arvore_gap = numero_aleatorio(0,4)
    arvore_y = 4.999999
    score = score + 1
    if score > hiscore:
        hiscore = score

def inicializar_jogador():
    global jogador_pos
    global score
    ligar_led(2,0,[0,0,1])
    jogador_pos = [2,0]
    score = -1

def mover_arvore(x):
    global arvore_y
    global arvore_gap
    dist = x/250_000
    apagar_linha(arvore_gap, int(arvore_y))
    arvore_y = arvore_y - dist
    if arvore_y < 0:
        inicializar_arvore()
        return
    ligar_linha(arvore_gap, int(arvore_y))

def morreu():
    x,y = jogador_pos
    if x != arvore_gap and y == int(arvore_y):
        return True
    else:
        return False

def pontuou():
    x, y = jogador_pos
    if y == int(arvore_y):
        return True
    return False

def jogo(delta):
    global score
    global morto
    if morreu():
        x, y = jogador_pos
        ligar_led(x, y, [1, 0, 0])
        if not morto:
            som_morreu()
            escrever_arquivo(HIGHSCORE_FILE, str(hiscore))
        morto = True
        if botao_a() or botao_b():
            morto = False
            limpar_tela()
            inicializar_jogador()
            inicializar_arvore()
        return
    limpar_display()
    escrever_display("score: " + str(score),0,0)
    escrever_display("hiscore: " + str(hiscore),0,10)
    mostrar_display()
    global arvore_y
    global arvore_gap
    mover_arvore(delta)
    if botao_a():
        jogador_esq()
    if botao_b():
        jogador_direita()

loop(jogo)
