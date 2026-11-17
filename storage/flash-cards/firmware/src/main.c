/*
 * ISM Flash Cards reader — SPI pin bring-up + card-detect LED.
 * Full USB MSC / SD protocol is a follow-up. Module pad N → GP(N-2).
 */
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/spi.h"
#include "tusb.h"

#define PIN_SD_CLK  0  /* pad 2 */
#define PIN_SD_MOSI 1  /* pad 3 */
#define PIN_SD_MISO 2  /* pad 4 */
#define PIN_SD_CS   3  /* pad 5 */
#define PIN_SD_DET  4  /* pad 6 */
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

  spi_init(spi0, 400 * 1000);
  gpio_set_function(PIN_SD_CLK, GPIO_FUNC_SPI);
  gpio_set_function(PIN_SD_MOSI, GPIO_FUNC_SPI);
  gpio_set_function(PIN_SD_MISO, GPIO_FUNC_SPI);
  gpio_init(PIN_SD_CS); gpio_set_dir(PIN_SD_CS, GPIO_OUT); gpio_put(PIN_SD_CS, 1);
  gpio_init(PIN_SD_DET); gpio_set_dir(PIN_SD_DET, GPIO_IN); gpio_pull_up(PIN_SD_DET);

  tusb_init();

  while (true) {
    tud_task();
    bool present = !gpio_get(PIN_SD_DET); /* active-low detect with pull-up */
    gpio_put(PIN_LED, present);
    sleep_ms(50);
  }
}
