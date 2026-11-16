#include "ism_bay_fw.h"

#include <stdio.h>
#include <string.h>

void ism_bay_init(ism_bay_state_t *s) {
  memset(s, 0, sizeof(*s));
  s->bit.rail_28v_ok = true;
  s->bit.rail_5v_ok = true;
  s->bit.rail_3v3_ok = true;
  s->bit.imu_ok = true;
  s->bit.radio_ok = true;
  s->bit.uplink_ok = true;
  s->bit.brownout = false;
  s->safe_state = false;
  ism_bay_apply_safe_defaults(s);
}

void ism_bay_set_uplink(ism_bay_state_t *s, bool ok) {
  s->bit.uplink_ok = ok;
}

void ism_bay_set_brownout(ism_bay_state_t *s, bool active) {
  s->bit.brownout = active;
  if (active) {
    s->bit.rail_3v3_ok = false;
  }
}

void ism_bay_apply_safe_defaults(ism_bay_state_t *s) {
  for (int i = 0; i < ISM_ACT_CH_COUNT; i++) {
    s->cmd_norm[i] = 0.0f;
  }
  s->safe_state = true;
}

static float clampf(float v, float lo, float hi) {
  if (v < lo) return lo;
  if (v > hi) return hi;
  return v;
}

bool ism_bay_set_actuator_cmd(ism_bay_state_t *s, int ch, float cmd) {
  if (ch < 0 || ch >= ISM_ACT_CH_COUNT) return false;
  if (s->safe_state) {
    s->cmd_norm[ch] = 0.0f;
    return false;
  }
  s->cmd_norm[ch] = clampf(cmd, -1.0f, 1.0f);
  return true;
}

bool ism_bay_set_inceptor(ism_bay_state_t *s, int idx, float value) {
  if (idx < 0 || idx >= ISM_INCEPTOR_COUNT) return false;
  s->inceptor_norm[idx] = clampf(value, -1.0f, 1.0f);
  return true;
}

void ism_bay_tick(ism_bay_state_t *s) {
  /* Safe-state: brownout or loss of uplink forces neutral actuators. */
  if (s->bit.brownout || !s->bit.uplink_ok) {
    ism_bay_apply_safe_defaults(s);
    return;
  }
  s->safe_state = false;
}

int ism_bay_format_bit_line(const ism_bay_state_t *s, char *buf, int buflen) {
  if (!buf || buflen < 8) return 0;
  return snprintf(
      buf, (size_t)buflen,
      "BIT board=%s ver=%s rail28=%d rail5=%d rail3v3=%d imu=%d radio=%d "
      "uplink=%d brownout=%d safe=%d "
      "act=%.2f,%.2f,%.2f,%.2f "
      "inc=%.2f,%.2f,%.2f,%.2f\n",
      ISM_FW_BOARD_ID, ISM_FW_VERSION, s->bit.rail_28v_ok, s->bit.rail_5v_ok,
      s->bit.rail_3v3_ok, s->bit.imu_ok, s->bit.radio_ok, s->bit.uplink_ok,
      s->bit.brownout, s->safe_state, s->cmd_norm[0], s->cmd_norm[1],
      s->cmd_norm[2], s->cmd_norm[3], s->inceptor_norm[0],
      s->inceptor_norm[1], s->inceptor_norm[2], s->inceptor_norm[3]);
}
