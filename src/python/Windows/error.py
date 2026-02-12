import customtkinter as ctk

class Error(ctk.CTkFrame):
    def __init__(self, parent,msg):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)
        self.readlabel=ctk.CTkLabel(self,text=msg)
        self.readlabel.place(relx=0.5, rely=0.45, anchor="center")
        self.backmenu = ctk.CTkButton(self, text='Back',command=lambda:parent.show_frame(parent.tools))
        self.backmenu.place(relx=0.5, rely=0.65, anchor="center")