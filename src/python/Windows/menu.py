import customtkinter as ctk

class Menu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.place(relwidth=1, relheight=1)
        self.main= ctk.CTkButton(self, text="Tools Menu", command=lambda:parent.show_frame(parent.tools))
        self.main.pack(pady=2)
        self.settings= ctk.CTkButton(self, text="Settings", compound="left",command=lambda:parent.show_frame(parent.settings))
        self.settings.pack(pady=2)
        self.reset= ctk.CTkButton(self, text="Reset", compound="left",command=lambda:parent.show_frame(parent.reset))
        self.reset.pack(pady=2)