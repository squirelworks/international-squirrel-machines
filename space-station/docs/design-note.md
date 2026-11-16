# Space station — design note (#42)

**Product:** ISM-SSN-1 study (modular orbital station)  
**Level:** public / educational station-architecture language (ISS-class teaching).

## Out of scope (hard limits)

- Weapons, munitions, seekers, guidance-to-target, warheads, fuzing, arming
- Combat employment, counterspace offense, or classified sensors
- Export-controlled (ITAR/EAR) station or docking-combat designs
- Nuclear propulsion plant design (power-source **class** stub only if mentioned)

---

## 1. Modules

| Module ID | Role | Study volume class | Notes |
|-----------|------|--------------------|-------|
| HAB-1 | Habitat / crew | Large pressurized | Sleep, galley stubs |
| LAB-1 | Science lab | Medium pressurized | Payload racks — civil science |
| NODE-1 | Node / berthing | Small pressurized | Docking ports |
| PWR-1 | Power module / truss attach | Unpressurized | Solar / radiator attach |
| LOG-1 | Logistics / cargo | Medium | Resupply berthing |

Arrangement is a teaching string: HAB–NODE–LAB with truss outboard. Not a classified configuration.

---

## 2. Power

| Source | Teaching class |
|--------|----------------|
| Solar arrays | Deployable wing class on truss |
| Batteries | Eclipse storage Wh class |
| Distribution | Primary HV stub → secondary 28 V / 120 V class rails |

Orbit-average teaching budget (provisional kW-class station study scaled down for ISM docs): see `eclss_budget_examples.py` and `../interfaces/station.yaml`.

---

## 3. Life support (ECLSS)

| Function | B5/station stance |
|----------|-------------------|
| Atmosphere revitalization | CO₂ removal + O₂ supply **class** stubs |
| Water recovery | Condensate / urine reclaim class — process block only |
| Thermal control | Active coolant loop + radiators |
| Fire / cabin sensors | Discrete stubs for later KiCad |
| Not in this PR | Detailed medical, food production, or classified ECLSS recipes |

Unlike submarine B3 (which excluded life-support design), **station ECLSS is in scope** at block-diagram / budget level.

---

## 4. Docking

| Port | Role | Placeholder fields |
|------|------|--------------------|
| PORT-FWD | Visiting vehicle | Capture envelope, mass limit, power/data umbilicals |
| PORT-AFT | Logistics | Same |
| PORT-RAD | Spare / rescue | Same |

Docking vehicles are **mass / berthing / power** stubs only — no weapons interfaces. See `../interfaces/docking-placeholders.yaml`.

---

## 5. Avionics

| Partition | Role |
|-----------|------|
| Station computer | Command & data handling |
| GN&C | Attitude / CMG or thruster class — station-keeping, **not** weapons pointing |
| Comms | S-band / Ka teaching class + local WLAN stub |
| Caution & warning | ECLSS / power discretes |

KiCad power / environmental / computing boards are the next roadmap step.

---

## 6. Structure study

`../shell/module_study.scad` — habitat cylinder + node stub + truss bar for packaging sketches.

## 7. Next steps
KiCad, structural design, Gerbers/STLs, BOM, polish.
