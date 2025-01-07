#include "status_light.h"

const uint8_t greenLightPin = 48;
const uint8_t yellowLightPin = 49;
const uint8_t redLightPin = 50;
const uint8_t buzzerPin = 51;

void setupStatusLight() {
    pinMode(greenLightPin, OUTPUT);
    pinMode(yellowLightPin, OUTPUT);
    pinMode(redLightPin, OUTPUT);
    pinMode(buzzerPin, OUTPUT);
}

void showStatus(Status status) {
    switch (status) {
        case Status::GREEN:
            digitalWrite(greenLightPin, HIGH);
            digitalWrite(yellowLightPin, LOW);
            digitalWrite(redLightPin, LOW);
            break;
        case Status::YELLOW:
            digitalWrite(greenLightPin, LOW);
            digitalWrite(yellowLightPin, HIGH);
            digitalWrite(redLightPin, LOW);
            break;
        case Status::RED:
            digitalWrite(greenLightPin, LOW);
            digitalWrite(yellowLightPin, LOW);
            digitalWrite(redLightPin, HIGH);
            break;
        case Status::OFF:
            digitalWrite(greenLightPin, LOW);
            digitalWrite(yellowLightPin, LOW);
            digitalWrite(redLightPin, LOW);
            break;
    }
}

void alarm(uint32_t length, uint32_t pause) {
    digitalWrite(buzzerPin, HIGH);
    delay(length);
    digitalWrite(buzzerPin, LOW);
    delay(pause);
}