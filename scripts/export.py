"""Export the committed SQLite database to a deterministic file:// readable snapshot."""
import json,sqlite3,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def export():
 con=sqlite3.connect('file:'+str(ROOT/'data/inventory.sqlite')+'?mode=ro',uri=True);con.row_factory=sqlite3.Row
 assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 components=[]
 for row in con.execute('SELECT * FROM components ORDER BY rowid'):
  item=dict(row);item.update(json.loads(item.pop('specs')));components.append(item)
 result={'schema':1,'components':components,'glossary':[dict(r) for r in con.execute('SELECT * FROM glossary ORDER BY term')],'tools':[dict(r) for r in con.execute('SELECT * FROM tools ORDER BY rowid')],'sources':json.loads((ROOT/'data/sources.json').read_text())}
 con.close()
 return 'window.CATALOG = '+json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+';\n'
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();target=ROOT/'data/catalog.js';content=export()
 con=sqlite3.connect('file:'+str(ROOT/'data/inventory.sqlite')+'?mode=ro',uri=True)
 dump='-- Gerado de inventory.sqlite; edite o banco e execute scripts/export.py.\n'+'\n'.join(con.iterdump())+'\nPRAGMA user_version=1;\n';con.close()
 sql=ROOT/'data/inventory.sql'
 if args.check:
  if not target.exists() or target.read_text()!=content or not sql.exists() or sql.read_text()!=dump: raise SystemExit('Snapshot desatualizado: execute python3 scripts/export.py')
  print('SQLite e snapshot consistentes.')
 else: target.write_text(content);sql.write_text(dump);print('Snapshot exportado para data/catalog.js.')
