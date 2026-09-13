# Pinagem da WeAct G474 Long — imagens e numeração do encapsulamento

Atualizado em 12/09/2026. Leia antes de alterar qualquer pinagem da G474.

## Regra principal

A placa usa o **STM32G474CEU6**. O **U** do código indica o encapsulamento **UFQFPN48** (QFN de 48 pinos com pad térmico). O número de pino do CI deve vir **sempre** da coluna UFQFPN48 da tabela 12 do datasheet ST **DS12288 Rev 6** ([stm32g474.pdf](../assets/documents/stm32g474.pdf)), e nunca da coluna LQFP48 ao lado.

Os dois encapsulamentos têm 48 pinos, mas não são intercambiáveis:

- no UFQFPN48, VSS e VSSA ficam no pad térmico (pino 49), sobrando posições para PC4, PC6, PC10 e PC11;
- o LQFP48 usa pinos para VSS/VSSA e **não tem** PC4, PC6, PC10 nem PC11;
- a partir de PB0 os números se deslocam entre os dois encapsulamentos.

O esquema WeAct ([g474-long-schematic.pdf](../assets/documents/g474-long-schematic.pdf), U1) confirma a numeração UFQFPN48. Exemplos: PB10 = 22, PB11 = 24, PB12 = 25, PA12 = 34, PA13 = 36.

## Imagens exibidas na ficha

A aba **Pinagem** da G474 mostra duas imagens, uma abaixo da outra. A ordem vem do campo `pinouts` da ficha no SQLite. São os únicos arquivos de pinagem da G474 em `assets/pinouts/`; o teste `test_g474_pinout_versions` falha se aparecer outro.

| Ordem | Arquivo | Conteúdo |
| ---: | --- | --- |
| 1 | [g474-long-pinout-simple.png](../assets/pinouts/g474-long-pinout-simple.png) | Visão rápida: GPIO e três funções principais por pino, sobre o render oficial WeAct. |
| 2 | [g474-long-pinout-full.png](../assets/pinouts/g474-long-pinout-full.png) | Referência completa: AF0–AF15 com número da AF, funções adicionais (ADC, COMP, OPAMP, RTC…), tolerância 5 V/3,6 V e pinos fora dos headers. |

As duas usam a numeração UFQFPN48, conferida na tabela 12 e no esquema.

SHA-256:

- `g474-long-pinout-simple.png`: `6ab8cba32311c8a2de0f75774082c784f8ea64507a4fd2f7871beb6877b6fcd6`
- `g474-long-pinout-full.png`: `200f99129058c296b4054a92a394f9b3b68d9014d79667b1fc001d92349c696d`

O texto dentro das imagens ainda mostra a revisão de origem: "v9" no rodapé da simples e "v11" no título e no rodapé da completa. Os nomes dos arquivos é que valem.

## Histórico da correção (12/09/2026)

As versões intermediárias do desenho simples (V2 a V9) tinham **13 números de pino do CI errados**: PB10, VREF+, PB11–PB15, PC6 e PA8–PA12. Esses números não seguiam o UFQFPN48 nem o LQFP48. PB11–PB15 coincidiam com o LQFP48, mas os demais não batiam com nenhum dos dois encapsulamentos.

A imagem simples atual é a V9 regerada com a lista corrigida pelo mesmo gerador. Nada mudou fora das 13 caixas de número. A completa é a antiga V11, sem alteração. As versões intermediárias (V2–V10, before-v7), o antigo `g474-long-pinout.png` (recorte do render WeAct), o gerador `scripts/make_g474_v9.py` e a receita da G474 em `scripts/prepare_pinouts.py` foram removidos a pedido do usuário. Os geradores das duas imagens atuais não estão versionados.

## Tabela de conferência

Posição contada a partir do USB-C (topo), com a placa vista de cima. A última coluna mostra, em negrito, os números errados das versões antigas.

### Header esquerdo

