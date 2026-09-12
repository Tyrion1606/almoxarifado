"""Recorta pinagens a partir de páginas e imagens oficiais, sem redesenhar ligações."""
import hashlib,subprocess,tempfile
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'assets/documents'
OUT=ROOT/'assets/pinouts'
SRC=OUT/'sources'
PAD=28
GAP=40
INK=245

# (arquivo, página física do PDF, faixa mantida antes de aparar as margens:
# topo e base, opcionalmente esquerda e direita, em fração da página).
# A faixa descarta cabeçalho, rodapé e encapsulamentos que não estão no acervo.
PAGES={
 'pic16f887':[('pic16f887.pdf',8,(0.075,0.55)),('pic16f887.pdf',9,(0.075,0.82))],
 'pic12f675':[('pic12f675.pdf',4,(0.28,0.42,0.12,0.85)),('pic12f675.pdf',8,(0.075,0.80))],
 'pic12f683':[('pic12f683.pdf',4,(0.075,0.272)),('pic12f683.pdf',4,(0.635,0.885))],
 'pic12f1501':[('pic12f1501.pdf',3,(0.075,0.345)),('pic12f1501.pdf',4,(0.075,0.72))],
 'uno-pinout':[('uno-pinout.pdf',1,(0.0,1.0))],
 'nano-pinout':[('nano-pinout.pdf',1,(0.0,1.0))],
}
# Página inteira, gravada como o Poppler entrega: a pinagem da BlackPill já é a melhor do acervo.
WHOLE={'blackpill-pinout':('blackpill-pinout.pdf',1)}
# Imagens já prontas: (arquivo em sources, região de busca da placa, ampliação).
IMAGES={
 'bluepill-pinout':('bluepill-generic-f103.png',None,1),
 'g474-long-pinout':('weact-g474-long-board.png',(0.415,0.0,1.0,1.0),2),
 'h7-pinout':('weact-h7r3-board.png',(0.405,0.0,1.0,1.0),2),
}

def render(pdf,page,tmp):
 base=tmp/f'{pdf.stem}-{page}'
 subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','2400','-png',str(pdf),str(base)],check=True)
 return Image.open(base.with_suffix('.png')).convert('RGB')

def trim(im,threshold=INK,pad=PAD):
 box=im.convert('L').point(lambda v:255 if v<threshold else 0).getbbox()
 if not box: return im
 l,t,r,b=box
 return im.crop((max(0,l-pad),max(0,t-pad),min(im.width,r+pad),min(im.height,b+pad)))

def collapse(im,keep=GAP):
 """Encurta faixas horizontais totalmente vazias, sem deslocar nada na horizontal."""
 rows=im.convert('L').point(lambda v:255 if v<INK else 0).tobytes()
 blank=[not any(rows[y*im.width:(y+1)*im.width]) for y in range(im.height)]
 bands,start=[],0
 while start<im.height:
  end=start
  while end<im.height and blank[end]==blank[start]: end+=1
  bands.append((start,min(end,start+keep) if blank[start] else end));start=end
 kept=[im.crop((0,a,im.width,b)) for a,b in bands if b>a]
 sheet=Image.new('RGB',(im.width,sum(p.height for p in kept)),'white')
 y=0
 for part in kept: sheet.paste(part,(0,y));y+=part.height
 return sheet

def stack(parts):
 width=max(p.width for p in parts)
 sheet=Image.new('RGB',(width,sum(p.height for p in parts)+GAP*(len(parts)-1)),'white')
 y=0
 for part in parts:
  sheet.paste(part,((width-part.width)//2,y));y+=part.height+GAP
 return sheet

def from_pages(recipe,tmp):
 parts=[]
 for name,page,band in recipe:
  im=render(DOCS/name,page,tmp)
  top,bottom,left,right=band if len(band)==4 else band+(0.0,1.0)
  window=im.crop((int(im.width*left),int(im.height*top),int(im.width*right),int(im.height*bottom)))
  parts.append(collapse(trim(window)))
 return stack(parts)

def from_image(name,region,scale):
 im=Image.open(SRC/name).convert('RGB')
 if region:
  im=im.crop((int(im.width*region[0]),int(im.height*region[1]),int(im.width*region[2]),int(im.height*region[3])))
  im=trim(im,threshold=120,pad=14)
 return im.resize((im.width*scale,im.height*scale),Image.LANCZOS) if scale>1 else im

if __name__=='__main__':
 for stem,(name,page) in WHOLE.items():
  subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','2400','-png',str(DOCS/name),str(OUT/stem)],check=True)
 with tempfile.TemporaryDirectory() as raw:
  tmp=Path(raw)
  for stem,recipe in PAGES.items(): from_pages(recipe,tmp).save(OUT/f'{stem}.png',optimize=True)
 for stem,(name,region,scale) in IMAGES.items(): from_image(name,region,scale).save(OUT/f'{stem}.png',optimize=True)
 for path in sorted(OUT.glob('*.png')):
  with Image.open(path) as im: size=im.size
  print(path.name,size,path.stat().st_size,hashlib.sha256(path.read_bytes()).hexdigest()[:12])
