// Calibration code based on: https://randomnerdtutorials.com/arduino-load-cell-hx711/
#include <Arduino.h>
#include "HX711.h"

const uint8_t loadcellDOutPin = 2;
const uint8_t loadcellSckPin = 3;

HX711 scale;

void setup() {
    Serial.begin(9600);
    scale.begin(loadcellDOutPin, loadcellSckPin);
}

void loop() {
    if (scale.is_ready()) {
        scale.set_scale();

        Serial.println("Tare... remove any weights from the scale.");
        delay(5000);
        scale.tare();
        Serial.println("Tare done...");

        Serial.print("Place a known weight on the scale...");
        delay(5000);
        int32_t reading = scale.get_units(10);
        Serial.print("Result: ");
        Serial.println(reading);
    } else {
        Serial.println("HX711 not found.");
    }
    delay(1000);
}