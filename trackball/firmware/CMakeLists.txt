cmake_minimum_required(VERSION 3.13)

# ISM Mouse firmware — TinyUSB HID mouse (original ISM, not QMK)
# Expects PICO_SDK_PATH in the environment.

include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(ism_trackball C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

add_executable(ism_trackball
  src/main.c
  src/usb_descriptors.c
)

target_include_directories(ism_trackball PRIVATE
  ${CMAKE_CURRENT_LIST_DIR}/src
)

target_link_libraries(ism_trackball
  pico_stdlib
  tinyusb_device
  tinyusb_board
  hardware_spi
  hardware_gpio
)

pico_enable_stdio_usb(ism_trackball 0)
pico_enable_stdio_uart(ism_trackball 0)

pico_add_extra_outputs(ism_trackball)

target_compile_definitions(ism_trackball PRIVATE
  CFG_TUSB_MCU=OPT_MCU_RP2040
)
