import customtkinter as ctk
import json
from config import load_settings,SETTINGS_PATH

class Modes(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)
        self.label=ctk.CTkLabel(self,text="Select Mode:")
        self.label.pack(pady=2,padx=2,anchor="nw")
        settings=load_settings(SETTINGS_PATH)
        #Light Mode
        def light_mode():
            ctk.set_appearance_mode("light")
            with open(SETTINGS_PATH, "w") as file:
                settings["CTkMode"]="light"
                json.dump(settings, file, indent=2)
        self.lm= ctk.CTkButton(self, text="Light Mode",command=light_mode,anchor="nw")
        self.lm.pack(pady=2)
        #Dark Mode 
        def dark_mode():
            ctk.set_appearance_mode("dark")
            with open(SETTINGS_PATH, "w") as file:
                settings["CTkMode"]="dark"
                json.dump(settings, file, indent=2)
        self.dm= ctk.CTkButton(self, text="Dark Mode",command=dark_mode,anchor="nw")
        self.dm.pack(pady=2)
        self.backmenu= ctk.CTkButton(self, text="Back",command=lambda:parent.show_frame(parent.settings))
        self.backmenu.pack(pady=2)