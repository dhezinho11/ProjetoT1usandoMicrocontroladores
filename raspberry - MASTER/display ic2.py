"""!
@file display_oled_i2c_128x64_exemplo.py
@brief Programa para escrever em um display OLED I2C de 128x64 usando o Raspberry Pi Pico.
@details Este programa utiliza a biblioteca ssd1306 para escrever em um display OLED de 128x64 via barramento I2C.
         Referência: https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
@author Rodrigo França
@date 2024-04-03
"""

from time import sleep

# Importa as classes Pin e I2C da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin, I2C
# Importa a classe SSD1306_I2C da biblioteca ssd1306.py
from ssd1306 import SSD1306_I2C

# Define os pinos do Raspberry Pi Pico conectados ao barramento I2C 0
i2c1_slc_pin = 19
i2c1_sda_pin = 18

# Inicializa o I2C0 com os pinos GPIO9 (SCL) e GPIO8 (SDA)
i2c1 = I2C(1, scl=Pin(i2c1_slc_pin), sda=Pin(i2c1_sda_pin), freq=400000)

# Inicializa o display OLED I2C de 128x64
display = SSD1306_I2C(128, 64, i2c1)

# Limpa o display
display.fill(0)
display.show()

def draw_closedlock_REL(x_pos):
    
    display.fill_rect(x_pos, 2, 10, 10, 0)
    
    display.fill_rect(x_pos, 8, 7, 6, 1)
    display.fill_rect(x_pos+1, 4, 1, 4, 1)
    display.fill_rect(x_pos+5, 4, 1, 4, 1)
    display.fill_rect(x_pos+1, 3, 5, 1, 1)
    
    display.show()
    
def draw_openedlock_REL(x_pos):
    display.fill_rect(x_pos, 2, 10, 10, 0)
    
    display.fill_rect(x_pos, 8, 7, 6, 1)
    display.fill_rect(x_pos+1, 3, 1, 3, 1)
    display.fill_rect(x_pos+5, 3, 1, 5, 1)
    display.fill_rect(x_pos+1, 2, 5, 1, 1)
    

    display.show()


def draw_top_info(card_lock, code_lock):
    display.text("CARD", 4, 6)
    display.text("SENHA", 60, 6)
    
    if card_lock:
        draw_openedlock_REL(40)
    elif not card_lock:
        draw_closedlock_REL(40)
        
    if code_lock:
        draw_openedlock_REL(105)
    elif not code_lock:
        draw_closedlock_REL(105)
        
    display.fill_rect(0, 15, 128, 2, 1)
    display.show()


draw_top_info(0,0)
sleep(2)
draw_top_info(1,0)


