import os
import tkinter as tk

# Assets
__location__ = os.path.realpath(os.path.dirname(__file__))

# The main clicker itself
class Main_GUI:
    def __init__(self):
        # Setup
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("Jovan Clicker")

        # Assets
        # need to be attribute otherwise it will be deleted after __init__ finishes
        self.GFX_main_clicker = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'Assets', 'main_clicker.png'))
        
        self.onclick = lambda: None

        # Code
        self.clicker = tk.Button(width=200, height=200, image = self.GFX_main_clicker)
        self.clicker.place(x=150, y=260)
        
        self.score = tk.IntVar()
        self.counter = tk.Label(textvariable=self.score)
        self.counter.place(x=0, y=0)
        
        # cannot execute mainloop here because need to configure gui in other
        # file

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = Main_GUI()
    gui.mainloop()