# RC522 – Notes & Warnings

## Voltage Requirements
- The RC522 operates at **3.3V ONLY**.
- Connecting the module to 5V may permanently damage it.
- Always power the module from the Arduino **3.3V pin**.

## SPI Bus Considerations
- The RC522 shares the SPI bus (D11, D12, D13) with other SPI devices.
- Each SPI device must have a **unique CS (Chip Select) pin**.
- Ensure that only one SPI device is active at a time.

## Recommended CS Assignment
| Module | CS Pin |
|------|--------|
| RC522 | D10 |
| CC1101 | D9 |
| ST7735 | D8 |

## Signal Integrity
- Keep SPI wiring short to reduce noise and signal degradation.
- Avoid routing SPI lines close to RF antennas or high-current traces.
- Use a common ground for all connected modules.

## IRQ Pin
- The IRQ pin is optional and not required for standard RFID/NFC usage.
- Leave it unconnected unless using interrupt-driven designs.

## Library Compatibility
- Tested with the **MFRC522 Arduino library**.
- Compatible with Arduino Uno and Arduino Nano.
