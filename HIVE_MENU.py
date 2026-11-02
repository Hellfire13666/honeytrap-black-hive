#!/usr/bin/env python3
"""BLACK HIVE interactive launcher; localhost-only guard, offline demo, vault."""
import subprocess,sys,webbrowser
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CYAN='\033[96m'; GOLD='\033[93m'; RESET='\033[0m'
ACTIONS={'1':['demo'],'2':['guard'],'3':['vault']}
def choice(value):
    if value not in ACTIONS: raise ValueError('Unknown menu selection')
    return [sys.executable,str(ROOT/'honeytrap.py'),*ACTIONS[value]]
def report_url():
    report=ROOT/"HoneyReports"/"report.html"
    return report.resolve().as_uri() if report.is_file() else None

def main():
    while True:
        print(f'\n{GOLD}⬡ HONEYTRAP // BLACK HIVE{RESET}  |  {CYAN}LOCAL DEFENSE CONSOLE{RESET}')
        print(' [1] DEMO  • simulated events')
        print(' [2] GUARD • localhost 127.0.0.1:8765 (Ctrl+C stops)')
        print(' [3] VAULT • generate local HTML report')
        print(' [4] SETTINGS • display privacy + route configuration')
        print(' [5] OPEN VAULT • view saved HTML report')
        print(' [0] EXIT')
        try: selection=input(' HIVE > ').strip()
        except (EOFError,KeyboardInterrupt): print('\n[HIVE] Closed');return
        if selection=='0': print('[HIVE] Closed'); return
        if selection=='4':
            print(' Bind: 127.0.0.1 only | Port: 8765 | Report path: HoneyReports/')
            print(' Passwords, headers, query strings and raw IP addresses are not stored.')
        elif selection=='5':
            url=report_url()
            if url:
                if not webbrowser.open(url): print('[HIVE] Browser did not open. Report:',url)
            else: print('[HIVE] No report yet. Use [3] VAULT first.')
        elif selection in ACTIONS:
            try: subprocess.run(choice(selection),cwd=ROOT,check=False)
            except KeyboardInterrupt: print('\n[HIVE] Returning to menu')
        else: print('[HIVE] Choose 0, 1, 2, 3, 4 or 5.')
if __name__=='__main__': main()
