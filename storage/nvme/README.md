# ISM NVMe

M.2 Key-M carrier for commodity NVMe SSDs. Original International Squirrel Machines design.

Generate: `python3 scripts/build_nvme.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| Host | USB-C (`J1`) bring-up |
| MCU | RP2040 module (`U1`) — PEDET / PERST |
| Socket | `ISM_M2_KeyM_Socket` (`J2`) — 2280 bay + `H_M2` |
| PCIe | Stubbed on this PCB (bridge ASIC follow-up) |
| Shell | Carrier + lid |

## Fab ordering

1. `python3 scripts/build_nvme.py`
2. Upload `storage/nvme/fab/ism-nvme-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd storage/nvme/shell && ./export.sh`

### Off-board BOM

- Commodity M.2 2280 NVMe SSD
- M2 screws (5× including retention)

## Flash

```bash
cd storage/nvme/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_nvme.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x001B**.

## Steve interface

See `interfaces/nvme.yaml`.

## Related

- [#54](https://github.com/squirelworks/international-squirrel-machines/issues/54) · umbrella [#49](https://github.com/squirelworks/international-squirrel-machines/issues/49)
- Follow-ups: [#229](https://github.com/squirelworks/international-squirrel-machines/issues/229)
