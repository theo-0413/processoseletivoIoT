from machine import Pin, I2C
import time

# Configuração dos pinos dos componentes
botao_pin = Pin(12, Pin.IN, Pin.PULL_UP)
i2c = I2C(0, scl=Pin(21), sda=Pin(22), freq=400000)  # Configuração do módulo i2c

# Definição de limites do sistema
limite_Tempo = 5000
limite_Temperatura = 3.0

# Definição dos estados iniciais
tempo_abertura = None   # Marcação de tempo do momento que a porta abriu
temperatura_ref = 0.0   # Referência de temperatura do sistema estável
alarme_porta = False
alarme_temp = False
alarme_anterior = False # Variável temporária para verificação da normalização do sistema


# Definição de valores de endereço para o imu1
MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B
TEMP_OUT_H = 0x41


def setup():
  i2c.writeto_mem(MPU_ADDR, PWR_MGMT_1, bytes([0x00])) # Inicialização do imu1
  print("Sistema de Monitoramento Inicializado")


# Função de leitura de temperatura com o imu1 a partir das fórmulas do datasheet
def ler_temperatura():
  dados = i2c.readfrom_mem(MPU_ADDR, TEMP_OUT_H, 2)
  valor_bruto = (dados[0] << 8) | dados[1]
  if valor_bruto > 32767:
      valor_bruto -= 65536
  return (valor_bruto / 340.0) + 36.53

# Função de verificação da porta (Botão pressionado)
def verificar_botao():
  return botao_pin.value() == 1


# Configuração do sistema
setup()
temperatura_ref = ler_temperatura() # Leitura inicial de temperatura para referência

# Loop Principal
while True:
  # leitura das informações de temperatura e de abertura do portão
  temperatura_atual = ler_temperatura()
  porta_fechada = verificar_botao()

  # Tratamento do caso da porta aberta
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
  
  # Tratamento do caso da temperatura elevada
  delta_t = temperatura_atual - temperatura_ref

  if (not alarme_temp) and delta_t >= limite_Temperatura:
    alarme_temp = True
    print("ALERTA: Degradacao termica detectada!")
  elif alarme_temp and delta_t < limite_Temperatura:
    alarme_temp = False

  # Atualização da temperatura de referência se a situação estiver normalizada
  if porta_fechada and not alarme_porta and not alarme_temp:
    temperatura_ref = temperatura_atual

  # Atualização do Status com garantia da normalização  
  alarme_atual = alarme_porta or alarme_temp
  if alarme_anterior and not alarme_atual:
    time.sleep_ms(500)
    print("Status: Sistema Normalizado.")
  alarme_anterior = alarme_atual

  time.sleep_ms(500)
