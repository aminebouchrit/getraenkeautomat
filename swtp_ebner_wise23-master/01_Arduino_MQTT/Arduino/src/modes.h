#pragma once

#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

#include "weight_sensor.h"
#include "serial_data.h"
#include "fill_glass.h"
#include "status_light.h"
#include "platform.h"
#include "configuration.h"
#include "led.h"

/**
 * Processes an order (moves platform to the specified positions and fills the glass).
 * @param lcd The display to print status information on
 * @param order The order to process
 */
void processOrder(LiquidCrystal_I2C &lcd, const Order &order);

/**
 * Runs the operating mode that processes inputs from serial (order, config, ...).
 * @param lcd The display to print status information on
 */
void operatingMode(LiquidCrystal_I2C &lcd);

/**
 * Runs the status mode that displays all configured stations.
 * @param lcd The display to print status information on
 */
void configListMode(LiquidCrystal_I2C &lcd);

/**
 * Runs the weighing mode that displays the current weight on the display.
 * @param lcd The display to print status information on
 */
void weighingMode(LiquidCrystal_I2C &lcd);