import customtkinter as ctk
import serial
import serial.serialutil
import time, os, json
import threading
from database import delete_reading,change_name,save_reading,get_data,get_reading
from config import SETTINGS_PATH,THEME_DIR
READ_TIMEOUT_SECONDS = 6
#('COM3' on Windows, '/dev/ttyUSB0' or '/dev/ttyACM0' on Linux/Mac)
def Scrollframe_color():
    with open(SETTINGS_PATH,"r") as file:
        settings=json.load(file)    
        theme_path = os.path.join(os.path.dirname(__file__),"..", "Assets", "Theme", settings["CTkTheme"])
        with open(theme_path,"r") as file2:
                 theme_color=json.load(file2)
    return theme_color["CTkScrollableFrame"]["fg_color"]

def theme_set(theme,parent):
            with open(SETTINGS_PATH, "r") as file:
                settings1 = json.load(file)
            theme_map={
            "Orange": "flipperzero.json",
            "Violet": "violet.json",
            "Red": "red.json",
            "Pink": "pink.json",
            "Coffee":"coffee.json"
            }
            settings1["CTkTheme"] = theme_map[theme]
            with open(SETTINGS_PATH, "w") as file:
                json.dump(settings1, file, indent=2)
            ctk.set_default_color_theme(THEME_DIR/settings1["CTkTheme"])
            parent.winfo_toplevel().rebuild_ui()

def get_tool_rec(parent, tool):
    """Get the recording frame for a tool."""
    tool_map = {
        "kHz": parent.khz_rec,
        "MHz": parent.mhz_rec,
        "GHz": parent.ghz_rec,
        "Ir": parent.ir_rec
    }
    return tool_map[tool]

def get_tool(parent, tool):
    """Get the frame for a tool."""
    tool_map = {
        "kHz": parent.tool_khz,
        "MHz": parent.tool_mhz,
        "GHz": parent.tool_ghz,
        "Ir": parent.tool_ir
    }
    return tool_map[tool]

def get_tool_header(tool):
    """Get the frame header for a tool."""
    tool_map = {
        "kHz":"125 kHz RFID:",
        "MHz":"13.56 MHz NFC:",
        "GHz":"Sub-GHz RF:",
        "Ir":"Infrared:"
    }
    return tool_map[tool]

def details(tool,name,parent):
    class Details(ctk.CTkFrame):
        def __init__(self,parent):
            super().__init__(parent)
            self.place(relwidth=1, relheight=1)
            self.title=ctk.CTkLabel(self,text="Details:")
            self.title.pack(pady=2,padx=2,anchor="nw")
            data=get_data(tool,name)
            if tool=="kHz":
                if data[0][3]:
                    checksum_valid="True"
                else:
                    checksum_valid="False"
                self.tag=ctk.CTkLabel(self,text=f" Tag (HEX): {data[0][0]}\n" f" Tag (Dec): {data[0][1]}\n"
                f" Checksum (HEX): {data[0][2]}\n" f" Checksum Val: {checksum_valid}\n"f" Date: {data[0][4]}",
                font=("helvb08", 13),justify="left")
                self.tag.pack(padx=2,anchor="w")
            elif tool=="MHz":
                self.data=ctk.CTkLabel(self,text=f" Card UID: {data[0][0]}\n"f" Type: {data[0][1]}\n"f" Date: {data[0][2]}",
                                       font=("helvb08",13),justify="left")
                self.data.pack(pady=2,padx=2,anchor="w")
            elif tool=="GHz" or tool=="Ir":
                self.data=ctk.CTkLabel(self,text=f" Data: {data[0][0]}\n"f" Date: {data[0][1]}",
                                       font=("helvb08",14),justify="left")
                self.data.pack(pady=2,padx=2,anchor="w")
            self.backmenu= ctk.CTkButton(self, text="Back", command=lambda: parent.show_frame(get_tool_rec(parent, tool)))
            self.backmenu.pack(pady=2,padx=2,anchor="center")
    details=Details(parent)
    details.tkraise()

