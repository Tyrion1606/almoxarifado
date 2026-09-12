"""Rebuild local text readers and pinout previews using Poppler, no network."""
from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[1]
for p in sorted((R/'assets/documents').glob('*.pdf')):
 text=subprocess.check_output(['pdftotext','-layout',str(p),'-']).decode('utf-8')
 pages=text.split('\f')
 if not pages[-1].strip():pages.pop()
 (R/'data/readers'/p.with_suffix('.js').name).write_text('window.DATASHEETS['+json.dumps(p.name)+'] = '+json.dumps(pages,ensure_ascii=False)+';\n')
 print(p.name,len(pages),'páginas')
for name in ['uno-pinout','nano-pinout','blackpill-pinout','g474-long-pinout','h7-pinout']:
 subprocess.run(['pdftoppm','-f','1','-singlefile','-scale-to','2400','-png',str(R/'assets/documents'/f'{name}.pdf'),str(R/'assets/pinouts'/name)],check=True)
