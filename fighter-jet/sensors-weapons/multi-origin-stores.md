# Multi-Origin Stores Compatibility — ISM-FJ-1

**Issue:** [#101](https://github.com/squirelworks/international-squirrel-machines/issues/101) · Related [#94](https://github.com/squirelworks/international-squirrel-machines/issues/94)  
**YAML for Steve:** `../interfaces/multi-origin-stores.yaml`  
**Stations:** `../interfaces/hardpoints.yaml` · prior inerts: `inert-stores.yaml`

## Hard stop
**Integration level only.** No guidance laws, seekers, propulsion/motors, warheads, fuzing, arming codes, or weapon-protocol / message-internals. Electrical layer is **connector / power / discrete / data-bus category** abstractions only.

## Mechanical interface options (per station)

### NATO lug classes (public)
| Class | Lug spacing | Typical public weight class | Cite |
|-------|-------------|-----------------------------|------|
| `nato_14in` | **14 in (355.6 mm)** | ~100–1000 lb class stores | mil-a-8591-table, mil-r-85325 |
| `nato_30in` | **30 in (762 mm)** | ~2000 lb class (and some 1000 lb) | mil-a-8591-table |

ISM study pylon lug spacing (80 mm) remains the **ISM native** attach for ISM-INERT-* stores; NATO spacing is offered via **adapter beams** on heavy pylons (STA-5…9).

### Russian-style classes (public / generic)
| Class | Role | Notes |
|-------|------|-------|
| `ru_apu_rail` | Rail launcher class (APU-* naming in open literature) | Wingtip / light outboard; no seeker detail |
| `ru_aku_ejector` | Ejector rack class (AKU-* naming in open literature) | Pylon eject; geometry abstracted |

### Chinese / Japanese family adapters
| Adapter | Role |
|---------|------|
| `cn_pylon_adapter` | Mechanical adapter from ISM pylon to CN-family lug/rail envelope (abstract) |
| `jp_pylon_adapter` | Mechanical adapter for JP-family rail/lug envelope (abstract) |

Native ISM hardware IDs from #94 (`rail_tip`, `pylon_rail_light`, `pylon_ejector_*`) remain first-class.

## Electrical / data layer (swappable)

| Layer ID | Family | Categories exposed to Flight Lab / MC |
|----------|--------|----------------------------------------|
| `elec_mil_std_1760_class` | NATO | Power rails, release discretes, multipurpose data-bus port — **no message formats** |
| `elec_adapter_ru` | RU-class | Power + discrete release/safe + serial stub categories |
| `elec_adapter_cn` | CN-class | Same abstract categories |
| `elec_adapter_jp` | JP-class | Same abstract categories |
| `elec_ism_native` | ISM | ISM-Bus stores topics (`sms-interface.yaml`) |

Adapter boxes are conceptual LRUs on the pylon/rail — pinouts freeze later; this track only names **categories**.

## Inert catalogue expansion
See YAML: adds family-tagged inerts seeded from public AIM-120 / R-73 / PL-class / JP AAM *order-of-magnitude* figures, plus existing AIM-9 / AGM-114 class models from #94. Citations in YAML.

## Compatibility matrix
`family × station × mechanical_adapter × electrical_adapter` tables in `multi-origin-stores.yaml` for Steve.

## Acceptance (#101)
- [x] Issue filed (#101)
- [x] This design note
- [x] Machine-readable YAML (catalogue + matrix)
- [x] Public citations for lug/1760-class
- [x] Hard-stop documented
