/*
 * ISM Macro Pad firmware — TinyUSB HID on RP2040 (original ISM, not QMK).
 * 4×4 matrix; default map = F1–F16 (HID 0x3A..0x49).
 */

#include <string.h>
#include "pico/stdlib.h"
#include "tusb.h"
#include "matrix.h"

static const uint8_t keymap[MATRIX_ROWS][MATRIX_COLS] = {
    /* r0 */ {0x3A, 0x3B, 0x3C, 0x3D}, /* F1-F4 */
    /* r1 */ {0x3E, 0x3F, 0x40, 0x41}, /* F5-F8 */
    /* r2 */ {0x42, 0x43, 0x44, 0x45}, /* F9-F12 */
    /* r3 */ {0x68, 0x69, 0x6A, 0x6B}, /* F13-F16 */
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
