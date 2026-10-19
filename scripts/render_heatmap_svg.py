#!/usr/bin/env python3
"""Render the contribution JSON as a self-contained animated SVG calendar."""
import datetime as dt
import html, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DATA, OUT = ROOT/"data"/"contributions.json", ROOT/"contrib-heatmap.svg"
COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def main():
    if not DATA.exists(): raise SystemExit("Run scripts/fetch_contributions.py first.")
    data = json.loads(DATA.read_text(encoding="utf-8")); days = data.get("days", [])
    if not days: raise SystemExit("Contribution data has no days.")
    cell,gap,left,top = 11,3,24,70
    first = dt.date.fromisoformat(days[0]["date"]); weeks = {}
    for d in days:
        date=dt.date.fromisoformat(d["date"]); week=((date-first).days+first.weekday())//7
        weeks.setdefault(week,[]).append(d)
    width=left*2+max(weeks)*(cell+gap)+cell; height=178
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ui-monospace,Menlo,Consolas,monospace">',
       '<style>@keyframes reveal{from{opacity:0;transform:translateY(-5px)}to{opacity:1;transform:translateY(0)}}.day{opacity:0;animation:reveal .28s ease-out forwards}@media(prefers-reduced-motion:reduce){.day{opacity:1;animation:none}}</style>',
       '<rect width="100%" height="100%" rx="12" fill="#0d1117"/><rect x=".5" y=".5" width="99.8%" height="99%" rx="12" fill="none" stroke="#30363d"/>',
       '<text x="24" y="28" fill="#e6edf3" font-size="15" font-weight="600">prithvikings@github:~$ contributions --year</text>',
       f'<text x="24" y="48" fill="#7d8590" font-size="11">{html.escape(data["range"]["start"])} — {html.escape(data["range"]["end"])}</text>']
    for week,wdays in weeks.items():
        for d in wdays:
            date=dt.date.fromisoformat(d["date"]); x=left+week*(cell+gap); y=top+date.weekday()*(cell+gap)
            level=max(0,min(4,int(d.get("level",0)))); delay=(week*7+date.weekday())*.006
            p.append(f'<rect class="day" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{COLORS[level]}"><title>{html.escape(d["date"])}: {int(d["count"])} contributions</title></rect>')
    lx=width-160; p.append(f'<text x="{lx-36}" y="162" fill="#7d8590" font-size="10">Less</text>')
    for i,c in enumerate(COLORS): p.append(f'<rect x="{lx+i*15}" y="151" width="11" height="11" rx="2" fill="{c}"/>')
    p.append(f'<text x="{lx+75}" y="162" fill="#7d8590" font-size="10">More</text>')
    p.append(f'<text x="24" y="162" fill="#7d8590" font-size="11">{data["total_contributions"]:,} contributions · {data["active_days"]} active days</text>')
    p.append("</svg>"); OUT.write_text("".join(p),encoding="utf-8"); print(f"Wrote {OUT}")
if __name__=="__main__": main()
