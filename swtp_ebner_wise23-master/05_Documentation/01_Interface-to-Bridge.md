# Interface Definition for Communication with the Python Bridge

Since the Arduino is not network capable, direct communication with the backend is not possible. For this, the Python bridge is necessary, which communicates directly with the serial port of the Arduino and provides an MQTT interface for the backend.

The messages sent via MQTT use the JSON format, as this is much more convenient to process in Python than the self-defined serial format. Therefore, a corresponding JSON counterpart exists for each serial format.

## Backend -> Bridge

### Configuration

The definition part (LED pin, pump pin) is different for other station types (see description of the serial format).

Unlike the serial format, multiple stations can be configured using one message.

```json
{
    "type": "config",
    "value": [<Station>,]
}

<Station> {
    "configID": 0,
    "stationID": <integer>,
    "position": <integer>,
    "pump_pin": <integer>,
    "led_pin": <integer>
}
```

Example:

```json
{
    "type": "config",
    "value": [
        {
            "configID": 0,
            "stationID": 0,
            "position": 31,
            "pump_pin": 4,
            "led_pin": 33
        },
        {
            "configID": 0,
            "stationID": 1,
            "position": 60,
            "pump_pin": 8,
            "led_pin": 36
        },
        {
            "configID": 0,
            "stationID": 2,
            "position": 91,
            "pump_pin": 10,
            "led_pin": 34
        }
    ]
}
```

### Order

```json
{
    "type": "order",
    "glass_weight": <integer>,
    "value": [<OrderEntry>,]
}

<OrderEntry> {
    "stationID": <integer>,
    "value": <integer>
}
```

Example:

```json
{
    "type": "order",
    "glass_weight": 236,
    "value": [
        {
            "stationID": 0,
            "value": 25
        },
        {
            "stationID": 2,
            "value": 50
        }
    ]
}
```

### LED configuration

Unlike the serial format, multiple LEDs can be configured using one message.

```json
{
    "type": "led",
    "value": [<LEDConfig>,]
}

<LEDConfig> {
    "stationID": <integer>,
    "colorID": <integer>
}
```

Example:

```json
{
    "type": "led",
    "value": [
        {
            "stationID": 0,
            "colorID": 1
        },
        {
            "stationID": 1,
            "colorID": 0
        }
    ]
}
```

## Bridge -> Backend

### Error

```json
{
    "type": "error",
    "value":
        {
            "error_code": <integer>,
            "error_info": <integer>
        }
}
```

Example:

```json
{
    "type": "error",
    "value":
        {
            "error_code": 0,
            "error_info": 1
        }
}
```

### Info

```json
{
    "type": "info",
    "value": <integer>
}
```

Example:

```json
{
    "type": "info",
    "value": 0
}
```
