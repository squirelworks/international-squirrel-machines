# Materials Program — ISM-FJ-1

Metallurgy and composite usage for primary structure, skins, spars/ribs, fasteners, and environmental protection. All callouts are ISM design choices for a fictional product line — not copies of any nation’s alloy specs sheets beyond generic public alloy families used as reference.

| Doc | Content |
|-----|---------|
| `trade-study.md` | Criteria matrix + zone recommendations (#92) |
| `candidates.yaml` | Scored candidate families (machine-readable) |
| `structure.md` | Where each material is used and why |
| `metallurgy-composites.md` | Alloy/composite families, thermal & corrosion notes, fasteners |

**Zone map for Steve / Flight Lab:** `../interfaces/materials-zones.yaml`

## Default materials philosophy
- **Weight-critical skins & covers:** carbon-fiber epoxy (ISM-CFRP-A)
- **Highly loaded fittings / landing gear / hook:** titanium alloy family (ISM-Ti-6); HS steel cost alternate
- **Carry-through & spar caps (baseline):** 7xxx aluminum (ISM-Al-7xxx) or Al-Li with CFRP webs/skins
- **Engine bay / hot structure:** nickel alloy / titanium; thermal barriers
- **Radome:** quartz/epoxy (ISM-RF-Q)

Product decision still open: **all-composite wing box vs hybrid Al-Li/7xxx + CFRP skins**. Baseline docs assume hybrid.
