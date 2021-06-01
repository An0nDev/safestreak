import tkinter

class safestreakApp (tkinter.Tk):
    def __init__ (self):
        super ().__init__ ()
        self.attributes ("-topmost", True)
        self.wait_visibility (self)
        self.wm_attributes ("-alpha", 0.5)
        self.configure (bg = "black")
        self.wm_title ("safestreak")
        self.test_text = tkinter.Label (self, text = "BOTTOM TEXT", bg = "black", fg = "white", font = ("Impact", 36))
        self.test_text.pack ()

app = safestreakApp ()
app.mainloop ()