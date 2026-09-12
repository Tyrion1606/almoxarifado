"""Restore a missing SQLite database from its reviewed, committed SQL snapshot."""
import sqlite3
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'data/inventory.sqlite'
if p.exists():
    raise SystemExit('Banco existente preservado. Para mudanças use uma migração explícita.')
with sqlite3.connect(p) as con:
    con.executescript((R/'data/inventory.sql').read_text())
    assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
print('Banco restaurado de data/inventory.sql.')
