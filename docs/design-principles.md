# ISM Design Principles

## Pure Development
Squirrel-OS/2 and ISM hardware are developed independently. Contemporary open keyboard PCBs, OpenSCAD case generators, and KiCad libraries may be studied as reference only. Resulting designs, footprints, and mechanical models are original.

## Scaffold First
Every device begins with:
1. A short design note (layout, form factor, key components, mounting).
2. Directory structure.
3. Placeholder KiCad project or OpenSCAD file.
4. An issue tracking the next concrete step.

## Mechanical + Electrical
- PCBs: KiCad (schematic + layout, production Gerbers).
- Shells and enclosures: Parametric OpenSCAD (or equivalent) exporting STL.
- Shared libraries live in `common/`.

## Branding
International Squirrel Machines. Clean, Warp-era industrial aesthetic with subtle squirrel motifs. No reliance on external trademarks.

## Release Cadence
When a device is polished, inquire before tagging a release or pushing production files.
