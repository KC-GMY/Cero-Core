# Cero-Core — Python Host (src/python)

This directory contains the **Python host application** for Cero-Core.

It is responsible for:
- Running the desktop GUI
- Handling serial communication
- Managing tool workflows (kHz, MHz, GHz, IR)
- Storing and retrieving captured data

The Python host acts as the **orchestration layer** between the user and the embedded system.

---

## What Lives Here (Scope)

This folder includes **everything needed on the PC side**:

- GUI (CustomTkinter)
- Serial communication logic
- Tool abstraction (RFID / NFC / RF / IR)
- Database storage
- Arduino firmware uploader (via arduino-cli)

**No hardware logic is implemented here** — all signal handling remains on the Arduino.

---

## Directory Structure

```text
src/python/
├─ main.py                  # Application entry point
├─ config.py                # Centralized configuration and paths
├─ database.py              # SQLite CRUD operations
├─ database.db              # Local database (generated at runtime)
│
├─ Assets/
│  ├─ Settings.json         # Global configuration (ports, theme, baudrate)
│  └─ Theme/                # CustomTkinter theme JSON files
│
├─ Arduino/
│  ├─ arduino-cli.yaml      # arduino-cli configuration
│  └─ ReadMHzkHz/
│     └─ ReadMHzkHz.ino     # Arduino firmware (RFID/NFC)
│  
│
├─ Tools/
│   ├─ tools_frame.py        # Unified tool UI (kHz, MHz, GHz, Ir)
│   ├─ tools_rec.py          # Unified recording manager
│   └─ tools_read.py         # Shared read workflow logic
│
├─ Windows/
│  ├─ menu.py               # Main menu UI
│  ├─ toolslist.py          # Tool selector
│  ├─ settings.py           # Settings window
│  ├─ theme.py              # Theme loader
│  ├─ modes.py              # Mode switching
│  ├─ reset.py              # Reset / recovery
│  ├─ error.py              # Error handling UI
│  ├─ functions.py          # Shared GUI helpers
│  └─ arduino_uploader.py   # Firmware logic
│
└─ README.md
```

## Application Flow

### Startup (`main.py`)
- Loads global settings from `Assets/Settings.json`
- Initializes the SQLite database
- Applies the selected UI theme
- Launches the main application window

### Menu & Navigation
- Navigation is handled by `menu.py` and `toolslist.py`
- Each tool opens inside its own dedicated frame
- Frame stacking is used to switch tools without restarting the app

### Tool Execution Model

The project uses a **unified tool architecture**:

- **ToolsFrame** (`tools_frame.py`) - Single class handling all tool UIs (parameterized by tool type)
- **ToolsRec** (`tools_rec.py`) - Single class managing recordings for all tools
- **tools_read.py** - Shared reading workflow logic

Each tool type (kHz, MHz, GHz, Ir) is instantiated from these unified classes:
```python
self.tool_khz = ToolsFrame(self, "kHz")
self.khz_rec = ToolsRec(self, "kHz")
```

This eliminates code duplication while maintaining tool isolation.

Shared read and timeout logic is centralized in `tools_read.py`.

### Data Handling
- Captured data is stored in SQLite via `database.py`
- Data is **tool-scoped**
- Only the tool that created a record can write it back

## Configuration

Global application settings are stored in:

Assets/Settings.json

This file controls:
- Selected UI theme
- Window size
- Baud rate
- Detected serial ports per tool

Serial ports are automatically detected after running the run.bat and the user is requested to change it manually.

## Error Handling & Recovery

- Serial timeouts are handled at the tool level
- Hardware disconnections trigger a safe error screen
- A reset mechanism allows returning to a clean state
  without restarting the application

This prevents crashes during unstable hardware communication.

## Data Storage Model

- SQLite is used for persistent storage
- Each tool stores data in an isolated scope
- Records include:
  - Tool type
  - Timestamp
  - Captured payload
  - Optional user-defined name

Cross-tool access is intentionally restricted.

## Known Limitations

- Windows-only support
- No concurrent tool execution
- Sub-GHz and IR features are partially implemented
- No standalone embedded UI yet

## Development Guidelines

- Keep hardware logic on the microcontroller
- Keep Python tools protocol-driven
- Do not share data across tools
- Follow existing tool structure when extending
