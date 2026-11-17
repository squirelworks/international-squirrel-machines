/*
 * ISM Thumb Drive — SPI NOR bring-up + activity LED heartbeat.
 * Full USB MSC is a follow-up. Module pad N → GP(N-2).
 */
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/spi.h"
#include "tusb.h"

#define PIN_FLASH_CLK  0  /* pad 2 */
#define PIN_FLASH_MOSI 1  /* pad 3 */
#define PIN_FLASH_MISO 2  /* pad 4 */
#define PIN_FLASH_CS   3  /* pad 5 */
#define PIN_LED        17 /* pad 19 */

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

  spi_init(spi0, 1 * 1000 * 1000);
  gpio_set_function(PIN_FLASH_CLK, GPIO_FUNC_SPI);
  gpio_set_function(PIN_FLASH_MOSI, GPIO_FUNC_SPI);
  gpio_set_function(PIN_FLASH_MISO, GPIO_FUNC_SPI);
  gpio_init(PIN_FLASH_CS); gpio_set_dir(PIN_FLASH_CS, GPIO_OUT); gpio_put(PIN_FLASH_CS, 1);

  tusb_init();

  while (true) {
    tud_task();
    gpio_put(PIN_LED, 1);
    sleep_ms(80);
    gpio_put(PIN_LED, 0);
    sleep_ms(920);
  }
}
