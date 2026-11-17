/*
 * ISM NVMe carrier — PEDET LED + PERST release.
 * PCIe / USB-NVMe bridge is a follow-up. Module pad N → GP(N-2).
 */
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "tusb.h"

#define PIN_PEDET  0  /* pad 2 */
#define PIN_PERST  1  /* pad 3 */
#define PIN_CLKREQ 2  /* pad 4 */
#define PIN_DEVSLP 3  /* pad 5 */
#define PIN_LED    17 /* pad 19 */

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
  gpio_init(PIN_LED); gpio_set_dir(PIN_LED, GPIO_OUT); gpio_put(PIN_LED, 0);

  gpio_init(PIN_PEDET); gpio_set_dir(PIN_PEDET, GPIO_IN); gpio_pull_up(PIN_PEDET);
  gpio_init(PIN_CLKREQ); gpio_set_dir(PIN_CLKREQ, GPIO_IN); gpio_pull_up(PIN_CLKREQ);
  gpio_init(PIN_DEVSLP); gpio_set_dir(PIN_DEVSLP, GPIO_OUT); gpio_put(PIN_DEVSLP, 0);

  /* Hold PERST low briefly, then release (active-low reset). */
  gpio_init(PIN_PERST); gpio_set_dir(PIN_PERST, GPIO_OUT); gpio_put(PIN_PERST, 0);
  sleep_ms(20);
  gpio_put(PIN_PERST, 1);

  tusb_init();

  while (true) {
    tud_task();
    bool present = !gpio_get(PIN_PEDET); /* active-low with pull-up */
    gpio_put(PIN_LED, present);
    sleep_ms(50);
  }
}
