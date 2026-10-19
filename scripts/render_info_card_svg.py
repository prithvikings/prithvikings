#!/usr/bin/env python3
"""Generate the animated developer identity card for Prithvi."""
from pathlib import Path
import html
OUT=Path(__file__).resolve().parent.parent/"info-card.svg"
ROWS=[("name","Prithvi Raj"),("role","Full Stack Developer"),("focus","AI-powered applications"),("frontend","React 19 / Next.js / TypeScript"),("backend","Node.js / Python / FastAPI"),("systems","Redis / BullMQ / Docker"),("interest","AI tooling / SaaS / DevTools")]
def main():
    p=['<svg xmlns="http://www.w3.org/2000/svg" width="840" height="880" viewBox="0 0 840 880" font-family="ui-monospace,Menlo,Consolas,monospace">','<style>@keyframes enter{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}.row{opacity:0;animation:enter .42s ease-out forwards}@media(prefers-reduced-motion:reduce){.row{opacity:1;animation:none}}</style>','<rect width="100%" height="100%" rx="12" fill="#0d1117"/><rect x=".5" y=".5" width="99.8%" height="99%" rx="12" fill="none" stroke="#30363d"/>','<line x1="0" y1="38" x2="840" y2="38" stroke="#30363d"/>','<circle cx="20" cy="19" r="5" fill="#ff5f56"/><circle cx="37" cy="19" r="5" fill="#ffbd2e"/><circle cx="54" cy="19" r="5" fill="#27c93f"/>','<text x="420" y="23" text-anchor="middle" fill="#7d8590" font-size="12">prithvikings@github:~$ neofetch</text>','<text x="28" y="82" fill="#39d353" font-size="22" font-weight="700">prithvikings</text>','<text x="28" y="112" fill="#7d8590" font-size="14">────────────────────────────────────────</text>']
    for i,(key,val) in enumerate(ROWS):
        y=166+i*76; delay=i*.12; p.extend([f'<g class="row" style="animation-delay:{delay:.2f}s">',f'<text x="30" y="{y}" fill="#39d353" font-size="17">$ {html.escape(key)}</text>',f'<text x="178" y="{y}" fill="#e6edf3" font-size="17">{html.escape(val)}</text>','</g>'])
    p.extend(['<line x1="28" y1="744" x2="812" y2="744" stroke="#30363d"/>','<text x="28" y="782" fill="#7d8590" font-size="14">status</text>','<text x="178" y="782" fill="#39d353" font-size="14">building · learning · shipping</text>','<text x="28" y="824" fill="#7d8590" font-size="12">Make useful things. Keep improving them.</text>','</svg>'])
    OUT.write_text("".join(p),encoding="utf-8"); print(f"Wrote {OUT}")
if __name__=="__main__": main()
