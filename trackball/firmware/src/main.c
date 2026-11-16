/*
 * ISM Trackball firmware — TinyUSB HID mouse on RP2040 (Pico SDK)
 * Original International Squirrel Machines work (not QMK).
 *
 * GPIO map (matches mouse README / planned PCB):
 *   BTN_L  GP0   BTN_R GP1   BTN_M GP2
 *   ENC_A  GP3   ENC_B GP4   ENC_SW GP5
 *   SENS_SCLK GP6  SENS_MOSI GP7  SENS_MISO GP8
 *   SENS_NCS GP9   SENS_MOTION GP10  SENS_RESET GP11
 */

#include <string.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/spi.h"
#include "tusb.h"

#define PIN_BTN_L       0
#define PIN_BTN_R       1
#define PIN_BTN_M       2
#define PIN_ENC_A       3
#define PIN_ENC_B       4
#define PIN_ENC_SW      5
#define PIN_SENS_SCLK   6
#define PIN_SENS_MOSI   7
#define PIN_SENS_MISO   8
#define PIN_SENS_NCS    9
#define PIN_SENS_MOTION 10
#define PIN_SENS_RESET  11

static int8_t enc_delta;
static uint8_t enc_prev;

static void gpio_init_inputs(void) {
  const uint pins[] = {
      PIN_BTN_L, PIN_BTN_R, PIN_BTN_M, PIN_ENC_A, PIN_ENC_B, PIN_ENC_SW, PIN_SENS_MOTION};
  for (unsigned i = 0; i < count_of(pins); i++) {
    gpio_init(pins[i]);
    gpio_set_dir(pins[i], GPIO_IN);
    gpio_pull_up(pins[i]);
  }

  gpio_init(PIN_SENS_NCS);
  gpio_set_dir(PIN_SENS_NCS, GPIO_OUT);
  gpio_put(PIN_SENS_NCS, 1);

  gpio_init(PIN_SENS_RESET);
  gpio_set_dir(PIN_SENS_RESET, GPIO_OUT);
  gpio_put(PIN_SENS_RESET, 1);

  spi_init(spi0, 1 * 1000 * 1000);
  gpio_set_function(PIN_SENS_SCLK, GPIO_FUNC_SPI);
  gpio_set_function(PIN_SENS_MOSI, GPIO_FUNC_SPI);
  gpio_set_function(PIN_SENS_MISO, GPIO_FUNC_SPI);
}

static void encoder_poll(void) {
  uint8_t a = (uint8_t)gpio_get(PIN_ENC_A);
  uint8_t b = (uint8_t)gpio_get(PIN_ENC_B);
  uint8_t cur = (uint8_t)((a << 1) | b);
  /* Gray-code quadrature: 00->01->11->10 */
  static const int8_t table[16] = {
      0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0};
  enc_delta += table[(enc_prev << 2) | cur];
  enc_prev = cur;
}

/* Stub optical read — returns zeros until ISM sensor bring-up. */
static void sensor_read_delta(int8_t *dx, int8_t *dy) {
  *dx = 0;
  *dy = 0;
  if (!gpio_get(PIN_SENS_MOTION)) {
    /* Motion asserted (active low): SPI transaction would go here. */
    gpio_put(PIN_SENS_NCS, 0);
    uint8_t tx[3] = {0x02, 0x00, 0x00}; /* placeholder delta registers */
    uint8_t rx[3] = {0};
    spi_write_read_blocking(spi0, tx, rx, 3);
    gpio_put(PIN_SENS_NCS, 1);
    *dx = (int8_t)rx[1];
    *dy = (int8_t)rx[2];
  }
}

void tud_hid_report_complete_cb(uint8_t instance, uint8_t const *report, uint16_t len) {
  (void)instance;
  (void)report;
  (void)len;
}

uint16_t tud_hid_get_report_cb(uint8_t instance, uint8_t report_id,
                               hid_report_type_t report_type, uint8_t *buffer, uint16_t reqlen) {
  (void)instance;
  (void)report_id;
  (void)report_type;
  (void)buffer;
  (void)reqlen;
  return 0;
}

void tud_hid_set_report_cb(uint8_t instance, uint8_t report_id,
                           hid_report_type_t report_type, uint8_t const *buffer, uint16_t bufsize) {
  (void)instance;
  (void)report_id;
  (void)report_type;
  (void)buffer;
  (void)bufsize;
}

static void hid_task(void) {
  if (!tud_hid_ready()) {
    return;
  }

  encoder_poll();

  uint8_t buttons = 0;
  if (!gpio_get(PIN_BTN_L)) {
    buttons |= MOUSE_BUTTON_LEFT;
  }
  if (!gpio_get(PIN_BTN_R)) {
    buttons |= MOUSE_BUTTON_RIGHT;
  }
  if (!gpio_get(PIN_BTN_M) || !gpio_get(PIN_ENC_SW)) {
    buttons |= MOUSE_BUTTON_MIDDLE;
  }

  int8_t dx = 0, dy = 0;
  sensor_read_delta(&dx, &dy);

  int8_t wheel = enc_delta;
  enc_delta = 0;

  if (buttons || dx || dy || wheel) {
    tud_hid_mouse_report(0, buttons, dx, dy, wheel, 0);
  }
}

int main(void) {
  gpio_init_inputs();
  tusb_init();

  while (true) {
    tud_task();
    hid_task();
    tight_loop_contents();
  }
}
