/*
 * ISM TKL keyboard firmware — TinyUSB HID on RP2040 (original ISM, not QMK).
 */

#include <string.h>
#include "pico/stdlib.h"
#include "tusb.h"
#include "matrix.h"

/* HID usage map for electrical ROW×COL (scripts/build_keyboard_75.py). */
static const uint8_t keymap[MATRIX_ROWS][MATRIX_COLS] = {
    /* r0 F-row */ {0x29, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x4C},
    /* r1 nums  */ {0x35, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x2D, 0x2E, 0x2A},
    /* r2 qwerty*/ {0x2B, 0x14, 0x1A, 0x08, 0x15, 0x17, 0x1C, 0x18, 0x0C, 0x12, 0x13, 0x2F, 0x30, 0x31},
    /* r3 asdf  */ {0x39, 0x04, 0x16, 0x07, 0x09, 0x0A, 0x0B, 0x0D, 0x0E, 0x0F, 0x33, 0x34, 0x28, 0x4B},
    /* r4 zxcv  */ {0xE1, 0x1D, 0x1B, 0x06, 0x19, 0x05, 0x11, 0x10, 0x36, 0x37, 0x38, 0xE5, 0x52, 0x4E},
    /* r5 mods  */ {0xE0, 0xE3, 0xE2, 0x2C, 0xE6, 0x00, 0x50, 0x51, 0x4F, 0x4A, 0x4D, 0x65, 0xE4, 0x49},
};

static uint16_t prev[MATRIX_ROWS];

void tud_hid_report_complete_cb(uint8_t instance, uint8_t const *report, uint16_t len) {
  (void)instance; (void)report; (void)len;
}

uint16_t tud_hid_get_report_cb(uint8_t instance, uint8_t report_id,
                               hid_report_type_t report_type, uint8_t *buffer, uint16_t reqlen) {
  (void)instance; (void)report_id; (void)report_type; (void)buffer; (void)reqlen;
  return 0;
}

void tud_hid_set_report_cb(uint8_t instance, uint8_t report_id,
                           hid_report_type_t report_type, uint8_t const *buffer, uint16_t bufsize) {
  (void)instance; (void)report_id; (void)report_type; (void)buffer; (void)bufsize;
}

static void hid_task(void) {
  if (!tud_hid_ready()) {
    return;
  }
  uint16_t now[MATRIX_ROWS];
  matrix_scan_full(now);
  uint8_t modifier = 0;
  uint8_t keys[6] = {0};
  unsigned ki = 0;
  for (unsigned r = 0; r < MATRIX_ROWS; r++) {
    for (unsigned c = 0; c < MATRIX_COLS; c++) {
      if (!(now[r] & (1u << c))) {
        continue;
      }
      uint8_t code = keymap[r][c];
      if (code == 0) {
        continue;
      }
      if (code >= 0xE0 && code <= 0xE7) {
        modifier |= (uint8_t)(1u << (code - 0xE0));
      } else if (ki < 6) {
        keys[ki++] = code;
      }
    }
    prev[r] = now[r];
  }
  tud_hid_keyboard_report(0, modifier, keys);
}

int main(void) {
  matrix_init();
  tusb_init();
  while (true) {
    tud_task();
    hid_task();
    sleep_ms(1);
  }
}
