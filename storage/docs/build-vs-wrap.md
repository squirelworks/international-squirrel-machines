# Storage range — build vs wrap

| Variant | Decision | ISM-original hardware |
|---------|----------|------------------------|
| Flash cards | **Wrap** | microSD reader (this PR) |
| Thumb drives | **Wrap** | USB-MSC stick board + shell (this PR) |
| NVMe | Wrap | M.2 carrier / enclosure |
| SATA / IDE / SCSI | Wrap | Form-factor enclosure + bridge board |
| Squirrel-ROM | TBD | Options in variant design note — needs Sarah/Eric |
| Squirrel-Floppy | TBD | Emulator board vs donor drive — needs Sarah/Eric |

See research plan C2 on [#49](https://github.com/squirelworks/international-squirrel-machines/issues/49).
