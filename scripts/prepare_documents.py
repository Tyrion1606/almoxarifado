"""Reconstrói o texto local dos datasheets com Poppler, sem rede. Pinagens: scripts/prepare_pinouts.py."""
from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[1]
for p in sorted((R/'assets/documents').glob('*.pdf')):
 text=subprocess.check_output(['pdftotext','-layout',str(p),'-']).decode('utf-8')
 pages=text.split('\f')
 if not pages[-1].strip():pages.pop()
 (R/'data/readers'/p.with_suffix('.js').name).write_text('window.DATASHEETS['+json.dumps(p.name)+'] = '+json.dumps(pages,ensure_ascii=False)+';\n')
 print(p.name,len(pages),'páginas')
