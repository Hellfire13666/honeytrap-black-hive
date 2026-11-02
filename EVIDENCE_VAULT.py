#!/usr/bin/env python3
"""Standalone, offline, sanitized HONEYTRAP event report builder."""
import argparse, collections, csv, datetime, html, json
from pathlib import Path

FIELDS=('timestamp_utc','path','method','category','visitor_fingerprint')
def read_events(folder):
    source=folder/'events.jsonl'
    if not source.is_file(): return []
    records=[]
    for line in source.read_text(encoding='utf-8').splitlines():
        try: e=json.loads(line)
        except (json.JSONDecodeError, TypeError): continue
        if not isinstance(e,dict): continue
        # Explicit allowlist; never propagate cookie values, raw IPs, request bodies, headers, etc.
        rec={k:str(e.get(k,''))[:160] for k in FIELDS}
        records.append(rec)
    return records

def create(folder):
    records=read_events(folder)
    folder.mkdir(parents=True,exist_ok=True)
    by_path=collections.Counter(r['path'] for r in records)
    by_category=collections.Counter(r['category'] for r in records)
    by_hour=collections.Counter(r['timestamp_utc'][:13] for r in records)
    unique=len({r['visitor_fingerprint'] for r in records if r['visitor_fingerprint']})
    summary={'event_count':len(records),'fingerprints':unique,'routes':dict(by_path),'categories':dict(by_category),'hourly':dict(sorted(by_hour.items())),'source_status':'LOCAL OBSERVED OR DEMO; NOT VERIFIED EXTERNAL ATTACKS'}
    (folder/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    with (folder/'events-sanitized.csv').open('w',encoding='utf-8',newline='') as out:
        writer=csv.DictWriter(out,fieldnames=FIELDS);writer.writeheader();writer.writerows(records)
    def esc(s): return html.escape(str(s),quote=True)
    rows=''.join('<tr>'+''.join(f'<td>{esc(r[k])}</td>' for k in FIELDS)+'</tr>' for r in reversed(records))
    pathrows=''.join(f'<tr><td>{esc(k)}</td><td>{v}</td></tr>' for k,v in by_path.most_common())
    timeline=''.join(f'<div class="bar"><span>{esc(k)} UTC</span><meter min="0" max="{max(by_hour.values(),default=1)}" value="{n}"></meter><b>{n}</b></div>' for k,n in sorted(by_hour.items()))
    page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BLACK HIVE · Evidence Vault</title><style>:root{color-scheme:dark}body{font-family:system-ui,sans-serif;background:#080b10;color:#f2e5b2;max-width:1150px;margin:auto;padding:28px}h1{color:#ffd35f}.sub{color:#b5b8c4}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}.stat,.panel{background:#131820;border:1px solid #4b3c20;border-radius:12px;padding:16px;margin:14px 0}.stat strong{display:block;font-size:28px;color:#ffcf54}input{background:#111;color:white;border:1px solid #98792e;padding:12px;border-radius:8px;width:min(95%,420px)}table{border-collapse:collapse;width:100%;font-size:13px}th,td{border-bottom:1px solid #353839;padding:10px;text-align:left;word-break:break-all}th{color:#ffd35f}.scroll{overflow:auto}.bar{display:flex;gap:14px;align-items:center;margin:8px 0}.bar span{min-width:120px}.bar meter{flex:1}a{color:#ffd35f}footer{color:#aeb1b9;font-size:12px;margin-top:20px}</style></head><body><h1>⬡ HONEYTRAP // BLACK HIVE</h1><p class="sub">EVIDENCE VAULT · OFFLINE LOCAL EVENTS · No claim of attacker identity</p>'
    page+=f'<div class="stats"><div class="stat">Events<strong>{len(records)}</strong></div><div class="stat">Routes<strong>{len(by_path)}</strong></div><div class="stat">Distinct fingerprints<strong>{unique}</strong></div></div>'
    page+='<section class="panel"><h2>Hourly activity (UTC)</h2>'+ (timeline or '<p>No events yet</p>')+'</section>'
    page+='<section class="panel"><h2>Decoy paths</h2><table><tr><th>Route</th><th>Events</th></tr>'+pathrows+'</table></section>'
    page+='<section class="panel"><h2>Event history</h2><label for="search">Filter recorded events</label><p><input id="search" type="search" placeholder="Search path, category, method or timestamp" oninput="filterRows()"></p><div class="scroll"><table id="records"><thead><tr>'+''.join(f'<th>{esc(k)}</th>' for k in FIELDS)+'</tr></thead><tbody>'+rows+'</tbody></table></div></section>'
    page+='<p><a href="events-sanitized.csv">CSV export</a> · <a href="summary.json">JSON summary</a></p><footer>Only sanitized fields from local records are displayed. Demo events may be included; repeated fingerprints are not verified identities. Offline HTML: no external scripts or uploads.</footer>'
    page+="<script>function filterRows(){const q=document.getElementById('search').value.toLowerCase();for(const tr of document.querySelectorAll('#records tbody tr'))tr.hidden=!tr.textContent.toLowerCase().includes(q)}</script></body></html>"
    (folder/'report.html').write_text(page,encoding='utf-8')
    print(f'[VAULT] {len(records)} events · {len(by_path)} routes · {unique} fingerprints')
    print(f'[VAULT] HTML: {folder/"report.html"}')
    print(f'[VAULT] CSV: {folder/"events-sanitized.csv"} | JSON: {folder/"summary.json"}')
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='HONEYTRAP offline evidence vault')
    parser.add_argument('--reports',type=Path,default=Path('HoneyReports'))
    create(parser.parse_args().reports)
