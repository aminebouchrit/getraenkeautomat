#pragma once

#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

#include "status_light.h"
#include "weight_sensor.h"
#include "order.h"
#include "serial_data.h"

/**
 * Enum used for the state machine in "fill_glass".
 */
enum class FillState {
    FILLING, GLASS_REMOVED, BOTTLE_EMPTY
};

/**
 * Configures the pin for the continue button.
 * Needs to be called before filling a glass.
 */
void setupFillGlass();

/**
 * Waits until the weight sensor detects a glass of a specific type.
 * @param lcd The display to print status information on
 * @param order The order that should be processed afterwards. Contains the information about the required glass weight
 */
void waitForGlass(LiquidCrystal_I2C &lcd, const Order &order);

/**
 * Fills an ingredient into the glass.
 * 
 * @param lcd The display to print status information on
 * @param stationID The station ID of the ingredient
 * @param pumpPin The pin of the pump that is connected to the ingredient
 * @param gramsToFill The total weight that should be reached
 */
void fillGlass(LiquidCrystal_I2C &lcd, uint16_t stationID, uint8_t pumpPin, int32_t gramsToFill);

/**
 * Waits until the weight sensor no longer detects a glass.
 * 
 * @param lcd The display to print status information on
 * @param order The order that was processed. Contains the information about the glass weight
 */
void waitUntilGlassIsRemoved(LiquidCrystal_I2C &lcd, const Order &order);