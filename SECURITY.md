# Security and privacy

BLACK HIVE is a **localhost-first defensive research tool**, not a public-facing intrusion detection service.

- Run it only on systems you own or administer.
- Keep listeners bound to `127.0.0.1`; never expose ports via router forwarding or public tunnels without a separate review.
- Keep `LiveSignalReports/`, event records, local logs, host details, credentials, cookies, and keys out of version control.
- Do not interpret a decoy hit as proof of malicious intent or a person's identity.
- Before publishing an archive, verify the exact archive contents, including metadata and scripts.
- Security questions can be raised privately with the repository owner; do not attach sensitive data to public issues.

The tests included in the release are functional checks, not a security certification.