| Posição | Serigrafia | Sinal | UFQFPN48 (correto) | LQFP48 | Número antigo (errado) |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | G | GND | — | — | — |
| 2 | G | GND | — | — | — |
| 3 | 5V | 5V | — | — | — |
| 4 | 5V | 5V | — | — | — |
| 5 | B12 | PB12 | **25** | 26 | **26** |
| 6 | B13 | PB13 | **26** | 27 | **27** |
| 7 | B14 | PB14 | **27** | 28 | **28** |
| 8 | B15 | PB15 | **28** | 29 | **29** |
| 9 | C6 | PC6 | **29** | não existe | **30** |
| 10 | A8 | PA8 | **30** | 30 | **31** |
| 11 | A9 | PA9 | **31** | 31 | **32** |
| 12 | A10 | PA10 | **32** | 32 | **33** |
| 13 | A11 | PA11 | **33** | 33 | **34** |
| 14 | A12 | PA12 | **34** | 34 | **35** |
| 15 | A15 | PA15 | **38** | 39 | 38 |
| 16 | C10 | PC10 | **39** | não existe | 39 |
| 17 | C11 | PC11 | **40** | não existe | 40 |
| 18 | B3 | PB3 | **41** | 40 | 41 |
| 19 | B4 | PB4 | **42** | 41 | 42 |
| 20 | B5 | PB5 | **43** | 42 | 43 |
| 21 | B6 | PB6 | **44** | 43 | 44 |
| 22 | B7 | PB7 | **45** | 44 | 45 |
| 23 | B9 | PB9 | **47** | 46 | 47 |
| 24 | G | GND | — | — | — |

### Header direito

| Posição | Serigrafia | Sinal | UFQFPN48 (correto) | LQFP48 | Número antigo (errado) |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | G | GND | — | — | — |
| 2 | G | GND | — | — | — |
| 3 | 3V3 | 3V3 | — | — | — |
| 4 | 3V3 | 3V3 | — | — | — |
| 5 | B11 | PB11 | **24** | 25 | **25** |
| 6 | B10 | PB10 | **22** | 22 | **24** |
| 7 | V+ | VREF+ | **20** | 20 | **21** |
| 8 | B2 | PB2 | **19** | 18 | 19 |
| 9 | B1 | PB1 | **18** | 17 | 18 |
| 10 | B0 | PB0 | **17** | 16 | 17 |
| 11 | C4 | PC4 | **16** | não existe | 16 |
| 12 | A7 | PA7 | **15** | 15 | 15 |
| 13 | A6 | PA6 | **14** | 14 | 14 |
| 14 | A5 | PA5 | **13** | 13 | 13 |
| 15 | A4 | PA4 | **12** | 12 | 12 |
| 16 | A3 | PA3 | **11** | 11 | 11 |
| 17 | A2 | PA2 | **10** | 10 | 10 |
| 18 | A1 | PA1 | **9** | 9 | 9 |
| 19 | A0 | PA0 | **8** | 8 | 8 |
| 20 | NR | NRST | **7** | 7 | 7 |
| 21 | C13 | PC13 | **2** | 2 | 2 |
| 22 | VB | VBAT | **1** | 1 | 1 |
| 23 | 3V3 | 3V3 | — | — | — |
| 24 | G | GND | — | — | — |

Fora dos headers (UFQFPN48): PC14 = 3, PC15 = 4 (cristal 32,768 kHz), PF0 = 5, PF1 = 6 (cristal 8 MHz), VDDA = 21, VDD = 23, 35 e 48, PA13 = 36 (SWDIO), PA14 = 37 (SWCLK), PB8-BOOT0 = 46, pad térmico = 49 (VSS).

## Como a completa foi feita

Desenho vetorial (HTML/SVG renderizado com o Chrome headless). Dados:

- AF0–AF15 extraídas da tabela 13 do DS12288 pelas coordenadas das palavras (`pdftotext -bbox`);
- funções adicionais, tipo de I/O (FT/TT) e números UFQFPN48 da tabela 12, conferidos palavra a palavra;
- desenho da placa baseado em foto da unidade do usuário.

## Ao mudar uma pinagem da G474

1. Confira os números na coluna **UFQFPN48** da tabela 12 e no U1 do esquema, nunca em imagens anteriores.
2. Substitua `g474-long-pinout-simple.png` ou `-full.png` mantendo os nomes; não crie arquivos `-vN`.
3. Se mudar nomes, ordem ou títulos, atualize `pinouts` no SQLite, rode `python3 scripts/export.py` e ajuste `test_g474_pinout_versions`.
