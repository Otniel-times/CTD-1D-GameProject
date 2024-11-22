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
        GFX_main_clicker = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'Assets', 'main_clicker.png'))

        # Code
        self.clicker = tk.Button(width=200, height=200, image = GFX_main_clicker)
        self.clicker.place(x=50, y=260)

        self.root.mainloop()

if __name__ == "__main__":
    Main_GUI()