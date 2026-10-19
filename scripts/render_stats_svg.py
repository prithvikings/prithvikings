#!/usr/bin/env python3
"""Render animated contribution and streak statistics from contribution JSON."""
import html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent; DATA=ROOT/"data"/"contributions.json"; OUT=ROOT/"stats.svg"
def main():
    if not DATA.exists(): raise SystemExit("Run scripts/fetch_contributions.py first.")
    d=json.loads(DATA.read_text(encoding="utf-8"))
    tiles=[("calendar contributions",f'{d["total_contributions"]:,}',"last year"),("active days",f'{d["active_days"]:,}',"days with activity"),("current streak",f'{d["current_streak"]:,} days',"consecutive days"),("longest streak",f'{d["longest_streak"]:,} days',"best run in this calendar"),("best day",f'{d["best_day"]["count"]:,}',d["best_day"]["date"]),("avg / active day",str(d["avg_per_active_day"]),"contributions")]
    w,h=860,480
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="ui-monospace,Menlo,Consolas,monospace">','<style>@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}.tile{opacity:0;animation:rise .45s ease-out forwards}@media(prefers-reduced-motion:reduce){.tile{opacity:1;animation:none}}</style>',f'<rect width="{w}" height="{h}" rx="12" fill="#0d1117"/><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="none" stroke="#30363d"/>','<line x1="0" y1="38" x2="860" y2="38" stroke="#30363d"/>','<circle cx="20" cy="19" r="5" fill="#ff5f56"/><circle cx="37" cy="19" r="5" fill="#ffbd2e"/><circle cx="54" cy="19" r="5" fill="#27c93f"/>','<text x="430" y="23" text-anchor="middle" fill="#7d8590" font-size="12">prithvikings@github:~$ ./stats.sh</text>']
    for i,(label,value,caption) in enumerate(tiles):
        col,row=i%2,i//2; x,y,delay=22+col*414,56+row*132,i*.12
        p.extend([f'<g class="tile" style="animation-delay:{delay:.2f}s">',f'<rect x="{x}" y="{y}" width="398" height="116" rx="9" fill="#161b22" stroke="#30363d"/>',f'<text x="{x+18}" y="{y+27}" fill="#7d8590" font-size="12">$ {html.escape(label)}</text>',f'<text x="{x+18}" y="{y+68}" fill="#39d353" font-size="29" font-weight="700">{html.escape(value)}</text>',f'<text x="{x+18}" y="{y+94}" fill="#7d8590" font-size="11">{html.escape(caption)}</text>','</g>'])
    p.append("</svg>"); OUT.write_text("".join(p),encoding="utf-8"); print(f"Wrote {OUT}")
if __name__=="__main__": main()
