/*
 * ISM Plotter firmware — TinyUSB bring-up + DRV8833 X/Y + pen lift.
 */
#include "pico/stdlib.h"
#include "tusb.h"

#define PIN_AIN1 0
#define PIN_AIN2 1
#define PIN_BIN1 2
#define PIN_BIN2 3
#define PIN_SLEEP 4
#define PIN_PEN 5
#define PIN_LIM_X 6
#define PIN_LIM_Y 7
#define PIN_HOME 8
#define PIN_BTN_HOME 9
#define PIN_BTN_STOP 10
#define PIN_BTN_PWR 11

void tud_hid_report_complete_cb(uint8_t i, uint8_t const *r, uint16_t n) {
  (void)i; (void)r; (void)n;
}
uint16_t tud_hid_get_report_cb(uint8_t i, uint8_t id, hid_report_type_t t, uint8_t *b, uint16_t n) {
  (void)i; (void)id; (void)t; (void)b; (void)n; return 0;
}
void tud_hid_set_report_cb(uint8_t i, uint8_t id, hid_report_type_t t, uint8_t const *b, uint16_t n) {
  (void)i; (void)id; (void)t; (void)b; (void)n;
}

static void step_axis(int a1, int a2, int ms) {
  gpio_put(a1, 1); gpio_put(a2, 0);
  sleep_ms(ms);
  gpio_put(a1, 0); gpio_put(a2, 0);
}

int main(void) {
  for (int p = PIN_AIN1; p <= PIN_PEN; p++) {
    gpio_init(p); gpio_set_dir(p, GPIO_OUT); gpio_put(p, 0);
  }
  gpio_put(PIN_SLEEP, 1);
  for (int p = PIN_LIM_X; p <= PIN_BTN_PWR; p++) {
    gpio_init(p); gpio_set_dir(p, GPIO_IN); gpio_pull_up(p);
  }
  tusb_init();
  while (true) {
    tud_task();
    if (!gpio_get(PIN_BTN_HOME)) {
      gpio_put(PIN_PEN, 0);
      while (gpio_get(PIN_LIM_X)) step_axis(PIN_AIN2, PIN_AIN1, 5);
      while (gpio_get(PIN_LIM_Y)) step_axis(PIN_BIN2, PIN_BIN1, 5);
    }
    sleep_ms(10);
  }
}
