# Gundam / mobile suit — design note (#46)

**Product:** ISM-MS-1 study (humanoid mobile suit packaging)  
**Level:** public / educational mecha-architecture language.

## Out of scope (hard limits)

- Seekers, guidance-to-target, munition propulsion, warheads, fuzing, arming codes
- Live launch / fire sequences or engagement doctrine
- Export-controlled (ITAR/EAR) weapon or fire-control designs
- Classified sensor internals

Weapons interfaces in this issue roadmap mean **stores / hardpoint integration placeholders** only (same spirit as fighter-jet inert stores).

---

## 1. Actuators

| Joint group | Actuation class | Notes |
|-------------|-----------------|-------|
| Hip / knee / ankle | Servo / EHA class stubs | Load / stroke placeholders |
| Shoulder / elbow / wrist | Same | End-effector mass budget |
| Neck / waist | Lower-power stubs | Sensor mast / torso twist |

No combat “weapon arm” kinematics beyond hardpoint mass at wrist/shoulder stations. See `../interfaces/suit.yaml`.

---

## 2. Sensors

| ID | Role | Scope |
|----|------|-------|
| SEN-HEAD-OPT | Head optics / camera class | Mass / FOV keepout |
| SEN-RADAR-CHEST | Chest aperture class | Mass / footprint only |
| SEN-IMU | Suit INS stub | Power / mass |

No classified EO/IR processing or fire-control track files.

---

## 3. Power

| Source | Teaching class |
|--------|----------------|
| Primary battery / generator stub | kW-class continuous |
| Peak actuator bus | Short-duration peak |
| Distribution | 48 V / HV stub rails |

Teaching continuous load vs peak actuator budget: `balance_examples.py`.

---

## 4. Cockpit

| Element | Stub |
|---------|------|
| Canopy / hatch | Envelope |
| Seat / restraints | Mass |
| HMI | Displays + SAFE/INHIBIT stores panel (integration only) |
| Escape | Class stub — no classified ejection design |

---

## 5. Weapons interfaces → stores placeholders

| Hardpoint | Location | Allowed content |
|-----------|----------|-----------------|
| HP-R-WRIST | Right wrist | Inert mass / footprint box |
| HP-L-WRIST | Left wrist | Same |
| HP-BACK | Dorsal rack | Same |
| HP-SKIRT | Hip skirt | Same |

**SAFE / INHIBIT** truth table (integration only — no arming or fire):

| Condition | SAFE | INHIBIT release |
|-----------|------|-----------------|
| Ground maintenance | asserted | asserted |
| Walk mode | asserted | asserted |
| Stores present, no release auth | asserted | asserted |
| Release auth (sim / inert only) | deasserted* | deasserted* |

\*Simulated inert release for Flight Lab–style tooling only — **no** live munitions.

Machine-readable: `../interfaces/stores-placeholders.yaml`.

---

## 6. Structure study

`../shell/frame_study.scad` — torso capsule + limb cylinders for packaging sketches.

## 7. Next steps
KiCad control/power, limb/armor structure, Gerbers/STLs, BOM, polish.
