# ISM Flash Cards — design note

## Build vs wrap

**Wrap commodity media:** ISM builds a **microSD reader/adapter** (RP2040 + Hirose DM3AT socket + USB-C). Flash silicon stays on commodity microSD cards (SD Physical Layer Simplified Spec family).

## Specs cited

- SD Association, *Physical Layer Simplified Specification* (mechanical / SPI electrical context)
- USB-IF Mass Storage Class (target protocol for firmware follow-up)

## Mechanical check (±0.2 mm)

| Dimension | Spec family | CAD (`card_shell`) | Tol. |
|-----------|-------------|--------------------|------|
| Width | ~15 mm microSD | 15.0 mm | ±0.2 |
| Depth | ~11 mm | 11.0 mm | ±0.2 |
| Thickness | ~1 mm | 1.0 mm | ±0.2 |

## Steve test hooks

See `interfaces/flash-cards.yaml`: enumerate USB, assert DET, SPI bring-up; MSC R/W verify is follow-up.
