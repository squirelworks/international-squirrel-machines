/*
 * ISM SCSI carrier — BSY LED + RST release.
 * USB–SCSI bridge / data path is a follow-up. Module pad N → GP(N-2).
 */
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "tusb.h"

#define PIN_BSY    0  /* pad 2 */
#define PIN_RST    1  /* pad 3 */
#define PIN_ACK    2  /* pad 4 */
#define PIN_REQ    3  /* pad 5 */
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

  gpio_init(PIN_BSY); gpio_set_dir(PIN_BSY, GPIO_IN); gpio_pull_up(PIN_BSY);
  gpio_init(PIN_ACK); gpio_set_dir(PIN_ACK, GPIO_IN); gpio_pull_up(PIN_ACK);
  gpio_init(PIN_REQ); gpio_set_dir(PIN_REQ, GPIO_IN); gpio_pull_up(PIN_REQ);

  /* Pulse RST# low, then release (active-low). */
  gpio_init(PIN_RST); gpio_set_dir(PIN_RST, GPIO_OUT); gpio_put(PIN_RST, 0);
  sleep_ms(20);
  gpio_put(PIN_RST, 1);

  tusb_init();

  while (true) {
    tud_task();
    bool busy = !gpio_get(PIN_BSY); /* active-low with pull-up */
    gpio_put(PIN_LED, busy);
    sleep_ms(50);
  }
}
