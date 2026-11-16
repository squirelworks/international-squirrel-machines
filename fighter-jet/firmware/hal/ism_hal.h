/* HAL stubs — bay I/O study board. Host profile no-ops; Pico port fills these. */
#ifndef ISM_HAL_H
#define ISM_HAL_H

#include <stdbool.h>
#include <stdint.h>

void ism_hal_init(void);
void ism_hal_watchdog_kick(void);
void ism_hal_watchdog_force_timeout(void); /* test hook */
bool ism_hal_watchdog_expired(void);

void ism_hal_pwm_set_norm(int ch, float cmd_norm); /* J1..J4 */
void ism_hal_discrete_set(int id, bool active);

float ism_hal_rail_3v3_v(void);
float ism_hal_rail_5v_v(void);
bool ism_hal_imu_self_test(void);

uint32_t ism_hal_uptime_s(void);
const char *ism_hal_firmware_hash(void);

#endif
