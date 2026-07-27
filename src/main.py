from machine import Pin, I2C
import time

# Configurações iniciais
bot_pino = Pin(12, Pin.IN, Pin.PULL_UP)
i2c = I2C(0, scl=Pin(21), sda=Pin(22), freq=400000) 

lim_Time = 5000
lim_Temp = 3.0

t_aberto = None 
temp_ref = 0.0  
alarme_porta = False
alarme_temp = False
alarme_ant = False

MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B
TEMP_OUT_H = 0x41

# Funções
def setup():
  i2c.writeto_mem(MPU_ADDR, PWR_MGMT_1, bytes([0x00])) # Inicialização do imu1
  print("Sistema de Monitoramento Inicializado")

def ler_temp():
  dados = i2c.readfrom_mem(MPU_ADDR, TEMP_OUT_H, 2)
  val_bruto = (dados[0] << 8) | dados[1]
  if val_bruto > 32767:
      val_bruto -= 65536
  return (val_bruto / 340.0) + 36.53

def verificar_botao():
  return bot_pino.value() == 1

setup()
temp_ref = ler_temp()

while True:
  temp_at = ler_temp()
  porta_fechada = verificar_botao()

  if porta_fechada:
    t_aberto = None
    alarme_porta = False

  else:
    if t_aberto is None:
      t_aberto = time.ticks_ms()
    
    t_passado = time.ticks_diff(time.ticks_ms(), t_aberto)
    
    if (not alarme_porta) and t_passado >= lim_Time:
      alarme_porta = True
      print("ALERTA: Porta aberta por muito tempo!")
  
  delta_t = temp_at - temp_ref

  if (not alarme_temp) and delta_t >= lim_Temp:
    alarme_temp = True
    print("ALERTA: Degradacao termica detectada!")
  elif alarme_temp and delta_t < lim_Temp:
    alarme_temp = False

  if porta_fechada and not alarme_porta and not alarme_temp:
    temp_ref = temp_at

  alarme_atual = alarme_porta or alarme_temp
  if alarme_ant and not alarme_atual:
    time.sleep_ms(500)
    print("Status: Sistema Normalizado.")
  alarme_ant = alarme_atual

  time.sleep_ms(500)