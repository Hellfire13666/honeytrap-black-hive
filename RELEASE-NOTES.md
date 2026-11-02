# BLACK HIVE // OBSIDIAN QUEEN v0.3.1

**Every hive has honey. This one has eyes.**

## Release highlights
- Local defensive decoy monitoring through Live Signal.
- Live Watch dashboard on loopback.
- Command Center and Evidence Vault.
- Purple-and-gold Obsidian Queen desktop identity.
- Corrected installation scripts in the release asset.

## Download
Use the **[v0.3.1 GitHub Release](https://github.com/Hellfire13666/honeytrap-black-hive/releases/tag/v0.3.1)** and select `BLACK-HIVE-v0.3.1-OBSIDIAN-QUEEN-INSTALLER-FIX.zip`.

## Install
Extract the ZIP, then within the extracted directory run:

```bash
bash INSTALL.sh
```

If an existing installation is present, the installer preserves it. To add a desktop menu launcher after installing:

```bash
bash INSTALL-DESKTOP.sh
```

The scripts are intended for a local Linux environment. No credentials or third-party API keys are required. Never publish locally generated monitoring reports.

## Verify
From the extracted directory:

```bash
python3 -m unittest discover -s tests -q
```

The release package's offline unit test run reported 22 passing tests. Run the tests yourself after downloading.

## Note
All example values and screenshots of monitoring events are illustrative unless explicitly accompanied by reproduced local test results.
