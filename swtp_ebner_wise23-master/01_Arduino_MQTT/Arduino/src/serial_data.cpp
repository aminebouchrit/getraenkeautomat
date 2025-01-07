#include "serial_data.h"

Order readOrderFromSerial() {
    uint16_t numEntries = Serial.readStringUntil(',').toInt();
    int32_t glassWeight = Serial.readStringUntil(',').toInt();

    // Must be allocated on the heap, otherwise the memory of the array would be freed when exiting the function
    OrderEntry *entries = new OrderEntry[numEntries];

    for (uint16_t i = 0; i < numEntries; i++) {
        uint16_t stationID = Serial.readStringUntil(',').toInt();
        entries[i].stationID = stationID;
        int16_t value = Serial.readStringUntil(',').toInt();
        entries[i].value = value;
    }

    Order order = { numEntries, glassWeight, entries };

    return order;
}

void freeOrder(Order &order) {
    delete[] order.entries;
    order.entries = nullptr;
}

Station readStationFromSerial() {
    Station station;

    uint16_t configID = Serial.readStringUntil(',').toInt();
    StationType type = configID == 0 ? StationType::BOTTLE : StationType::EMPTY; // convert id to type
    uint16_t stationID = Serial.readStringUntil(',').toInt();
    uint16_t position = Serial.readStringUntil(',').toInt();

    station.id = stationID;
    station.type = type;
    station.position = position;

    // Read data depending on the station type
    if (type == StationType::BOTTLE) {
        uint8_t pumpPin = Serial.readStringUntil(',').toInt();
        uint8_t ledPin = Serial.readStringUntil(',').toInt();

        station.data.bottleData.pumpPin = pumpPin;
        station.data.bottleData.ledPin = ledPin;
    }
    // Support for more configuration types can be added here (e.g. ice cube station, mixer)

    return station;
}

LEDConfig readLEDConfigFromSerial() {
    uint16_t stationID = Serial.readStringUntil(',').toInt();
    uint16_t colorID = Serial.readStringUntil(',').toInt();
    LEDPattern pattern = (LEDPattern) colorID; // convert id to pattern

    LEDConfig config = { stationID, pattern };
    return config;
}

void sendInfoToSerial(uint8_t infoCode) {
    Serial.print("info,");
    Serial.println(infoCode);
}

void sendErrorToSerial(uint8_t errorCode, uint16_t errorInfo) {
    Serial.print("error,");
    Serial.print(errorCode);
    Serial.print(",");
    Serial.println(errorInfo);
}