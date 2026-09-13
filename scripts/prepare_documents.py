"""Reconstrói o texto local dos datasheets com Poppler, sem rede. Pinagens: scripts/prepare_pinouts.py."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for pdf in sorted((ROOT / 'assets/documents').glob('*.pdf')):
    text = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-']).decode('utf-8')
    pages = text.split('\f')
    if not pages[-1].strip():
        pages.pop()
    reader = ROOT / 'data/readers' / pdf.with_suffix('.js').name
    reader.write_text('window.DATASHEETS[' + json.dumps(pdf.name) + '] = ' + json.dumps(pages, ensure_ascii=False) + ';\n')
    print(pdf.name, len(pages), 'páginas')
