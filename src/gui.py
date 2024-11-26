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
        self.GFX_main_clicker = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'Assets', 'sutdCoin100.png'))
        self.GFX_printer = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'Assets', 'pixelPrinter.png'))
        self.GFX_background = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'Assets', 'background.png'))

        # Code
        self.background = tk.Label(image = self.GFX_background)
        self.background.place(x=0, y=0)

        self.printer = tk.Label(image = self.GFX_printer)
        self.printer.place(x=260, y=71)

        self.clicker = tk.Button(width=100, height=100, image = self.GFX_main_clicker)
        self.clicker.place(x=397, y=250)
        
        # Total
        self.score = tk.IntVar()
        self.counter = tk.Label(textvariable=self.score, font=("Arial", 18), background="grey", foreground="white", width=5)
        self.counter.place(x=410, y=150)
        
        # Prints per click
        self.ppc_display = tk.IntVar()
        self.counter = tk.Label(textvariable=self.ppc_display, font=("Arial", 14), background="grey", foreground="white", width=17)
        self.counter.place(x=350, y=190)
        
        # Prints per click
        self.pps_display = tk.IntVar()
        self.counter = tk.Label(textvariable=self.pps_display, font=("Arial", 12), background="grey", foreground="white", width=17)
        self.counter.place(x=365, y=220)

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = Main_GUI()
    gui.mainloop()