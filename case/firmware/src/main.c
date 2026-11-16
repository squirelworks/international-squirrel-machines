/*
 * ISM Case front-panel firmware — power/reset buttons + status LEDs + ATX mirrors.
 * Module pad N maps to GP(N-2) for pads 2..13 (same convention as other ISM boards).
 */
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "tusb.h"

#define PIN_BTN_PWR   0  /* pad 2 */
#define PIN_BTN_RST   1  /* pad 3 */
#define PIN_LED_PWR   2  /* pad 4 */
#define PIN_LED_HDD   3  /* pad 5 */
#define PIN_ATX_PWR   4  /* pad 6 — pulse motherboard PWR_SW */
#define PIN_ATX_RST   5  /* pad 7 */
#define PIN_ATX_PLED  6  /* pad 8 — sense/drive panel PWR LED from ATX */
#define PIN_ATX_HLED  7  /* pad 9 */

void tud_hid_report_complete_cb(uint8_t i, uint8_t const *r, uint16_t n) {
  (void)i; (void)r; (void)n;
}
uint16_t tud_hid_get_report_cb(uint8_t i, uint8_t id, hid_report_type_t t, uint8_t *b, uint16_t n) {
  (void)i; (void)id; (void)t; (void)b; (void)n; return 0;
}
void tud_hid_set_report_cb(uint8_t i, uint8_t id, hid_report_type_t t, uint8_t const *b, uint16_t n) {
  (void)i; (void)id; (void)t; (void)b; (void)n;
}

static void pulse(uint pin, uint ms) {
  gpio_put(pin, 0); /* open-drain style: assert low */
  sleep_ms(ms);
  gpio_put(pin, 1);
}

int main(void) {
  gpio_init(PIN_BTN_PWR); gpio_set_dir(PIN_BTN_PWR, GPIO_IN); gpio_pull_up(PIN_BTN_PWR);
  gpio_init(PIN_BTN_RST); gpio_set_dir(PIN_BTN_RST, GPIO_IN); gpio_pull_up(PIN_BTN_RST);

  gpio_init(PIN_LED_PWR); gpio_set_dir(PIN_LED_PWR, GPIO_OUT); gpio_put(PIN_LED_PWR, 0);
  gpio_init(PIN_LED_HDD); gpio_set_dir(PIN_LED_HDD, GPIO_OUT); gpio_put(PIN_LED_HDD, 0);

  gpio_init(PIN_ATX_PWR); gpio_set_dir(PIN_ATX_PWR, GPIO_OUT); gpio_put(PIN_ATX_PWR, 1);
  gpio_init(PIN_ATX_RST); gpio_set_dir(PIN_ATX_RST, GPIO_OUT); gpio_put(PIN_ATX_RST, 1);

  gpio_init(PIN_ATX_PLED); gpio_set_dir(PIN_ATX_PLED, GPIO_IN); gpio_pull_up(PIN_ATX_PLED);
  gpio_init(PIN_ATX_HLED); gpio_set_dir(PIN_ATX_HLED, GPIO_IN); gpio_pull_up(PIN_ATX_HLED);

  tusb_init();

  bool prev_pwr = true;
  bool prev_rst = true;
  while (true) {
    tud_task();

    bool pwr = gpio_get(PIN_BTN_PWR);
    bool rst = gpio_get(PIN_BTN_RST);
    if (prev_pwr && !pwr) {
      pulse(PIN_ATX_PWR, 200);
    }
    if (prev_rst && !rst) {
      pulse(PIN_ATX_RST, 100);
    }
    prev_pwr = pwr;
    prev_rst = rst;

    /* Mirror ATX LED senses onto panel LEDs (active-low typical) */
    gpio_put(PIN_LED_PWR, gpio_get(PIN_ATX_PLED) ? 0 : 1);
    gpio_put(PIN_LED_HDD, gpio_get(PIN_ATX_HLED) ? 0 : 1);

    sleep_ms(5);
  }
}
