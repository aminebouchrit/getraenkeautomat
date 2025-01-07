#pragma once

#include <Arduino.h>

/**
 * The type of a station (necessary for future expansions such as an ice cube station or a mixer)
 */
enum class StationType {
    EMPTY, BOTTLE
};

/**
 * Configuration data for a station
 * @param type Determines what part of the union is used
 * @param id Station ID
 * @param position Position of the station in cm
 * @param data Configuration data depending on the station type
 */
struct Station {
    StationType type;
    uint16_t id;
    uint16_t position;
    union {
        struct {
            uint8_t pumpPin;
            uint8_t ledPin;
        } bottleData;
        // More configuration types can be added here (e.g. ice cube station, mixer)
    } data;
};

/**
 * Adds a station to the internal database.
 * @param station The station to add
 * @return True if the station was added successfully
 */
bool addStation(Station station);

/**
 * Returns information about a station.
 * @param id The id (array index) of the station
 * @return The specified station. An empty station is returned if the id is out of range
 */
Station getStation(uint16_t id);

/**
 * @return The maximum number of stations
*/
uint16_t getMaxStations();

/**
 * @return True if no stations have been configured yet
*/
bool isConfigurationEmpty();