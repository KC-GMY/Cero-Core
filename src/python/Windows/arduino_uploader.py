import time,threading,json
import serial
from config import SETTINGS_PATH

MODE = {
    "MHz": b"\x00",
    "kHz": b"\x01",
}

def get_port_for_tool(tool: str) -> str:
    with open(SETTINGS_PATH, "r") as f:
        settings = json.load(f)
    return settings["serial_ports"][tool]



def target_change(tool, parent):
    port = get_port_for_tool(tool)
    mode = MODE.get(tool)
    if mode is None:
        raise ValueError(f"Unknown tool: {tool}")

    # close old port if any
    ser = getattr(parent, "arduino", None)
    if ser and ser.is_open:
        try:
            ser.close()
        except Exception:
            pass
        time.sleep(0.3)

    for _ in range(5):
        try:
            ser = serial.Serial(port, 9600, timeout=1, write_timeout=1)
            parent.arduino = ser
            time.sleep(1.6)
            ser.reset_input_buffer()
            ser.write(mode)
            ser.flush()
            return
        except serial.SerialException:
            time.sleep(0.3)

    raise serial.SerialException(f"Could not open {port}")


def target_change_async(tool, parent):
    threading.Thread(target=target_change, args=(tool, parent), daemon=True).start()