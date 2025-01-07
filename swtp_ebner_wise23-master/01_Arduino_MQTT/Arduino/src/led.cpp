#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#include "led.h"
#include "configuration.h"

// LED type: WS2812b
neoPixelType type = NEO_GRB + NEO_KHZ800;
const uint8_t numPixels = 12;

void fill(Adafruit_NeoPixel &pixels, uint32_t color) {
    // Fill all pixels with the given color
    for (uint16_t i = 0; i < pixels.numPixels(); i++) {
        pixels.setPixelColor(i, color);
    }
    pixels.show();
}

void movingDot(Adafruit_NeoPixel &pixels, uint32_t color) {
    // Clear all pixels
    fill(pixels, Adafruit_NeoPixel::Color(0, 0, 0));
    pixels.show();

    // Show moving pixel
    for (uint16_t i = 0; i < pixels.numPixels(); i++) {
        pixels.setPixelColor(i, color);
        if (i > 0) pixels.setPixelColor(i - 1, pixels.Color(0, 0, 0));
        pixels.show();

        // Wait before changing pattern
        delay(100);
    }

    // Turn off last pixel
    pixels.setPixelColor(pixels.numPixels() - 1, pixels.Color(0, 0, 0));
    pixels.show();
}

void fadeWhite(Adafruit_NeoPixel &pixels) {
    // Maximum brightness
    const uint8_t brightnessLimit = 20;

    // Delay before changing pattern
    const uint8_t delayTime = 100;

    // Fade in
    for (uint8_t i = 0; i <= brightnessLimit; i++) {
        fill(pixels, Adafruit_NeoPixel::Color(i, i, i));
        pixels.show();

        delay(delayTime);
    }

    // Fade out
    for (int8_t i = brightnessLimit; i >= 0; i--) {
        fill(pixels, Adafruit_NeoPixel::Color(i, i, i));
        pixels.show();

        delay(delayTime);
    }
}

bool showLEDPattern(LEDConfig config) {
    Station station = getStation(config.stationID);

    if (station.type != StationType::BOTTLE) {
        // Only bottle stations have an LED pin
        return false;
    }

    // Get LED pin from station
    uint8_t ledPin = station.data.bottleData.ledPin;

    // Initialize the LED ring
    Adafruit_NeoPixel pixels = Adafruit_NeoPixel(numPixels, ledPin, type);
    pixels.begin();

    // Show selected pattern
    switch (config.pattern) {
        case LEDPattern::CONSTANT_WHITE:
            fill(pixels, Adafruit_NeoPixel::Color(100, 100, 100));
            break;
        case LEDPattern::CONSTANT_YELLOW:
            fill(pixels, Adafruit_NeoPixel::Color(100, 100, 0));
            break;
        case LEDPattern::CONSTANT_RED:
            fill(pixels, Adafruit_NeoPixel::Color(100, 0, 0));
            break;
        case LEDPattern::ERROR_RED:
            movingDot(pixels, Adafruit_NeoPixel::Color(20, 0, 0));
            break;
        case LEDPattern::FADING_WHITE:
            fadeWhite(pixels);
            break;
    }

    return true;
}