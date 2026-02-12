# IR TX/RX – Pinout

This document defines the pin mapping between the **IR TX/RX**
and an **Arduino Uno / Arduino Nano**.

## IR Receiver (TSOP4838 / VS1838)

| Receiver Pin | Arduino Uno |
|--------------|-------------|
| VCC          | 3.3V        |
| GND          | GND         |
| DATA         | D2          |

## IR Transmitter (IR LED)

| LED Pin | Arduino Uno |
|--------|-------------|
| Anode (+) | D3 (via resistor) |
| Cathode (–) | GND |