import os
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk, font
from PIL import ImageTk
from common import *
from login import *

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
        self.canvas.tag_bind(self.image, "<ButtonPress-1>",
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

# Moving object
class moving_object:
    '''
    This class is used for objects that are moveable to resolve crisises
    '''
    object_is_moving = False
    def __init__(self, canvas: tk.Canvas, image: tk.Image, x: int, y:int):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image: int = self.canvas.create_image(x, y, image=image)
        self.get_binds()
    
    def get_binds(self):
        self.canvas.tag_bind(self.image, "<ButtonPress-1>", self.move_start)
        self.canvas.tag_bind(self.image, "<ButtonRelease-1>", self.move_stop)
        self.canvas.tag_bind(self.image, "<B1-Motion>", self.move)

    def move_start(self, event):
        self.object_is_moving = True

        self.current_x_position = event.x
        self.current_y_position = event.y
        self.original_x_position = event.x
        self.original_y_position = event.y

    def move_stop(self, event):
        self.object_is_moving = False

        # TODO: Check for correct filament position when the crisis hits
        if False: # Trigger: The crisis for filaments is happening AND The position is within the bounds
            pass
        else:
            self.x_diff = self.original_x_position - self.current_x_position
            self.y_diff = self.original_y_position - self.current_y_position
            self.canvas.move(self.image, self.x_diff, self.y_diff)

        self.current_x_position = 0
        self.current_y_position = 0

    def move(self, event):
        if self.object_is_moving:
            dx = event.x - self.current_x_position
            dy = event.y - self.current_y_position

            self.canvas.move(self.image, dx, dy)

            self.current_x_position = event.x
            self.current_y_position = event.y

class PowerupDisplay:
    def __init__(self, canvas: tk.Canvas, image: tk.Image | ImageTk.PhotoImage, textvariable, x: int, y: int):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image = self.canvas.create_image(x, y, image=image, anchor='w')
        self.countdown = self.canvas.create_text(
            x + 32,
            y,
            anchor='w',
            fill='white',
            font=font.Font(size=24, weight=font.BOLD),
        )
        self.powerup_description = tk.Label(
            self.canvas,
            textvariable=textvariable,
            font=("Arial", 9),
            background="grey",
            foreground="white",
            justify='left'
        )

        self.hide()
    def appear(self):
        self.canvas.itemconfigure(self.image, state='normal')
        self.canvas.itemconfigure(self.countdown, state='normal')
        self.powerup_description.place(x=0, y=250, anchor='nw')
    def hide(self):
        self.canvas.itemconfigure(self.image, state='hidden')
        self.canvas.itemconfigure(self.countdown, state='hidden')
        self.powerup_description.place_forget()
    def change_image(self, image):
        self.canvas.itemconfigure(self.image, image=image)
    def update_text(self, text):
        self.canvas.itemconfigure(self.countdown, text=text)


# The main clicker itself
class Main_GUI:
    def __init__(self):
        # Setup
        self.root = tk.Tk()
        self.root.minsize(width=400, height=300)
        self.root.title("It's So Joever")
        self.root.resizable(False, False)

        # Assets
        assets = os.path.join(__location__, os.pardir, 'assets')
        self.GFX_main_clicker = tk.PhotoImage(file=os.path.join(assets, 'sutdCoin100.png'))
        self.GFX_printer = tk.PhotoImage(file=os.path.join(assets, 'pixelPrinter.png'))
        self.GFX_printer_head = tk.PhotoImage(file=os.path.join(assets, 'pixelPrinterHead.png'))
        self.GFX_background = tk.PhotoImage(file=os.path.join(assets, 'background.png'))
        
        POWERUP_SIZE = (128,128)
        image = ImageTk.Image.open(os.path.join(assets, 'jovan eepy.jpg')).resize(POWERUP_SIZE)
        self.GFX_november = ImageTk.PhotoImage(image)
        image = ImageTk.Image.open(os.path.join(assets, 'douyinIon.jpg')).resize(POWERUP_SIZE)
        self.GFX_douyin = ImageTk.PhotoImage(image)
        image = ImageTk.Image.open(os.path.join(assets, 'anyquadratic.jpg')).resize(POWERUP_SIZE)
        self.GFX_anyquadratic = ImageTk.PhotoImage(image)

        self.menu_frame = ttk.Frame()
        self.menu_frame.pack()
        
        self.active_frame = self.menu_frame
        self.create_menu_frame()

        self.game_frame = ttk.Frame()
        self.create_game_frame()
        
        self.name_frame = ttk.Frame()
        self.create_name_frame()
        self.score_frame = ttk.Frame()
        self.create_score_frame()
    
    def create_menu_frame(self):
        master = self.menu_frame
        # TODO: Image
        self.title_image = ttk.Label(
            master,
            text="Jo's\n3D Printing Adventure",
            font=font.Font(
                family="Comic Sans MS",
                size=18,
                weight='bold',
                slant='italic'
            ),
            justify='center'
            )
        self.title_image.pack()
        
        self.play_callback = lambda: None

        # using lambdas to pass function with pre-filled arguments
        self.play_button = ttk.Button(
            master,
            text="Play",
            command=lambda: self.change_frame(self.name_frame),
            width=32
            )
        self.play_button.pack()
        self.scoreboard_button = ttk.Button(
            master,
            text="Scoreboard",
            command=lambda: self.change_frame(self.score_frame),
            width=32
            )
        self.scoreboard_button.pack()
        self.exit_button = ttk.Button(
            master,
            text="Exit",
            command=self.root.destroy,
            width=32
            )
        self.exit_button.pack()
    
    # TODO: Nicholas
    def create_score_frame(self):
        master = self.score_frame
    
    def create_name_frame(self):
        self.loginobject = Login(self.root)
        self.name_frame = self.loginobject.root
        def play_callback():
            self.change_frame(self.game_frame)
            self.on_play()
        self.loginobject.play_callback = play_callback


    def create_game_frame(self):
        master = self.game_frame
        self.background = tk.Canvas(master, width=900, height=600)
        self.background.create_image(450, 300, image=self.GFX_background)
        self.background.create_image(450, 300, image=self.GFX_printer )

        self.background.pack()

        self.printer_head = Print_Head(self.background, self.GFX_printer_head, 340, 300)
        self.clicker = Clicker_Button(self.background, self.GFX_main_clicker, 450, 240)
        # This is for testing
        self.filament = moving_object(self.background, self.GFX_main_clicker, 450, 100) # TODO: Replace with actual asset

        # Username display
        self.test_username = tk.StringVar()
        display = tk.Label(
            master,
            textvariable=self.test_username,
            font=("Arial", 20),
            background="grey",
            foreground="white"
        )
        display.place(anchor = "nw")

        # Time display
        self.time_remaining = tk.StringVar()
        display = tk.Label(
            master,
            textvariable=self.time_remaining,
            font=("Arial", 20),
            background="grey",
            foreground="white"
        )
        display.place(x = 0, y = 40)

        # Total
        self.score = tk.IntVar()
        counter = tk.Label(
            master,
            textvariable=self.score,
            font=("Arial", 20),
            background="grey",
            foreground="white",
            width=5
        )
        counter.place(x=409, y=370)
        
        # Prints per click
        self.ppc_display = tk.StringVar()
        counter = tk.Label(
            master,
            textvariable=self.ppc_display,
            font=("Arial", 14),
            background="grey",
            foreground="white",
            width=17
        )
        counter.place(x=354, y=410)
        
        # Prints per second
        self.pps_display = tk.StringVar()
        counter = tk.Label(
            master,
            textvariable=self.pps_display,
            font=("Arial", 12),
            background="grey",
            foreground="white",
            width=17
        )
        counter.place(x=370, y=440)
        
        self.powerup_string = tk.StringVar()
        self.powerup_display = PowerupDisplay(
            self.background,
            self.GFX_november,
            self.powerup_string,
            0,
            200
        )
    
    def show_powerup_popup(self, powerup: Powerup, time: int):
        match powerup:
            case Powerup.Anyquadratic:
                powerup_string = "You got a free\nAnyquadratic printer!"
                image = self.GFX_anyquadratic
            case Powerup.Bamboo:
                powerup_string = "You got a free\nBamboo printer!"
                image = self.GFX_anyquadratic
            case Powerup.DouyinIonThrusters:
                powerup_string = "Douyin Ion Thrusters are\npowering your printer"
                image = self.GFX_douyin
            case Powerup.November:
                powerup_string = "Jovan is coming to help you"
                image = self.GFX_november

        self.powerup_display.appear()
        self.powerup_string.set(powerup_string)
        self.powerup_display.change_image(image=image)
        
    def create_crisis(self, crisis_index):
        messagebox.askquestion("Crisis!", "Printing has stopped", type=messagebox.OK)

        # No Filament
        if crisis_index == 1:
            pass

        # No Plate
        elif crisis_index == 2:
            pass
    
    def popup_fablab(self):
        messagebox.askquestion("Crisis Resolved", "Fablab staff have come to fix your problems", type=messagebox.OK)
    
    def change_frame(self, new_frame: ttk.Frame | tk.Frame):
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