# Full System Wiring Overview

This wiring configuration combines multiple RFID technologies on a single
Arduino board in order to support both low-frequency and high-frequency
contactless systems.

## Connected Modules
- RDM6300 – 125 kHz RFID (UART)
- RC522 – 13.56 MHz RFID / NFC (SPI)

Each module retains its own dedicated interface and power domain, allowing
simultaneous operation without protocol or electrical conflicts.

## Communication Interfaces
- SPI bus is used exclusively by the RC522.
- UART (SoftwareSerial) is used by the RDM6300.
- Interfaces are isolated at the protocol level.

## Reference Documentation
Detailed pin mappings and electrical notes are available in the following
module-specific files:

- `wiring/rc522/PINOUT.md`
- `wiring/rc522/notes.md`
- `wiring/rdm6300/PINOUT.md`
- `wiring/rdm6300/notes.md`
