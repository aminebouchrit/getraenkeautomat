#include <Arduino.h>
#include <HX711.h>

#include "weight_sensor.h"

const uint8_t loadcellDOutPin = 2;
const uint8_t loadcellSckPin = 3;

// Calibration factor = calibration reading / weight of object = -17054 / 43,12 g
// (to recalibrate, use "weight_sensor_calibration.cpp")
const float calibrationFactor = -395.5F;

HX711 scale;

void calibrateWeightSensor() {
    scale.begin(loadcellDOutPin, loadcellSckPin);
    scale.tare();
    scale.set_scale(calibrationFactor); 
}

int32_t measureWeight() {
    // Calculate the average of 10 readings
    return scale.get_units(10);
}