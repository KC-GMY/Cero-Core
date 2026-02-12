import customtkinter as ctk
from .functions import Scrollframe_color,theme_set

class Theme(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)
        scroll_frame = ctk.CTkScrollableFrame(
            self,border_width=0,corner_radius=0,label_text="Themes Menu:",label_anchor="nw",fg_color=Scrollframe_color())
        scroll_frame.pack(padx=3, pady=5,expand=True)
        self.orange= ctk.CTkButton(scroll_frame, text="Orange", command=lambda: theme_set(self.orange.cget("text"),parent),anchor="nw")
        self.orange.pack(pady=2)
        self.violet= ctk.CTkButton(scroll_frame, text="Violet", command=lambda: theme_set(self.violet.cget("text"),parent),anchor="nw")
        self.violet.pack(pady=2)
        self.red= ctk.CTkButton(scroll_frame, text="Red", command=lambda: theme_set(self.red.cget("text"),parent),anchor="nw")
        self.red.pack(pady=2)
        self.pink= ctk.CTkButton(scroll_frame, text="Pink", command=lambda: theme_set(self.pink.cget("text"),parent),anchor="nw")
        self.pink.pack(pady=2)
        self.coffee= ctk.CTkButton(scroll_frame, text="Coffee", command=lambda: theme_set(self.coffee.cget("text"),parent),anchor="nw")
        self.coffee.pack(pady=2)
        self.backmenu= ctk.CTkButton(scroll_frame, text="Back", command=lambda: parent.show_frame(parent.settings))
        self.backmenu.pack(pady=2)