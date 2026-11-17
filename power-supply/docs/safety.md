# ISM Power Supply — safety notes

## Mains

- **This PCB never carries mains.** Input is SELV **12 V DC** from a **certified** AC-DC module / brick (approvals on the brick, not this board).
- Do not substitute an uncertified open-frame mains supply without a qualified person and product certification plan.
- Reviewers: confirm schematic shows only DC at `J_IN` (barrel), never L/N/PE.

## Standards (documentation list — ISM does not claim certification)

- IEC 62368-1 (AV/ICT equipment safety)
- Intel ATX design guide (rail / PS_ON / PWR_OK timing context)
- 80 PLUS / ENERGY STAR (efficiency context for the off-board brick)
- IEC 62040 series (UPS — when building `ups/`)

## Handling

- Short-circuit and reverse-polarity risk on the barrel: observe polarity silk; first-article fuse on brick recommended.
- Inductors and regulators run hot under load — allow airflow / enclosure vents (`shell/`).
