# Pinagem da WeAct STM32H7R3 Core Board — imagens, esferas e fileiras

Atualizado em 12/09/2026. Leia antes de alterar qualquer pinagem da H7R3.

## Regras principais

1. **O CI é BGA.** A placa usa o **STM32H7R3Z8J6**: Z = 144 pinos, J = UFBGA com passo de 0,8 mm (DS14360, cap. 8). O pino do CI é identificado pela **esfera** (letra + número, ex.: K1), não por um número sequencial.
2. **Use a coluna "UFBGA144 SMPS GP"** da tabela 19 do DS14360 Rev 3 ([stm32h7r3.pdf](../assets/documents/stm32h7r3.pdf)). A coluna vizinha "UFBGA144 SMPS GFx" é da H7R7/S7 e tem outras esferas; por exemplo, PC13 é B2 na GP e C3 na GFx. As 92 esferas do U1 no esquema WeAct conferem com a coluna GP.
3. **Os dois headers são duplos (2 × 24) e têm paridade invertida**, conforme o esquema e a serigrafia do desenho mecânico WeAct:
   - header direito (P1 + P3, lado do USB HS): fileira **externa = pinos pares**, interna = ímpares;
   - header esquerdo (P2 + P4, lado do USB FS): fileira **externa = pinos ímpares**, interna = pares.
   Nas imagens, a linha de cima de cada par é a fileira externa (borda da placa) e a de baixo é a interna.
4. **Funções filtradas para este modelo e encapsulamento.** A tabela 20 do DS14360 vale para a família H7Rxx8 inteira. Foram removidas as funções que a STM32H7R3Z8J6 não tem:
   - LTDC (`LCD_*`), ausente na linha H7R3 (tabela 2);
   - Ethernet MII: o Z8J6 só tem RMII (tabela 3); nomes como `ETH_MII_RX_DV/ETH_RMII_CRS_DV` mantêm a parte RMII;
   - Hexa-SPI (`XSPIM_*_IO8` a `IO15`), só nas versões com sufixo H.

   FMC foi mantido, mas neste encapsulamento a tabela 3 não lista NOR/PSRAM, NAND nem SDRAM (só display paralelo).

## Imagens exibidas na ficha

A aba **Pinagem** mostra sete imagens, nesta ordem (campo `pinouts`). As duas primeiras são **visões gerais da placa inteira**, mantidas a pedido do usuário; para ler os detalhes, é preciso clicar e ampliar. As outras cinco são folhas separadas **por header** para caberem legíveis no painel do app, que tem ~1.050 px numa tela de 1440 px. As folhas aparecem na largura total do painel, sem limite de altura (classe `pinout-sheet`), e o painel rola.

| Ordem | Arquivo | Conteúdo |
| ---: | --- | --- |
| 1 | [h7-pinout-simple.png](../assets/pinouts/h7-pinout-simple.png) | Visão geral simples (estilo V9), placa inteira com os dois headers (5605 × 4844 px). |
| 2 | [h7-pinout-full.png](../assets/pinouts/h7-pinout-full.png) | Visão geral completa (estilo V11), placa inteira com todas as funções em colunas (≈10,9 mil px de largura). |
| 3 | [h7-pinout-simple-left.png](../assets/pinouts/h7-pinout-simple-left.png) | Simples (estilo V9), header esquerdo P2+P4: esfera + pino do header, GPIO, até 3 funções, faixa da placa em escala com as linhas até os furos e mapa pequeno da placa. |
| 4 | [h7-pinout-simple-right.png](../assets/pinouts/h7-pinout-simple-right.png) | Idem, header direito P1+P3. |
| 5 | [h7-pinout-full-left.png](../assets/pinouts/h7-pinout-full-left.png) | Completa, header esquerdo: lista na ordem física (posição 1 = junto ao USB-C), externo/interno, todas as AF0–AF15 com número e funções adicionais, coloridas por família. |
| 6 | [h7-pinout-full-right.png](../assets/pinouts/h7-pinout-full-right.png) | Idem, header direito. |
| 7 | [h7-pinout-full-extra.png](../assets/pinouts/h7-pinout-full-extra.png) | Pinos do MCU fora dos headers, com todas as funções, e notas (recursos, SWD, alimentação, cuidados). |

Tamanhos de referência:

- simples: folha de 2.731 px de largura, funções em 37 px, que dão ~14 px na tela a 1.050 px;
- completa: folha de 3.000 px, chips em 40 px, também ~14 px na tela.

Não volte a juntar os dois headers numa imagem só: a folha ficaria larga demais e o texto, ilegível.

SHA-256:

