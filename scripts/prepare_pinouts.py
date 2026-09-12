"""Render manufacturer pinout pages without redrawing electrical connections."""
import subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for name,page in [('pic16f887',8),('pic12f675',4),('pic12f683',4),('pic12f1501',3),('stm32f103c8',26)]:
 subprocess.run(['pdftoppm','-f',str(page),'-singlefile','-scale-to','2400','-png',str(R/'assets/documents'/f'{name}.pdf'),str(R/'assets/pinouts'/name)],check=True)
 print(name,page)
