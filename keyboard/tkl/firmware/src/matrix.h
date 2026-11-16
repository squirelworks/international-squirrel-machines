#pragma once
#include <stdint.h>
#define MATRIX_ROWS 6
#define MATRIX_COLS 15
void matrix_init(void);
void matrix_scan(uint8_t out[MATRIX_ROWS]);
void matrix_scan_full(uint16_t out[MATRIX_ROWS]);
