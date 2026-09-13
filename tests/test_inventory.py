"""Data, document and clone-readiness checks; run with standard Python 3."""
import unittest,sqlite3,json,hashlib,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class InventoryTests(unittest.TestCase):
 def setUp(self):
  self.db=sqlite3.connect('file:'+str(ROOT/'data/inventory.sqlite')+'?mode=ro',uri=True)
  self.data=json.loads((ROOT/'data/catalog.js').read_text().split(' = ',1)[1].removesuffix(';\n'))
 def tearDown(self): self.db.close()
 def test_integrity_and_foreign_keys(self):
  self.assertEqual(self.db.execute('PRAGMA integrity_check').fetchone()[0],'ok')
  self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(),[])
 def test_inventory_scope(self):
  parts=self.data['components'];self.assertEqual(len(parts),10);self.assertEqual(sum(p['quantity'] for p in parts),19)
  self.assertEqual(sum(p['quantity'] for p in parts if p['estimated']),10)
  self.assertEqual(len(self.data['tools']),3)
 def test_confirmed_variants(self):
  p={p['id']:p for p in self.data['components']}
  self.assertIn('STM32F411CEU6',p['blackpill']['package']);self.assertIn('8 MiB',p['blackpill']['external']);self.assertIn('25 MHz',p['blackpill']['oscillator'])
  self.assertIn('STM32G474CEU6',p['g474']['package']);self.assertEqual(p['g474']['ram'],131072)
  self.assertIn('64 KiB',p['h7r3']['flash']);self.assertEqual(p['h7r3']['dac'],'Não')
 def test_every_local_asset(self):
  for p in self.data['components']:
   for directory,key in [('assets/documents','datasheet'),('assets/pinouts','pinout'),('assets/documents','pinout_source')]:
    self.assertTrue((ROOT/directory/p[key]).is_file(),(p['id'],key))
   self.assertTrue((ROOT/'data/readers'/p['datasheet'].replace('.pdf','.js')).is_file())
   if p.get('schematic'):self.assertTrue((ROOT/'assets/documents'/p['schematic']).is_file())
   if p.get('evidence'):self.assertTrue((ROOT/p['evidence']).is_file())
 def test_source_checksums_and_readers(self):
  for source in self.data['sources']:
   path=ROOT/source['file'];blob=path.read_bytes()
   self.assertTrue(blob.startswith(b'%PDF'));self.assertEqual(hashlib.sha256(blob).hexdigest(),source['sha256'])
   reader=ROOT/'data/readers'/path.with_suffix('.js').name
   pages=json.loads(reader.read_text().split(' = ',1)[1].removesuffix(';\n'))
   self.assertTrue(pages);self.assertTrue(any(page.strip() for page in pages))
 def test_pinout_credits_and_sources(self):
  for part in self.data['components']:
   self.assertTrue(part.get('pinout_credit'),part['id'])
  for source in json.loads((ROOT/'data/pinout_sources.json').read_text()):
   blob=(ROOT/source['file']).read_bytes()
   self.assertTrue(blob.startswith(b'\x89PNG\r\n\x1a\n'),source['file'])
   self.assertEqual(hashlib.sha256(blob).hexdigest(),source['sha256'])
   self.assertTrue(source['credit'] and source['license'],source['file'])
 def test_g474_pinout_versions(self):
  # Simples e completa aparecem empilhadas, ambas com numeração UFQFPN48 (docs/G474-PINOUT.md).
  g474={p['id']:p for p in self.data['components']}['g474']
  self.assertEqual([p['file'] for p in g474['pinouts']],['g474-long-pinout-simple.png','g474-long-pinout-full.png'])
  self.assertEqual(g474['pinout'],g474['pinouts'][0]['file'])
  for p in g474['pinouts']:
   self.assertTrue((ROOT/'assets/pinouts'/p['file']).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'),p['file'])
  self.assertEqual(sorted(p.name for p in (ROOT/'assets/pinouts').glob('g474*.png')),['g474-long-pinout-full.png','g474-long-pinout-simple.png'])
 def test_h7r3_pinout_versions(self):
  # Simples e completa empilhadas; pinos do CI pela esfera UFBGA144 SMPS GP (docs/H7R3-PINOUT.md).
  h7={p['id']:p for p in self.data['components']}['h7r3']
  self.assertEqual([p['file'] for p in h7['pinouts']],['h7-pinout-simple.png','h7-pinout-full.png'])
  self.assertEqual(h7['pinout'],h7['pinouts'][0]['file'])
  for p in h7['pinouts']:
   self.assertTrue((ROOT/'assets/pinouts'/p['file']).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'),p['file'])
 def test_sql_roundtrip(self):
  restored=sqlite3.connect(':memory:');restored.executescript((ROOT/'data/inventory.sql').read_text())
  for table,key in [('components','id'),('glossary','term'),('tools','id'),('categories','id')]:
   self.assertEqual(self.db.execute(f'SELECT * FROM {table} ORDER BY {key}').fetchall(),restored.execute(f'SELECT * FROM {table} ORDER BY {key}').fetchall())
  restored.close()
 def test_deterministic_exports(self):
  subprocess.run(['python3',str(ROOT/'scripts/export.py'),'--check'],check=True,capture_output=True)
 def test_no_runtime_network_dependencies(self):
  html=(ROOT/'index.html').read_text();js=(ROOT/'assets/app.js').read_text();css=(ROOT/'assets/style.css').read_text()
  self.assertNotRegex(html,r'(?:src|href)="https?://')
  self.assertNotRegex(js,r'\b(?:fetch|XMLHttpRequest|WebSocket)\s*\(')
  self.assertNotRegex(css,r'@import|url\([\'"]?https?://')
if __name__=='__main__':unittest.main()
