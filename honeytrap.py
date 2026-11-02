#!/usr/bin/env python3
"""HONEYTRAP Black Hive - localhost-only defensive decoy monitor."""
import argparse
import collections
import datetime as dt
import hashlib
import html
import json
import os
from pathlib import Path
import secrets
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

ROUTES = {'/admin':'ADMIN DECOY','/login':'LOGIN DECOY','/.env':'CONFIG DECOY','/api/private':'API DECOY','/wp-admin':'CMS DECOY'}
BANNER = '\033[33m⬡ HONEYTRAP // BLACK HIVE\033[0m'

def timestamp():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

def classify(path):
    return ROUTES.get(path, 'OTHER PATH')

def safe_event(path, method, client, salt):
    # No raw client IP, query string, headers, passwords, cookies or bodies retained.
    path = path if path in ROUTES else '/other'
    fingerprint = hashlib.sha256((salt + client).encode()).hexdigest()[:12]
    return {'timestamp_utc':timestamp(), 'path':path, 'method':method,
            'category':classify(path), 'visitor_fingerprint':fingerprint}

def save_event(folder, event):
    folder.mkdir(parents=True, exist_ok=True)
    file = folder/'events.jsonl'
    with file.open('a', encoding='utf-8') as out:
        out.write(json.dumps(event, separators=(',', ':'))+'\n')
    try: os.chmod(file,0o600)
    except OSError: pass

def make_handler(folder, salt):
    class Decoy(BaseHTTPRequestHandler):
        server_version = 'BlackHive/0.1'
        sys_version = ''
        def log_message(self, *args):
            pass
        def do_GET(self): self.serve()
        def do_POST(self): self.serve()
        def do_HEAD(self): self.serve()
        def do_PUT(self): self.serve()
        def serve(self):
            raw_path = urlsplit(self.path).path
            path = raw_path if raw_path in ROUTES else '/other'
            event = safe_event(path, self.command, self.client_address[0], salt)
            save_event(folder, event)
            print(f"\033[33m[{event['timestamp_utc']}]\033[0m  ◇ {event['path']:<14}  {event['category']:<15} fingerprint={event['visitor_fingerprint']}", flush=True)
            body=b'<html><title>Not Found</title><body>Not Found</body></html>'
            self.send_response(404)
            self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Cache-Control','no-store')
            self.send_header('Content-Length',str(len(body)))
            self.end_headers()
            if self.command != 'HEAD':
                try: self.wfile.write(body)
                except BrokenPipeError: pass
    return Decoy

def demo(folder):
    salt=secrets.token_hex(16)
    print(BANNER+'  [OFFLINE DEMO]')
    for route in ['/admin','/.env','/login']:
        event=safe_event(route,'GET','demo-client',salt)
        save_event(folder,event)
        print(f"[DEMO] {route} → 404 | sanitized event saved")
    print(f'[HIVE] Demo events written to {folder / "events.jsonl"}')

def report(folder):
    file=folder/'events.jsonl'
    if not file.is_file():
        print('[HIVE] No events found. Run demo or guard first.')
        return
    counts=collections.Counter()
    total=0
    with file.open(encoding='utf-8') as stream:
        for line in stream:
            try:
                item=json.loads(line)
                counts[item.get('path','/other')]+=1
                total+=1
            except (ValueError, TypeError): continue
    dest=folder/'report.html'
    rows=''.join(f'<tr><td>{html.escape(k)}</td><td>{v}</td></tr>' for k,v in counts.most_common())
    dest.write_text('<!doctype html><html><head><meta charset="utf-8"><title>Black Hive report</title><style>body{font:18px system-ui;background:#080808;color:#efc24f;padding:3em}td,th{border:1px solid #85651b;padding:10px}table{border-collapse:collapse}</style></head><body><h1>⬡ HONEYTRAP // BLACK HIVE</h1><p>Sanitized local event summary</p><p>Total: '+str(total)+'</p><table><tr><th>Decoy</th><th>Events</th></tr>'+rows+'</table></body></html>',encoding='utf-8')
    print(f'[HIVE] {total} events | HTML report: {dest}')

def main():
    p=argparse.ArgumentParser(description='Black Hive local defensive HTTP honeypot. No credential collection.')
    p.add_argument('mode',choices=['demo','guard','vault'])
    p.add_argument('--port',type=int,default=8765)
    p.add_argument('--reports',type=Path,default=Path('HoneyReports'))
    args=p.parse_args()
    if args.mode=='demo': demo(args.reports); return
    if args.mode=='vault':
        from EVIDENCE_VAULT import create
        create(args.reports)
        return
    if not 1024 <= args.port <= 65535: p.error('port must be 1024..65535')
    salt=secrets.token_hex(16)
    server=ThreadingHTTPServer(('127.0.0.1',args.port),make_handler(args.reports,salt))
    print(BANNER+'  [GUARD ACTIVE]')
    print(f'[HIVE] Listening on http://127.0.0.1:{args.port} (local computer only)')
    print('[HIVE] Press Ctrl+C to stop. No passwords/cookies/request bodies saved.')
    try: server.serve_forever(poll_interval=.1)
    except KeyboardInterrupt: print('\n[HIVE] Guard stopped')
    finally: server.server_close()

if __name__=='__main__': main()
