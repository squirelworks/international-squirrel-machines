/*
 * ISM Full Size matrix — ROW0–6 / COL0–14
 * ROW5 pad27→GP19; COL14 pad28→GP20; ROW6 pad29→GP21
 */
#include "matrix.h"
#include "hardware/gpio.h"
#include "pico/stdlib.h"
static const uint row_pins[MATRIX_ROWS] = {0,1,2,3,4,19,21};
static const uint col_pins[MATRIX_COLS] = {5,6,7,8,9,10,11,12,13,14,15,16,17,18,20};
void matrix_init(void){
  for(unsigned r=0;r<MATRIX_ROWS;r++){gpio_init(row_pins[r]);gpio_set_dir(row_pins[r],GPIO_IN);gpio_disable_pulls(row_pins[r]);}
  for(unsigned c=0;c<MATRIX_COLS;c++){gpio_init(col_pins[c]);gpio_set_dir(col_pins[c],GPIO_IN);gpio_pull_up(col_pins[c]);}
}
void matrix_scan(uint8_t out[MATRIX_ROWS]){uint16_t f[MATRIX_ROWS];matrix_scan_full(f);for(unsigned r=0;r<MATRIX_ROWS;r++)out[r]=(uint8_t)(f[r]&0xFF);}
void matrix_scan_full(uint16_t out[MATRIX_ROWS]){
  for(unsigned r=0;r<MATRIX_ROWS;r++){
    for(unsigned i=0;i<MATRIX_ROWS;i++){gpio_set_dir(row_pins[i],i==r?GPIO_OUT:GPIO_IN);if(i==r)gpio_put(row_pins[i],0);}
    sleep_us(5); uint16_t bits=0;
    for(unsigned c=0;c<MATRIX_COLS;c++) if(!gpio_get(col_pins[c])) bits|=(uint16_t)(1u<<c);
    out[r]=bits; gpio_set_dir(row_pins[r],GPIO_IN);
  }
}
