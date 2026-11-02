#!/usr/bin/env bash
set -euo pipefail
src="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
command -v python3 >/dev/null || { echo 'Python 3 required'; exit 1; }
(cd "$src" && python3 -m unittest discover -s tests -q)
dest="$HOME/HONEYTRAP-BLACK-HIVE-v0.3.1-LIVE-WATCH-WORKSHOP"
if [ -e "$dest" ]; then echo 'Existing v0.3.1 preserved'; exit 0; fi
mkdir -p "$dest/tests"
for f in honeytrap.py BLACK-HIVE-COMMAND-CENTER.py EVIDENCE_VAULT.py HIVE_MENU.py LIVE_SIGNAL.py LIVE_WATCH.py INSTALL.sh INSTALL-DESKTOP.sh README.md RECIPES.md BLACK-HIVE-OBSIDIAN-QUEEN-ICON.png; do
    cp "$src/$f" "$dest/"
done
cp "$src"/tests/test_*.py "$dest/tests/"
echo '[BLACK HIVE] v0.3.1 installed. Run bash INSTALL-DESKTOP.sh for a desktop menu launcher.'
