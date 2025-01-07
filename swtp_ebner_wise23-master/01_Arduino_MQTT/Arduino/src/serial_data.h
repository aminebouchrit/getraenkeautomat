#pragma once

#include <Arduino.h>

#include "configuration.h"
#include "order.h"
#include "led.h"

/**
 * Reads a new order from the serial interface in the format:
 * "order,Number of entries,Glass weight,Station ID of first entry,Value associated with first entry,..."
 * @return The order that was received
 */
Order readOrderFromSerial();

/**
 * Frees the memory of the entry array.
 * Needs to be called after processing an order to avoid memory leaks.
 * @param order The struct that is no longer needed
 */
void freeOrder(Order &order);

/**
 * Reads a new station configuration from the serial interface in the format:
 * "config,Config ID,Station ID,Station position (in cm),Data"
 * The data depends on the type of the station that is determined by the config ID.
 * Currently, only one station type is implemented (config ID 0 -> Bottle):
 * "config,0,Station ID,Station position (in cm),Data,Pump pin,LED pin"
 * @return The bottle that was read in
 */
Station readStationFromSerial();

/**
 * Reads a LED configuration from the serial interface in the format:
 * "led,Station ID,Color ID"
 * Color ID: 0 -> white, 1 -> yellow, 2 -> red
 * @return The config that was read in
 */
LEDConfig readLEDConfigFromSerial();

/**
 * Sends an info message using the serial interface in the format:
 * "info,Info Code"
 * @param infoCode The message type
*/
void sendInfoToSerial(uint8_t infoCode);

/**
 * Sends an error message using the serial interface in the format:
 * "error,Error Code,Error Info"
 * @param errorCode The message type
 * @param errorInfo Information about the specific error
*/
void sendErrorToSerial(uint8_t errorCode, uint16_t errorInfo);