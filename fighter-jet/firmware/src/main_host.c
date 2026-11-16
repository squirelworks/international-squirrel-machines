/* Host UART/stdio profile demo for HIL / analyzer hooks (#84 / A1 #119).
 * Commands (one per line):
 *   help | bit | act <ch> <cmd> | inc <idx> <val>
 *   uplink 0|1 | brownout 0|1 | watchdog 0|1 | inceptor_ok 0|1 | tick | quit
 */
#include "ism_bay_fw.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void print_bit(const ism_bay_state_t *s) {
  char line[384];
  ism_bay_format_bit_line(s, line, (int)sizeof(line));
  fputs(line, stdout);
  fflush(stdout);
}

int main(void) {
  ism_bay_state_t st;
  char line[128];

  ism_bay_init(&st);
  st.safe_state = true;
  puts("ISM-FJ bay firmware host profile " ISM_FW_VERSION);
  puts("type 'help'");
  print_bit(&st);

  while (fgets(line, sizeof(line), stdin)) {
    char cmd[32];
    float a = 0, b = 0;
    int n = sscanf(line, "%31s %f %f", cmd, &a, &b);
    if (n < 1) continue;
    if (strcmp(cmd, "help") == 0) {
      puts("bit | act <0-3> <-1..1> | inc <0-3> <-1..1> | uplink 0|1 | "
           "brownout 0|1 | watchdog 0|1 | inceptor_ok 0|1 | tick | quit");
    } else if (strcmp(cmd, "bit") == 0) {
      print_bit(&st);
    } else if (strcmp(cmd, "act") == 0 && n >= 3) {
      ism_bay_tick(&st);
      if (!ism_bay_set_actuator_cmd(&st, (int)a, b))
        puts("ERR act (safe or bad ch)");
      else
        print_bit(&st);
    } else if (strcmp(cmd, "inc") == 0 && n >= 3) {
      if (!ism_bay_set_inceptor(&st, (int)a, b))
        puts("ERR inc");
      else
        print_bit(&st);
    } else if (strcmp(cmd, "uplink") == 0 && n >= 2) {
      ism_bay_set_uplink(&st, a != 0.0f);
      ism_bay_tick(&st);
      print_bit(&st);
    } else if (strcmp(cmd, "brownout") == 0 && n >= 2) {
      ism_bay_set_brownout(&st, a != 0.0f);
      ism_bay_tick(&st);
      print_bit(&st);
    } else if (strcmp(cmd, "watchdog") == 0 && n >= 2) {
      ism_bay_set_watchdog(&st, a != 0.0f);
      ism_bay_tick(&st);
      print_bit(&st);
    } else if (strcmp(cmd, "inceptor_ok") == 0 && n >= 2) {
      ism_bay_set_inceptor_ok(&st, a != 0.0f);
      ism_bay_tick(&st);
      print_bit(&st);
    } else if (strcmp(cmd, "tick") == 0) {
      ism_bay_tick(&st);
      print_bit(&st);
    } else if (strcmp(cmd, "quit") == 0 || strcmp(cmd, "exit") == 0) {
      break;
    } else {
      puts("ERR unknown (help)");
    }
  }
  return 0;
}
