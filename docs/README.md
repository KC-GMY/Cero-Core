# Documentation

This folder contains high-level diagrams that explain how **Flipper-Cero** works,
from a system perspective down to the execution flow.

These diagrams are meant to give contributors and reviewers a **fast mental model**
before diving into the code or hardware.

---

## System Architecture

**File:** `architecture.svg`

This diagram shows the global structure of the project and how the main components interact:

- Python Host (GUI, database, orchestration)
- Arduino firmware
- Communication layer (Serial)
- External modules (RFID / NFC / RF / IR)

It answers the question:
> *“What are the main blocks of Flipper-Cero and how are they connected?”*

---

## Functional Flow (Fast Diagram)

**File:** `functional-flow.png`

This is the **fast overview diagram** of the project.

It represents the end-to-end execution flow:
1. User interaction from the GUI
2. Command dispatch from Python
3. Arduino processing
4. Data capture / response
5. Storage and feedback to the user

It answers the question:
> *“What happens, step by step, when I press a button?”*

This diagram is intentionally simplified to be readable in under 30 seconds.

---

## How to Read These Diagrams

- Start with **System Architecture** to understand *what exists*
- Then read **Functional Flow** to understand *how things move*
- Code and schematics are implementations of these two views

If something in the code contradicts a diagram, **the diagram is the reference**
and the implementation should be aligned accordingly.