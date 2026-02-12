# CC1101 – Notes

- CC1101 operates at **3.3V ONLY** (no 5V tolerance).
- SPI bus is shared with RC522.
- Each SPI device must have a unique CS pin.
- D3 is used for GDO interrupt handling.
- Keep SPI wires short to avoid RF noise.
- Recommended antenna: 315 / 433 / 868 / 915 MHz matched.
- Tested with Arduino Uno and Arduino Nano.