import customtkinter as ctk
from Windows.functions import Record,get_tool_header,get_tool_rec
from Windows.arduino_uploader import target_change_async
class ToolsFrame(ctk.CTkFrame):
    def __init__(self,parent,tool):
        super().__init__(parent)
        self.place(relwidth=1,relheight=1)
        self.label=ctk.CTkLabel(self,text=get_tool_header(tool))
        self.label.pack(pady=2,padx=2,anchor="nw")
        button_frame= ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack()
        def on_read():
            if tool in ("kHz","MHz"):
                parent.show_frame(parent.tools_read)
                target_change_async(tool,parent)
                self.after(1000, lambda: Record(tool, parent))
                return
            elif tool in("GHz","Ir"):
                parent.show_frame(parent.error_feature)
                return
        self.read= ctk.CTkButton(button_frame, text='Read',command=on_read,width=20,height=25)    
        self.read.pack(side="left",padx=10)
        self.write= ctk.CTkButton(button_frame, text='Saved',command=lambda:parent.show_frame(get_tool_rec(parent, tool)),width=20,height=25)
        self.write.pack(side="left",padx=10)
        self.backmenu= ctk.CTkButton(self, text='Back',command=lambda:parent.show_frame(parent.tools))
        self.backmenu.pack(pady=10)