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
    def __init__(self, canvas: tk.Canvas, image: tk.Image, x: int, y: int):
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

# Filament
class Filament:
    object_is_moving = False
    def __init__(self, canvas: tk.Canvas, image: tk.Image, x: int, y:int):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image: int = self.canvas.create_image(x, y, image=image)
    
    def get_binds(self,fn):
        self.canvas.tag_bind(self.image, "<ButtonPress-1>", lambda event: (self.move_start(), fn()))
        self.canvas.tag_bind(self.image, "<ButtonRelease-1>", lambda event: (self.move_stop(), fn()))
        self.canvas.tag_bind(self.image, "<B1-Motion>", lambda event: (self.move(), fn()))

    def move_start(self, event):
        self.object_is_moving = True

        self.current_x_position = event.x
        self.current_y_position = event.y

    def move_stop(self):
        self.object_is_moving = False

        self.current_x_position = 0
        self.current_y_position = 0

    def move(self, event):
        if self.object_is_moving:
            dx = event.x - self.current_x_position
            dy = event.y - self.current_y_position

            self.canvas.move(self.image, dx, dy)

            self.current_x_position = event.x
            self.current_y_position = event.y


# The main clicker itself
class Main_GUI:
    def __init__(self):
        # Setup
        self.root = tk.Tk()
        #self.root.geometry("900x600")
        self.root.minsize(width=400, height=300)
        self.root.title("It's So Joever")
        self.root.resizable(False, False)
        
        self.menu_frame = ttk.Frame()
        self.menu_frame.pack()
        
        self.active_frame = self.menu_frame
        
        # TODO: Image
        self.title_image = ttk.Label(
            self.menu_frame,
            text="Jo's 3D Printing Adventure",
            )
        self.title_image.pack()
        
        self.play_callback = lambda: None

        self.play_button = ttk.Button(
            self.menu_frame,
            text="Play",
            command=self.on_play,
            width=32
            )
        self.play_button.pack()
        # TODO: open scoreboard
        self.scoreboard_button = ttk.Button(
            self.menu_frame,
            text="Scoreboard",
            command=lambda: self.change_frame(self.score_frame),
            width=32
            )
        self.scoreboard_button.pack()
        self.exit_button = ttk.Button(
            self.menu_frame,
            text="Exit",
            command=self.root.destroy,
            width=32
            )
        self.exit_button.pack()

        self.game_frame = ttk.Frame()
        self.create_game_frame()
        
        self.name_frame = ttk.Frame()
        self.score_frame = ttk.Frame()

    def create_game_frame(self):
        # Assets
        asset_folder = os.path.join(__location__, os.pardir, 'assets')
        self.GFX_main_clicker = tk.PhotoImage(file=os.path.join(asset_folder, 'sutdCoin100.png'))
        self.GFX_printer = tk.PhotoImage(file=os.path.join(asset_folder, 'pixelPrinter.png'))
        self.GFX_printer_head = tk.PhotoImage(file=os.path.join(asset_folder, 'pixelPrinterHead.png'))
        self.GFX_background = tk.PhotoImage(file=os.path.join(asset_folder, 'background.png')) # TODO: Replace Placeholder

        # Code
        self.background = tk.Canvas(self.game_frame, width=900, height=600)
        self.background.create_image(450, 300, image=self.GFX_background)
        self.background.create_image(450, 300, image=self.GFX_printer )

        self.background.pack()

        self.printer_head = Print_Head(self.background, self.GFX_printer_head, 340, 300)
        self.clicker = Clicker_Button(self.background, self.GFX_main_clicker, 450, 240)
        self.filament = Filament(self.background, self.GFX_main_clicker, 450, 100)

        # Username display
        self.test_username = tk.StringVar()
        self.username_display = tk.Label(
            self.game_frame,
            textvariable=self.test_username,
            font=("Arial", 20),
            background="grey",
            foreground="white"
            )
        self.username_display.place(anchor = "nw")

        # Total
        self.score = tk.IntVar()
        self.counter = tk.Label(
            self.game_frame,
            textvariable=self.score,
            font=("Arial", 20),
            background="grey",
            foreground="white",
            width=5
            )
        self.counter.place(x=409, y=370)
        
        # Prints per click
        self.ppc_display = tk.StringVar()
        self.counter = tk.Label(
            self.game_frame,
            textvariable=self.ppc_display,
            font=("Arial", 14),
            background="grey",
            foreground="white",
            width=17
            )
        self.counter.place(x=354, y=410)
        
        # Prints per second
        self.pps_display = tk.StringVar()
        self.counter = tk.Label(
            self.game_frame,
            textvariable=self.pps_display,
            font=("Arial", 12),
            background="grey",
            foreground="white",
            width=17
            )
        self.counter.place(x=370, y=440)

        self.animation_offset = 0
        self.animation_ongoing = False
        
    def create_crisis(self, crisis_name, crisis_text):
        messagebox.askquestion(crisis_name, crisis_text, type=messagebox.OK)
    
    def change_frame(self, new_frame: ttk.Frame):
        self.active_frame.pack_forget()
        self.active_frame = new_frame
        self.active_frame.pack()
    
    def on_play(self):
        self.change_frame(self.game_frame)
        self.play_callback()

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = Main_GUI()
    gui.mainloop()