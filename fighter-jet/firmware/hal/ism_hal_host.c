#include "ism_hal.h"

#include <math.h>

static bool wd_expired;
static uint32_t uptime;
static float pwm[4];   /* host readback retained for future HIL */
static bool disc[2];

/* Silence -Wunused-but-set until host readback lands */
static float ism_hal_pwm_get(int ch) { return (ch >= 0 && ch < 4) ? pwm[ch] : 0.f; }
static bool ism_hal_disc_get(int id) { return (id >= 0 && id < 2) ? disc[id] : false; }

void ism_hal_init(void) {
  wd_expired = false;
  uptime = 0;
  for (int i = 0; i < 4; i++) pwm[i] = 0.0f;
  disc[0] = disc[1] = false;
}

void ism_hal_watchdog_kick(void) { wd_expired = false; }
void ism_hal_watchdog_force_timeout(void) { wd_expired = true; }
bool ism_hal_watchdog_expired(void) { return wd_expired; }

void ism_hal_pwm_set_norm(int ch, float cmd_norm) {
  if (ch >= 0 && ch < 4) pwm[ch] = cmd_norm;
  (void)ism_hal_pwm_get(ch);
}

void ism_hal_discrete_set(int id, bool active) {
  if (id >= 0 && id < 2) disc[id] = active;
  (void)ism_hal_disc_get(id);
}

float ism_hal_rail_3v3_v(void) { return 3.30f; }
float ism_hal_rail_5v_v(void) { return 5.00f; }
bool ism_hal_imu_self_test(void) { return true; }

uint32_t ism_hal_uptime_s(void) { return uptime++; }
const char *ism_hal_firmware_hash(void) { return "hoststub"; }
