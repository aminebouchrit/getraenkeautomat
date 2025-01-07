#pragma once

/**
 * Enum used for selecting the color/pattern that should be shown on an LED ring.
 */
enum class LEDPattern {
    CONSTANT_WHITE, CONSTANT_YELLOW, CONSTANT_RED, ERROR_RED, FADING_WHITE
};

/**
 * Configuration data for an LED ring.
 * @param stationID The station that the LED ring belongs to
 * @param pattern The pattern that should be shown on the LED ring
 */
struct LEDConfig {
    uint16_t stationID;
    LEDPattern pattern;
};

/**
 * Shows a pattern on the LED ring.
 * @param config The pin of the LED ring/the pattern to show
 * @return True of the change was successfull (only bottle stations have an LED ring)
 */
bool showLEDPattern(LEDConfig config);