"""
Cero-Core Python Host Application
This file is the main entry point of the application.
It initializes:
- UI configuration and themes
- Database layer
- Tool windows and navigation
Hardware communication is handled through backend logic
and serial interfaces, not directly in the GUI.
"""
import customtkinter as ctk 
from pathlib import Path
import os,sys
from Windows.menu import Menu
from Windows.toolslist import ToolsList
from Windows.theme import Theme
from Windows.settings import Settings
from Windows.reset import Reset
from Windows.modes import Modes
from Windows.error import Error

from Tools.tools_read import ToolsRead
from Tools.tools_rec import ToolsRec
from Tools.tools_frame import ToolsFrame

from database import create_table
from config import load_settings, resolve_theme_path, SETTINGS_PATH
sys.path.insert(0, str(Path(__file__).resolve().parent))

class Main(ctk.CTk):
    def __init__(self):
        super().__init__()
        settings = load_settings(SETTINGS_PATH)
        self.geometry(settings["CTkWindowsize"])
        theme_path = resolve_theme_path(settings["CTkTheme"])
        if os.path.isfile(theme_path):
            ctk.set_default_color_theme(theme_path)
        ctk.set_appearance_mode(settings["CTkMode"])
        self.build_ui()

    def build_ui(self):
        create_table()
        #Main menus
        self.main_menu = Menu(self)
        self.settings  = Settings(self)
        self.themes    = Theme(self)
        self.reset     = Reset(self)
        self.modes     = Modes(self)
        #Error handling
        self.error_timeout = Error(self, "Timeout.")
        self.error_port    = Error(self, "Port Missing.")
        self.error_serial  = Error(self, "Serial Error.")
        self.error_config  = Error(self, "Config Error.")
        self.error_feature = Error(self, "Feature Missing.")
        #Tools
        self.tools    = ToolsList(self)
        self.tool_ir  = ToolsFrame(self,"Ir")
        self.tool_khz = ToolsFrame(self,"kHz")
        self.tool_ghz = ToolsFrame(self,"GHz")
        self.tool_mhz = ToolsFrame(self,"MHz")
        #Readings
        self.tools_read = ToolsRead(self)
        #Recording
        self.ir_rec  = ToolsRec(self,"Ir")
        self.ghz_rec = ToolsRec(self,"GHz")
        self.mhz_rec = ToolsRec(self,"MHz")
        self.khz_rec = ToolsRec(self,"kHz")
        self.show_frame(self.main_menu)

    def rebuild_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.build_ui()

    def show_frame(self, frame):
        frame.tkraise()
    
if __name__ == "__main__": 
    app = Main() 
    app.mainloop()    