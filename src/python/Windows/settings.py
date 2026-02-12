import customtkinter as ctk

class Settings(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)
        self.modes=ctk.CTkButton(self,text="Modes",command=lambda:parent.show_frame(parent.modes))
        self.modes.pack(pady=2)
        self.theme= ctk.CTkButton(self, text="Themes",command=lambda:parent.show_frame(parent.themes))
        self.theme.pack(pady=2)
        self.backmenu= ctk.CTkButton(self, text="Back",command=lambda:parent.show_frame(parent.main_menu))
        self.backmenu.pack(pady=2)