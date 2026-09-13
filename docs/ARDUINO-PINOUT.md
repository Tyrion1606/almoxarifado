# Pinagem do Arduino Uno R3 e do Arduino Nano

Atualizado em 13/09/2026.

## Imagens exibidas nas fichas

| Placa | Ordem | Arquivo | Conteúdo |
| --- | ---: | --- | --- |
| Uno | 1 | [uno-pinout-simple.png](../assets/pinouts/uno-pinout-simple.png) | Desenho do almoxarifado no estilo das folhas simples da G474/H7R3 |
| Uno | 2 | [uno-pinout.png](../assets/pinouts/uno-pinout.png) | Folha oficial Arduino A000066 (CC BY-SA 4.0), recortada por `scripts/prepare_pinouts.py` |
| Nano | 1 | [nano-pinout-simple.png](../assets/pinouts/nano-pinout-simple.png) | Mesmo estilo, com as diferenças do Nano |
| Nano | 2 | [nano-pinout.png](../assets/pinouts/nano-pinout.png) | Folha oficial Arduino A000005 (CC BY-SA 4.0) |

Cada furo das folhas simples é lido da placa para fora: nome Arduino → porta do ATmega328P → número do pino no chip → até três funções (PWM/timer, SPI, I2C, UART, ADC, comparador, INT/PCINT, uso na placa). Também trazem o ICSP 2×3, a legenda e notas sobre PWM, interrupções, corrente e pinos internos. A ordem das imagens vem do campo `pinouts` (migrações 3 e 4 em `scripts/migrate.py`).

SHA-256:

- `uno-pinout-simple.png`: `d288071498aa7fb5987b79b66dacc57c217ea8ba957e1bdd65c063d05f618489`
- `nano-pinout-simple.png`: `87885b0a7b4b9e2f9aa9deccb3f1110a45fe0dc590068aee36b3f97275b11011`

## Como alterar

As duas folhas saem de [scripts/make_arduino_pinouts.py](../scripts/make_arduino_pinouts.py): `python3 scripts/make_arduino_pinouts.py` (ou `uno` / `nano`). Requer Pillow e fontes DejaVu. D0–D13 e RESET ficam em `digital_pins()` e A0–A5 em `analog_pin()`, compartilhados pelas duas placas porque o chip é o mesmo. A ordem dos furos e o que é exclusivo de cada placa ficam em `UNO` e `NANO`. Não edite os PNGs à mão.

## Diferenças entre as placas

| | Uno R3 | Nano |
| --- | --- | --- |
| Chip | ATmega328P-PU, DIP-28 no soquete (clones SMD: QFP-32) | ATmega328P-AU, QFP-32 |
| Pino do chip na folha | DIP e QFP | só QFP |
| A6 / A7 | não existem no DIP | ADC6 (QFP 19) e ADC7 (QFP 22), só analógicos: sem porta digital, pull-up ou PCINT |
| USB-serial | ATmega16U2 | FT232RL no original, CH340 na maioria dos clones |
| 3V3 | regulador da placa, 50 mA | vem do chip USB: 50 mA no FT232RL; em clones CH340 costuma ser bem menos |
| RESET no header | 1 | 2 (mesmo sinal PC6) |
| Extras | IOREF, NC, SDA/SCL separados (= A4/A5) | — |

## Interrupções (pergunta do usuário em 13/09/2026)

Todo pino de I/O do ATmega328P tem PCINT, por isso a caixa aparece em todas as linhas. Só D2 (INT0) e D3 (INT1) aceitam `attachInterrupt()` com escolha de borda. PCINT dispara em qualquer mudança, tem uma única rotina por porta (B = D8–D13, C = A0–A5, D = D0–D7) e exige PCICR/PCMSK ou biblioteca. As caixas de PCINT dizem "sem attachInterrupt", e uma nota da folha explica a diferença.

## Fontes e cuidados

- Funções alternativas e numeração QFP-32: Figura 1-1 do [datasheet ATmega328P](../assets/documents/atmega328p.pdf). Ligações das placas: [folha Uno](../assets/documents/uno-pinout.pdf) (p. 1, 3 e 5) e [folha Nano](../assets/documents/nano-pinout.pdf) (p. 1–3). Conferidas pino a pino.
- DIP-28: numeração do ATmega328P-PU. O PDF local é a edição automotiva (só TQFP/QFN), então a figura PDIP não está nele.
- Revisões físicas das placas do usuário não registradas: clones mudam o chip USB e às vezes o chip AVR (QFP no Uno). Os pinos do header não mudam.
- Limites: 40 mA por pino e 200 mA em VCC/GND (tabela 28.1); 20 mA por pino, 50 mA no 3V3 e VIN 7–12 V (folhas Arduino).
- Desenhos das placas esquemáticos e fora de escala; não use para medir furação.
