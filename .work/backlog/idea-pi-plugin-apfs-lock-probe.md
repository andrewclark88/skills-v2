---
id: idea-pi-plugin-apfs-lock-probe
created: 2026-08-02
updated: 2026-08-02
tags: [pi, plugins, macos, upstream]
---

`@nklisch/pi-plugins` 0.2.4 fails closed during startup on this macOS/APFS
machine with `filesystem locking capability is unknown or unsupported on this
platform`. Pi 0.83.0 and the bridge install successfully, but the extension
cannot start, so `/plugins` is unavailable.

Direct evidence: Node's `fs.promises.statfs()` reports filesystem type `26`
(`0x1a`) on the project volume, while the bridge's Darwin allowlist accepts only
`0x41504653` (APFS) and `0x48465300` (HFS+). Preserve the fail-closed locking
boundary, but investigate the correct Darwin `statfs` representation and send
the fix upstream rather than patching installed package output.
