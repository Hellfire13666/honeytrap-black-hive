#!/usr/bin/env python3
"""Local-only orchestrator for existing Black Hive v0.3.1; no engine modifications."""
import argparse
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path.home() / 'HONEYTRAP-BLACK-HIVE-v0.3.1-LIVE-WATCH-WORKSHOP'
PORTS = {'signal':8766,'watch':8767}

def check(url):
    try:
        with urllib.request.urlopen(url, timeout=1) as r:
            return r.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False

def state():
    for name,port in PORTS.items():
        ok=check(f'http://127.0.0.1:{port}/')
        print(f'[{name.upper()}] {"ONLINE" if ok else "OFFLINE"}  http://127.0.0.1:{port}/')

def run(action):
    if not ROOT.is_dir(): raise SystemExit('v0.3.1 installation missing. Existing tools unchanged.')
    if action == 'status':
        state()
        subprocess.run([sys.executable,'LIVE_SIGNAL.py','status'],cwd=ROOT,check=False)
    elif action in ('signal','watch'):
        target={'signal':'LIVE_SIGNAL.py','watch':'LIVE_WATCH.py'}[action]
        if not (ROOT/target).is_file(): raise SystemExit(f'Missing {target}; unchanged')
        url=f'http://127.0.0.1:{PORTS[action]}/'
        if check(url):
            print(f'[BLACK HIVE] {action.upper()} ALREADY ONLINE · {url} · no duplicate started',flush=True)
            if action=='watch':
                subprocess.Popen(['xdg-open',url],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            return
        print(f'[BLACK HIVE] Starting {action} locally. Ctrl+C to stop.',flush=True)
        subprocess.run([sys.executable,'-u',target,*(['serve'] if action=='signal' else [])],cwd=ROOT,check=False)
    elif action=='vault':
        subprocess.run([sys.executable,'LIVE_SIGNAL.py','vault'],cwd=ROOT,check=True)
        report=ROOT/'LiveSignalReports'/'report.html'
        if report.exists():
            print('[BLACK HIVE] HTML vault:',report)
            subprocess.Popen(['xdg-open',str(report)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    elif action=='open':
        subprocess.Popen(['xdg-open','http://127.0.0.1:8767/'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    elif action=='menu':
        options={'1':'signal','2':'watch','3':'open','4':'status','5':'vault','0':'quit'}
        while True:
            print('\n⬡ BLACK HIVE // COMMAND CENTER · LOCAL ONLY')
            print('[1] Live Signal  [2] Live Watch  [3] Open Watch')
            print('[4] Status       [5] Evidence Vault [0] Exit')
            try: choice=input('HIVE > ').strip()
            except (KeyboardInterrupt,EOFError): print(); return
            if choice=='0':return
            if choice in options:run(options[choice])
            else:print('Choose 0–5')

def main():
    p=argparse.ArgumentParser(description='BLACK HIVE local-only command center')
    p.add_argument('action',nargs='?',default='menu',choices=['menu','signal','watch','open','status','vault'])
    run(p.parse_args().action)
if __name__=='__main__':main()
