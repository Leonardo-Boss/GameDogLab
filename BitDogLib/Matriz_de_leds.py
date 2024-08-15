#Programa para acender os LEDs individualmente na cor desejada

# Importação das Bibliotecas: Importa as bibliotecas Pin e neopixel necessárias para controlar os LEDs.
from machine import Pin
import neopixel

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
        if 0 <= x < ROW_SIZE and 0 <= y < COL_SIZE:
            self.np[indice] = cor  # Define a cor do LED específico
            self.np.write()  # Atualiza a matriz de LEDs para aplicar a mudança

# FIM
