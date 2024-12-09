import os
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk, font
from PIL import ImageTk
from common import *
from login import *
from leaderboard import *

# Assets
__location__ = os.path.realpath(os.path.dirname(__file__))
# https://stackoverflow.com/questions/70996098/tkinter-button-over-transparent-background
#TBD
class Clicker_Button():
    '''
    The SUTD Coin button
    '''
    def __init__(self, canvas: tk.Canvas, image: tk.Image, x: int, y: int, **kwargs):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image: int = self.canvas.create_image(x, y, image=image)
        self.clicker_animation_delay = 100

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
    '''
    The moving printer head with animation checks etc.
    '''
    print_head_animation_delay = 10
    def __init__(self, canvas: tk.Canvas, image: tk.Image, x: int, y: int):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image: int = self.canvas.create_image(x, y, image=image)
        self.animation_offset = 0
        self.animation_ongoing = False
        self.enabled = True

    def animation_check(self):
        if not self.animation_ongoing and self.enabled:
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
class Moving_Object:
    '''
    This class is used for objects that are moveable to resolve crisises
    (x/y)_(lower/upper) is for the bounds of the final dragging position.
    '''
    def __init__(self, canvas: tk.Canvas, image: tk.Image, x: int, y:int, x_lower: int, x_upper: int, y_lower: int, y_upper: int, crisis_id: int):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image: int = self.canvas.create_image(x, y, image=image)
        self.object_is_moving = False
        self.x_lower = x_lower
        self.x_upper = x_upper
        self.y_lower = y_lower
        self.y_upper = y_upper
        self.crisis_id = crisis_id
        
        self.get_binds()

        self.callback = lambda: None
    
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

        # print(f"self.current_x_position: {self.current_x_position:}, self.x_lower: {self.x_lower}, self.x_upper: {self.x_upper}")
        # print(f"self.current_y_position: {self.current_y_position:}, self.y_lower: {self.y_lower}, self.y_upper: {self.y_upper}")

        # The position is within the bounds, x_lower < (current x) < x_upper and y_lower < (current y) < y_upper
        if self.current_x_position > self.x_lower and self.current_x_position < self.x_upper and self.current_y_position > self.y_lower and self.current_y_position < self.y_upper:
            self.callback()
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

