// ISM-FJ-TOOL-050 — Wing lower-skin layup tool (male, study mm). Issue #106.
// Vacuum boss sinks into tool face for manifold union.

root_chord = 110;
tip_chord = 45;
semi_span = 140;
tool_t = 18;
boss_sink = 2;

module wing_skin_layup_tool() {
    union() {
        hull() {
            translate([0, 0, 0]) cube([root_chord, 2, tool_t], center = true);
            translate([(root_chord - tip_chord) / 4, semi_span, 0])
                cube([tip_chord, 2, tool_t * 0.7], center = true);
        }
        translate([root_chord / 4, 20, tool_t / 2 - boss_sink])
            cylinder(h = 8 + boss_sink, d = 16, $fn = 32);
    }
}

wing_skin_layup_tool();
