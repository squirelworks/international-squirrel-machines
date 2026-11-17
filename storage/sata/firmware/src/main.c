/*
 * ISM SATA carrier — DET sense → ACT LED.
 * USB–SATA bridge / data path is a follow-up. Module pad N → GP(N-2).
 */
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "tusb.h"

#define PIN_DET    0  /* pad 2 */
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

  /* R3 pulls to +3V3; R4 from +5V raises DET when drive power is present. */
  gpio_init(PIN_DET); gpio_set_dir(PIN_DET, GPIO_IN); gpio_pull_up(PIN_DET);

  tusb_init();

  while (true) {
    tud_task();
    bool present = gpio_get(PIN_DET);
    gpio_put(PIN_LED, present);
    sleep_ms(50);
  }
}