def Frame(tool,name,parent):
    class Rec(ctk.CTkFrame):
        def __init__(self,parent):
            super().__init__(parent)
            self.place(relwidth=1, relheight=1)
            self.scroll_frame = ctk.CTkScrollableFrame(
            self,border_width=0,corner_radius=0,label_text=name,label_anchor="nw",fg_color=Scrollframe_color())
            self.scroll_frame.pack(padx=3, pady=5,expand=True)
            self.write= ctk.CTkButton(self.scroll_frame, text='Write', command=lambda:(parent.show_frame(parent.error_feature)),anchor="w")
            self.write.pack(pady=2)

            def rename(tool):
                class Rename(ctk.CTkFrame):
                    def __init__(self,parent,tool):
                        super().__init__(parent)
                        self.place(relwidth=1, relheight=1)
                        self.label=ctk.CTkLabel(self,text=f"Renaming: {name}")
                        self.label.pack(pady=2,padx=5,anchor="nw")
                        self.text=ctk.CTkEntry(self,placeholder_text="Enter your new name:")
                        self.text.pack(pady=2,padx=2)
                        def get_user_input():
                            change_name(tool,name,self.text.get())
                            tool_rec=get_tool_rec(parent, tool)
                            tool_rec.refresh(tool,parent)
                            parent.show_frame(tool_rec)
                        self.ok=ctk.CTkButton(self,text="OK",command=get_user_input,anchor="w")
                        self.ok.pack()
                rename_frame=Rename(parent,tool)
                rename_frame.tkraise()

            self.rename = ctk.CTkButton(self.scroll_frame, text='Rename',command=lambda:rename(tool),anchor="w")
            self.rename.pack(pady=2)
            self.details=ctk.CTkButton(self.scroll_frame, text='Details',command=lambda:details(tool,name,parent),anchor="w")
            self.details.pack(pady=2)
            tool_rec=get_tool_rec(parent, tool)
            self.delete= ctk.CTkButton(self.scroll_frame, text='Delete', 
            command=lambda:(delete_reading(tool,name),tool_rec.refresh(tool,parent),parent.show_frame(tool_rec)),anchor="w")
            self.delete.pack(pady=2)
            self.backmenu= ctk.CTkButton(self.scroll_frame, text="Back", command=lambda: parent.show_frame(tool_rec))
            self.backmenu.pack(pady=2)
    rec_frame=Rec(parent)
    rec_frame.tkraise()

def Record(tool,parent):
    def name(info):
        class Name(ctk.CTkFrame):
            def __init__(self,parent):
                super().__init__(parent)
                self.place(relwidth=1, relheight=1)
                self.label=ctk.CTkLabel(self,text="Naming:")
                self.label.pack(pady=2,padx=5,anchor="nw")
                self.text=ctk.CTkEntry(self,placeholder_text="Enter a name:")
                self.text.pack(pady=2,padx=2)
                def get_user_input():
                    save_reading(tool,self.text.get(),info)
                    tool_rec=get_tool_rec(parent, tool)
                    tool_rec.refresh(tool,parent)
                    parent.show_frame(tool_rec)
                self.ok=ctk.CTkButton(self,text="OK",command=get_user_input)
                self.ok.pack()
        name_frame=Name(parent)
        name_frame.tkraise()
    def read_worker():
        arduino = parent.arduino
        try:
            lines = []
            deadline = time.time() + READ_TIMEOUT_SECONDS
            if tool=="MHz":
                while time.time() < deadline and len(lines) < 2:
                    if arduino.in_waiting:
                        line = arduino.readline().decode("utf-8", errors="ignore").strip()
                        if line:
                            lines.append(line)
                    else:
                        time.sleep(0.05)

                if len(lines) < 2:
                    raise TimeoutError("Read timeout")
                data = f"{lines[0]}\n{lines[1]}"
            elif tool=="kHz":
                while time.time() < deadline and len(lines) < 4:
                    if arduino.in_waiting:
                        line = arduino.readline().decode("utf-8", errors="ignore").strip()
                        if line:
                            lines.append(line)
                    else:
                        time.sleep(0.05)

                if len(lines) < 4:
                    raise TimeoutError("Read timeout")
                data = f"{lines[0]}\n{lines[1]}\n{lines[2]}\n{lines[3]}"
            parent.after(0, lambda: name(data))

        except TimeoutError:
            parent.after(0, lambda: parent.show_frame(parent.error_timeout))
        except json.JSONDecodeError:
            parent.after(0, lambda: parent.show_frame(parent.error_config))
        except KeyError:
            parent.after(0, lambda: parent.show_frame(parent.error_port))
        except (serial.serialutil.SerialException, OSError):
            parent.after(0, lambda: parent.show_frame(parent.error_serial))
        finally:
            if arduino is not None and arduino.is_open:
                arduino.close()
            return
    threading.Thread(target=read_worker, daemon=True).start()

def load_readings(self,tool,parent):
    for widget in self.scroll_frame.winfo_children():
        widget.destroy()
    rows = get_reading(tool)
    for row in rows:
        btn = ctk.CTkButton(self.scroll_frame, text=row[0],
                        command=lambda name=row[0]: Frame(tool, name, self.master),anchor="w")
        btn.pack(pady=2)
    self.backmenu = ctk.CTkButton(self.scroll_frame, text='Back',
                                  command=lambda: self.master.show_frame(get_tool(parent, tool)))
    self.backmenu.pack(pady=2)
