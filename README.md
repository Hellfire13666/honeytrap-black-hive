# 🐝 HONEYTRAP // BLACK HIVE
## OBSIDIAN QUEEN · v0.3.1

**Every hive has honey. This one has eyes.**

A defensive, **localhost-first** honeypot workshop for observing requests to decoy paths on a computer you control. BLACK HIVE brings together colorful terminal alerts, a Command Center, Live Signal monitoring, Live Watch, and an Evidence Vault.

### Included in the v0.3.1 package

- **Command Center** — menu-driven access to BLACK HIVE tools.
- **Live Signal** — local decoy-request monitoring and terminal alerts.
- **Live Watch** — local monitoring view.
- **Evidence Vault** — inspection of locally generated records.
- **Tests and recipes** — test suite and usage documentation.
- **Obsidian Queen artwork** — official crowned-bee desktop icon.

### 🔒 Privacy and scope

BLACK HIVE is intended for **defensive use on systems you own or are authorized to test**. Its local-only design uses the loopback address **`127.0.0.1`**, not a public internet listener. It is **not** a substitute for a firewall, intrusion detection service, or full security audit.

**Never publish** real event logs, local reports, credentials, browser cookies, private keys, usernames, hostnames, local absolute paths, or configuration containing personal information. Review the contents of an archive *before* distributing it. Public GitHub visibility means anyone can download files you commit.

### Download and current repository status

The v0.3.1 archive currently available in this repository is:

[`BLACK-HIVE-v0.3.1-OBSIDIAN-QUEEN-RELEASE.zip`](./BLACK-HIVE-v0.3.1-OBSIDIAN-QUEEN-RELEASE.zip)

**Important:** The ZIP was uploaded directly to the repository. Its individual source files have **not yet** been published here as browsable files, and a separate tagged GitHub Release has **not yet** been established. The ZIP's contents must be independently reviewed before it is treated as a finalized public release.

The developer's local staging run reported **22 passing tests**; that is not a GitHub CI result or an independent verification of the uploaded binary archive.

### Source layout expected for release

When the reviewed source files are published individually, the project will contain:

```text
honeytrap.py
BLACK-HIVE-COMMAND-CENTER.py
HIVE_MENU.py
LIVE_SIGNAL.py
LIVE_WATCH.py
EVIDENCE_VAULT.py
INSTALL.sh
INSTALL-DESKTOP.sh
README.md
RECIPES.md
tests/
BLACK-HIVE-OBSIDIAN-QUEEN-ICON.png
```

### From GlitchByte Phantom Labs

**BLACK HIVE // OBSIDIAN QUEEN** is a standalone project. It does not require publishing private reports or files from other Phantom Labs tools.

*Defensive monitoring. Local control. Keep the receipts private.*
