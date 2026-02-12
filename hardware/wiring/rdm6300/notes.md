# RDM6300 – Notes & Warnings

## Power Requirements
- The RDM6300 operates at **5V**.
- Do NOT power the module from the 3.3V pin.
- Ensure a stable 5V supply to avoid read errors.

## Serial Communication
- The RDM6300 transmits data via **UART (TX only)**.
- Use **SoftwareSerial** on Arduino (e.g. D6) to avoid conflicts with USB serial.
- Default baudrate is **9600 bps**.

## Pin Usage
- Only the **TX pin** is required for standard operation.
- The RX pin of the module is not used in this setup.
- Ensure a common ground between Arduino and RDM6300.

## Signal Integrity
- Keep wires between the reader and Arduino short.
- Avoid placing the module close to high-current or RF-emitting components.
- Do not mount the RDM6300 antenna directly over metal surfaces.

## Reading Behavior
- The module continuously outputs tag data when a card is present.
- Duplicate reads should be filtered in software.
- Output data includes a checksum that should be validated.

## Compatibility
- Tested with Arduino Uno and Arduino Nano.
- Compatible with common RDM6300 / EM4100 libraries.
