from machine import Pin, I2C
import time

botao_pin = Pin(12, Pin.IN, Pin.PULL_UP)
i2c = I2C(0, scl=Pin(21), sda=Pin(22), freq=400000)
limite_Tempo = 5000
limite_Temperatura = 3.0

tempo_abertura = None  
temperatura_ref = 0.0 
alarme_porta = False
alarme_temp = False
alarme_anterior = False

MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B
TEMP_OUT_H = 0x41


def setup():
  i2c.writeto_mem(MPU_ADDR, PWR_MGMT_1, bytes([0x00]))
  print("Sistema de Monitoramento Inicializado")

def ler_temperatura():
  dados = i2c.readfrom_mem(MPU_ADDR, TEMP_OUT_H, 2)
  valor_bruto = (dados[0] << 8) | dados[1]
  if valor_bruto > 32767:
      valor_bruto -= 65536
  return (valor_bruto / 340.0) + 36.53

def verificar_botao():
  return botao_pin.value() == 1

setup()
temperatura_ref = ler_temperatura()

while True:
  temperatura_atual = ler_temperatura()
  porta_fechada = verificar_botao()

  if porta_fechada:
    tempo_abertura = None
    alarme_porta = False

  else:
    if tempo_abertura is None:
      tempo_abertura = time.ticks_ms()
    
    decorrido = time.ticks_diff(time.ticks_ms(), tempo_abertura)
    
    if (not alarme_porta) and decorrido >= limite_Tempo:
      alarme_porta = True
      print("ALERTA: Porta aberta por muito tempo!")
  
  delta_t = temperatura_atual - temperatura_ref

  if (not alarme_temp) and delta_t >= limite_Temperatura:
    alarme_temp = True
    print("ALERTA: Degradacao termica detectada!")
  elif alarme_temp and delta_t < limite_Temperatura:
    alarme_temp = False

  if porta_fechada and not alarme_porta and not alarme_temp:
    temperatura_ref = temperatura_atual

  alarme_atual = alarme_porta or alarme_temp
  if alarme_anterior and not alarme_atual:
    time.sleep_ms(500)
    print("Status: Sistema Normalizado.")
  alarme_anterior = alarme_atual

  time.sleep_ms(500)