#include "modes.h"

uint32_t lastChange = 0;

void processOrder(LiquidCrystal_I2C &lcd, const Order &order) {
    waitForGlass(lcd, order);

    int32_t totalWeight = 0;
    for (uint16_t i = 0; i < order.numEntries; i++) {
        // Move the platform to the correct position
        Station station = getStation(order.entries[i].stationID);
        movePlatformTo(station.position);

        // Wait to ensure that the platform is stationary
        delay(1000);

        // Action depending on the station type
        if (station.type == StationType::BOTTLE) {
            totalWeight += order.entries[i].value;
            fillGlass(lcd, station.id, station.data.bottleData.pumpPin, totalWeight);
        }

        // Wait to ensure that the filling of the glass is completed
        delay(1000);
    }

    // Move back to the starting position
    movePlatformTo(0);

    waitUntilGlassIsRemoved(lcd, order);
}

void operatingMode(LiquidCrystal_I2C &lcd) {
    lcd.setCursor(0, 0);
    lcd.print("Operating mode");
    lcd.setCursor(0, 1);
    lcd.print("Ready");

    // Wait for data from serial input
    if (Serial.available()) {
        String type = Serial.readStringUntil(',');

        if (type.equals("config")) {
            Station station = readStationFromSerial();
            bool success = addStation(station);

            if (!success) {
                // Send configuration error to python bridge
                sendErrorToSerial(4, 0);
            }
        } else if (type.equals("order")) {
            Order order = readOrderFromSerial();

            // Check if the order can be processed with the current configuration
            if (isOrderValid(order)) {
                // Process the order
                processOrder(lcd, order);

                // Send success message to python bridge
                sendInfoToSerial(0);
            } else {
                // Send error message to python bridge
                uint16_t stationID = getMissingConfiguration(order);
                sendErrorToSerial(2, stationID);

                // Show error on the LCD
                lcd.clear();
                lcd.setCursor(0, 0);
                lcd.print("Missing config");
                lcd.setCursor(0, 1);
                lcd.print("for id: ");
                lcd.print(stationID);
                delay(4000);
                lcd.clear();
            }

            // Free memory
            freeOrder(order);
        } else if (type.equals("led")) {
            LEDConfig config = readLEDConfigFromSerial();
            bool success = showLEDPattern(config);

            if (!success) {
                // Send error message to python bridge
                sendErrorToSerial(3, 0);
            }
        }
    }
}

void configListMode(LiquidCrystal_I2C &lcd) {
    static uint16_t stationIndex = 0;

    Station station = getStation(stationIndex);

    // Change displayed station every two seconds
    if ((millis() - lastChange) >= 2000) {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("ST: Stations");

        if (isConfigurationEmpty()) {
            lcd.setCursor(0, 1);
            lcd.print("Empty");
        } else {
            // Show saved configurations
            lcd.setCursor(0, 1);
            lcd.print(station.id);
            lcd.print(": ");
            lcd.print(station.position);
            lcd.print(" cm");

            // Skip empty configurations
            do {
                if (stationIndex < getMaxStations() - 1) {
                    stationIndex++;
                } else {
                    stationIndex = 0;
                }
            } while (getStation(stationIndex).type == StationType::EMPTY);
        }

        lastChange = millis();
    }
}

void weighingMode(LiquidCrystal_I2C &lcd) {
    if ((millis() - lastChange) >= 1000) {
        // Update weight once per second
        int32_t weight = measureWeight();
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("ST: Glass weight");
        lcd.setCursor(0, 1);
        lcd.print(weight);
        lcd.print(" g");

        lastChange = millis();
    }
}