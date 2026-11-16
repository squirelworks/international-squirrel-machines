/*
 * ISM CPU module firmware — SPI flash probe + UART heartbeat to motherboard BMC.
 * Module pad N → GP(N-2) for pads 2..13 (ISM convention).
 */
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/spi.h"
#include "hardware/uart.h"
#include "tusb.h"

#define PIN_CLK     0
#define PIN_CS      1
#define PIN_DQ0     2  /* MOSI */
#define PIN_DQ1     3  /* MISO */
#define PIN_TX      10 /* pad 12 → BMC CPU_RX */
#define PIN_RX      11 /* pad 13 ← BMC CPU_TX */
#define PIN_LED     18 /* pad 20 */

#define FLASH_JEDEC_ID 0x9F

void tud_hid_report_complete_cb(uint8_t i, uint8_t const *r, uint16_t n) {
  (void)i; (void)r; (void)n;
}
uint16_t tud_hid_get_report_cb(uint8_t i, uint8_t id, hid_report_type_t t, uint8_t *b, uint16_t n) {
  (void)i; (void)id; (void)t; (void)b; (void)n; return 0;
}
void tud_hid_set_report_cb(uint8_t i, uint8_t id, hid_report_type_t t, uint8_t const *b, uint16_t n) {
  (void)i; (void)id; (void)t; (void)b; (void)n;
}

static void flash_jedec(uint8_t id[3]) {
  uint8_t cmd = FLASH_JEDEC_ID;
  gpio_put(PIN_CS, 0);
  spi_write_blocking(spi0, &cmd, 1);
  spi_read_blocking(spi0, 0, id, 3);
  gpio_put(PIN_CS, 1);
}

int main(void) {
  gpio_init(PIN_LED); gpio_set_dir(PIN_LED, GPIO_OUT); gpio_put(PIN_LED, 0);
  gpio_init(PIN_CS); gpio_set_dir(PIN_CS, GPIO_OUT); gpio_put(PIN_CS, 1);

  spi_init(spi0, 8 * 1000 * 1000);
  gpio_set_function(PIN_CLK, GPIO_FUNC_SPI);
  gpio_set_function(PIN_DQ0, GPIO_FUNC_SPI);
  gpio_set_function(PIN_DQ1, GPIO_FUNC_SPI);

  uart_init(uart0, 115200);
  gpio_set_function(PIN_TX, GPIO_FUNC_UART);
  gpio_set_function(PIN_RX, GPIO_FUNC_UART);

  tusb_init();

  uint8_t jedec[3] = {0};
  flash_jedec(jedec);

  while (true) {
    tud_task();
    uart_puts(uart0, "ISM-CPU\r\n");
    gpio_put(PIN_LED, 1);
    sleep_ms(50);
    gpio_put(PIN_LED, 0);
    sleep_ms(950);
    (void)jedec;
  }
}
