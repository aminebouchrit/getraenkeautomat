#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

#include "weight_sensor.h"
#include "fill_glass.h"
#include "status_light.h"
#include "platform.h"
#include "modes.h"

const uint8_t modeButtonPin = 35;
uint32_t timestamp = 0;
uint8_t mode = 0;

// I2C address: 0x27, 2 rows with 16 characters
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
    Serial.begin(9600);

    lcd.init();
    lcd.backlight();

    lcd.setCursor(0, 0);
    lcd.print("Running setup");

    setupStatusLight();
    showStatus(Status::YELLOW); // Setup is still ongoing

    calibrateWeightSensor();

    setupFillGlass();

    setupStepper();

    pinMode(modeButtonPin, INPUT);

    showStatus(Status::GREEN); // Setup is done
}

void loop() {
    if (digitalRead(modeButtonPin) == HIGH) {
        if (millis() - timestamp > 500) {
            // Activate the next mode if a certain time has passed since the last button press
            // (prevents one button press from being registered multiple times)
            mode = (mode + 1) % 3;
            timestamp = millis();
            lcd.clear();
        }
    }

    if (mode == 0) {
        operatingMode(lcd);
    } else if (mode == 1) {
        configListMode(lcd);
    } else if (mode == 2) {
        weighingMode(lcd);
    }
}