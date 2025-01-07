#pragma once

#include <Arduino.h>

#include "configuration.h"

/**
 * Represents a step in an incoming order
 * @param stationID ID of the station
 * @param value If station is a bottle: weight in gram
 */
struct OrderEntry {
    uint16_t stationID;
    int16_t value;
};

/**
 * Represents an incoming order
 * @param numEntries Number of entries that this order contains
 * @param glassWeight Weight of the glass that is required to fulfill this order
 * @param entries Pointer to an array of order entries
 */
struct Order {
    uint16_t numEntries;
    int32_t glassWeight;
    OrderEntry *entries;
};

/**
 * @param order The order to validate
 * @return true if all required stations are configured correctly
 */
bool isOrderValid(const Order &order);

/**
 * @param order The order that is invalid
 * @return The ID of the station that is missing its configuration (call isOrderValid() first)
 */
uint16_t getMissingConfiguration(const Order &order);