/*
 * ISM Memory SPD probe — TinyUSB + I2C reader for module J2 header.
 * Wire Pico GP4=SDA, GP5=SCL to memory/J2 pins 3/4; 3V3/GND to 1/2.
 * Original International Squirrel Machines work.
 */
#include <stdio.h>
#include <string.h>
#include "pico/stdlib.h"
#include "hardware/i2c.h"
#include "tusb.h"

#define I2C_PORT i2c0
#define PIN_SDA 4
#define PIN_SCL 5
#define SPD_ADDR 0x50

int main(void) {
  stdio_init_all();
  tusb_init();
  i2c_init(I2C_PORT, 100 * 1000);
  gpio_set_function(PIN_SDA, GPIO_FUNC_I2C);
  gpio_set_function(PIN_SCL, GPIO_FUNC_I2C);
  gpio_pull_up(PIN_SDA);
  gpio_pull_up(PIN_SCL);

  while (true) {
    tud_task();
    uint8_t reg = 0;
    uint8_t buf[16];
    int wr = i2c_write_blocking(I2C_PORT, SPD_ADDR, &reg, 1, true);
    int rd = i2c_read_blocking(I2C_PORT, SPD_ADDR, buf, sizeof buf, false);
    if (wr == 1 && rd == (int)sizeof buf) {
      printf("ISM SPD:");
      for (unsigned i = 0; i < sizeof buf; i++) {
        printf(" %02x", buf[i]);
      }
      printf("\n");
    } else {
      printf("ISM SPD: no ack (check J2)\n");
    }
    sleep_ms(1000);
  }
}