# The main game GUI
class Main_GUI:
    def __init__(self):
        # Setup
        self.root = tk.Tk()
        self.root.minsize(width=900, height=600)
        self.root.title("Jo's 3D Printing Adventure")
        self.root.resizable(False, False)

        # Assets
        assets = os.path.join(__location__, os.pardir, 'assets')
        self.GFX_main_clicker = tk.PhotoImage(file=os.path.join(assets, 'sutdCoin100.png'))
        self.GFX_printer = tk.PhotoImage(file=os.path.join(assets, 'Printer.png'))
        self.GFX_printer_head = tk.PhotoImage(file=os.path.join(assets, 'Printer Head.png'))
        self.GFX_background = tk.PhotoImage(file=os.path.join(assets, 'background.png'))
        self.GFX_background_title = tk.PhotoImage(file=os.path.join(assets, 'backgroundTitle.png'))
        self.GFX_filament_static = tk.PhotoImage(file=os.path.join(assets, 'Filament (In AMS).png'))

        # Moving asset
        self.GFX_filament = tk.PhotoImage(file=os.path.join(assets, 'Filament.png'))
        self.GFX_printer_bed = tk.PhotoImage(file=os.path.join(assets, 'Print Bed.png'))

        # Title
        self.GFX_title = tk.PhotoImage(file=os.path.join(assets, 'Title.png'))
        
        # Powerups
        POWERUP_SIZE = (260,260)
        image = ImageTk.Image.open(os.path.join(assets, 'jovan eepy.jpg')).resize(POWERUP_SIZE)
        self.GFX_november = ImageTk.PhotoImage(image)
        image = ImageTk.Image.open(os.path.join(assets, 'douyinIon.jpg')).resize(POWERUP_SIZE)
        self.GFX_douyin = ImageTk.PhotoImage(image)
        image = ImageTk.Image.open(os.path.join(assets, 'anyquadratic.png')).resize(POWERUP_SIZE)
        self.GFX_anyquadratic = ImageTk.PhotoImage(image)
        image = ImageTk.Image.open(os.path.join(assets, 'bamboo.png')).resize(POWERUP_SIZE)
        self.GFX_bamboo = ImageTk.PhotoImage(image)

        self.menu_frame = ttk.Frame()
        self.menu_frame.pack()
        
        self.active_frame = self.menu_frame
        self.create_menu_frame()

        self.game_frame = ttk.Frame()
        self.create_game_frame()
        
        self.name_frame = ttk.Frame()
        self.create_name_frame()
        self.score_frame = ttk.Frame()
        #self.create_score_frame()
    
    def create_menu_frame(self):
        master = self.menu_frame
        self.title_image = tk.Label(
            master,
            image=self.GFX_background_title
            )
        self.title_image.pack()
        self.play_callback = lambda: None

        s = ttk.Style()

        # using lambdas to pass function with pre-filled arguments
        self.play_button = ttk.Button(
            master,
            text="Play",
            command=lambda: self.change_frame(self.name_frame),
            width=32,
            style='my.TButton'
            )
        self.play_button.place(x=239,y=300)
        self.scoreboard_button = ttk.Button(
            master,
            text="Scoreboard",
            command=lambda: self.change_frame(self.score_frame),
            width=32,
            style='my.TButton'
            )
        self.scoreboard_button.place(x=239,y=350)
        self.exit_button = ttk.Button(
            master,
            text="Exit",
            command=self.root.destroy,
            width=32,
            style='my.TButton'
            )
        
        s.configure('my.TButton', font=('Helvetica', 18))
        self.exit_button.place(x=239,y=400)
    
    # TODO: Nicholas
    
    def create_score_frame(self):
        self.scoreobject = Leaderboard(self.root)
        self.score_frame = self.scoreobject.root

    def create_name_frame(self):
        self.loginobject = Login(self.root)
        self.name_frame = self.loginobject.root
        self.loginobject.play_callback = self.on_play


    def create_game_frame(self):
        master = self.game_frame
        self.background = tk.Canvas(master, width=900, height=600)
        self.background.create_image(450, 300, image=self.GFX_background)
        self.background.create_image(450, 300, image=self.GFX_printer )
        self.filament_static = self.background.create_image(350, 18, image=self.GFX_filament_static)
        self.printer_bed_static = self.background.create_image(447, 486, image=self.GFX_printer_bed)

        self.background.pack()

        self.printer_head = Print_Head(self.background, self.GFX_printer_head, 340, 430)
        self.clicker = Clicker_Button(self.background, self.GFX_main_clicker, 450, 325)
        self.filament = Moving_Object(self.background, self.GFX_filament, 800, 500, 295, 408, 2, 115, 1)
        self.printer_bed = Moving_Object(self.background, self.GFX_printer_bed, 800, 600, 321, 566, 458, 514, 2)

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
        # Time till fablab staff intervenes
        self.time_intervention = tk.StringVar()
        display = tk.Label(
            master,
            textvariable=self.time_intervention,
            font=("Arial", 20),
            background="grey",
            foreground="white",
            justify='left'
        )
        display.place(x = 0, y = 80)

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
        counter.place(x=407, y=230)
        
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
        counter.place(x=354, y=520)
        
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
        counter.place(x=370, y=550)
        
        self.powerup_string = tk.StringVar()
        self.powerup_display = PowerupDisplay(
            self.background,
            self.GFX_november,
            self.powerup_string,
            0,
            400
        )
    
    def register_callbacks(self, play, name, clicker, resolve_filament, resolve_bed, resolve_error):
        self.play_callback = play
        self.loginobject.name_callback = name
        self.clicker.on_click(clicker)
        self.filament.callback = resolve_filament
        self.printer_bed.callback = resolve_bed

    def update_print_display(self, prints_per_click, prints_per_sec):
        self.ppc_display.set(f"Prints per click: {prints_per_click}")
        self.pps_display.set(f"Auto Prints/sec: {prints_per_sec}")
    
    def update_time_display(self, time, time_crisis_start):
        time_remaining_minutes = time // 60
        time_remaining_seconds = time % 60
        time_string = f"{time_remaining_minutes :02d}:{time_remaining_seconds :02d}"
        self.time_remaining.set(time_string)
        print(time_string)

        time_till_intervention = FABLAB_TIMEOUT - time_crisis_start + time
        if time_till_intervention <= 0 or time_crisis_start <= 0:
            self.time_intervention.set("")
        else:
            self.time_intervention.set(f"{time_till_intervention :02d}s\nUntil Intervention\nby Lab Staff")
    
    def show_powerup_popup(self, powerup: Powerup, time: int):
        match powerup:
            case Powerup.Anyquadratic:
                powerup_string = "You got a free\nAnyquadratic printer!"
                image = self.GFX_anyquadratic
            case Powerup.Bamboo:
                powerup_string = "You got a free\nBamboo printer!"
                image = self.GFX_bamboo
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
        messagebox.askquestion(
            "Crisis!",
            "Printing has stopped",
            type=messagebox.OK,
            icon=messagebox.ERROR
        )
        self.printer_head.enabled = False
        self.current_crisis_index = crisis_index

        # No Filament
        if crisis_index == 1:
            self.background.itemconfigure(self.filament_static, state='hidden')

        # No Plate
        elif crisis_index == 2:
            self.background.itemconfigure(self.printer_bed_static, state='hidden')

        # Error code
        elif crisis_index == 3:
            pass
    
    # Used to re-show elements that have been hidden by crisises
    def show_filament(self):
        self.background.itemconfigure(self.filament_static, state='normal')

    def show_plate(self):
        self.background.itemconfigure(self.printer_bed_static, state='normal')

    def user_resolved(self):
        self.printer_head.enabled = True

    def popup_fablab(self):
        messagebox.askquestion(
            "Crisis Resolved",
            "Fablab staff have come to fix your problems",
            type=messagebox.OK,
            icon=messagebox.WARNING
        )
        self.printer_head.enabled = True
    
    def change_frame(self, new_frame: ttk.Frame | tk.Frame):
        if new_frame is self.game_frame:
            self.loginobject.button.configure(state=tk.DISABLED)
        else:
            self.loginobject.button.configure(state=tk.NORMAL)
        self.active_frame.pack_forget()
        self.active_frame = new_frame
        self.active_frame.pack()
    
    def on_play(self):
        if self.active_frame is self.game_frame:
            return
        self.change_frame(self.game_frame)
        self.play_callback()

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = Main_GUI()
    gui.mainloop()