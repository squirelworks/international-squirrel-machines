/*
 * ISM Camera firmware — TinyUSB bring-up + SCCB/XCLK stubs.
 */
#include "pico/stdlib.h"
#include "hardware/pwm.h"
#include "tusb.h"

#define PIN_SDA 0
#define PIN_SCL 1
#define PIN_XCLK 2
#define PIN_RST 6
#define PIN_PWDN 7
#define PIN_SHUT 15
#define PIN_MODE 16

void tud_hid_report_complete_cb(uint8_t i, uint8_t const *r, uint16_t n) {
  (void)i; (void)r; (void)n;
}
uint16_t tud_hid_get_report_cb(uint8_t i, uint8_t id, hid_report_type_t t, uint8_t *b, uint16_t n) {
  (void)i; (void)id; (void)t; (void)b; (void)n; return 0;
}
void tud_hid_set_report_cb(uint8_t i, uint8_t id, hid_report_type_t t, uint8_t const *b, uint16_t n) {
  (void)i; (void)id; (void)t; (void)b; (void)n;
}

int main(void) {
  gpio_init(PIN_RST); gpio_set_dir(PIN_RST, GPIO_OUT); gpio_put(PIN_RST, 0);
  gpio_init(PIN_PWDN); gpio_set_dir(PIN_PWDN, GPIO_OUT); gpio_put(PIN_PWDN, 0);
  gpio_init(PIN_SHUT); gpio_set_dir(PIN_SHUT, GPIO_IN); gpio_pull_up(PIN_SHUT);
  gpio_init(PIN_MODE); gpio_set_dir(PIN_MODE, GPIO_IN); gpio_pull_up(PIN_MODE);
  gpio_set_function(PIN_XCLK, GPIO_FUNC_PWM);
  uint slice = pwm_gpio_to_slice_num(PIN_XCLK);
  pwm_set_wrap(slice, 4);
  pwm_set_chan_level(slice, pwm_gpio_to_channel(PIN_XCLK), 2);
  pwm_set_enabled(slice, true);
  sleep_ms(10);
  gpio_put(PIN_RST, 1);
  tusb_init();
  while (true) {
    tud_task();
    sleep_ms(10);
  }
}
