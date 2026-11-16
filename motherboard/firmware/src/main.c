/*
 * ISM Motherboard BMC firmware — board-ID I2C + SPI expansion stub + activity LED.
 * Module pad N maps to GP(N-2) for pads 2..13 (ISM convention).
 */
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/i2c.h"
#include "tusb.h"

#define PIN_CLK      0
#define PIN_CS       1
#define PIN_SDA      8   /* pad 10 */
#define PIN_SCL      9   /* pad 11 */
#define PIN_LED_ACT  18  /* pad 20 */
#define PIN_EXP_CS   23  /* pad 25 */
#define PIN_CPU_RST  17  /* pad 19 */

#define EEPROM_ADDR  0x50

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
  gpio_init(PIN_LED_ACT); gpio_set_dir(PIN_LED_ACT, GPIO_OUT); gpio_put(PIN_LED_ACT, 0);
  gpio_init(PIN_CS); gpio_set_dir(PIN_CS, GPIO_OUT); gpio_put(PIN_CS, 1);
  gpio_init(PIN_EXP_CS); gpio_set_dir(PIN_EXP_CS, GPIO_OUT); gpio_put(PIN_EXP_CS, 1);
  gpio_init(PIN_CPU_RST); gpio_set_dir(PIN_CPU_RST, GPIO_OUT); gpio_put(PIN_CPU_RST, 1);

  i2c_init(i2c0, 100 * 1000);
  gpio_set_function(PIN_SDA, GPIO_FUNC_I2C);
  gpio_set_function(PIN_SCL, GPIO_FUNC_I2C);
  gpio_pull_up(PIN_SDA);
  gpio_pull_up(PIN_SCL);

  tusb_init();

  uint8_t addr = 0;
  uint8_t id = 0;
  i2c_write_blocking(i2c0, EEPROM_ADDR, &addr, 1, true);
  i2c_read_blocking(i2c0, EEPROM_ADDR, &id, 1, false);

  while (true) {
    tud_task();
    gpio_put(PIN_LED_ACT, 1);
    sleep_ms(40);
    gpio_put(PIN_LED_ACT, 0);
    sleep_ms(960);
    (void)id;
  }
}
