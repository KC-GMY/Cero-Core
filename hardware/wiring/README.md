# Wiring

This folder documents how the hardware components of the project are physically
connected together.

It focuses on **practical wiring information** only: how to plug modules into
the microcontroller so the system works as intended.

## Scope

The wiring documentation is organized by module.  
Each module has its own folder containing:
- A wiring diagram
- A pin mapping reference
- Notes and warnings specific to that hardware

System-level wiring layouts that combine multiple modules may also be included
to show how components coexist on a single board.

## Usage

Use this folder when:
- Building the hardware prototype
- Verifying pin assignments
- Debugging electrical or connection issues
- Extending the system with additional modules

For software behavior, data flow, and user interaction, refer to the main
project documentation.

## Notes

All wiring diagrams assume a shared ground and correct power levels for each
module. Always verify voltage requirements before powering any component.