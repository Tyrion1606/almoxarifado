"""Gera as pinagens simples do Arduino Uno R3 e do Arduino Nano no estilo das folhas G474/H7R3.

Uso: python3 scripts/make_arduino_pinouts.py [uno|nano]   (sem argumento gera as duas; requer Pillow e fontes DejaVu)

Saídas: assets/pinouts/uno-pinout-simple.png e assets/pinouts/nano-pinout-simple.png.
Placa vista de cima no centro; cada furo é lido da placa para fora: nome Arduino → porta do
ATmega328P → número do pino no chip → até três funções alternativas separadas por cor.

Fontes dos dados (conferir antes de mudar; detalhes em docs/ARDUINO-PINOUT.md):
- funções alternativas e numeração QFP-32: ATmega328P, Figura 1-1 (assets/documents/atmega328p.pdf);
- ligações das placas: folhas oficiais Arduino UNO R3 A000066 (uno-pinout.pdf, p. 1, 3 e 5) e
  Nano A000005 (nano-pinout.pdf, p. 1–3);
- numeração DIP-28 do Uno: ATmega328P-PU do Uno R3 original (a figura PDIP não está no PDF local);
- limites: tabela 28.1 do datasheet (40 mA por pino, 200 mA em VCC/GND) e avisos das folhas Arduino.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = Path('/usr/share/fonts/truetype/dejavu')

# ================================================================ dados comuns

# Categoria → (fundo, texto). Mesmas cores da legenda das folhas G474/H7R3, mais INTERRUPÇÃO e PLACA.
COLORS = {
    'power': ('#ff1d1d', '#ffffff'),
    'ground': ('#101010', '#ffffff'),
    'arduino': ('#00878f', '#ffffff'),
    'gpio': ('#fff4a3', '#1a1a1a'),
    'pin': ('#2ec5e8', '#10222a'),
    'analog': ('#35e035', '#0d2a0d'),
    'timer': ('#f28b8b', '#2a0d0d'),
    'uart': ('#39b6e6', '#08202c'),
    'spi': ('#8f86e8', '#140f33'),
    'i2c': ('#c6def0', '#0f2433'),
    'int': ('#ffbd6b', '#331d00'),
    'board': ('#f3f3f3', '#1a1a1a'),
    'nc': ('#d9d9d9', '#555555'),
}


def legend(pin_label):
    return [('power', 'ALIMENTAÇÃO'), ('ground', 'GROUND'), ('arduino', 'NOME ARDUINO'), ('gpio', 'PORTA DO CHIP'),
            ('pin', pin_label), ('analog', 'ANALÓGICO'), ('timer', 'PWM / TIMER'), ('uart', 'UART'),
            ('spi', 'SPI'), ('i2c', 'I2C'), ('int', 'INTERRUPÇÃO'), ('board', 'PLACA / SISTEMA')]


def pin(arduino, silk, gpio, dip, qfp, *functions):
    return {'arduino': arduino, 'silk': silk, 'gpio': gpio, 'dip': dip, 'qfp': qfp, 'functions': list(functions)}


def wide(category, silk, label, detail='', **chip):
    """Furo sem função de I/O (alimentação, GND, NC, AREF): uma caixa larga no lugar das funções."""
    return {'wide': (category, label, detail), 'silk': silk, **chip}


def pcint(n, port):
    # PCINT existe em todo pino de I/O, mas é agrupada por porta e não serve para attachInterrupt().
    return ('int', f'PCINT{n}', f'porta {port} · sem attachInterrupt')


def int_pin(n, arduino_pin):
    return ('int', f'INT{n}', f'attachInterrupt · pino {arduino_pin}')


def analog_pin(n, dip, qfp):
    """A0–A5: porta C, ADC, digital D14–D19 e PCINT8–13; A4/A5 também são o I2C."""
    functions = [('analog', f'ADC{n}', f'analogRead(A{n}) · 10 bits')]
    if n == 4:
        functions += [('i2c', 'I2C SDA', 'mesmo sinal do pino SDA'), ('int', 'D18 · PCINT12', 'digital · sem attachInterrupt')]
    elif n == 5:
        functions += [('i2c', 'I2C SCL', 'mesmo sinal do pino SCL'), ('int', 'D19 · PCINT13', 'digital · sem attachInterrupt')]
    else:
        functions += [('board', f'DIGITAL D{14 + n}', f'pinMode(A{n}, …) funciona'), pcint(8 + n, 'C')]
    return pin(f'A{n}', f'A{n}', f'PC{n}', dip, qfp, *functions)


def digital_pins(usb_chip, qfp_only=False):
    """D2–D13 são iguais nas duas placas (mesmo ATmega328P); D0/D1 dependem do chip USB-serial."""
    d = lambda dip: None if qfp_only else dip  # noqa: E731
    return {
        'D13': pin('D13', '13', 'PB5', d(19), 17, ('spi', 'SPI SCK', 'ICSP pino 3'), ('board', 'LED L', 'LED_BUILTIN'), pcint(5, 'B')),
        'D12': pin('D12', '12', 'PB4', d(18), 16, ('spi', 'SPI MISO (CIPO)', 'ICSP pino 1'), pcint(4, 'B')),
        'D11': pin('~D11', '~11', 'PB3', d(17), 15, ('timer', 'PWM · OC2A', 'Timer2 · ~490 Hz'), ('spi', 'SPI MOSI (COPI)', 'ICSP pino 4'), pcint(3, 'B')),
        'D10': pin('~D10', '~10', 'PB2', d(16), 14, ('timer', 'PWM · OC1B', 'Timer1 · ~490 Hz'), ('spi', 'SPI SS', 'seleção do escravo'), pcint(2, 'B')),
        'D9': pin('~D9', '~9', 'PB1', d(15), 13, ('timer', 'PWM · OC1A', 'Timer1 · ~490 Hz'), pcint(1, 'B')),
        'D8': pin('D8', '8', 'PB0', d(14), 12, ('timer', 'ICP1', 'captura de entrada · Timer1'), ('board', 'CLKO', 'saída de clock (fuse CKOUT)'), pcint(0, 'B')),
        'D7': pin('D7', '7', 'PD7', d(13), 11, ('analog', 'AIN1', 'comparador analógico −'), pcint(23, 'D')),
        'D6': pin('~D6', '~6', 'PD6', d(12), 10, ('timer', 'PWM · OC0A', 'Timer0 · ~980 Hz'), ('analog', 'AIN0', 'comparador analógico +'), pcint(22, 'D')),
        'D5': pin('~D5', '~5', 'PD5', d(11), 9, ('timer', 'PWM · OC0B', 'Timer0 · ~980 Hz'), ('timer', 'T1', 'entrada de contagem Timer1'), pcint(21, 'D')),
        'D4': pin('D4', '4', 'PD4', d(6), 2, ('timer', 'T0', 'entrada de contagem Timer0'), ('uart', 'XCK', 'clock da USART síncrona'), pcint(20, 'D')),
        'D3': pin('~D3', '~3', 'PD3', d(5), 1, ('timer', 'PWM · OC2B', 'Timer2 · ~490 Hz'), int_pin(1, 3), pcint(19, 'D')),
        'D2': pin('D2', '2', 'PD2', d(4), 32, int_pin(0, 2), pcint(18, 'D')),
        'D1': pin('D1 · TX', 'TX→1', 'PD1', d(3), 31, ('uart', 'UART TXD', f'Serial · vai ao {usb_chip}'), ('board', 'USB-SERIAL', 'resistor 1 kΩ · evite com USB'), pcint(17, 'D')),
        'D0': pin('D0 · RX', 'RX←0', 'PD0', d(2), 30, ('uart', 'UART RXD', f'Serial · vem do {usb_chip}'), ('board', 'USB-SERIAL', 'resistor 1 kΩ · evite com USB'), pcint(16, 'D')),
        'RESET': pin('RESET', 'RESET', 'PC6', d(1), 29, ('board', 'RESET', 'ativo em 0 V · botão · ICSP 5'), ('board', 'AUTO-RESET', 'pelo USB ao gravar'), ('int', 'PCINT14', 'só com fuse RSTDISBL')),
    }


ICSP = [('1', 'MISO', 'D12'), ('2', '5V', ''), ('3', 'SCK', 'D13'), ('4', 'MOSI', 'D11'), ('5', 'RESET', ''), ('6', 'GND', '')]

NOTE_PWM = ('~ = saída PWM com analogWrite(): 3, 5, 6, 9, 10 e 11. D5/D6 usam o Timer0 (~980 Hz), que também conta millis() e delay(); os demais ~490 Hz. '
            'A biblioteca Servo usa o Timer1 e desliga o PWM de 9 e 10; tone() usa o Timer2 e afeta 3 e 11.')
NOTE_INTERRUPT = ('Interrupções: attachInterrupt() só funciona em D2 (INT0) e D3 (INT1), com subida, descida, mudança ou nível baixo. '
                  'PCINT existe em todos os pinos de I/O, mas dispara em qualquer mudança, tem uma única rotina por porta (B = D8–D13, C = A0–A5, D = D0–D7) '
                  'e exige os registradores PCICR/PCMSK ou uma biblioteca.')


def note_current(three_v3):
    return ('Corrente: até 20 mA por pino (recomendação Arduino); 40 mA é o máximo absoluto do ATmega328P e a soma em VCC/GND não pode passar de 200 mA. '
            f'{three_v3} Saídas têm 5 V: módulos de 3,3 V que recebem esses sinais precisam de conversor de nível.')


# ================================================================ Arduino Uno R3

UNO_PINS = digital_pins('USB (16U2)')
UNO = {
    'output': 'uno-pinout-simple.png',
    'title': 'ARDUINO UNO R3 · PINOUT SIMPLES',
    'subtitle': 'ATmega328P · 8 bits · 16 MHz · lógica 5 V · placa vista de cima, USB e jack no topo',
    'pin_label': 'PINO DIP-28 / QFP-32',
    'board_w': 640,
    'align_left': 'bottom',  # A5 na altura de D0, como na placa
    # Header digital (direita), do USB para baixo; None = espaço entre os dois conectores.
    'right': [
        pin('SCL', 'SCL', 'PC5', 28, 28, ('i2c', 'I2C SCL', 'Wire · sem pull-up na placa'), ('analog', 'ADC5', 'mesmo sinal de A5'), pcint(13, 'C')),
        pin('SDA', 'SDA', 'PC4', 27, 27, ('i2c', 'I2C SDA', 'Wire · sem pull-up na placa'), ('analog', 'ADC4', 'mesmo sinal de A4'), pcint(12, 'C')),
        wide('board', 'AREF', 'REFERÊNCIA EXTERNA DO ADC', 'analogReference(EXTERNAL) · nunca acima de 5 V', gpio='AREF', dip=21, qfp=20),
        wide('ground', 'GND', 'GROUND'),
        *[UNO_PINS[k] for k in ('D13', 'D12', 'D11', 'D10', 'D9', 'D8')],
        None,
        *[UNO_PINS[k] for k in ('D7', 'D6', 'D5', 'D4', 'D3', 'D2', 'D1', 'D0')],
    ],
    # Alimentação e analógico (esquerda).
    'left': [
        wide('nc', 'NC', 'NÃO CONECTADO', 'reservado · sem ligação na placa'),
        wide('power', 'IOREF', 'IOREF · 5 V', 'informa aos shields a tensão lógica da placa'),
        UNO_PINS['RESET'],
        wide('power', '3.3V', 'SAÍDA 3,3 V', 'regulador da placa · máximo 50 mA'),
        wide('power', '5V', 'SAÍDA 5 V', 'regulador (VIN/jack) ou USB · não alimente por aqui com USB ligado'),
        wide('ground', 'GND', 'GROUND'),
        wide('ground', 'GND', 'GROUND'),
        wide('power', 'VIN', 'ENTRADA VIN · 7–12 V', 'recomendado · limite 6–20 V · mesmo circuito do jack'),
        None,
        *[analog_pin(n, 23 + n, 23 + n) for n in range(6)],
    ],
    'notes': [
        NOTE_PWM,
        NOTE_INTERRUPT,
        note_current('O pino 3.3V fornece no máximo 50 mA.'),
        'Fora dos headers: cristal de 16 MHz em PB6/PB7 (DIP 9/10 · QFP 7/8); ADC6 e ADC7 só existem no chip QFP-32 e não chegam aos conectores. '
        'Os LEDs TX/RX piscam pelo ATmega16U2 (USB), não pelos pinos D0/D1. Pino do chip: DIP-28 no Uno R3 original (ATmega328P-PU no soquete); QFP-32 em versões SMD e clones.',
    ],
    'sources': 'Fontes: datasheet ATmega328P (Figura 1-1, tabela 28.1) e folha oficial Arduino UNO R3 A000066. Desenho da placa esquemático, fora de escala.',
}

# ================================================================ Arduino Nano

NANO_PINS = digital_pins('FT232RL/CH340', qfp_only=True)
NANO_PINS['RESET']['functions'][0] = ('board', 'RESET', 'ativo em 0 V · botão · ICSP 5')
NANO = {
    'output': 'nano-pinout-simple.png',
    'title': 'ARDUINO NANO · PINOUT SIMPLES',
    'subtitle': 'ATmega328P-AU (QFP-32) · 8 bits · 16 MHz · lógica 5 V · placa vista de cima, mini-USB no topo',
    'pin_label': 'PINO QFP-32',
    'board_w': 560,
    'align_left': 'top',
    # Header direito, do USB para baixo.
    'right': [
        *[NANO_PINS[k] for k in ('D12', 'D11', 'D10', 'D9', 'D8', 'D7', 'D6', 'D5', 'D4', 'D3', 'D2')],
        wide('ground', 'GND', 'GROUND'),
        {**NANO_PINS['RESET'], 'silk': 'RST'},
        {**NANO_PINS['D0'], 'silk': 'RX0'},
        {**NANO_PINS['D1'], 'silk': 'TX1'},
    ],
    # Header esquerdo, do USB para baixo.
    'left': [
        NANO_PINS['D13'],
        wide('power', '3V3', 'SAÍDA 3,3 V', 'do chip USB · até 50 mA no FT232RL · clones CH340: confira'),
        wide('board', 'REF', 'REFERÊNCIA EXTERNA DO ADC', 'AREF · analogReference(EXTERNAL) · até 5 V', gpio='AREF', dip=None, qfp=20),
        *[analog_pin(n, None, 23 + n) for n in range(6)],
        pin('A6', 'A6', 'ADC6', None, 19, ('analog', 'ADC6', 'analogRead(A6) · 10 bits'), ('board', 'SÓ ANALÓGICO', 'sem digital, pull-up ou PWM'), ('nc', 'SEM INTERRUPÇÃO', 'não é porta de I/O')),
        pin('A7', 'A7', 'ADC7', None, 22, ('analog', 'ADC7', 'analogRead(A7) · 10 bits'), ('board', 'SÓ ANALÓGICO', 'sem digital, pull-up ou PWM'), ('nc', 'SEM INTERRUPÇÃO', 'não é porta de I/O')),
        wide('power', '5V', '5 V', 'saída do regulador ou do USB · entrada só com 5 V regulados'),
        NANO_PINS['RESET'] | {'silk': 'RST'},
        wide('ground', 'GND', 'GROUND'),
        wide('power', 'VIN', 'ENTRADA VIN · 7–12 V', 'tensão não regulada · passa pelo regulador de 5 V da placa'),
    ],
    'notes': [
        NOTE_PWM,
        NOTE_INTERRUPT,
        note_current('O 3V3 vem do chip USB-serial: até 50 mA no FT232RL do Nano original; em clones com CH340 costuma ser bem menos.'),
        'A6 e A7 são entradas só analógicas (ADC6/ADC7): não têm porta digital, pull-up interno nem PCINT. Os dois RST são o mesmo sinal (PC6). '
        'USB-serial: FT232RL no Nano original, CH340 na maioria dos clones (pode exigir driver). Os LEDs TX/RX são acionados pelo chip USB. Cristal/ressonador de 16 MHz em PB6/PB7 (QFP 7/8).',
    ],
    'sources': 'Fontes: datasheet ATmega328P (Figura 1-1, tabela 28.1) e folha oficial Arduino Nano A000005. Desenho da placa esquemático, fora de escala.',
}

SHEETS = {'uno': UNO, 'nano': NANO}

# ================================================================ desenho

MARGIN = 60
ROW = 84          # passo entre furos
BOX_H = 72
GAP = 8
GAP_ROW = 44      # espaço entre dois conectores do mesmo lado
FUNC_W = 330
ARD_W = 150
GPIO_W = 118
PIN_W = 132
TABLE_W = ARD_W + GPIO_W + PIN_W + 3 * FUNC_W + 5 * GAP
LEAD = 40         # fio entre a placa e a primeira caixa
TOP = 390

font_cache = {}


def font(size, bold=True, condensed=False):
    name = 'DejaVuSansCondensed-Bold.ttf' if condensed else 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
    if (name, size) not in font_cache:
        font_cache[name, size] = ImageFont.truetype(str(FONTS / name), size)
    return font_cache[name, size]


def fit(draw, text, width, size, bold=True):
    """Maior fonte (normal ou condensada) em que o texto cabe na largura."""
    for s in range(size, 11, -1):
        for condensed in (False, True):
            f = font(s, bold, condensed)
            if draw.textlength(text, font=f) <= width:
                return f
    return font(12, bold, True)


def box(draw, x, y, w, category, main, detail='', h=BOX_H):
    fill, ink = COLORS[category]
    outline = '#9a9a9a' if category in ('board', 'nc', 'gpio') else None
    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=fill, outline=outline, width=2)
    if detail:
        draw.text((x + w / 2, y + h * 0.36), main, font=fit(draw, main, w - 16, 27), fill=ink, anchor='mm')
        draw.text((x + w / 2, y + h * 0.74), detail, font=fit(draw, detail, w - 14, 21, bold=False), fill=ink, anchor='mm')
    else:
        draw.text((x + w / 2, y + h / 2), main, font=fit(draw, main, w - 16, 28), fill=ink, anchor='mm')


def pin_cell(row):
    if row.get('dip'):
        return ('pin', f"DIP {row['dip']}", f"QFP {row['qfp']}", PIN_W)
    return ('pin', f"QFP {row['qfp']}", '', PIN_W)


def rows_y(rows, start):
    y, result = start, []
    for row in rows:
        if row is None:
            y += GAP_ROW
        else:
            result.append((row, y))
            y += ROW
    return result, y


def cells_for(row):
    functions_w = 3 * FUNC_W + 2 * GAP
    if 'wide' in row:
        category, label, detail = row['wide']
        if 'gpio' in row:
            return [('board', row['silk'], '', ARD_W), ('gpio', row['gpio'], '', GPIO_W), pin_cell(row), (category, label, detail, functions_w)]
        return [(category, label, detail, TABLE_W)]
    functions = row['functions'] + [None] * (3 - len(row['functions']))
    return ([('arduino', row['arduino'], '', ARD_W), ('gpio', row['gpio'], '', GPIO_W), pin_cell(row)]
            + [(f[0], f[1], f[2], FUNC_W) if f else None for f in functions])


def draw_side(draw, rows, side, board_x0, board_x1):
    for row, y in rows:
        yb, mid = y + (ROW - BOX_H) / 2, y + ROW / 2
        if side == 'right':
            x = board_x1 + LEAD
            for cell in cells_for(row):
                if cell:
                    box(draw, x, yb, cell[3], cell[0], cell[1], cell[2])
                x += (cell[3] if cell else FUNC_W) + GAP
            draw.line((board_x1 - 44, mid, board_x1 + LEAD, mid), fill='#222222', width=3)
            draw.ellipse((board_x1 - 50, mid - 6, board_x1 - 38, mid + 6), fill='#222222')
        else:
            x = board_x0 - LEAD
            for cell in cells_for(row):
                w = cell[3] if cell else FUNC_W
                if cell:
                    box(draw, x - w, yb, w, cell[0], cell[1], cell[2])
                x -= w + GAP
            draw.line((board_x0 - LEAD, mid, board_x0 + 44, mid), fill='#222222', width=3)
            draw.ellipse((board_x0 + 38, mid - 6, board_x0 + 50, mid + 6), fill='#222222')


def draw_headers(draw, x0, x1, left, right):
    """Barras pretas dos conectores, furos dourados e serigrafia branca."""
    for rows, hx, anchor, lx in [(right, x1 - 60, 'rm', x1 - 84), (left, x0 + 16, 'lm', x0 + 84)]:
        ys = [y for _, y in rows]
        start = ys[0]
        for a, b in zip(ys, ys[1:] + [None]):
            if b is None or b - a > ROW:
                draw.rectangle((hx, start + 4, hx + 44, a + ROW - 4), fill='#111111')
                start = b
        for row, y in rows:
            draw.rectangle((hx + 12, y + ROW / 2 - 10, hx + 32, y + ROW / 2 + 10), fill='#c8a44a')
            draw.text((lx, y + ROW / 2), row['silk'], font=fit(draw, row['silk'], 120, 26), fill='white', anchor=anchor)


def vertical_text(img, text, center, size, color):
    layer = Image.new('RGBA', (int(len(text) * size * 0.8) + 20, size + 20), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((layer.width / 2, layer.height / 2), text, font=font(size), fill=color, anchor='mm')
    layer = layer.rotate(90, expand=True)
    img.paste(layer, (int(center[0] - layer.width / 2), int(center[1] - layer.height / 2)), layer)


def icsp_block(draw, x, y):
    draw.rectangle((x, y, x + 130, y + 90), fill='#151515')
    for c in range(3):
        for r in range(2):
            draw.rectangle((x + 18 + c * 38, y + 16 + r * 38, x + 36 + c * 38, y + 34 + r * 38), fill='#d4af37')
    draw.text((x + 65, y + 118), 'ICSP', font=font(22), fill='white', anchor='mm')


def draw_uno(img, draw, x0, x1, first_row, last_row, left, right):
    y0, y1 = first_row - 40, last_row + 60
    teal, dark = '#00878f', '#00656b'
    draw.rounded_rectangle((x0, y0, x1, y1), radius=36, fill=teal, outline=dark, width=6)
    for cx, cy in [(x0 + 300, y0 + 95), (x0 + 180, y1 - 30), (x0 + 470, y1 - 30)]:
        draw.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill='white', outline=dark, width=4)
    # Jack (topo esquerdo) e USB-B (topo direito) ultrapassam a borda, como na placa.
    draw.rectangle((x0 + 70, y0 - 60, x0 + 250, y0 + 170), fill='#151515')
    draw.text((x0 + 160, y0 + 200), 'JACK 7–12 V', font=font(22), fill='white', anchor='mm')
    draw.rectangle((x0 + 350, y0 - 90, x0 + 510, y0 + 150), fill='#b8bec4', outline='#7d858c', width=4)
    for k in range(7):
        draw.line((x0 + 365, y0 - 70 + k * 28, x0 + 495, y0 - 70 + k * 28), fill='#8f979e', width=3)
    draw.text((x0 + 430, y0 + 180), 'USB-B', font=font(22), fill='white', anchor='mm')
    # Cristal, botão RESET e ATmega16U2 (ponte USB-serial), fora da área da serigrafia dos headers.
    draw.rounded_rectangle((x0 + 255, y0 + 250, x0 + 310, y0 + 360), radius=26, fill='#d6d6d6', outline='#8a8a8a', width=3)
    draw.text((x0 + 282, y0 + 385), '16 MHz', font=font(18), fill='white', anchor='mm')
    draw.rounded_rectangle((x0 + 340, y0 + 245, x0 + 410, y0 + 315), radius=8, fill='#d9d9d9', outline='#777', width=3)
    draw.ellipse((x0 + 358, y0 + 263, x0 + 392, y0 + 297), fill='#9a9a9a')
    draw.text((x0 + 375, y0 + 335), 'RESET', font=font(18), fill='white', anchor='mm')
    draw.rectangle((x0 + 335, y0 + 400, x0 + 425, y0 + 490), fill='#1d1d1d')
    draw.text((x0 + 380, y0 + 512), '16U2 · USB', font=font(17), fill='white', anchor='mm')
    for i, (label, color) in enumerate([('L', '#ffcc33'), ('TX', '#ffcc33'), ('RX', '#ffcc33'), ('ON', '#66ff66')]):
        ly = (y0 + 560 + i * 50) if label != 'ON' else y1 - 250
        draw.rounded_rectangle((x0 + 350, ly, x0 + 380, ly + 22), radius=4, fill=color)
        draw.text((x0 + 392, ly + 11), label, font=font(20), fill='white', anchor='lm')
    # ATmega328P DIP-28.
    cx0, cx1, cy0, cy1 = x0 + 250, x0 + 380, y0 + 700, y1 - 250
    draw.rectangle((cx0, cy0, cx1, cy1), fill='#1b1b1b')
    for k in range(14):
        py = cy0 + 24 + k * (cy1 - cy0 - 48) / 13
        draw.rectangle((cx0 - 16, py - 7, cx0, py + 7), fill='#c9c9c9')
        draw.rectangle((cx1, py - 7, cx1 + 16, py + 7), fill='#c9c9c9')
    vertical_text(img, 'ATMEGA328P', ((cx0 + cx1) / 2, (cy0 + cy1) / 2), 34, '#e8e8e8')
    icsp_block(draw, x0 + 250, y1 - 170)
    draw_headers(draw, x0, x1, left, right)
    return y1


def draw_nano(img, draw, x0, x1, first_row, last_row, left, right):
    y0, y1 = first_row - 130, last_row + 200
    cx = (x0 + x1) / 2
    teal, dark = '#00878f', '#00656b'
    draw.rounded_rectangle((x0, y0, x1, y1), radius=24, fill=teal, outline=dark, width=6)
    for hx, hy in [(x0 + 40, y0 + 40), (x1 - 40, y0 + 40), (x0 + 40, y1 - 40), (x1 - 40, y1 - 40)]:
        draw.ellipse((hx - 18, hy - 18, hx + 18, hy + 18), fill='white', outline=dark, width=4)
    # Mini-USB ultrapassa a borda superior.
    draw.rectangle((cx - 85, y0 - 60, cx + 85, y0 + 95), fill='#b8bec4', outline='#7d858c', width=4)
    for k in range(5):
        draw.line((cx - 70, y0 - 40 + k * 26, cx + 70, y0 - 40 + k * 26), fill='#8f979e', width=3)
    draw.text((cx, y0 + 118), 'MINI-USB', font=font(20), fill='white', anchor='mm')
    # ATmega328P-AU (QFP-32) girado 45°, como na placa.
    chip_y = first_row + 330
    side = 108
    chip = Image.new('RGBA', (side + 40, side + 40), (0, 0, 0, 0))
    chip_draw = ImageDraw.Draw(chip)
    for k in range(8):
        p = 20 + 12 + k * (side - 24) / 7
        chip_draw.rectangle((p - 3, 6, p + 3, 20), fill='#c9c9c9')
        chip_draw.rectangle((p - 3, side + 20, p + 3, side + 34), fill='#c9c9c9')
        chip_draw.rectangle((6, p - 3, 20, p + 3), fill='#c9c9c9')
        chip_draw.rectangle((side + 20, p - 3, side + 34, p + 3), fill='#c9c9c9')
    chip_draw.rectangle((20, 20, side + 20, side + 20), fill='#1b1b1b')
    chip = chip.rotate(45, expand=True, resample=Image.BICUBIC)
    img.paste(chip, (int(cx - chip.width / 2), int(chip_y - chip.height / 2)), chip)
    draw.text((cx, chip_y), '328P', font=font(22), fill='#e8e8e8', anchor='mm')
    draw.text((cx, chip_y + 118), 'ATMEGA328P-AU', font=font(17), fill='white', anchor='mm')
    # Ressonador de 16 MHz e botão RESET.
    draw.rounded_rectangle((cx - 34, first_row + 510, cx + 34, first_row + 548), radius=10, fill='#d6d6d6', outline='#8a8a8a', width=3)
    draw.text((cx, first_row + 570), '16 MHz', font=font(18), fill='white', anchor='mm')
    draw.rounded_rectangle((cx - 42, first_row + 640, cx + 42, first_row + 724), radius=8, fill='#d9d9d9', outline='#777', width=3)
    draw.ellipse((cx - 20, first_row + 662, cx + 20, first_row + 702), fill='#9a9a9a')
    draw.text((cx, first_row + 745), 'RESET', font=font(18), fill='white', anchor='mm')
    # LEDs.
    for i, (label, color) in enumerate([('L', '#ffcc33'), ('ON', '#66ff66'), ('TX', '#ffcc33'), ('RX', '#ffcc33')]):
        ly = first_row + 810 + i * 50
        draw.rounded_rectangle((cx - 50, ly, cx - 20, ly + 22), radius=4, fill=color)
        draw.text((cx - 8, ly + 11), label, font=font(20), fill='white', anchor='lm')
    draw.text((cx, first_row + 1040), 'USB-serial', font=font(17), fill='#d8f2f3', anchor='mm')
    draw.text((cx, first_row + 1064), 'no verso', font=font(17), fill='#d8f2f3', anchor='mm')
    icsp_block(draw, cx - 65, y1 - 185)
    draw_headers(draw, x0, x1, left, right)
    return y1


def draw_title(draw, sheet, width):
    draw.text((MARGIN, 56), sheet['title'], font=font(58), fill='#1a1a1a')
    draw.text((MARGIN, 132), sheet['subtitle'], font=font(28, bold=False), fill='#333333')
    draw.text((MARGIN, 176), 'Cada furo é lido da placa para fora: nome no Arduino → porta do chip → pino do chip → funções alternativas.',
              font=font(24, bold=False), fill='#555555')
    bx0, by0 = width - MARGIN - 900, 40
    draw.rounded_rectangle((bx0, by0, width - MARGIN, by0 + 235), radius=10, fill='#f0f0f0', outline='#9a9a9a', width=2)
    draw.text((bx0 + 24, by0 + 22), 'ICSP DO ATMEGA328P · 2×3 · GRAVAÇÃO SEM BOOTLOADER', font=font(24), fill='#1a1a1a')
    draw.text((bx0 + 24, by0 + 58), 'pino 1 marcado na serigrafia · mesmo sinal dos pinos D11–D13', font=font(19, bold=False), fill='#555')
    for i, (num, name, alias) in enumerate(ICSP):
        x, y = bx0 + 24 + (i % 2) * 430, by0 + 92 + (i // 2) * 46
        category = {'5V': 'power', 'GND': 'ground', 'RESET': 'board'}.get(name, 'spi')
        box(draw, x, y, 60, 'pin', num, h=40)
        box(draw, x + 68, y, 330, category, f'{name}{" · " + alias if alias else ""}', h=40)
    draw.line((MARGIN, 290, width - MARGIN, 290), fill='#cfcfcf', width=3)


def draw_footer(draw, sheet, y, width):
    draw.line((MARGIN, y, width - MARGIN, y), fill='#cfcfcf', width=3)
    y += 30
    draw.text((MARGIN, y + 20), 'LEGENDA', font=font(26), fill='#1a1a1a', anchor='lm')
    x = MARGIN + 150
    for category, label in legend(sheet['pin_label']):
        w = max(150, draw.textlength(label, font=font(19)) + 30)
        if x + w > width - MARGIN:
            x, y = MARGIN + 150, y + 54
        box(draw, x, y, w, category, label, h=40)
        x += w + 12
    y += 80
    body = font(23, bold=False)
    for note in sheet['notes']:
        line = ''
        for word in note.split():
            candidate = f'{line} {word}'.strip()
            if draw.textlength(candidate, font=body) > width - 2 * MARGIN:
                draw.text((MARGIN, y), line, font=body, fill='#333')
                y, line = y + 34, word
            else:
                line = candidate
        draw.text((MARGIN, y), line, font=body, fill='#333')
        y += 48
    draw.text((MARGIN, y + 6), sheet['sources'], font=font(20, bold=False), fill='#777')
    return y + 60


def render(key):
    sheet = SHEETS[key]
    width = 2 * MARGIN + 2 * (LEAD + TABLE_W) + sheet['board_w']
    img = Image.new('RGB', (width, 3200), 'white')
    draw = ImageDraw.Draw(img)
    right, right_end = rows_y(sheet['right'], TOP)
    left_height = sum(GAP_ROW if r is None else ROW for r in sheet['left'])
    left, left_end = rows_y(sheet['left'], right_end - left_height if sheet['align_left'] == 'bottom' else TOP)
    board_x0 = MARGIN + LEAD + TABLE_W
    board_x1 = board_x0 + sheet['board_w']
    bottom = max(right_end, left_end)
    board_draw = draw_uno if key == 'uno' else draw_nano
    draw_title(draw, sheet, width)
    board_y1 = board_draw(img, draw, board_x0, board_x1, TOP, bottom, left, right)
    draw.text(((board_x0 + board_x1) / 2, board_y1 + 30), 'VISTA DE CIMA', font=font(22), fill='#555555', anchor='mm')
    draw_side(draw, right, 'right', board_x0, board_x1)
    draw_side(draw, left, 'left', board_x0, board_x1)
    end = draw_footer(draw, sheet, board_y1 + 70, width)
    img = img.crop((0, 0, width, int(end)))
    output = ROOT / 'assets/pinouts' / sheet['output']
    img.save(output, optimize=True)
    print(f'{output.relative_to(ROOT)} {img.width}×{img.height}')


if __name__ == '__main__':
    for key in sys.argv[1:] or SHEETS:
        render(key)
