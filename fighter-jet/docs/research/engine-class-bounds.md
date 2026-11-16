# Engine class bounds — ISM-FJ-1 (A2 #120)

**Scale:** full-scale class figures. **Purpose:** bound a black-box turbofan envelope for packaging and viability — not an engine design.

Every number below has a source ID (see `citations.yaml` + inline). Bands, not points.

## Public class table (2–3 engines)

| Bound | Dry thrust | Reheat thrust | Length | Inlet/max dia (class) | Dry mass | Source IDs |
|-------|------------|---------------|--------|------------------------|----------|------------|
| **EJ200-class** | ~60 kN | ~90 kN | ~4 m class | ~0.74–0.8 m class | ~1000 kg class | `ef-tecguide-2013`, `eurofighter-features`, `wiki-ej200` |
| **M88-class** | ~50 kN | ~75 kN | ~3.5–4 m class | ~0.7 m class | ~900 kg class | `wiki-m88`, `dassault-rafale-2023` |
| **F414-class** | ~58 kN | ~98 kN | ~3.9 m class | ~0.89 m class | ~1100 kg class | `wiki-f414`, `ge-f414-product` (URL live check 2026-11-16, HTTP 301) |

ISM packaging **nominal** (twin baseline): dry **60 kN**/eng, wet **90 kN**/eng, L **3.9 m**, dia **0.80 m**, mass **1050 kg** — midpoint-ish of the band, flagged `provisional: true` in `propulsion.yaml`.

## Installed thrust for gates

| Config | Dry total | Wet total | T/W @ MTOW 18500 kg (wet) |
|--------|-----------|-----------|----------------------------|
| Twin baseline | 120 kN | 180 kN | ≈ 0.99 (`G-TW-MTOW` pass band 0.75–1.20) |
| Single alternate | one ~160–180 kN-class | same order total | Similar T/W; larger single envelope (see twin-vs-single) |

Empty 9800 kg → installed T/W empty wet ≈ 1.87 (class check only).

## Access notes

- Safran M88 marketing URL returned HTTP 403 to this environment (2026-11-16); encyclopedia + Rafale public materials used for M88-class bounds.
- GE F414 product page returned HTTP 301 (followed OK). Recorded as `ge-f414-product`.
- Textbook sizing methods: Mattingly / Seddon / Raymer (DOI only; no paywalled quotes).

## Hard limits

- No engine internals (fan map, combustor, FADEC laws).
- No missile/munition propulsion.
- IR plume details deferred to A3 (textbook only).
