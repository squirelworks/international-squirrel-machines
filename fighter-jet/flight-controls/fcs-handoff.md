# FCS Hand-off — Flight Lab vs HIL vs Article (#74)

| Venue | Issue | What runs there |
|-------|-------|-----------------|
| **Flight Lab** (SquirrelSoft) | #79 / SS#168 | Aero + FCS co-check, trim/stability, mode entry/exit scripts, envelope limiter response, stores asymmetry derate |
| **HIL bench** | #80 | Inceptor→EHA latency, WOW mode switch, BIT / lane-fail injection, hardover monitor |
| **Hardware article / iron bird** | ISM | Surface rig, taxi NWS |

**Rule:** Flight Lab is source of **law behaviour** checks. HIL proves **electrical / timing ICD**. Iron bird proves **mechanical attach + loads**. Steve consumes `flight-controls.yaml` + `actuators.yaml` + `sensors.yaml` from this repo — do not fork.
