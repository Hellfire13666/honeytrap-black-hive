#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PYINNER'
from pathlib import Path
import sys
root = Path.home() / 'HONEYTRAP-BLACK-HIVE-v0.3.1-LIVE-WATCH-WORKSHOP'
center = root / 'BLACK-HIVE-COMMAND-CENTER.py'
icon = root / 'BLACK-HIVE-OBSIDIAN-QUEEN-ICON.png'
if not center.is_file() or not icon.is_file():
    sys.exit('[BLACK HIVE] Install the complete v0.3.1 package first; nothing changed.')
apps = Path.home() / '.local/share/applications'
entry = apps / 'honeytrap-black-hive.desktop'
wrapper = root / 'OPEN-BLACK-HIVE.sh'
if entry.exists() or wrapper.exists():
    sys.exit('[BLACK HIVE] Existing launcher preserved; nothing overwritten.')
apps.mkdir(parents=True, exist_ok=True)
wrapper.write_text(
    '#!/bin/sh\n'
    'cd "$HOME/HONEYTRAP-BLACK-HIVE-v0.3.1-LIVE-WATCH-WORKSHOP" || exit 1\n'
    'exec python3 BLACK-HIVE-COMMAND-CENTER.py menu\n',
    encoding='utf-8'
)
wrapper.chmod(0o755)
entry.write_text(
    '[Desktop Entry]\n'
    'Version=1.0\n'
    'Type=Application\n'
    'Name=BLACK HIVE // Obsidian Queen\n'
    'Comment=Defensive localhost-only command center\n'
    'Exec=' + str(wrapper) + '\n'
    'Path=' + str(root) + '\n'
    'Terminal=true\n'
    'Icon=' + str(icon) + '\n'
    'Categories=Utility;Security;\n',
    encoding='utf-8'
)
entry.chmod(0o755)
print('[BLACK HIVE] v0.3.1 application-menu launcher installed; existing projects untouched.')
PYINNER
