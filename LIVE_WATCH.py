#!/usr/bin/env python3
"""Local-only live monitoring view for previously recorded, sanitized Black Hive events."""
import argparse
import collections
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from EVIDENCE_VAULT import read_events

PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BLACK HIVE // LIVE WATCH</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{font:15px system-ui;background:#080b10;color:#eadfb9;max-width:1100px;margin:auto;padding:26px}h1{color:#ffce50}p.muted{color:#aeb6c5}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}.stat,.panel{background:#131923;border:1px solid #564320;border-radius:12px;padding:16px;margin:12px 0}.stat b{display:block;font-size:31px;color:#ffd760}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:10px;border-bottom:1px solid #313743}th{color:#f7c545}.scroll{overflow:auto}input{background:#0e131b;color:white;border:1px solid #7e6428;padding:10px;border-radius:7px;width:100%;max-width:400px}.top{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}.signal{color:#a8edae}.error{color:#f6a8a8}.pill{border:1px solid #715c29;border-radius:20px;padding:7px 12px}footer{font-size:12px;color:#aeb6c5;margin-top:24px}
</style></head><body><div class="top"><h1>⬡ HONEYTRAP // LIVE WATCH</h1><span class="pill" id="state">Connecting…</span></div><p class="muted">PRIVATE LOCAL ACTIVITY · 2-second refresh · Demo requests are not attacks</p><div class="stats"><div class="stat">Observed events<b id="events">0</b></div><div class="stat">Routes<b id="routes">0</b></div><div class="stat">Fingerprints<b id="fingerprints">0</b></div></div><section class="panel"><h2>Decoy routes</h2><div id="paths">No events yet</div></section><section class="panel"><h2>Recent event feed</h2><input id="search" type="search" placeholder="Filter routes, methods, categories"><div class="scroll"><table><thead><tr><th>UTC time</th><th>Route</th><th>Method</th><th>Classification</th></tr></thead><tbody id="feed"></tbody></table></div></section><footer>This view reads a local sanitized events file. No raw IPs, cookies, bodies or credentials. No external libraries or uploads. Fingerprints do not establish identities.</footer><script>
const $=id=>document.getElementById(id);let latest=[];function draw(){const q=$('search').value.toLowerCase();$('feed').replaceChildren();for(const e of latest.filter(e=>[e.timestamp_utc,e.path,e.method,e.category].join(' ').toLowerCase().includes(q))){const tr=document.createElement('tr');for(const k of ['timestamp_utc','path','method','category']){let td=document.createElement('td');td.textContent=e[k]||'';tr.append(td)}$('feed').append(tr)}}$('search').oninput=draw;
async function poll(){try{const r=await fetch('/api/events',{cache:'no-store'});if(!r.ok)throw Error('HTTP '+r.status);const data=await r.json();$('events').textContent=data.total;$('routes').textContent=Object.keys(data.routes).length;$('fingerprints').textContent=data.fingerprints;$('paths').replaceChildren();for(const [path,n] of Object.entries(data.routes)){const div=document.createElement('div');div.textContent=path+' · '+n;$('paths').append(div)}latest=data.recent;draw();$('state').textContent='● LOCAL MONITOR ACTIVE';$('state').className='pill signal'}catch(e){$('state').textContent='● DISCONNECTED';$('state').className='pill error'}}poll();setInterval(poll,2000)
</script></body></html>"""

def collect(folder):
    # EVIDENCE_VAULT performs field allowlisting. Cap the browser feed.
    events=read_events(folder)
    paths=collections.Counter(e['path'] for e in events)
    return {'total':len(events),'routes':dict(paths),'fingerprints':len({e['visitor_fingerprint'] for e in events if e['visitor_fingerprint']}),'recent':list(reversed([{k:e[k] for k in ('timestamp_utc','path','method','category')} for e in events[-100:]])),'source_status':'LOCAL OBSERVED OR DEMO; NOT VERIFIED EXTERNAL ATTACKS'}

def handler_factory(folder):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args): pass
        def do_GET(self):
            if self.path=='/':data=PAGE.encode();mime='text/html; charset=utf-8';status=200
            elif self.path=='/api/events':data=json.dumps(collect(folder)).encode();mime='application/json';status=200
            else:data=b'Not Found';mime='text/plain';status=404
            self.send_response(status)
            self.send_header('Content-Type',mime)
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'")
            self.send_header('Content-Length',str(len(data)))
            self.end_headers();self.wfile.write(data)
    return Handler

def main():
    p=argparse.ArgumentParser(description='Local Black Hive live event board')
    p.add_argument('--reports',type=Path,default=Path('LiveSignalReports'))
    p.add_argument('--port',type=int,default=8767)
    args=p.parse_args()
    if not 1024<=args.port<=65535:p.error('port must be between 1024 and 65535')
    srv=ThreadingHTTPServer(('127.0.0.1',args.port),handler_factory(args.reports))
    print(f'[LIVE WATCH] Open http://127.0.0.1:{args.port}/ · localhost only',flush=True)
    try:srv.serve_forever()
    except KeyboardInterrupt:print('\n[LIVE WATCH] Stopped')
    finally:srv.server_close()
if __name__=='__main__':main()
