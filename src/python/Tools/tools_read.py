import customtkinter as ctk

class ToolsRead(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)
        self.readlabel=ctk.CTkLabel(self,text="Reading...")
        self.readlabel.place(relx=0.5, rely=0.5, anchor="center")