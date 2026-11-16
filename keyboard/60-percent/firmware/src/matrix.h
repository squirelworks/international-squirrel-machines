#pragma once

#include <stdint.h>
#include <stdbool.h>

#define MATRIX_ROWS 5
#define MATRIX_COLS 14

void matrix_init(void);
void matrix_scan(uint8_t out[MATRIX_ROWS]);
void matrix_scan_full(uint16_t out[MATRIX_ROWS]);
