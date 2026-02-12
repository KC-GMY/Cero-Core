import customtkinter as ctk
from database import drop_table

class Reset(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)
        self.header=ctk.CTkLabel(self,text="Are you sure?")
        self.header.pack(pady=2,padx=5,anchor="nw")
        self.answer=ctk.CTkFrame(self, fg_color="transparent")
        self.answer.pack()
        self.yes=ctk.CTkButton(self.answer, text='Yes',
        command=lambda:(drop_table(),parent.winfo_toplevel().rebuild_ui()),width=20,height=25)
        self.yes.pack(side="left",padx=10)
        self.no=ctk.CTkButton(self.answer, text='No', command=lambda:parent.show_frame(parent.main_menu),width=20,height=25)
        self.no.pack(side="left",padx=10)