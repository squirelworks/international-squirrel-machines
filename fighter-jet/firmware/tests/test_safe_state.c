#include "ism_bay_fw.h"

#include <stdio.h>
#include <string.h>

static int fails;

static void expect(int cond, const char *msg) {
  if (!cond) {
    fprintf(stderr, "FAIL: %s\n", msg);
    fails++;
  }
}

int main(void) {
  ism_bay_state_t s;
  char buf[384];

  ism_bay_init(&s);
  expect(s.safe_state, "init starts safe/neutral");
  expect(s.cmd_norm[0] == 0.0f, "actuators neutral at init");
  expect(!s.disc_radio_enable, "radio discrete inactive at init");

  /* Uplink OK + tick → leave safe; accept actuator cmds */
  ism_bay_set_uplink(&s, true);
  ism_bay_set_inceptor_ok(&s, true);
  ism_bay_tick(&s);
  expect(!s.safe_state, "tick with uplink clears safe");
  expect(ism_bay_set_actuator_cmd(&s, 0, 0.5f), "act accepted");
  expect(s.cmd_norm[0] > 0.4f, "act stored");

  ism_bay_set_inceptor(&s, 0, -0.25f);
  expect(s.inceptor_norm[0] < 0.0f, "inceptor stored");

  /* SS-UL-01 */
  ism_bay_set_uplink(&s, false);
  ism_bay_tick(&s);
  expect(s.safe_state, "loss of uplink → safe");
  expect(s.cmd_norm[0] == 0.0f, "actuators zeroed on uplink loss");
  expect(!ism_bay_set_actuator_cmd(&s, 0, 1.0f), "cmd rejected in safe");
  expect(s.bit.fault_bits & ISM_FAULT_UPLINK, "uplink fault bit");

  /* SS-BO-01 */
  ism_bay_set_uplink(&s, true);
  ism_bay_tick(&s);
  ism_bay_set_actuator_cmd(&s, 1, -1.0f);
  ism_bay_set_brownout(&s, true);
  ism_bay_tick(&s);
  expect(s.safe_state, "brownout → safe");
  expect(s.cmd_norm[1] == 0.0f, "actuators zeroed on brownout");
  expect(s.bit.fault_bits & ISM_FAULT_BROWNOUT, "brownout fault bit");

  /* SS-WD-01 */
  ism_bay_set_brownout(&s, false);
  ism_bay_set_uplink(&s, true);
  ism_bay_tick(&s);
  ism_bay_set_actuator_cmd(&s, 2, 0.25f);
  ism_bay_set_watchdog(&s, true);
  ism_bay_tick(&s);
  expect(s.safe_state, "watchdog → safe");
  expect(s.cmd_norm[2] == 0.0f, "actuators zeroed on watchdog");
  expect(s.bit.fault_bits & ISM_FAULT_WATCHDOG, "watchdog fault bit");

  /* SS-IN-01 */
  ism_bay_set_watchdog(&s, false);
  ism_bay_tick(&s);
  ism_bay_set_actuator_cmd(&s, 3, 0.8f);
  ism_bay_set_inceptor_ok(&s, false);
  ism_bay_tick(&s);
  expect(s.safe_state, "inceptor loss → safe");
  expect(s.cmd_norm[3] == 0.0f, "actuators zeroed on inceptor loss");
  expect(s.bit.fault_bits & ISM_FAULT_INCEPTOR, "inceptor fault bit");

  expect(ism_bay_format_bit_line(&s, buf, (int)sizeof(buf)) > 0, "BIT line");
  expect(strstr(buf, ISM_FW_BOARD_ID) != NULL, "BIT has board id");
  expect(strstr(buf, "imu=") != NULL, "BIT has imu health");
  expect(strstr(buf, "fw_hash=") != NULL, "BIT has firmware hash");
  expect(strstr(buf, "uptime=") != NULL, "BIT has uptime");
  expect(strstr(buf, "fault=") != NULL, "BIT has fault bits");

  if (fails) {
    fprintf(stderr, "%d failure(s)\n", fails);
    return 1;
  }
  puts("test_safe_state OK");
  return 0;
}
