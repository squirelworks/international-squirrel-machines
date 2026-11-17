# Military sibling roadmap status (reconcile)

**Purpose:** GitHub roadmap issues for these devices still show unticked boxes even though boards / fab / BOM exist in-tree. This page is the **in-repo source of truth** until issue bodies are synced (agent token cannot `updateIssue`).

**Polish** remains open on every sibling (inquire-for-release). Soft is N/A for non-FJ siblings.

| Device | Issue | Design note | KiCad | Structural | Gerbers+STL | BOM/assembly | Polish |
|--------|-------|-------------|-------|------------|-------------|--------------|--------|
| Warship | [#43](https://github.com/squirelworks/international-squirrel-machines/issues/43) | done | done | done | done | done | open |
| Submarine | [#44](https://github.com/squirelworks/international-squirrel-machines/issues/44) | done | done | done | done | done | open |
| Aircraft carrier | [#45](https://github.com/squirelworks/international-squirrel-machines/issues/45) | done | done | done | done | done | open |
| Gundam | [#46](https://github.com/squirelworks/international-squirrel-machines/issues/46) | done | done | done | done | done | open |
| Rocket | [#41](https://github.com/squirelworks/international-squirrel-machines/issues/41) | done | done | done | done | done | open |
| Satellite | [#31](https://github.com/squirelworks/international-squirrel-machines/issues/31) | done | done | done | done | done | open |
| Space station | [#42](https://github.com/squirelworks/international-squirrel-machines/issues/42) | done | done | done | done | done | open |
| Sonar | [#40](https://github.com/squirelworks/international-squirrel-machines/issues/40) | done | done | done | done | done | open |

**Audit result (4a):** no missing design notes, structural docs, fab packages, or BOM/assembly files for the rows above. No new roadmap issues required — each device already has one. Remaining gap = **polish / inquire** (and GitHub checkbox sync).

**Fighter jet (#85 / #78):** bay Gerbers + study BOM done; Soft #79/#80 blocked on Steve; product decisions in `fighter-jet/docs/decisions.md` are **PROPOSED only**.

## Weapons boundary
Unchanged per device READMEs (mass/footprint or SAFE/INHIBIT / educational echo / civil habitat / hobby rocket / payload stubs as applicable).
