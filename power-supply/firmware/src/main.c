/*
 * ISM Power Supply firmware — rail sense + PS_ON / PWR_OK bring-up.
 * Module pad N → GP(N-2) for pads 2..13 (ISM convention).
 * Sense GPIOs are digital thresholds here; ADC mapping is a follow-up.
 */
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "tusb.h"

#define PIN_PS_ON   0  /* pad 2 */
#define PIN_PWR_OK  1  /* pad 3 */
#define PIN_SNS_12  2  /* pad 4 */
#define PIN_SNS_5   3  /* pad 5 */
#define PIN_SNS_33  4  /* pad 6 */
#define PIN_LED     17 /* pad 19 */

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

  gpio_init(PIN_PS_ON); gpio_set_dir(PIN_PS_ON, GPIO_IN); gpio_pull_up(PIN_PS_ON);
  gpio_init(PIN_PWR_OK); gpio_set_dir(PIN_PWR_OK, GPIO_OUT); gpio_put(PIN_PWR_OK, 0);
  gpio_init(PIN_SNS_12); gpio_set_dir(PIN_SNS_12, GPIO_IN);
  gpio_init(PIN_SNS_5); gpio_set_dir(PIN_SNS_5, GPIO_IN);
  gpio_init(PIN_SNS_33); gpio_set_dir(PIN_SNS_33, GPIO_IN);

  tusb_init();

  while (true) {
    tud_task();
    /* ATX: PS_ON# low means "on". Assert PWR_OK when sense pins read high (rails up). */
    bool on = !gpio_get(PIN_PS_ON);
    bool rails = gpio_get(PIN_SNS_12) && gpio_get(PIN_SNS_5) && gpio_get(PIN_SNS_33);
    bool ok = on && rails;
    gpio_put(PIN_PWR_OK, ok);
    gpio_put(PIN_LED, ok);
    sleep_ms(20);
  }
}
