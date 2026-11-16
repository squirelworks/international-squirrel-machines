/*
 * ISM Graphics Card firmware — SPI slave stub + EDID I2C + framebuffer probe.
 * Module pad N → GP(N-2) for pads 2..13 (ISM convention).
 */
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/spi.h"
#include "hardware/i2c.h"
#include "tusb.h"

#define PIN_EXP_SCK  0
#define PIN_EXP_MOSI 1
#define PIN_EXP_MISO 2
#define PIN_EXP_CS   3
#define PIN_FB_CLK   4
#define PIN_FB_CS    5
#define PIN_HPD      10
#define PIN_LED      17  /* pad 19 */
#define PIN_HDMI_SDA 18  /* pad 20 */
#define PIN_HDMI_SCL 19  /* pad 21 */

#define EDID_ADDR 0x50

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
  gpio_init(PIN_FB_CS); gpio_set_dir(PIN_FB_CS, GPIO_OUT); gpio_put(PIN_FB_CS, 1);
  gpio_init(PIN_HPD); gpio_set_dir(PIN_HPD, GPIO_IN); gpio_pull_down(PIN_HPD);

  spi_init(spi0, 8 * 1000 * 1000);
  gpio_set_function(PIN_FB_CLK, GPIO_FUNC_SPI);

  i2c_init(i2c0, 100 * 1000);
  gpio_set_function(PIN_HDMI_SDA, GPIO_FUNC_I2C);
  gpio_set_function(PIN_HDMI_SCL, GPIO_FUNC_I2C);
  gpio_pull_up(PIN_HDMI_SDA);
  gpio_pull_up(PIN_HDMI_SCL);

  tusb_init();

  uint8_t addr = 0;
  uint8_t edid0 = 0;
  i2c_write_blocking(i2c0, EDID_ADDR, &addr, 1, true);
  i2c_read_blocking(i2c0, EDID_ADDR, &edid0, 1, false);

  while (true) {
    tud_task();
    bool hpd = gpio_get(PIN_HPD);
    gpio_put(PIN_LED, hpd);
    sleep_ms(100);
    (void)edid0;
  }
}
