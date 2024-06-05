from mfrc522 import MFRC522
import utime

from time import sleep

# Importa as classes Pin e I2C da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin, I2C
# Importa a classe SSD1306_I2C da biblioteca ssd1306.py
from ssd1306 import SSD1306_I2C
#================================================================================================================================================================================================================================================
#================================================================================================================================================================================================================================================

pin_coms = Pin(6, Pin.OUT)
pin_coms.value(0)

#================================================================================================================================================================================================================================================
#================================================================================================================================================================================================================================================
#APROVACOES

card_status = False
passcode_status = False

#================================================================================================================================================================================================================================================
#================================================================================================================================================================================================================================================
#SETANDO PIN DO MOTOR

pin_solenoide = Pin(7, Pin.OUT)
pin_solenoide.value(0)

def unlock(time):
    pin_solenoide.value(1)
    sleep(time)
    pin_solenoide.value(0)

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

def write_passcode(text):
    display.fill_rect(0, 50, 128, 30, 0)     # desenha um retângulo sólido de 0,0 a 32,32, cor = 1
    display.text(text, 16, 50)
    display.show()
    
def write_mid(text):
    height = 25
    display.fill_rect(0, height, 128, 10, 0)
    display.text(text, 0, height)
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


def draw_top_info():
    display.text("CARD", 4, 6)
    display.text("SENHA", 60, 6)
    
    if card_status:
        draw_openedlock_REL(40)
    elif not card_status:
        draw_closedlock_REL(40)
        
    if passcode_status:
        draw_openedlock_REL(105)
    else:
        draw_closedlock_REL(105)
        
    display.fill_rect(0, 15, 128, 2, 1)
    display.show()
#================================================================================================================================================================================================================================================
#================================================================================================================================================================================================================================================
# MEMBRANA TECLADO

# defenir Pins de acordo com os cabos
col_list=[16,17,20,21]
row_list=[22,26,27,28]
 
# preparar linhas
for x in range(0,4):
    row_list[x]=Pin(row_list[x], Pin.OUT)
    row_list[x].value(1)
 
# prepara coluna
for x in range(0,4):
    col_list[x] = Pin(col_list[x], Pin.IN, Pin.PULL_UP)
 
# Criar KeyMap de Teclado
# Possivel Substituir por outros chars
key_map=[["D","#","0","*"],\
    ["C","9","8","7"],\
    ["B","6","5","4"],\
    ["A","3","2","1"]]
 
def Keypad4x4Read(cols,rows):
    for r in rows:
        r.value(0)
        result=[cols[0].value(),cols[1].value(),cols[2].value(),cols[3].value()]
        if min(result)==0:
            key=key_map[int(rows.index(r))][int(result.index(0))]
            r.value(1) 
            return(key)
        r.value(1)

passcode = []
code = ["1","2","3","4"]

#================================================================================================================================================================================================================================================
#================================================================================================================================================================================================================================================


reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

print("Bring TAG closer...")
print("")

registered_cards = ["2735748832"]






while True:
    
    draw_top_info()
    
    #Porta do Cofre aberta, aguardando para aproximar o cartao e resetar o loop
    if card_status and passcode_status:
        write_mid("Abrir.")
        unlock(time = 2)
        write_mid("Aproximar card.")
        
        while card_status:
            reader.init()
            (stat, tag_type) = reader.request(reader.REQIDL)
            if stat == reader.OK:
                (stat, uid) = reader.SelectTagSN()
                if stat == reader.OK:
                    card = int.from_bytes(bytes(uid),"little",False)
                    #print("CARD ID: "+str(card))
                    if str(card) in registered_cards:
                        write_mid("Fechar.")
                        
                        #retornando o segundo raspberry para funcao normal e contagem de moedas
                        pin_coms.value(0)
                        
                        card_status = False
                        passcode_status = False
                        unlock(time = 2)
                    else:
                        pass
    
    
    # loop antes de autorizar via cartao
    elif not card_status:
        
        write_mid("Aproxime o card.")
        
        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                card = int.from_bytes(bytes(uid),"little",False)
                print(card)
                #print("CARD ID: "+str(card))
                if str(card) in registered_cards:
                    print("accept")
                    card_status = True
                else:
                    print("refuse")
                    card_status = False
                    pin_solenoide.value(0)
                    
    # loop apos autorizar cartao
    # autiticacao de senha
    elif card_status:
        
        write_mid("Digite a senha.")
        
        key=Keypad4x4Read(col_list, row_list)
        if key != None:
            #print("You pressed: "+key)
            
            if key == "D":
                if passcode == code:
                    passcode_status = True
                    draw_top_info()
                    write_mid("Autorizado.")
                    
                    pin_coms.value(1)
                    
                    passcode.clear()
                    sleep(1)
                    
                    
                else:
                    card_status = False
                    draw_top_info()
                    write_mid("Senha incorreta.")
                    sleep(3)
                    
                    passcode.clear()
                    sleep(0.5)
    
                    
            elif key == "A":
                if len(passcode)>0:
                    del passcode[-1]
                    print(passcode)
            
            else:
                passcode.append(key)
                print(passcode)
            
            string_passcode = "".join(passcode)
            write_passcode(string_passcode)
        
        
        pass
        
                
                
print('out')
utime.sleep_ms(500) 
