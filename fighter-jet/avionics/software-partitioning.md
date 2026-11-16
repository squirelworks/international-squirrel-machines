# Software Partitioning — ISM-FJ-1

Aligned with pure ISM development. **Platform split** (flight-critical RTOS + SquirrelBIOS vs Squirrel OS/2 ground/lab): `computing-platform.md`. Partitions below are design intent — production FCC image is out of scope for Soft apps; bay I/O bring-up lives in `../firmware/` (#84).

## Partitions
| Partition | Criticality | Host | Notes |
|-----------|-------------|------|-------|
| FCC control laws | Flight-critical | FCC lanes | No dynamic allocation from MC |
| FCC monitors / vote | Flight-critical | FCC | Cross-lane |
| MC sensor fusion | Mission | MC | May restart without flight loss |
| Stores management | Safety-related | MC + safe/arm discretes | Dual-factor release |
| Comms / data-link | Mission | MC / radio | |
| Maintenance BIT | Ground | All | Inhibited in air where required |
| Bay I/O firmware | Study / I/O | `kicad/` MCU | Maps channels; not sole flight-critical path on full article |

## Rules
1. Flight-critical code does not depend on mission apps.
2. Shared libraries are version-pinned per partition.
3. Data load cannot overwrite FCC without maintenance interlocks.
4. Contemporaries (open autopilots, etc.) are reference only — ISM laws are original.
