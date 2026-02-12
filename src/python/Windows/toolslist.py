import customtkinter as ctk
from .functions import Scrollframe_color
class ToolsList(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)
        scroll_frame = ctk.CTkScrollableFrame(self,border_width=0,corner_radius=0,
                    label_text="Tools Menu:",label_anchor="nw",fg_color=Scrollframe_color())
        scroll_frame.pack(padx=3,pady=5,expand=True)
        self.rfid= ctk.CTkButton(scroll_frame, text="125 kHz RFID", command=lambda:(parent.show_frame(parent.tool_khz)),anchor="w")
        self.rfid.pack(pady=2)
        self.mhz=ctk.CTkButton(scroll_frame, text="13.56 MHz NFC", command=lambda:(parent.show_frame(parent.tool_mhz)),anchor="w")
        self.mhz.pack(pady=2)
        self.sghz= ctk.CTkButton(scroll_frame, text="Sub-GHz RF", command=lambda: parent.show_frame(parent.tool_ghz),anchor="w")
        self.sghz.pack(pady=2)
        self.ir= ctk.CTkButton(scroll_frame, text="Infrared", command=lambda: parent.show_frame(parent.tool_ir),anchor="w")
        self.ir.pack(pady=2)
        self.backmenu= ctk.CTkButton(scroll_frame, text='Back', command=lambda: parent.show_frame(parent.main_menu))
        self.backmenu.pack(pady=2)