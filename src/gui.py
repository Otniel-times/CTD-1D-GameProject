import os
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk

# Assets
__location__ = os.path.realpath(os.path.dirname(__file__))
# https://stackoverflow.com/questions/70996098/tkinter-button-over-transparent-background
#TBD
class Clicker_Button():
    clicker_animation_delay = 100
    def __init__(self, canvas: tk.Canvas, image: tk.Image, x: int, y: int, **kwargs):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image: int = self.canvas.create_image(x, y, image=image)

    def on_click(self, fn):
        self.canvas.tag_bind(self.image, "<ButtonRelease-1>",
            lambda event: (self.clicker_flash(), fn()))
        
    # Button animation function
    def clicker_flash(self):
        self.canvas.move(self.image, 0, -5)
        self.canvas.after(self.clicker_animation_delay, self.set_state)

    def set_state(self):
        self.canvas.move(self.image, 0, 5)

class Print_Head():
    print_head_animation_delay = 10
    def __init__(self, canvas: tk.Canvas, image: tk.Image, x: int, y: int, **kwargs):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image: int = self.canvas.create_image(x, y, image=image)
        self.animation_offset = 0
        self.animation_ongoing = False

    def animation_check(self):
        if not self.animation_ongoing:
            self.animation_ongoing = True
            self.go_right()

    def go_right(self):
        self.canvas.move(self.image, 10, 0)
        self.animation_offset += 10
        if self.animation_offset < 220:
            self.canvas.after(self.print_head_animation_delay, self.go_right)
        else:
            self.go_left()

    def go_left(self):
        self.canvas.move(self.image, -10, 0)
        self.animation_offset -= 10
        if self.animation_offset > 0:
            self.canvas.after(self.print_head_animation_delay, self.go_left)
        else:
            self.animation_ongoing = False

# The main clicker itself
class Main_GUI:
    def __init__(self):
        # Setup
        self.root = tk.Tk()
        self.root.geometry("900x600")
        self.root.title("内内个内个内个内个内个内内")

        # Assets
        self.GFX_main_clicker = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'assets', 'sutdCoin100.png'))
        self.GFX_printer = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'assets', 'pixelPrinter.png'))
        self.GFX_printer_head = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'assets', 'pixelPrinterHead.png'))
        self.GFX_background = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'assets', 'background.png')) # TODO: Replace Placeholder

        # Code
        self.background = tk.Canvas(width=900, height=600)
        self.background.create_image(450, 300, image=self.GFX_background)
        self.background.create_image(450, 300, image=self.GFX_printer )

        self.background.place(x=0, y=0)

        self.clicker = Clicker_Button(self.background, self.GFX_main_clicker, 450, 240)
        self.printer_head = Print_Head(self.background, self.GFX_printer_head, 340, 300)
        # Total
        self.score = tk.IntVar()
        self.counter = tk.Label(textvariable=self.score, font=("Arial", 20), background="grey", foreground="white", width=5)
        self.counter.place(x=409, y=370)
        
        # Prints per click
        self.ppc_display = tk.StringVar()
        self.counter = tk.Label(textvariable=self.ppc_display, font=("Arial", 14), background="grey", foreground="white", width=17)
        self.counter.place(x=354, y=410)
        
        # Prints per second
        self.pps_display = tk.StringVar()
        self.counter = tk.Label(textvariable=self.pps_display, font=("Arial", 12), background="grey", foreground="white", width=17)
        self.counter.place(x=370, y=440)

        self.animation_offset = 0
        self.animation_ongoing = False
        
    def create_crisis(self, crisis_name, crisis_text):
        messagebox.askquestion(crisis_name, crisis_text, type=messagebox.OK)

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = Main_GUI()
    gui.mainloop()