- `h7-pinout-simple.png`: `3f55dea801d696cbfc2ae67d370585b51fcd8fd17c056e555f2f105e7681f175`
- `h7-pinout-full.png`: `39e50440c69d8e8b5956f9567f8bde6ae04fded07f7bd5c1c6c3bd6edd5cb0bf` (regerada em 13/09/2026 com as correções de extração abaixo; visual igual ao anterior)
- `h7-pinout-simple-left.png`: `e539dfee3d164c299cc5aacee88c2f9ef6ea6905b9367ceb19297a8110ca5ae2`
- `h7-pinout-simple-right.png`: `8302830fe24e0883eb9de2574599c770614c914da5bf9d5dda117b1c7c13386d`
- `h7-pinout-full-left.png`: `914ef032ffb888665b46065809b348bf339d814918f0db28835ca286a1175bb1`
- `h7-pinout-full-right.png`: `d5f67776b10cf7860ad18a1da9ae501cccc58887411a1b6080e25a66fdb51a77`
- `h7-pinout-full-extra.png`: `5ad776fa1cf18c16af5b79c5eebe2588fed925f55bad1763c6a4c7d8fe919758`

A placa é desenhada em escala a partir do desenho mecânico WeAct (38,68 × 74,2 mm; passo 2,54 mm; furos a 1,53 e 4,03 mm da borda), vista de cima com os USB-C no topo. As linhas de ligação passam entre os furos até o furo correto. O antigo `h7-pinout.png` (recorte do render WeAct, gerado por `scripts/prepare_pinouts.py`) continua no repositório, mas a ficha não o exibe.

**Correções de extração (13/09/2026):** na AF0, o nome do pino da coluna vizinha caía dentro do texto. Os nomes corretos são `JTMS-SWDIO` (PA13), `JTCK-SWCLK` (PA14), `PWR_CSTOP` (PA5) e `PWR_CSLEEP` (PA6). Um "4" de nota de rodapé grudava em `XSPIM_P1_IO0` (PP0). PH0/PH1 com `TRACED0/1` na AF15 é o que a tabela 20 traz.

## Tabela de conferência dos headers

Posição 1 = junto aos USB-C. Formato: conector-pino · **sinal** · esfera.

| Pos. | Esquerdo externo (ímpar) | Esquerdo interno (par) | Direito interno (ímpar) | Direito externo (par) |
| ---: | --- | --- | --- | --- |
| 1 | P4-7 · **GND** | P4-8 · **5V** | P3-7 · **3V3** | P3-8 · **3V3** |
| 2 | P4-5 · **GND** | P4-6 · **5V** | P3-5 · **GND** | P3-6 · **PM13** · E6 |
| 3 | P4-3 · **GND** | P4-4 · **3V3** | P3-3 · **PM14** · C7 | P3-4 · **PM9** · A8 |
| 4 | P4-1 · **GND** | P4-2 · **3V3** | P3-1 · **PM8** · B8 | P3-2 · **PM3** · B11 |
| 5 | P2-39 · **VBAT** · B1 | P2-40 · **PC13** · B2 | P1-39 · **PM2** · B10 | P1-40 · **PM1** · C10 |
| 6 | P2-37 · **PD5** · B6 | P2-38 · **PD6** · C6 | P1-37 · **PM0** · E8 | P1-38 · **PD4** · B12 |
| 7 | P2-35 · **PD7** · A5 | P2-36 · **PB3** · B5 | P1-35 · **PD3** · D10 | P1-36 · **PD2** · C11 |
| 8 | P2-33 · **PB4** · C5 | P2-34 · **PB5** · A4 | P1-33 · **PC12** · C12 | P1-34 · **PC11** · E9 |
| 9 | P2-31 · **PB6** · A3 | P2-32 · **PB7** · D4 | P1-31 · **PC10** · D11 | P1-32 · **PA15** · D12 |
| 10 | P2-29 · **PB8** · A2 | P2-30 · **PB9** · C3 | P1-29 · **PA12** · E11 | P1-30 · **PA11** · F12 |
| 11 | P2-27 · **PE0** · B4 | P2-28 · **PE1** · B3 | P1-27 · **PA10** · F11 | P1-28 · **PA9** · G12 |
| 12 | P2-25 · **PE2** · C4 | P2-26 · **PE3** · D3 | P1-25 · **PA8** · F10 | P1-26 · **PC7** · G9 |
| 13 | P2-23 · **PE4** · E3 | P2-24 · **PE5** · D1 | P1-23 · **PC8** · G11 | P1-24 · **PC9** · G10 |
| 14 | P2-21 · **PE6** · E2 | P2-22 · **NRST** · F4 | P1-21 · **PB15** · J12 | P1-22 · **PC6** · H12 |
| 15 | P2-19 · **PC1** · G5 | P2-20 · **PC0** · G3 | P1-19 · **PB14** · H9 | P1-20 · **PB13** · J11 |
| 16 | P2-17 · **VREF+** · K3 | P2-18 · **PC2** · J1 | P1-17 · **PB11** · K12 | P1-18 · **PB12** · H10 |
| 17 | P2-15 · **PC3** · H2 | P2-16 · **PA0** · K1 | P1-15 · **PB10** · J10 | P1-16 · **PD14** · H11 |
| 18 | P2-13 · **PA1** · J2 | P2-14 · **PA2** · L1 | P1-13 · **PD13** · L12 | P1-14 · **PD12** · K11 |
| 19 | P2-11 · **PA3** · K2 | P2-12 · **PA4** · L2 | P1-11 · **PD11** · L11 | P1-12 · **PD10** · M11 |
| 20 | P2-9 · **PA5** · J4 | P2-10 · **PA6** · M2 | P1-9 · **PD8** · J8 | P1-10 · **PP7** · M10 |
| 21 | P2-7 · **PA7** · K4 | P2-8 · **PC4** · L3 | P1-7 · **PP6** · M9 | P1-8 · **PP5** · M8 |
| 22 | P2-5 · **PC5** · M3 | P2-6 · **PB0** · L4 | P1-5 · **PP4** · M5 | P1-6 · **PO5** · L7 |
| 23 | P2-3 · **PB1** · M4 | P2-4 · **PB2** · L5 | P1-3 · **PO2** · L9 | P1-4 · **PO1** · J6 |
| 24 | P2-1 · **GND** | P2-2 · **GND** | P1-1 · **GND** | P1-2 · **GND** |

