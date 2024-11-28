import os
import tkinter as tk

# Assets
__location__ = os.path.realpath(os.path.dirname(__file__))
# https://stackoverflow.com/questions/70996098/tkinter-button-over-transparent-background
#TBD
class CanvasButton():
    flash_delay = 100
    def __init__(self, canvas: tk.Canvas, image: tk.Image, x: int, y: int, **kwargs):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image: int = self.canvas.create_image(x, y, image=image)
    def on_click(self, fn):
        self.canvas.tag_bind(self.image, "<ButtonRelease-1>",
            lambda event: (self.flash(), fn()))
    # Button animation function
    def flash(self):
        #self.set_state(tk.HIDDEN)
        self.canvas.move(self.image, -10, 0)
        self.canvas.after(self.flash_delay, self.set_state, tk.NORMAL)
    def set_state(self, state):
        self.canvas.move(self.image, 10, 0)


# The main clicker itself
class Main_GUI:
    def __init__(self):
        # Setup
        self.root = tk.Tk()
        self.root.geometry("900x600")
        self.root.title("内内个内个内个内个内个内内")

        # Assets
        # All of these are placeholder
        self.GFX_main_clicker = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'assets', 'sutdCoin100.png'))
        self.GFX_printer = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'assets', 'pixelPrinter.png'))
        self.GFX_background = tk.PhotoImage(file=os.path.join(__location__, os.pardir, 'assets', 'background.png'))


        # Code
        self.background = tk.Canvas(width=900, height=600)
        self.background.create_image(450, 300, image=self.GFX_background)
        self.background.create_image(450, 300, image=self.GFX_printer )

        self.background.place(x=0, y=0)

        self.clicker = CanvasButton(self.background, self.GFX_main_clicker, 450, 300)
        # Total
        self.score = tk.IntVar()
        self.counter = tk.Label(textvariable=self.score, font=("Arial", 20), background="grey", foreground="white", width=5)
        self.counter.place(x=409, y=370)
        
        # Prints per click
        self.ppc_display = tk.StringVar()
        self.counter = tk.Label(textvariable=self.ppc_display, font=("Arial", 14), background="grey", foreground="white", width=17)
        self.counter.place(x=354, y=410)
        
        # Prints per click
        self.pps_display = tk.StringVar()
        self.counter = tk.Label(textvariable=self.pps_display, font=("Arial", 12), background="grey", foreground="white", width=17)
        self.counter.place(x=370, y=440)

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = Main_GUI()
    gui.mainloop()