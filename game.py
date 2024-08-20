#Programa para acender os LEDs individualmente na cor desejada

# Importação das Bibliotecas: Importa as bibliotecas Pin e neopixel necessárias para controlar os LEDs.
# lib
from machine import Pin
import neopixel

# lib
from utime import ticks_us

# lib
import random

# Configuração inicial

# Número de LEDs na sua matriz 5x5
# lib / aula
NUM_LEDS = 25
ROW_SIZE = 5
COL_SIZE = 5

# Inicializar a matriz de NeoPixels no GPIO7
# A Raspberry Pi Pico está conectada à matriz de NeoPixels no pino GPIO7

# lib
LED_MAP = [[04, 03, 02, 01, 00],
           [05, 06, 07, 08, 09],
           [14, 13, 12, 11, 10],
           [15, 16, 17, 18, 19],
           [24, 23, 22, 21, 20]]

class Leds:
    def __init__(self):
        self.np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

    def acender_led(self, x, y, cor):
        if 0 > x >= ROW_SIZE:
            print("Índice x fora do intervalo. Por favor, escolha um índice de 0 a", NUM_LEDS - 1)
            return
        if 0 > y >= COL_SIZE:
            print("Índice x fora do intervalo. Por favor, escolha um índice de 0 a", NUM_LEDS - 1)
            return

        indice = LED_MAP[y][x]
        # Verifica se o índice está dentro do intervalo permitido
        self.np[indice] = cor  # Define a cor do LED específico
        self.np.write()  # Atualiza a matriz de LEDs para aplicar a mudança

    def apagar_led(self, x, y):
        if 0 > x  and x >= ROW_SIZE:
            print("Índice x fora do intervalo. Por favor, escolha um índice de 0 a", NUM_LEDS - 1)
            return
        if 0 > y and y >= COL_SIZE:
            print("Índice x fora do intervalo. Por favor, escolha um índice de 0 a", NUM_LEDS - 1)
            return

        indice = LED_MAP[y][x]
        self.np[indice] = (0,0,0)  # Define a cor do LED específico
        self.np.write()  # Atualiza a matriz de LEDs para aplicar a mudança

def numero_aleatorio(numero1, numero2):
    return random.randint(numero1, numero2)

button_a = Pin(5, Pin.IN, Pin.PULL_UP)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

button_a_a = 1
button_b_a = 1

def botao_a():
    global button_a_a
    r = False
    a = button_a.value()
    if a == 0 and button_a_a != a:
        r = True
    button_a_a = a
    return r

def botao_b():
    global button_b_a
    r = False
    b = button_b.value()
    if b == 0 and button_b_a != b:
        r = True
    button_b_a = b
    return r

def tempo_de_jogo(old):
    new = ticks_us()
    delta = abs(new - old)
    old = new
    return (delta, old)

def loop(func):
    old = ticks_us()
    while True:
        delta, old = tempo_de_jogo(old)
        func(delta)


def limpar_tela():
    i = 0
    while i < 5:
        j = 0
        while j < 5:
            m.apagar_led(i,j)
            j = j + 1
        i = i + 1

# aula

m = Leds()
m.acender_led(2,0,(0,0,1))
jogador_pos = [2,0]

def jogador_esq():
    x, y = jogador_pos
    if x <= 0:
        return
    m.apagar_led(x, y)
    jogador_pos[0] -= 1
    x, y = jogador_pos
    m.acender_led(x,y,(0,0,1))

def jogador_direita():
    x, y = jogador_pos
    if x >= ROW_SIZE - 1:
        return
    m.apagar_led(x, y)
    jogador_pos[0] += 1
    x, y = jogador_pos
    m.acender_led(x,y,(0,0,1))

def acender_linha(buraco, arvore_y):
    i = 0
    while i < 5:
        if i != buraco:
            m.acender_led(i, arvore_y, (0,1,0))
        i = i + 1

def apagar_linha(buraco, y):
    i = 0
    while i < 5:
        if i != buraco:
            m.apagar_led(i, y)
        i = i + 1

# inicializar arvore
arvore_gap = numero_aleatorio(0,4)
arvore_y = 4.999999
acender_linha(arvore_gap, int(arvore_y))

def inicializar_arvore():
    global arvore_gap
    global arvore_y
    arvore_gap = numero_aleatorio(0,4)
    arvore_y = 4.999999

def inicializar_jogador():
    global jogador_pos
    m.acender_led(2,0,(0,0,1))
    jogador_pos = [2,0]

def mover_arvore(x):
    global arvore_y
    global arvore_gap
    dist = x/250_000
    apagar_linha(arvore_gap, int(arvore_y))
    arvore_y = arvore_y - dist
    if arvore_y < 0:
        inicializar_arvore()
        return
    acender_linha(arvore_gap, int(arvore_y))

def morreu():
    x,y = jogador_pos
    if x != arvore_gap and y == int(arvore_y):
        return True
    else:
        return False

def jogo(delta):
    if morreu():
        x, y = jogador_pos
        m.acender_led(x, y, (1, 0, 0))
        if botao_a() or botao_b():
            limpar_tela()
            inicializar_arvore()
            inicializar_jogador()
        return
    global arvore_y
    global arvore_gap
    mover_arvore(delta)
    if botao_a():
        jogador_esq()
    if botao_b():
        jogador_direita()


loop(jogo)
