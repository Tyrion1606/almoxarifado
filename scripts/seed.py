"""Restaura um banco ausente a partir do SQL versionado (data/inventory.sql)."""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import db  # noqa: E402

if db.DATABASE.exists():
    raise SystemExit('Banco existente preservado. Para mudanças use uma migração explícita (scripts/migrate.py).')
with sqlite3.connect(db.DATABASE) as con:
    con.executescript((db.DATA / 'inventory.sql').read_text())
    assert con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
print('Banco restaurado de data/inventory.sql.')
