import os
import tkinter as tk

# Assets
__location__ = os.path.realpath(os.path.dirname(__file__))

# The main clicker itself
class Main_GUI:
    def __init__(self):
        # Setup
        self.root = tk.Tk()
        self.root.geometry("900x600")
        self.root.title("内内个内个内个内个内个内内")

        # Assets
        # All of these are placeholder
        self.GFX_main_clicker = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'Assets', 'main_clicker.png'))
        self.GFX_printer = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'Assets', 'printer.png'))
        self.GFX_background = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'Assets', 'background.png'))

        # Code
        self.background = tk.Label(image = self.GFX_background)
        self.background.place(x=0, y=0)

        self.printer = tk.Label(image = self.GFX_printer)
        self.printer.place(x=127, y=135)

        self.clicker = tk.Button(width=100, height=100, image = self.GFX_main_clicker)
        self.clicker.place(x=200, y=250)
        
        self.score = tk.IntVar()
        self.counter = tk.Label(textvariable=self.score)
        self.counter.place(x=0, y=0)

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = Main_GUI()
    gui.mainloop()