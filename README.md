# Cero-Core (V0)

Cero-Core is a **work-in-progress, open-source embedded system** designed 
to analyze, audit, and experiment with **contactless communication technologies**
such as RFID, NFC, Sub-GHz RF, and Infrared.

This project is a **solo end-to-end design** with a strong emphasis 
on **modularity, transparency, and educational value**.

---

## Project Goals

- Design a flexible and extensible embedded platform for contactless systems
- Provide low-level access to multiple communication technologies
- Keep the entire hardware and software stack open and understandable
- Serve as a learning and experimentation tool for embedded systems and contactless security analysis

---

## Supported Technologies (Current / Planned)

- **RFID / NFC**
  - 125 kHz (LF)
  - 13.56 MHz (HF)
- **Sub-GHz RF**
  - Signal capture and analysis (CC1101)
- **Infrared**
  - Capture and replay of IR signals
- **Embedded User Interface**
  - Lightweight GUI for control and data management

---

## System Architecture

![System Architecture](docs/architecture.svg)

The project follows a layered architecture:

- **Hardware layer**
  - Arduino-based acquisition
  - Modular RF, RFID/NFC, and IR modules
- **Communication layer**
  - Serial protocol between microcontroller and host
- **Backend**
  - SQLite database for persistent storage
  - CRUD operations per technology
- **Frontend**
  - Python GUI using CustomTkinter
  - Standardized interfaces across tools
- **Configuration layer**
  - JSON-based themes and user settings

This separation ensures **maintainability, scalability, and clarity**.

---

## Benchmarking & Design Choices

Key components were selected after comparative benchmarking based on:
- flexibility
- documentation quality
- power consumption
- cost
- suitability for signal analysis

Examples:
- **Arduino Nano/Uno** for simplicity, portability, and ecosystem support
- **CC1101** for Sub-GHz flexibility and modulation support
- **MFRC522 & RDM6300** to cover common RFID/NFC standards
- **Python + C++** for a clean hardware/software split

---

## Project Status

🚧 **Work in Progress**

### Implemented
- Hardware integration and wiring
- RFID/NFC reading pipeline
- GUI navigation and tool selection
- Database architecture and data management

### Planned
- Full Sub-GHz and IR activation
- Writing/emulation synchronization
- Standalone embedded display
- Migration to a more powerful embedded platform

---

## Installation & Setup

Cero-Core is currently supported on **Windows**.

### Requirements
- Python 3.10+
- Arduino board (Uno / Nano)
- USB cable
- Windows 10/11

### Quick Start
1. Clone or download this repository
2. Install the required font (Haxrcorp 4089)
3. Connect the Arduino board via USB
4. Run `run.bat` from the project root

This script will:
- Locate the COM connected to your arduino
- Create a Python virtual environment
- Install Python and its dependencies (pyserial, customtkinter)
- Upload Arduino firmware using the bundled arduino-cli

For advanced configuration and development details,
see `src/python/README.md`.

## Repository Structure

```Cero-Core/
├─ src/      #Arduino and Python source code
├─ hardware/ #Wiring diagrams and schematics
├─ docs/     #Architecture diagrams and documentation
└─ README.md
```
---

## Disclaimer

This project is intended for **educational and research purposes only**.
It must be used responsibly and within legal and ethical boundaries.

---

## License

This project is licensed under the **GNU General Public License v3.0**.
