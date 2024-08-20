#Programa para acender os LEDs individualmente na cor desejada

# Importação das Bibliotecas: Importa as bibliotecas Pin e neopixel necessárias para controlar os LEDs.
from machine import Pin
import neopixel
import time

# Configuração inicial

# Número de LEDs na sua matriz 5x5
NUM_LEDS = 25
ROW_SIZE = 5
COL_SIZE = 5

# Inicializar a matriz de NeoPixels no GPIO7
# A Raspberry Pi Pico está conectada à matriz de NeoPixels no pino GPIO7

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

        print('y',y)
        print('x',x)
        indice = LED_MAP[y][x]
        self.np[indice] = (0,0,0)  # Define a cor do LED específico
        self.np.write()  # Atualiza a matriz de LEDs para aplicar a mudança

m = Leds()
m.acender_led(2,0,(1,0,0))
jogador_pos = [2,0]

button_a = Pin(5, Pin.IN, Pin.PULL_UP)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

def jogador_esq():
    x, y = jogador_pos
    if x <= 0: return
    m.apagar_led(x, y)
    jogador_pos[0] -= 1
    x, y = jogador_pos
    m.acender_led(x,y,(1,0,0))

def jogador_direita():
    x, y = jogador_pos
    if x >= ROW_SIZE - 1: return
    m.apagar_led(x, y)
    jogador_pos[0] += 1
    x, y = jogador_pos
    m.acender_led(x,y,(1,0,0))

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

while True:
    if botao_a():
        jogador_esq()
    if botao_b():
        jogador_direita()
