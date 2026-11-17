/*
 * ISM IDE carrier — DASP LED + RESET release.
 * USB–PATA bridge / ATA data path is a follow-up. Module pad N → GP(N-2).
 */
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "tusb.h"

#define PIN_DASP   0  /* pad 2 */
#define PIN_RESET  1  /* pad 3 */
#define PIN_INTRQ  2  /* pad 4 */
#define PIN_IORDY  3  /* pad 5 */
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

  gpio_init(PIN_DASP); gpio_set_dir(PIN_DASP, GPIO_IN); gpio_pull_up(PIN_DASP);
  gpio_init(PIN_INTRQ); gpio_set_dir(PIN_INTRQ, GPIO_IN); gpio_pull_up(PIN_INTRQ);
  gpio_init(PIN_IORDY); gpio_set_dir(PIN_IORDY, GPIO_IN); gpio_pull_up(PIN_IORDY);

  /* Pulse RESET# low, then release (active-low). */
  gpio_init(PIN_RESET); gpio_set_dir(PIN_RESET, GPIO_OUT); gpio_put(PIN_RESET, 0);
  sleep_ms(20);
  gpio_put(PIN_RESET, 1);

  tusb_init();

  while (true) {
    tud_task();
    bool present = !gpio_get(PIN_DASP); /* active-low with pull-up */
    gpio_put(PIN_LED, present);
    sleep_ms(50);
  }
}
