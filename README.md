## Relatório do Candidato
### Théo Pereira de Souza
### github.com/theo-0413

## Visão Geral da Solução

O projeto aqui descrito teve como objetivo o desenvolvimento de uma proposta de solução embarcada para controle de qualidade e auditoria em ambientes refrigerados, estufas ou painéis elétricos, monitorando o tempo de exposição a temperaturas possivelmente prejudiciais e a integridade do isolamento físico a fim de evitar a degradação de insumos ou sobreaquecimento de componentes. 

O sistema é conectado a uma porta e monitora consistentemente a temperatura ambiente: caso a porta permaneça aberta por um intervalo de tempo determinad como excessivo, ou a temperatura ultrapasse o limite estabelecido, o sistema aciona um alarme a fim de avisar o usuário destes problemas. O sistema também avisa quando é inicializado ou quando ambos os fatores são retornados ao seu estado normal.


## Arquitetura do Sistema Embarcado

O programa em _MicroPython_ foi escrito de modo a seguir um fluxo relativamente simples: O hardware é inicializado, reportando este início ao usuário, juntamente dos valores iniciais → O sistema passa a ocorrer dentro um _loop_ de _while_, onde, a cada _loop_, testes sobre o botão e o sensor MPU6050 são realizados para verificar anomalias, usando os limites estabelecidos na inicialização como referência → No caso de um anomalia ser detectada por um teste, alarmes são acionados.

Caso ambas anamolias na exposição térmica devido à abertura a porta e a temperatura do ambiente sejam normalizaddas, o sistema volta ao seu estado comum, comunicando a normalização de suas variáveis.

## Componentes Utilizados na Simulação

Como requisitado, o diagrama contido no `diagram.json` contém os seguintes componentes conectados:

> Um Microcontrolador ESP32
>
> Um Sensor Temperatura MPU 6050
>
> Um botão _pushbutton_

## Decisões Técnicas Relevantes

O código foi testado várias vezes, usando tolerâncias de tempo de exposição (porta aberta) diferentes, visando monitorar o desempenho do programa sobre diferentes condições. Além disso, para os casos de teste, os valores que representam se o botão está pressionado ou foi solto foi invertido, de modo a acomodar melhor o funcionamento do programa.

## Resultados Obtidos

Descreva o comportamento final do sistema:

- O que funciona corretamente
- Quais requisitos foram atendidos
- Resultado observado na simulação do Wokwi

O comportamento final do sistema atendeu a todos os requisitos necessários, funcionando sob diferentes condições e sendo observado por vários ângulos, além de ter sido corretamente validado pela testagem final, atingindo um desempenho considerado satisfatório.
