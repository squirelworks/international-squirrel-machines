/*
 * ISM Monitor OSD firmware — TinyUSB HID on RP2040 (bring-up).
 * Buttons → HID keyboard; BL_PWM / PNL_EN GPIO drive.
 */
#include "pico/stdlib.h"
#include "hardware/pwm.h"
#include "tusb.h"

#define PIN_BTN_PWR  0
#define PIN_BTN_MENU 1
#define PIN_BTN_UP   2
#define PIN_BTN_DN   3
#define PIN_BL_PWM   4
#define PIN_PNL_EN   5
#define PIN_HPD      6

static const uint8_t btns[] = {PIN_BTN_PWR, PIN_BTN_MENU, PIN_BTN_UP, PIN_BTN_DN};
static const uint8_t codes[] = {0x66 /* power */, 0x65 /* app */, 0x52 /* up */, 0x51 /* down */};

void tud_hid_report_complete_cb(uint8_t i, uint8_t const *r, uint16_t n) {
  (void)i; (void)r; (void)n;
}
uint16_t tud_hid_get_report_cb(uint8_t i, uint8_t id, hid_report_type_t t, uint8_t *b, uint16_t n) {
  (void)i; (void)id; (void)t; (void)b; (void)n; return 0;
}
void tud_hid_set_report_cb(uint8_t i, uint8_t id, hid_report_type_t t, uint8_t const *b, uint16_t n) {
  (void)i; (void)id; (void)t; (void)b; (void)n;
}

static void hid_task(void) {
  if (!tud_hid_ready()) return;
  uint8_t keys[6] = {0};
  unsigned ki = 0;
  for (unsigned i = 0; i < 4; i++) {
    if (!gpio_get(btns[i]) && ki < 6) keys[ki++] = codes[i];
  }
  tud_hid_keyboard_report(0, 0, keys);
}

int main(void) {
  for (unsigned i = 0; i < 4; i++) {
    gpio_init(btns[i]);
    gpio_set_dir(btns[i], GPIO_IN);
    gpio_pull_up(btns[i]);
  }
  gpio_init(PIN_PNL_EN); gpio_set_dir(PIN_PNL_EN, GPIO_OUT); gpio_put(PIN_PNL_EN, 1);
  gpio_init(PIN_HPD); gpio_set_dir(PIN_HPD, GPIO_IN); gpio_pull_down(PIN_HPD);
  gpio_set_function(PIN_BL_PWM, GPIO_FUNC_PWM);
  uint slice = pwm_gpio_to_slice_num(PIN_BL_PWM);
  pwm_set_wrap(slice, 255);
  pwm_set_chan_level(slice, pwm_gpio_to_channel(PIN_BL_PWM), 180);
  pwm_set_enabled(slice, true);
  tusb_init();
  while (true) {
    tud_task();
    hid_task();
    sleep_ms(10);
  }
}
