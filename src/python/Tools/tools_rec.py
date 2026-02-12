import customtkinter as ctk
from Windows.functions import Scrollframe_color,load_readings

class ToolsRec(ctk.CTkFrame):
    def __init__(self,parent,tool):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)
        self.scroll_frame = ctk.CTkScrollableFrame(self,border_width=0,corner_radius=0,
                                              label_text="Recordings:",label_anchor="nw",
            fg_color=Scrollframe_color())
        load_readings(self,tool,parent)
        self.scroll_frame.pack(padx=3, pady=5, expand=True)

    def refresh(self,tool,parent):
        load_readings(self,tool,parent)