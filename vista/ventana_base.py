from tkinter import Toplevel

class VentanaBase(Toplevel):
    def __init__(self, master, titulo):
        super().__init__(master)
        self.title(titulo)
        self.geometry("400x400+100+20")
        self.config(bg="#1A477A", padx=10, pady=10)
        self.resizable(False, False)