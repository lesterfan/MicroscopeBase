import Tkinter as tk
import tkMessageBox

class MappingGUI():
    """description of class"""
    master = None
    frame = None

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()
