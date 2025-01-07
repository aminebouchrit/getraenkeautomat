#pragma once

#include <Arduino.h>

/**
 * Configures the stepper and moves the platform to its initial position.
 * Needs to be called before moving to a position.
 */
void setupStepper();

/**
 * Moves the platform to a specified position
 * @param position Position in centimeters
 */
void movePlatformTo(uint16_t position);