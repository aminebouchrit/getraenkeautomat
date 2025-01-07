#pragma once

#include <Arduino.h>

enum class Status {
    GREEN, YELLOW, RED, OFF
};

/**
 * Configures the pins for the status light.
 * Needs to be called before showing a color or using the buzzer.
 */
void setupStatusLight();

/**
 * Enables the specified color on the status light.
 * 
 * @param status The color to show
 */
void showStatus(Status status);

/**
 * Enables the built-in buzzer.
 * @param length The length of the alarm (in ms)
 * @param pause Waiting time after the alarm (in ms)
 */
void alarm(uint32_t length, uint32_t pause);