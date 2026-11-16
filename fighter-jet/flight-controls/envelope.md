# Flight Envelope Protections — ISM-FJ-1 (#74)

Numeric limits in `../interfaces/flight-controls.yaml` → `envelope` (provisional; refine with aero DB / #103 / #78).

## Protections (baseline set)
| Protection | Intent | Provisional limit |
|------------|--------|-------------------|
| AOA | Departure / deep stall; cue + hard | soft 22° / hard 28° |
| Nz | Structural & crew | −3 … +9 g |
| Roll / yaw rate | Structural & PIO margin | 220 °/s roll; 40 °/s yaw |
| Airspeed / Mach | Overspeed warn → hard | 650/700 KEAS; M 1.6/1.8 |
| Gear / flap placard | Inhibit unsafe configs | gear ≤250 KEAS; flap ≤230 KEAS |
| High AOA yaw | Rudder authority vs sideslip | law-managed |

## Sensor validity
Air-data or AOA disagree beyond threshold → widen protections; declare **direct_degraded** on HUD.

## Stores asymmetry
MC provides stores state; FCC derates roll authority with asymmetric heavy stores (`sms-interface.yaml` / inert catalogue).

## Still stubbed
- Refined AOA/Nz from Flight Lab aero co-check (#79)
- High-Mach inlet/engine coupling
- Spin recovery law (Block 2)
