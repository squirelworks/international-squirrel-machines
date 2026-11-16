#include "ism_bay_fw.h"

#include "ism_hal.h"

#include <stdio.h>
#include <string.h>

void ism_bay_init(ism_bay_state_t *s) {
  memset(s, 0, sizeof(*s));
  ism_hal_init();
  s->bit.rail_28v_ok = true;
  s->bit.rail_5v_ok = true;
  s->bit.rail_3v3_ok = true;
  s->bit.imu_ok = true;
  s->bit.radio_ok = true;
  s->bit.uplink_ok = true;
  s->bit.inceptor_ok = true;
  s->bit.brownout = false;
  s->bit.watchdog = false;
  s->bit.fault_bits = 0;
  s->safe_state = false;
  ism_bay_apply_safe_defaults(s);
}

void ism_bay_set_uplink(ism_bay_state_t *s, bool ok) { s->bit.uplink_ok = ok; }

void ism_bay_set_brownout(ism_bay_state_t *s, bool active) {
  s->bit.brownout = active;
  if (active) {
    s->bit.rail_3v3_ok = false;
  } else {
    s->bit.rail_3v3_ok = true;
  }
}

void ism_bay_set_watchdog(ism_bay_state_t *s, bool expired) {
  s->bit.watchdog = expired;
  if (expired) {
    ism_hal_watchdog_force_timeout();
  } else {
    ism_hal_watchdog_kick();
  }
}

void ism_bay_set_inceptor_ok(ism_bay_state_t *s, bool ok) {
  s->bit.inceptor_ok = ok;
}

void ism_bay_apply_safe_defaults(ism_bay_state_t *s) {
  for (int i = 0; i < ISM_ACT_CH_COUNT; i++) {
    s->cmd_norm[i] = 0.0f;
    ism_hal_pwm_set_norm(i, 0.0f);
  }
  s->disc_radio_enable = false;
  s->disc_imu_gate = false;
  ism_hal_discrete_set(ISM_DISC_RADIO, false);
  ism_hal_discrete_set(ISM_DISC_IMU_GATE, false);
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
    ism_hal_pwm_set_norm(ch, 0.0f);
    return false;
  }
  s->cmd_norm[ch] = clampf(cmd, -1.0f, 1.0f);
  ism_hal_pwm_set_norm(ch, s->cmd_norm[ch]);
  return true;
}

bool ism_bay_set_inceptor(ism_bay_state_t *s, int idx, float value) {
  if (idx < 0 || idx >= ISM_INCEPTOR_COUNT) return false;
  s->inceptor_norm[idx] = clampf(value, -1.0f, 1.0f);
  return true;
}

static void refresh_faults(ism_bay_state_t *s) {
  uint16_t f = 0;
  if (s->bit.brownout) f |= ISM_FAULT_BROWNOUT;
  if (!s->bit.uplink_ok) f |= ISM_FAULT_UPLINK;
  if (s->bit.watchdog || ism_hal_watchdog_expired()) f |= ISM_FAULT_WATCHDOG;
  if (!s->bit.inceptor_ok) f |= ISM_FAULT_INCEPTOR;
  if (!s->bit.imu_ok) f |= ISM_FAULT_IMU;
  if (!s->bit.rail_3v3_ok || !s->bit.rail_5v_ok) f |= ISM_FAULT_RAIL;
  s->bit.fault_bits = f;
}

void ism_bay_tick(ism_bay_state_t *s) {
  s->bit.uptime_s = ism_hal_uptime_s();
  s->bit.imu_ok = ism_hal_imu_self_test();
  if (ism_hal_watchdog_expired()) s->bit.watchdog = true;

  /* Safe-state triggers: brownout, uplink loss, watchdog, inceptor loss */
  if (s->bit.brownout || !s->bit.uplink_ok || s->bit.watchdog ||
      !s->bit.inceptor_ok) {
    ism_bay_apply_safe_defaults(s);
    refresh_faults(s);
    return;
  }
  s->safe_state = false;
  if (!s->safe_state) {
    ism_hal_watchdog_kick();
  }
  refresh_faults(s);
}

int ism_bay_format_bit_line(const ism_bay_state_t *s, char *buf, int buflen) {
  if (!buf || buflen < 8) return 0;
  return snprintf(
      buf, (size_t)buflen,
      "BIT board=%s ver=%s fw_hash=%s rail28=%d rail5=%d rail3v3=%d "
      "v3v3=%.2f imu=%d radio=%d uplink=%d brownout=%d safe=%d "
      "uptime=%u fault=%u "
      "act=%.2f,%.2f,%.2f,%.2f "
      "inc=%.2f,%.2f,%.2f,%.2f\n",
      ISM_FW_BOARD_ID, ISM_FW_VERSION, ism_hal_firmware_hash(),
      s->bit.rail_28v_ok, s->bit.rail_5v_ok, s->bit.rail_3v3_ok,
      ism_hal_rail_3v3_v(), s->bit.imu_ok, s->bit.radio_ok, s->bit.uplink_ok,
      s->bit.brownout, s->safe_state, s->bit.uptime_s, s->bit.fault_bits,
      s->cmd_norm[0], s->cmd_norm[1], s->cmd_norm[2], s->cmd_norm[3],
      s->inceptor_norm[0], s->inceptor_norm[1], s->inceptor_norm[2],
      s->inceptor_norm[3]);
}
