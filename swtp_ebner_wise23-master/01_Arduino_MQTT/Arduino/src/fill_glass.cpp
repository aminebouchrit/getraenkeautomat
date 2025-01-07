#include "fill_glass.h"

const uint8_t continueButtonPin = 22;

void setupFillGlass() {
    pinMode(continueButtonPin, INPUT);
}

void waitForGlass(LiquidCrystal_I2C &lcd, const Order &order) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Place ");
    lcd.print(order.glassWeight);
    lcd.print(" g gl.");

    // Wait until the sensor detects a glass of the correct type
    // A variation of up to 10 g is allowed
    int32_t measuredWeight = measureWeight();

    while (!(measuredWeight >= order.glassWeight - 10 && measuredWeight <= order.glassWeight + 10)) {
        // Wait a second between measurements
        delay(1000);

        if (measuredWeight > 50) {
            // There was a weight detected, but it does not match the glass type
            lcd.setCursor(0, 1);
            lcd.print("Wrong glass: ");
            lcd.print(measuredWeight);
            lcd.print(" g");
        }

        measuredWeight = measureWeight();
    }

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Glass detected.");

    // Show that the machine is busy
    showStatus(Status::YELLOW);

    // Wait to ensure that the user does not touch the glass anymore and
    // then remove the weight of the glass from the measurement
    delay(3000);
    calibrateWeightSensor();
}

void fillGlass(LiquidCrystal_I2C &lcd, uint16_t stationID, uint8_t pumpPin, int32_t gramsToFill) {
    pinMode(pumpPin, OUTPUT);

    // Wait until the glass is full
    uint32_t lastChange = millis();
    int32_t lastWeight = measureWeight();
    FillState state = FillState::FILLING;

    while (lastWeight < gramsToFill) {
        int32_t newWeight = measureWeight();
        lcd.clear();

        switch (state) {
            case FillState::FILLING:
            {
                if (newWeight != lastWeight) {
                    lastWeight = newWeight;
                    lastChange = millis();
                }

                lcd.setCursor(0, 0);
                lcd.print("Filling glass");

                if (newWeight < -20) {
                    // Disable pump if the glass is removed
                    state = FillState::GLASS_REMOVED;

                    // Send error message to python bridge
                    sendErrorToSerial(1, 0);
                } else if ((millis() - lastChange) > 5000) {
                    // If the weight has not changed for more than 5 seconds, the bottle must be empty
                    state = FillState::BOTTLE_EMPTY;

                    // Send error message to python bridge
                    sendErrorToSerial(0, stationID);
                } else {
                    // Activate the pump
                    digitalWrite(pumpPin, HIGH);
                }
                break;
            }
            case FillState::GLASS_REMOVED:
            {
                digitalWrite(pumpPin, LOW);

                lcd.setCursor(0, 0);
                lcd.print("Glass removed");

                // Show error with a blinking light and an alarm
                showStatus(Status::RED);
                delay(200);
                showStatus(Status::OFF);
                delay(200);
                alarm(1000, 1000);

                if (digitalRead(continueButtonPin) == HIGH) {
                    // Restart pump after placing glass again
                    showStatus(Status::YELLOW);

                    // Send info message to python bridge
                    sendInfoToSerial(1);

                    state = FillState::FILLING;
                    lastChange = millis();
                }
                break;
            }
            case FillState::BOTTLE_EMPTY:
            {
                digitalWrite(pumpPin, LOW);

                lcd.setCursor(0, 0);
                lcd.print("Bottle empty");

                // Show error with a blinking light
                showStatus(Status::OFF);
                delay(400);
                showStatus(Status::RED);
                delay(400);

                if (digitalRead(continueButtonPin) == HIGH) {
                    // Restart pump after refill
                    showStatus(Status::YELLOW);

                    // Send info message to python bridge
                    sendInfoToSerial(1);

                    state = FillState::FILLING;
                    lastChange = millis();
                }
                break;
            }
        }

        // Print weight
        lcd.setCursor(0, 1);
        lcd.print(newWeight);
        lcd.print(" g");
    }

    // The glass is full, so disable the pump
    digitalWrite(pumpPin, LOW);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Filled in:");
    lcd.setCursor(0, 1);
    lcd.print(lastWeight);
    lcd.print(" g");
}

void waitUntilGlassIsRemoved(LiquidCrystal_I2C &lcd, const Order &order) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Remove glass");

    // If the user has not removed the glass after 5 seconds, enable an alarm as a reminder
    // A variation of up to 20 g is allowed
    delay(5000);

    while (measureWeight() > -(order.glassWeight - 20)) {
        alarm(1000, 3000);
    }

    // Recalibrate after the glass is removed
    calibrateWeightSensor();

    // Show that the machine is ready
    showStatus(Status::GREEN);
}