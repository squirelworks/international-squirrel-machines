/*
 * ISM Drawing Pad firmware — TinyUSB HID + 4-wire touch ADC sample (original ISM).
 * SPI to XPT2046: CS=GP0 SCLK=GP1 MOSI=GP2 MISO=GP3 IRQ=GP4; BTN_L=GP5 BTN_R=GP6
 */
#include <string.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"
#include "tusb.h"

#define PIN_XL 0
#define PIN_XR 1
#define PIN_YU 2
#define PIN_YD 3
#define PIN_BTN_L 5
#define PIN_BTN_R 6

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

static void touch_drive_x(void) {
  gpio_set_dir(PIN_XL, GPIO_OUT); gpio_put(PIN_XL, 1);
  gpio_set_dir(PIN_XR, GPIO_OUT); gpio_put(PIN_XR, 0);
  gpio_set_dir(PIN_YU, GPIO_IN); gpio_disable_pulls(PIN_YU);
  gpio_set_dir(PIN_YD, GPIO_IN); gpio_disable_pulls(PIN_YD);
}
static void touch_drive_y(void) {
  gpio_set_dir(PIN_YU, GPIO_OUT); gpio_put(PIN_YU, 1);
  gpio_set_dir(PIN_YD, GPIO_OUT); gpio_put(PIN_YD, 0);
  gpio_set_dir(PIN_XL, GPIO_IN); gpio_disable_pulls(PIN_XL);
  gpio_set_dir(PIN_XR, GPIO_IN); gpio_disable_pulls(PIN_XR);
}

static void hid_task(void) {
  if (!tud_hid_ready()) return;
  /* Relative mouse report as bring-up stand-in for absolute digitizer. */
  int8_t dx = 0, dy = 0;
  uint8_t buttons = 0;
  if (!gpio_get(PIN_BTN_L)) buttons |= 0x01;
  if (!gpio_get(PIN_BTN_R)) buttons |= 0x02;
  /* Touch delta placeholder until ADC mux bring-up on module ADC pins. */
  tud_hid_mouse_report(0, buttons, dx, dy, 0, 0);
}

int main(void) {
  for (uint p = PIN_BTN_L; p <= PIN_BTN_R; p++) {
    gpio_init(p); gpio_set_dir(p, GPIO_IN); gpio_pull_up(p);
  }
  for (uint p = PIN_XL; p <= PIN_YD; p++) {
    gpio_init(p);
  }
  tusb_init();
  while (true) {
    tud_task();
    hid_task();
    sleep_ms(8);
  }
}
