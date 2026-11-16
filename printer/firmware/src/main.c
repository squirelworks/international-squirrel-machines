/*
 * ISM Printer firmware — TinyUSB HID bring-up + DRV8833 GPIO.
 */
#include "pico/stdlib.h"
#include "tusb.h"

#define PIN_AIN1 0
#define PIN_AIN2 1
#define PIN_BIN1 2
#define PIN_BIN2 3
#define PIN_SLEEP 4
#define PIN_PAPER 8
#define PIN_FEED 9
#define PIN_CANCEL 10
#define PIN_PWR 11

void tud_hid_report_complete_cb(uint8_t i, uint8_t const *r, uint16_t n) {
  (void)i; (void)r; (void)n;
}
uint16_t tud_hid_get_report_cb(uint8_t i, uint8_t id, hid_report_type_t t, uint8_t *b, uint16_t n) {
  (void)i; (void)id; (void)t; (void)b; (void)n; return 0;
}
void tud_hid_set_report_cb(uint8_t i, uint8_t id, hid_report_type_t t, uint8_t const *b, uint16_t n) {
  (void)i; (void)id; (void)t; (void)b; (void)n;
}

static void feed_pulse(void) {
  gpio_put(PIN_AIN1, 1); gpio_put(PIN_AIN2, 0);
  sleep_ms(80);
  gpio_put(PIN_AIN1, 0); gpio_put(PIN_AIN2, 0);
}

int main(void) {
  for (int p = PIN_AIN1; p <= PIN_SLEEP; p++) {
    gpio_init(p); gpio_set_dir(p, GPIO_OUT); gpio_put(p, 0);
  }
  gpio_put(PIN_SLEEP, 1);
  for (int p = PIN_FEED; p <= PIN_PWR; p++) {
    gpio_init(p); gpio_set_dir(p, GPIO_IN); gpio_pull_up(p);
  }
  gpio_init(PIN_PAPER); gpio_set_dir(PIN_PAPER, GPIO_IN); gpio_pull_up(PIN_PAPER);
  tusb_init();
  while (true) {
    tud_task();
    if (!gpio_get(PIN_FEED)) feed_pulse();
    sleep_ms(10);
  }
}
