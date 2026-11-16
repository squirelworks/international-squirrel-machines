/*
 * ISM Network Card firmware — SPI master bring-up for W5500 + EXP slave pins.
 * Module pad N → GP(N-2) for pads 2..13 (ISM convention).
 */
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/spi.h"
#include "tusb.h"

#define PIN_EXP_SCK   0
#define PIN_EXP_MOSI  1
#define PIN_EXP_MISO  2
#define PIN_EXP_CS    3
#define PIN_ETH_SCLK  4  /* pad 6 */
#define PIN_ETH_MOSI  5  /* pad 7 */
#define PIN_ETH_MISO  6  /* pad 8 */
#define PIN_ETH_CS    7  /* pad 9 */
#define PIN_ETH_INT   10 /* pad 12 */
#define PIN_ETH_RST   11 /* pad 13 */
#define PIN_LED       17 /* pad 19 */

void tud_hid_report_complete_cb(uint8_t i, uint8_t const *r, uint16_t n) {
  (void)i; (void)r; (void)n;
}
uint16_t tud_hid_get_report_cb(uint8_t i, uint8_t id, hid_report_type_t t, uint8_t *b, uint16_t n) {
  (void)i; (void)id; (void)t; (void)b; (void)n; return 0;
}
void tud_hid_set_report_cb(uint8_t i, uint8_t id, hid_report_type_t t, uint8_t const *b, uint16_t n) {
  (void)i; (void)id; (void)t; (void)b; (void)n;
}

static void w5500_reset(void) {
  gpio_put(PIN_ETH_RST, 0);
  sleep_ms(2);
  gpio_put(PIN_ETH_RST, 1);
  sleep_ms(2);
}

int main(void) {
  gpio_init(PIN_LED); gpio_set_dir(PIN_LED, GPIO_OUT); gpio_put(PIN_LED, 0);

  gpio_init(PIN_EXP_CS); gpio_set_dir(PIN_EXP_CS, GPIO_IN); gpio_pull_up(PIN_EXP_CS);
  gpio_set_function(PIN_EXP_SCK, GPIO_FUNC_SPI);
  gpio_set_function(PIN_EXP_MOSI, GPIO_FUNC_SPI);
  gpio_set_function(PIN_EXP_MISO, GPIO_FUNC_SPI);

  spi_init(spi0, 8 * 1000 * 1000);
  gpio_set_function(PIN_ETH_SCLK, GPIO_FUNC_SPI);
  gpio_set_function(PIN_ETH_MOSI, GPIO_FUNC_SPI);
  gpio_set_function(PIN_ETH_MISO, GPIO_FUNC_SPI);
  gpio_init(PIN_ETH_CS); gpio_set_dir(PIN_ETH_CS, GPIO_OUT); gpio_put(PIN_ETH_CS, 1);
  gpio_init(PIN_ETH_RST); gpio_set_dir(PIN_ETH_RST, GPIO_OUT); gpio_put(PIN_ETH_RST, 1);
  gpio_init(PIN_ETH_INT); gpio_set_dir(PIN_ETH_INT, GPIO_IN); gpio_pull_up(PIN_ETH_INT);

  w5500_reset();
  tusb_init();

  absolute_time_t next = make_timeout_time_ms(400);
  bool on = false;
  while (true) {
    tud_task();
    if (absolute_time_diff_us(get_absolute_time(), next) <= 0) {
      on = !on;
      gpio_put(PIN_LED, on || !gpio_get(PIN_ETH_INT));
      next = make_timeout_time_ms(400);
    }
  }
}
