/*
 * ISM 60% key matrix scan — ROW drivers / COL inputs (diode toward COL)
 * GPIO map matches keyboard/60-percent/README.md Steve interface.
 */

#include "matrix.h"
#include "hardware/gpio.h"
#include "pico/stdlib.h"

/* ROW0..ROW4 on GP0..GP4; COL0..COL13 on GP5..GP18 (skipping holes per PCB) */
static const uint row_pins[MATRIX_ROWS] = {0, 1, 2, 3, 4};
static const uint col_pins[MATRIX_COLS] = {
    5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18};

void matrix_init(void) {
  for (unsigned r = 0; r < MATRIX_ROWS; r++) {
    gpio_init(row_pins[r]);
    gpio_set_dir(row_pins[r], GPIO_IN);
    gpio_disable_pulls(row_pins[r]);
  }
  for (unsigned c = 0; c < MATRIX_COLS; c++) {
    gpio_init(col_pins[c]);
    gpio_set_dir(col_pins[c], GPIO_IN);
    gpio_pull_up(col_pins[c]);
  }
}

void matrix_scan(uint8_t out[MATRIX_ROWS]) {
  for (unsigned r = 0; r < MATRIX_ROWS; r++) {
    /* Drive one row low */
    for (unsigned i = 0; i < MATRIX_ROWS; i++) {
      gpio_set_dir(row_pins[i], i == r ? GPIO_OUT : GPIO_IN);
      if (i == r) {
        gpio_put(row_pins[i], 0);
      }
    }
    sleep_us(5);
    uint8_t bits = 0;
    for (unsigned c = 0; c < 8 && c < MATRIX_COLS; c++) {
      if (!gpio_get(col_pins[c])) {
        bits |= (uint8_t)(1u << c);
      }
    }
    /* High columns packed into a second pass for HID layer — store low 8 here;
     * main.c reads full cols via matrix_scan_full if needed. */
    out[r] = bits;
    gpio_set_dir(row_pins[r], GPIO_IN);
  }
}

void matrix_scan_full(uint16_t out[MATRIX_ROWS]) {
  for (unsigned r = 0; r < MATRIX_ROWS; r++) {
    for (unsigned i = 0; i < MATRIX_ROWS; i++) {
      gpio_set_dir(row_pins[i], i == r ? GPIO_OUT : GPIO_IN);
      if (i == r) {
        gpio_put(row_pins[i], 0);
      }
    }
    sleep_us(5);
    uint16_t bits = 0;
    for (unsigned c = 0; c < MATRIX_COLS; c++) {
      if (!gpio_get(col_pins[c])) {
        bits |= (uint16_t)(1u << c);
      }
    }
    out[r] = bits;
    gpio_set_dir(row_pins[r], GPIO_IN);
  }
}
