# ICD Freeze — Rev A (#78)

**Pinned list:** `../interfaces/icd-freeze.yaml`  
**Manifest:** `../interfaces/schema-manifest.yaml`  
**Device index:** `../../docs/devices/fighter-jet.md`

## Freeze statement
Rev **A** pins interface **keys and drawing cross-refs** after firmware bring-up (#84). Field values marked `provisional: true` may change; key renames require **Rev B** and an explicit bump in `icd-freeze.yaml`.

## Boundaries
| Boundary | Authority files |
|----------|-----------------|
| Mechanical / datum | `aircraft-geometry.yaml`, `mechanical-airframe.yaml`, DWG-010…060 |
| Materials | `materials-zones.yaml`, `materials-allowables.yaml` |
| FBW / actuators | `flight-controls.yaml`, `actuators.yaml`, `hydraulics.yaml` |
| Avionics / FW | `avionics-bus.yaml`, `avionics-architecture.yaml`, `firmware-bringup.yaml` |
| Sensors | `sensors.yaml` |
| Stores (integration only) | `hardpoints.yaml`, `sms-interface.yaml`, `inert-stores.yaml` |

## Soft MVP
Flight Lab (#79) and HIL UI (#80) are Steve’s lane — co-checks listed in `validation-matrix.yaml` remain **pending Soft** where noted.
