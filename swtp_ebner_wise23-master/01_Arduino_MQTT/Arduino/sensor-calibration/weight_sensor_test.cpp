#include <Arduino.h>
#include "HX711.h"

const uint8_t loadcellDOutPin = 2;
const uint8_t loadcellSckPin = 3;

// Calibration factor = calibration reading / weight of object = -17054 / 43,12 g
// (to recalibrate, use "weight_sensor_calibration.cpp")
const float calibrationFactor = -395.5F;

HX711 scale;

void setup() {
  Serial.begin(9600);
  scale.begin(loadcellDOutPin, loadcellSckPin);

  // Calibration
  Serial.println("Calibrating, please remove any weights from the scale.");
  delay(3000);
  scale.tare();
  scale.set_scale(calibrationFactor); 
  Serial.println("Done.");
}

void loop() {
  if (scale.wait_ready_timeout()) {
    int32_t weight = scale.get_units(10);
    Serial.print("Weight: ");
    Serial.print(weight);
    Serial.println(" g");
  } else {
    Serial.println("HX711 not found.");
  }
  delay(1000);
}