Observações:

- **5V** é o VCC da placa (entrada de 3,3–6 V, alimentada pelos USB por diodos Schottky).
- **VREF** é o VREF+ (K3), ligado ao VDDA pelo S1 (47 Ω). **VB** é o VBAT (B1), com BAT54C para o 3V3.
- PM0–PM3 aparecem no DS14360 com o código de I/O "TF_uc"/"TF_ud", reproduzido sem interpretação.

## Pinos do MCU fora dos headers

| Sinal | Esfera | Uso na placa |
| --- | --- | --- |
| PA13 | E12 | SWD · DIO |
| PA14 | E10 | SWD · CLK |
| PC14 | C1 | cristal 32,768 kHz |
| PC15 | C2 | cristal 32,768 kHz |
| PH0 | G2 | cristal 24 MHz |
| PH1 | H1 | cristal 24 MHz |
| PM5 | B9 | USB HS · D− |
| PM6 | A9 | USB HS · D+ |
| PM11 | A7 | USB FS · D+ |
| PM12 | B7 | USB FS · D− |
| PO0 | J7 | flash QSPI · CS |
| PO4 | M7 | flash QSPI · CLK |
| PP0 | L8 | flash QSPI · IO0 |
| PP1 | L10 | flash QSPI · IO1 |
| PP2 | L6 | flash QSPI · IO2 |
| PP3 | M6 | flash QSPI · IO3 |
| BOOT0 | A6 | botão BOOT0 |

## Recursos da placa ligados a pinos dos headers

- microSD: PC8 (D0), PC9 (D1), PC10 (D2), PC11 (D3/CD), PC12 (CLK) e PD2 (CMD), com pull-up de 47 kΩ; detecção do cartão em PA8.
- LED azul em PB2; botão KEY em PC13 (liga ao 3V3 por 330 Ω).

## Como as imagens foram feitas

Os dados vieram das tabelas do DS14360, extraídas pelas coordenadas das palavras (`pdftotext -bbox`):

- tabela 20: AF0–AF15;
- tabela 19: esferas UFBGA144 SMPS GP, I/O e funções adicionais;
- tabelas 2 e 3: recursos da STM32H7R3Z8J6.

Mapeamento dos headers:

- rótulos dos conectores P1–P4 no esquema (página 1);
- paridade das fileiras pela serigrafia do desenho mecânico, confirmada no render WeAct.

Renderização: HTML/SVG no Chrome headless. O gerador não está versionado.

## Ao mudar uma pinagem da H7R3

1. Pino do CI = esfera da coluna **UFBGA144 SMPS GP**, conferida no U1 do esquema.
2. Respeite a paridade: externa = par no header direito (P1/P3) e ímpar no esquerdo (P2/P4).
3. Substitua as visões gerais `h7-pinout-simple.png`/`h7-pinout-full.png` e as folhas `h7-pinout-simple-left/right.png` e `h7-pinout-full-left/right/extra.png` mantendo os nomes; o teste exige exatamente esses arquivos `h7-pinout-*.png`. Se mudar nomes, ordem ou títulos, atualize `pinouts` no SQLite, rode `python3 scripts/export.py` e ajuste `test_h7r3_pinout_versions`.
