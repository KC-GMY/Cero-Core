# RC522 Pinout (13.56 MHz RFID / NFC)

This document defines the pin mapping between the **MFRC522 (RC522)** RFID/NFC module
and an **Arduino Uno / Arduino Nano** using the SPI interface.

---

## RC522 ↔ Arduino Pin Mapping

| RC522 Pin | Arduino Pin|
|-----------|------------|
| SDA (SS)  | D10        |
| SCK       | D13        |
| MOSI      | D11        |
| MISO      | D12        |
| RST       | D7         |
| 3.3V      | 3.3V       |
| GND       | GND        |
| IRQ       | Not connect|

---