from mfrc522 import MFRC522
import utime

from time import sleep

# Importa as classes Pin e I2C da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin, I2C
# Importa a classe SSD1306_I2C da biblioteca ssd1306.py
from ssd1306 import SSD1306_I2C
#================================================================================================================================================================================================================================================
#================================================================================================================================================================================================================================================

pin_coms = Pin(28, Pin.IN)
cleared = False

#================================================================================================================================================================================================================================================
#================================================================================================================================================================================================================================================
#SETANDO O DISPLAY
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

                    #================================================================================================================================================================================================================================================
        #funções auxiliares para desenho no display


sensores = [machine.Pin(2, machine.Pin.IN), machine.Pin(3, machine.Pin.IN), machine.Pin(4, machine.Pin.IN), machine.Pin(5, machine.Pin.IN), machine.Pin(6, machine.Pin.IN)]

touching = [False, False, False, False, False]
amount_coin = [0, 0, 0, 0, 0]
cash_vector = [1,0.5,0.25,0.1,0.05]

led = machine.Pin(25, machine.Pin.OUT)

                    #================================================================================================================================================================================================================================================
        #funções auxiliares para desenho no display



def draw_top_info():
    #limpando area de escrita
    display.fill_rect(0, 0, 128, 20, 0)
    
    sum = 0
    for i in range(len(amount_coin)):
        sum += cash_vector[i]*amount_coin[i]
        
    display.text(f"R${sum}", 4, 6)
    
    
    display.fill_rect(0, 15, 128, 2, 1)
    display.show()

#================================================================================================================================================================================================================================================
#================================================================================================================================================================================================================================================


led.toggle()

while True:
    
    draw_top_info()
    
    if pin_coms.value() == 0:
        
        if cleared == True:
            cleared = False
    
        for i in range(len(sensores)):
            if sensores[i].value() == 0 and touching[i] == False:
                touching[i] = True
                amount_coin[i] += 1
                led.toggle()
            
            if sensores[i].value() == 1 and touching[i] == True:
                touching[i] = False
        
    if pin_coms.value() == 1:
        if cleared == False:
            amount_coin = [0, 0, 0]
            cleared = True
        
        
            
        
    # Aguarda um curto período de tempo antes de ler novamente
    sleep(0.01)
    
    
    
    
    