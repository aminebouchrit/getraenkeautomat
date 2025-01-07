# Interface Definition for Communication with Arduino

Since the bottles are now managed in the backend, the exchange formats between the Python bridge and the Arduino had to be adapted.

## Bridge -> Arduino

### Configuration

```text
config,<Config ID>,<Station ID>,<Position from origin in cm>,<Definitions>
```

| Config ID | Description                                      | Definitions            |
|-----------|--------------------------------------------------|------------------------|
| 0         | Configure bottle                                 | `<Pump pin>,<LED pin>` |
| 1         | Configure ice cube station (not implemented yet) |                        |
| 2         | Configure mixer station (not implemented yet)    | Possibly `<Mixer pin>` |

Example:

```text
config,0,0,31,4,33
config,0,1,60,8,36
config,0,2,91,10,34
```

### Order

```text
order,<Number of entries>,<Glass weight>,[<Station ID>,<Additional info>,]
```

For a bottle station, the additional info corresponds to the number of grams. For a mixer station, this could be a time in seconds, for example.

Example:

```text
order,2,236,0,75,2,50
```

### LED configuration

```text
led,<Station ID>,<Color ID>
```

An LED configuration is only allowed for bottle stations.

| Color ID | Color  |
|----------|--------|
| 0        | white  |
| 1        | yellow |
| 2        | red    |

Example:

```text
led,1,1
```

## Arduino -> Bridge

### Error

```text
error,<Error code>,<Error info>
```

| Error code | Description                                                                              | Error info                             |
|------------|------------------------------------------------------------------------------------------|----------------------------------------|
| 0          | Bottle empty                                                                             | Station ID of the bottle that is empty |
| 1          | Glass was removed                                                                        | Unused                                 |
| 2          | Order cannot be processed (required station is not defined)                              | ID of the station that is not defined  |
| 3          | LED color cannot be changed (station ID is undefined or does not correspond to a bottle) | Unused                                 |
| 4          | Configuration error (station ID is out of bounds)                                        | Unused                                 |

Example:

```text
error,0,1
```

### Info

```text
info,<Info code>
```

| Info code | Description                                            |
|-----------|--------------------------------------------------------|
| 0         | Order completed successfully                           |
| 1         | Error has been fixed, order is being processed further |

Example:

```text
info,0
```
