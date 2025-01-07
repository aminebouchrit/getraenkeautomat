#include "order.h"

bool isOrderValid(const Order &order) {
    for (uint16_t i = 0; i < order.numEntries; i++) {
        Station station = getStation(order.entries[i].stationID);
        if (station.type == StationType::EMPTY) {
            // Station configuration is missing
            return false;
        }
    }

    return true;
}

uint16_t getMissingConfiguration(const Order &order) {
    for (uint16_t i = 0; i < order.numEntries; i++) {
        Station station = getStation(order.entries[i].stationID);
        if (station.type == StationType::EMPTY) {
            // Return index of the missing station configuration
            return order.entries[i].stationID;
        }
    }

    return -1;
}