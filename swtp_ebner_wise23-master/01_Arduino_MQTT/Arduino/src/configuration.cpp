#include "configuration.h"

const uint16_t maxStations = 30;
Station stations[maxStations];

bool addStation(Station station) {
    // Check if the id is out of range
    if (station.id >= maxStations) {
        return false;
    }

    stations[station.id] = station;
    return true;
}

Station getStation(uint16_t id) {
    if (id >= maxStations) {
        // Return empty station if the id is out of range
        Station errorStation;
        errorStation.type = StationType::EMPTY;
        return errorStation;
    }

    return stations[id];
}

uint16_t getMaxStations() {
    return maxStations;
}

bool isConfigurationEmpty() {
    // Check if all stations are empty
    for (uint16_t i = 0; i < maxStations; i++) {
        if (stations[i].type != StationType::EMPTY) {
            return false;
        }
    }

    return true;
}