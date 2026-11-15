# Major Assembly Breakdown — ISM-FJ-1

## Top-level assemblies

```
ISM-FJ-1 Air Vehicle
├── A01 Forward Fuselage (nose → FS-42)
│   ├── Radome + sensor suite
│   ├── Nose landing gear
│   └── Cockpit module (seat, stick, HUD, canopy)
├── A02 Center Fuselage (FS-42 → FS-72)
│   ├── Avionics bay + dorsal hatch
│   ├── Wing carry-through box
│   ├── Main landing gear wells
│   └── Fuel cells / systems tunnels
├── A03 Aft Fuselage (FS-72 → FS-100)
│   ├── Inlet ducts / engines
│   ├── Empennage attachments
│   └── Nozzle / IR suppress (concept)
├── A04 Left Wing
├── A05 Right Wing
├── A06 Horizontal Stabilizer (L/R or slab)
├── A07 Vertical Stabilizer + rudder
├── A08 Landing Gear (NLG + MLG L/R)
├── A09 Propulsion (twin turbofan modules)
└── A10 Mission Systems (avionics LRUs, stores, gun opt.)
```

## Join philosophy
- **Forward ↔ center:** circumferential splice at FS-42 with titanium tension fittings and composite skin doublers; break for transport/maintenance.
- **Center ↔ aft:** FS-72 splice; engine removal aft without separating cockpit.
- **Wings:** side-of-body pins into carry-through box; detachable for depot move.
- **Empennage:** bolted spars into aft bulkheads; fin removable as unit with rudder actuators.

## Mate / break priorities
1. Wings off for hangar width.
2. Engines out aft on rails.
3. Avionics bay LRU swap through dorsal hatch (no splice break).
4. Radome swing for radar/EO access.

## Study model mapping
OpenSCAD `shell/airframe.scad` currently prints a monolithic study shell. Next shell revision should split modules A01–A07 with alignment pins matching FS/WS stations.
