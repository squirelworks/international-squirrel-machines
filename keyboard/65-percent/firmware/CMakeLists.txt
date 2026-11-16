cmake_minimum_required(VERSION 3.13)

# ISM 65% keyboard firmware — TinyUSB HID keyboard (original ISM, not QMK)
# Expects PICO_SDK_PATH in the environment.

include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(ism_keyboard_65 C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

add_executable(ism_keyboard_65
  src/main.c
  src/usb_descriptors.c
  src/matrix.c
)

target_include_directories(ism_keyboard_65 PRIVATE
  ${CMAKE_CURRENT_LIST_DIR}/src
)

target_link_libraries(ism_keyboard_65
  pico_stdlib
  tinyusb_device
  tinyusb_board
  hardware_gpio
)

pico_enable_stdio_usb(ism_keyboard_65 0)
pico_enable_stdio_uart(ism_keyboard_65 0)

pico_add_extra_outputs(ism_keyboard_65)

target_compile_definitions(ism_keyboard_65 PRIVATE
  CFG_TUSB_MCU=OPT_MCU_RP2040
)
