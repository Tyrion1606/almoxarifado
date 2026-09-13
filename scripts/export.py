"""Gera data/catalog.js (lido pela página via file://) e data/inventory.sql a partir do SQLite.

Uso: python3 scripts/export.py [--check]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import db  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='só confere; falha se algum snapshot estiver desatualizado')
    args = parser.parse_args()
    con = db.connect(db.DATABASE, readonly=True)
    files = db.snapshots(con)
    con.close()
    if args.check:
        if any(not path.exists() or path.read_text() != content for path, content in files.items()):
            raise SystemExit('Snapshot desatualizado: execute python3 scripts/export.py')
        print('SQLite e snapshots consistentes.')
        return
    for path, content in files.items():
        path.write_text(content)
    print('Snapshots exportados para data/catalog.js e data/inventory.sql.')


if __name__ == '__main__':
    main()
