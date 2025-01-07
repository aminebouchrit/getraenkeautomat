#include <AccelStepper.h>

#include "platform.h"

const uint8_t enablePin = 12;
AccelStepper stepper(AccelStepper::DRIVER, 11, 13);

const uint8_t magnetPin = 9;

const uint8_t stepperButtonPin = 7;

const uint16_t cmToStepsFactor = 385;

void setupStepper() {
    // Configure pins and speed
    pinMode(enablePin, OUTPUT);
    digitalWrite(enablePin, LOW);
    pinMode(stepperButtonPin, INPUT);
    pinMode(magnetPin, OUTPUT);

    stepper.setMaxSpeed(1000);
    stepper.setAcceleration(1000.0F);

    // Hold the platform with magnets
    digitalWrite(magnetPin, HIGH);

    // Move the platform until the stepper button is reached
    stepper.moveTo(50000); // high value to ensure that the position is reached
    while (digitalRead(stepperButtonPin) == HIGH) {
        // The button is LOW active, so digitalRead() returns LOW if it is pressed
        // and not HIGH as with the other buttons
        stepper.run();
    }

    // Set this position as the initial position
    stepper.setCurrentPosition(0);

    // Release the platform
    digitalWrite(magnetPin, LOW);
}

void movePlatformTo(uint16_t position) {
    // Hold the platform with magnets
    digitalWrite(magnetPin, HIGH);

    uint32_t steps = position * cmToStepsFactor; // convert cm to steps
    stepper.runToNewPosition(-steps); // -: other direction (away from the stepper button)

    // Release the platform
    digitalWrite(magnetPin, LOW);
}