# Twin vs single engine — packaging trade (A2 #120)

Open **product decision #1**. Baseline in-tree remains **twin**. Numbers are provisional class deltas for Flight Lab / viability — not frozen OEMs.

**Scale:** full-scale. Study OML scale factor **36.9**.

## Trade table

| Metric | Twin (baseline) | Single alternate | Δ (single − twin) | Notes / source |
|--------|-----------------|------------------|-------------------|----------------|
| Engine count | 2 | 1 | −1 | product decision |
| Thrust wet total | 180 kN | ~180 kN class | ~0 | Match G-TW-MTOW; single needs higher per-engine class |
| Propulsion dry mass | ~2100 kg | ~1400–1600 kg | **≈ −500 to −700 kg** | 2×1050 vs one F119/F414+ class; provisional |
| Aft-body width (engine bay) | ~2 × 0.80 m + splitter ≈ 2.0 m class | ~1.1–1.2 m class | **≈ −0.8 m** | packaging |
| Aft wetted area (engine bay region) | baseline A | ~0.75×A | **≈ −25% region** | Raymer conceptual; provisional |
| CG shift | CG ~FS-58 class | CG aft shift reduced / nose-heavy trend | **≈ −1 to −2 %MAC** aft mass removed | sign: single often moves CG forward vs twin aft pair; provisional |
| Asymmetric thrust after engine-out | available | none | — | safety/ops driver for twin baseline |
| Inlet count / capture | 2 × 0.36 m² | 1 × ~0.70 m² | duct packaging simpler | Seddon/Mattingly class |
| Generator offtake | 2 × 40 kVA | 1 × 60–80 kVA class | redundancy loss | buses-power |
| Removal path | twin rails FS-82–98 | single centerline rail | rail length similar | maintainability |

### Δ summary (single vs twin)

| Δmass (propulsion install) | ΔCG (%MAC) | Δwetted area (aft bay region) |
|----------------------------|------------|--------------------------------|
| **−600 kg** class (provisional) | **−1.5 %MAC** class (CG forward vs twin) | **−25%** aft bay region (provisional) |

Effects on gates:

- **G-CG:** both stay inside travel band if fuel/stores schedule adjusted; single needs forward-fuel bias check.
- **G-SM:** slight beneficial static-margin if CG moves forward; provisional until AVL.
- **G-TW-MTOW:** matched by choosing single wet class ≈ twin total.

## Recommendation (non-binding)

Keep **twin** until ops/safety review closes asymmetric-thrust and ferry-on-one requirements. Single remains an open alternate with the table above as the packaging delta.

## Citations

`ef-tecguide-2013`, `raymer-ads`, `seddon-goldsmith`, `mattingly-aed`, `wiki-ej200`, `wiki-f414`, `maintainability.md`.
