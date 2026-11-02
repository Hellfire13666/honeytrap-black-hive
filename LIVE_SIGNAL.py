#!/usr/bin/env python3
"""BLACK HIVE LIVE SIGNAL: local opt-in public-demo and decoy tripwire.
No public listening by default. No identity collection or credentials.
"""
import argparse
import collections
import html
import json
import secrets
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from honeytrap import ROUTES, safe_event, save_event
from EVIDENCE_VAULT import create, read_events

DEMO_PATHS={'/demo/admin':'/admin','/demo/login':'/login','/demo/config':'/.env'}
LANDING='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Black Hive | Public Demo</title><style>body{background:#090c12;color:#f5df9b;font:17px system-ui;max-width:700px;padding:35px;margin:auto}a{color:#ffca43}section{padding:20px;border:1px solid #715b2d;border-radius:12px}small{color:#b7bcc9}</style></head><body><h1>⬡ BLACK HIVE // LIVE SIGNAL</h1><section><p>Voluntary, simulated security-tripwire demonstration. This page does not identify visitors or request credentials.</p><p><a href="/demo/admin">Try admin decoy</a> · <a href="/demo/login">Try login decoy</a> · <a href="/demo/config">Try configuration decoy</a></p><small>Clicking a demo link records a sanitized event (time, decoy path, request method). Do not submit private data. The server responds 404 to decoy requests.</small></section></body></html>'

def handler_factory(reports, minimum_interval=0.25):
    salt=secrets.token_hex(16)
    recent={}
    lock=threading.Lock()
    class Handler(BaseHTTPRequestHandler):
        server_version='BlackHiveLive/0.3'
        sys_version=''
        def log_message(self,*args): pass
        def do_GET(self): self.respond()
        def do_HEAD(self): self.respond()
        def do_POST(self): self.respond()
        def respond(self):
            path=urlsplit(self.path).path
            if path=='/' and self.command in ('GET','HEAD'):
                data=LANDING.encode()
                return self.send_payload(200,data,'text/html; charset=utf-8')
            route=DEMO_PATHS.get(path,path)
            if route not in ROUTES: route='/other'
            # No raw IP written to disk, hashed client identifier only for request throttling.
            now=time.monotonic()
            with lock:
                key=self.client_address[0]
                blocked=now-recent.get(key,-1e10)<minimum_interval
                recent[key]=now
                if len(recent)>2048: recent.clear()
            if blocked: return self.send_payload(429,b'Rate limited\n','text/plain; charset=utf-8')
            event=safe_event(route,self.command,self.client_address[0],salt)
            event['category']=('VOLUNTARY DEMO: '+event['category']) if path in DEMO_PATHS else event['category']
            save_event(reports,event)
            print('[LIVE SIGNAL] '+event['timestamp_utc']+' | '+event['path']+' | '+event['category']+' | 404',flush=True)
            self.send_payload(404,b'Decoy endpoint: Not Found\n','text/plain; charset=utf-8')
        def send_payload(self,status,data,mime):
            self.send_response(status)
            self.send_header('Content-Type',mime)
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'none'; style-src 'unsafe-inline'")
            self.send_header('Content-Length',str(len(data)))
            self.end_headers()
            if self.command!='HEAD':
                try:self.wfile.write(data)
                except (ConnectionResetError,BrokenPipeError):pass
    return Handler

def summary(reports):
    events=read_events(reports)
    counts=collections.Counter(e['path'] for e in events)
    print('[LIVE SIGNAL] Recorded events:',len(events),'| Routes:',dict(counts))
    print('[LIVE SIGNAL] Counts are observations, not unique people or verified attacks.')
    return counts

def main():
    p=argparse.ArgumentParser(description='Black Hive local demonstration + sanitized decoy event monitor')
    p.add_argument('mode',choices=['serve','status','vault'])
    p.add_argument('--port',type=int,default=8766)
    p.add_argument('--reports',type=Path,default=Path('LiveSignalReports'))
    args=p.parse_args()
    if args.mode=='status':summary(args.reports);return
    if args.mode=='vault':create(args.reports);return
    if not 1024<=args.port<=65535:p.error('port must be between 1024 and 65535')
    srv=ThreadingHTTPServer(('127.0.0.1',args.port),handler_factory(args.reports))
    srv.daemon_threads=True
    print(f'[LIVE SIGNAL] Local demo http://127.0.0.1:{args.port}/',flush=True)
    print('[LIVE SIGNAL] LOCALHOST ONLY. Public deployment requires a separate, reviewed configuration.',flush=True)
    try:srv.serve_forever(poll_interval=0.1)
    except KeyboardInterrupt:print('\n[LIVE SIGNAL] Stopped')
    finally:srv.server_close()
if __name__=='__main__':main()
