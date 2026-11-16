/*
 * ISM Sound Card firmware — SPI slave stub + I2S pin bring-up for PCM5102A.
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
#define PIN_I2S_BCLK  4  /* pad 6 */
#define PIN_I2S_DOUT  5  /* pad 7 */
#define PIN_I2S_LRCLK 6  /* pad 8 */
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

int main(void) {
  gpio_init(PIN_LED); gpio_set_dir(PIN_LED, GPIO_OUT); gpio_put(PIN_LED, 0);

  /* EXP SPI slave bring-up (host clocks; pins idle-ready) */
  gpio_init(PIN_EXP_CS); gpio_set_dir(PIN_EXP_CS, GPIO_IN); gpio_pull_up(PIN_EXP_CS);
  gpio_set_function(PIN_EXP_SCK, GPIO_FUNC_SPI);
  gpio_set_function(PIN_EXP_MOSI, GPIO_FUNC_SPI);
  gpio_set_function(PIN_EXP_MISO, GPIO_FUNC_SPI);

  /* I2S bit-clock / data / LRCLK as outputs (PIO/I2S driver follow-up) */
  gpio_init(PIN_I2S_BCLK); gpio_set_dir(PIN_I2S_BCLK, GPIO_OUT); gpio_put(PIN_I2S_BCLK, 0);
  gpio_init(PIN_I2S_DOUT); gpio_set_dir(PIN_I2S_DOUT, GPIO_OUT); gpio_put(PIN_I2S_DOUT, 0);
  gpio_init(PIN_I2S_LRCLK); gpio_set_dir(PIN_I2S_LRCLK, GPIO_OUT); gpio_put(PIN_I2S_LRCLK, 0);

  tusb_init();

  absolute_time_t next = make_timeout_time_ms(500);
  bool on = false;
  while (true) {
    tud_task();
    if (absolute_time_diff_us(get_absolute_time(), next) <= 0) {
      on = !on;
      gpio_put(PIN_LED, on);
      next = make_timeout_time_ms(500);
    }
  }
}
