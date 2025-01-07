#pragma once

/**
 * Calibrates the weight sensor.
 * Needs to be called before measuring the weight.
 */
void calibrateWeightSensor();

/**
 * Waits until the sensor is ready and then returns the current weight.
 * @return The measured weight
 */
int32_t measureWeight();