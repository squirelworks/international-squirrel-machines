# ISM-FJ-1 bay I/O firmware — host bring-up profile (#84)
# Toolchain: gcc (C11). Optional Pico SDK port later — see README.

CC ?= gcc
CFLAGS ?= -std=c11 -Wall -Wextra -Werror -O2 -Iinclude
BUILD := build

.PHONY: all test run clean

all: $(BUILD)/ism_bay_host $(BUILD)/test_safe_state

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/ism_bay_fw.o: src/ism_bay_fw.c include/ism_bay_fw.h | $(BUILD)
	$(CC) $(CFLAGS) -c -o $@ src/ism_bay_fw.c

$(BUILD)/main_host.o: src/main_host.c include/ism_bay_fw.h | $(BUILD)
	$(CC) $(CFLAGS) -c -o $@ src/main_host.c

$(BUILD)/test_safe_state.o: tests/test_safe_state.c include/ism_bay_fw.h | $(BUILD)
	$(CC) $(CFLAGS) -c -o $@ tests/test_safe_state.c

$(BUILD)/ism_bay_host: $(BUILD)/ism_bay_fw.o $(BUILD)/main_host.o
	$(CC) $(CFLAGS) -o $@ $^

$(BUILD)/test_safe_state: $(BUILD)/ism_bay_fw.o $(BUILD)/test_safe_state.o
	$(CC) $(CFLAGS) -o $@ $^

test: $(BUILD)/test_safe_state
	./$(BUILD)/test_safe_state

run: $(BUILD)/ism_bay_host
	./$(BUILD)/ism_bay_host

clean:
	rm -rf $(BUILD)
