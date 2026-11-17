# Tooling — drawing cross-refs (ISM-FJ-1 / #106 / 4b)

Study tooling keyed to airframe drawing index. Tools are **reduced-scale mm** solids; full-scale factor **36.9** remains in `tooling.yaml` for Eric / travelers.

## Drawing map

| Drawing | Role | Tools |
|---------|------|-------|
| ISM-FJ-DWG-010 | 3-view / OML | TOOL-030, TOOL-060, TOOL-070, TOOL-080 |
| ISM-FJ-DWG-020 | Sections / frames | TOOL-040 |
| ISM-FJ-DWG-030 | Wing planform | TOOL-020 |
| ISM-FJ-DWG-050 | Stations / splices | TOOL-010, TOOL-030, TOOL-040, TOOL-060, TOOL-080 |
| ISM-FJ-DWG-060 | Wing structure | TOOL-020, TOOL-050 |

## Tool sketches (study)

Each OpenSCAD file is the controlled geometry. STL is the printable export; STEP is a **study placeholder** (repo convention — not a full B-rep CAD extract).

| Tool | Stations | Sketch notes |
|------|----------|--------------|
| TOOL-010 | FS-42, FS-72 | Circumferential splice rings on saddle |
| TOOL-020 | WS-0…10 | Spar cradles + rib posts |
| TOOL-030 | FS-88, FS-92 | VT posts + HT hinge cradles |
| TOOL-040 | FS-22/42/48 | Edge clamp + bushing row |
| TOOL-050 | WS-0…10 | Male lower-skin plank + vacuum boss |
| TOOL-060 | FS-12…28 | Male/female Al skin form pair |
| TOOL-070 | FS-18…28 | Canopy bubble mandrel |
| TOOL-080 | FS-55…75 | Inlet duct mandrel (packaging only) |

## Regenerating exports

```bash
cd fighter-jet/tooling && ./export.sh
```
