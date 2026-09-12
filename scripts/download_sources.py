"""Obtain only the explicitly listed manufacturer documents; record provenance."""
import urllib.request, urllib.parse, json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
gh='https://raw.githubusercontent.com/WeActStudio/'
sources={
'pic16f887.pdf':'https://ww1.microchip.com/downloads/en/devicedoc/41291d.pdf',
'pic12f675.pdf':'https://ww1.microchip.com/downloads/en/devicedoc/41190c.pdf',
'pic12f683.pdf':'https://ww1.microchip.com/downloads/en/devicedoc/41211d_.pdf',
'pic12f1501.pdf':'https://ww1.microchip.com/downloads/aemDocuments/documents/OTH/ProductDocuments/DataSheets/40001615C.pdf',
'atmega328p.pdf':'https://docs.arduino.cc/resources/datasheets/ATmega328P-datasheet.pdf',
'uno-pinout.pdf':'https://docs.arduino.cc/resources/pinouts/A000066-full-pinout.pdf',
'nano-pinout.pdf':'https://docs.arduino.cc/resources/pinouts/A000005-full-pinout.pdf',
'stm32f103c8.pdf':gh+'BluePill-Plus/master/Doc/STM32F103C8T6/DS5319-STM32F103x8-Datasheet.pdf',
'stm32g474.pdf':gh+'WeActStudio.STM32G474CoreBoard/master/Doc/STM32G474xE_DS12288.pdf',
'g474-long-schematic.pdf':gh+'WeActStudio.STM32G474CoreBoard/master/Hardware/QFN48/WeAct-STM32G474CoreBoard_Long/WeAct-STM32G474CoreBoard_Long_V10 SchDoc.pdf',
'g474-long-pinout.pdf':gh+'WeActStudio.STM32G474CoreBoard/master/Hardware/QFN48/WeAct-STM32G474CoreBoard_Long/WeAct-STM32G474CoreBoard_Long_V10 Board Shape 外形.pdf',
'stm32h7r3.pdf':gh+'WeActStudio.STM32H7R3Zx_CoreBoard/master/Doc/stm32h7r3z8.pdf',
'h7-schematic.pdf':gh+'WeActStudio.STM32H7R3Zx_CoreBoard/master/Hardware/WeAct-STM32H7R3Zx_CoreBoard_V10 SchDoc.pdf',
'h7-pinout.pdf':gh+'WeActStudio.STM32H7R3Zx_CoreBoard/master/Hardware/WeAct-STM32H7R3Zx_CoreBoard_V10 Board Shape 外形.pdf',
'stm32f411ce.pdf':gh+'WeActStudio.MiniSTM32F4x1/master/Datasheet/STM32F411CEU6_Datasheet.pdf',
'blackpill-pinout.pdf':gh+'WeActStudio.MiniSTM32F4x1/master/General document/STM32F4x1 v2.0+ Pin Layout.pdf',
}
manifest=[]
failures=[]
for name,url in sources.items():
 path=ROOT/'assets/documents'/name
 try:
  if not path.exists():
   payload=urllib.request.urlopen(urllib.parse.quote(url,safe=':/+'),timeout=45).read()
   if not payload.startswith(b'%PDF'): raise ValueError('Not a PDF')
   path.write_bytes(payload)
  manifest.append(dict(file=str(path.relative_to(ROOT)),url=url,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),retrieved='2026-09-12'))
  print(name,path.stat().st_size,flush=True)
 except Exception as e:
  failures.append(name)
  print('FAILED',name,str(e),flush=True)
if failures: raise SystemExit('Downloads incompletos; manifesto anterior preservado: '+', '.join(failures))
(ROOT/'data/sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
