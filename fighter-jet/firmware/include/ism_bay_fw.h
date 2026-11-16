/* ISM-FJ-1 bay I/O firmware bring-up API — issues #84 / A1 #119 */
#ifndef ISM_BAY_FW_H
#define ISM_BAY_FW_H

#include <stdbool.h>
#include <stdint.h>

#define ISM_FW_BOARD_ID "ISM-FJ-BAY-IO"
#define ISM_FW_VERSION "0.2.0"
#define ISM_ACT_CH_COUNT 4
#define ISM_INCEPTOR_COUNT 4
#define ISM_DISC_RADIO 0
#define ISM_DISC_IMU_GATE 1

#define ISM_FAULT_BROWNOUT (1u << 0)
#define ISM_FAULT_UPLINK (1u << 1)
#define ISM_FAULT_WATCHDOG (1u << 2)
#define ISM_FAULT_INCEPTOR (1u << 3)
#define ISM_FAULT_IMU (1u << 4)
#define ISM_FAULT_RAIL (1u << 5)

typedef struct {
  bool rail_28v_ok;
  bool rail_5v_ok;
  bool rail_3v3_ok;
  bool imu_ok;
  bool radio_ok;
  bool uplink_ok;
  bool brownout;
  bool watchdog;
  bool inceptor_ok;
  uint16_t fault_bits;
  uint32_t uptime_s;
} ism_bit_status_t;

typedef struct {
  float cmd_norm[ISM_ACT_CH_COUNT]; /* -1..+1 → J1..J4 */
  float inceptor_norm[ISM_INCEPTOR_COUNT];
  bool disc_radio_enable;
  bool disc_imu_gate;
  ism_bit_status_t bit;
  bool safe_state;
} ism_bay_state_t;

void ism_bay_init(ism_bay_state_t *s);
void ism_bay_set_uplink(ism_bay_state_t *s, bool ok);
void ism_bay_set_brownout(ism_bay_state_t *s, bool active);
void ism_bay_set_watchdog(ism_bay_state_t *s, bool expired);
void ism_bay_set_inceptor_ok(ism_bay_state_t *s, bool ok);
void ism_bay_apply_safe_defaults(ism_bay_state_t *s);
bool ism_bay_set_actuator_cmd(ism_bay_state_t *s, int ch, float cmd);
bool ism_bay_set_inceptor(ism_bay_state_t *s, int idx, float value);
void ism_bay_tick(ism_bay_state_t *s);
/* Write one BIT line to buf (UART/stdio profile). Returns bytes written. */
int ism_bay_format_bit_line(const ism_bay_state_t *s, char *buf, int buflen);

#endif
