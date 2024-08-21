from machine import Pin

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

