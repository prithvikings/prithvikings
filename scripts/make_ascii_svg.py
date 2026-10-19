#!/usr/bin/env python3
"""Convert a prepared grayscale image to an animated monochrome ASCII SVG."""
import html,os,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent; RAMP=" .`:-=+*cs#%@"
def main():
    src=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/"source-prepped.png"; out=Path(sys.argv[2]) if len(sys.argv)>2 else ROOT/"prithvi-ascii.svg"
    if not src.exists(): raise SystemExit("Run scripts/prep_photo.py <private-photo> source-prepped.png first.")
    cols=int(os.environ.get("COLS","100")); rows=round(cols*8/15); im=Image.open(src).convert("L").resize((cols,rows),Image.Resampling.LANCZOS); px=im.load()
    cw,ch,pad,title=8.,15.,20,34; artw,arth=cols*cw,rows*ch; width,height=int(artw+pad*2),int(title+arth+50); duration=5.8/rows
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ui-monospace,Menlo,Consolas,monospace">','<rect width="100%" height="100%" rx="12" fill="#0d1117"/><rect x=".5" y=".5" width="99.8%" height="99%" rx="12" fill="none" stroke="#30363d"/>',f'<line x1="0" y1="{title}" x2="{width}" y2="{title}" stroke="#30363d"/>','<circle cx="20" cy="17" r="5" fill="#ff5f56"/><circle cx="36" cy="17" r="5" fill="#ffbd2e"/><circle cx="52" cy="17" r="5" fill="#27c93f"/>','<text x="50%" y="21" text-anchor="middle" fill="#7d8590" font-size="12">prithvikings@github:~$ ./portrait.sh</text>']
    for y in range(rows):
        chars=[]
        for x in range(cols):
            lum=(px[x,y]/255.)**1.12; idx=min(len(RAMP)-1,int((1-lum)*(len(RAMP)-1)+.5)); chars.append(RAMP[idx] if lum<.88 else " ")
        baseline=title+pad*.25+y*ch+ch*.78; delay=y*duration; line=html.escape("".join(chars))
        p.append(f'<text x="{pad}" y="{baseline:.1f}" fill="#c9d1d9" font-size="13" textLength="{artw}" lengthAdjust="spacingAndGlyphs" xml:space="preserve" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="{duration:.3f}s" fill="freeze"/>{line}</text>')
    sy=title+arth+pad*.6; p.append(f'<line x1="0" y1="{sy-16:.1f}" x2="{width}" y2="{sy-16:.1f}" stroke="#30363d"/>'); p.append(f'<text x="{pad}" y="{sy:.1f}" fill="#7d8590" font-size="12">prithvikings@github:~$ whoami <tspan fill="#c9d1d9">Prithvi Raj</tspan></text>'); p.append("</svg>")
    out.write_text("".join(p),encoding="utf-8"); print(f"Wrote {out}")
if __name__=="__main__": main()
