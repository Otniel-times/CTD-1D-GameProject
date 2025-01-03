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
    # Shift the button up and down
    def clicker_flash(self):
        self.canvas.move(self.image, 0, -5)
        self.canvas.after(self.clicker_animation_delay, self.set_state)

    def set_state(self):
        self.canvas.move(self.image, 0, 5)

class Print_Head():
    '''
    The moving printer head with animation checks etc.
    '''
    def __init__(self, canvas: tk.Canvas, image: tk.Image, x: int, y: int):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image: int = self.canvas.create_image(x, y, image=image)
        self.print_head_animation_delay = 10
        self.animation_offset = 0
        self.animation_ongoing = False
        self.enabled = True

    def animation_check(self):
        """
        Function to be called to begin animation
        """
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
    def __init__(
            self,
            canvas: tk.Canvas,
            image: tk.Image,
            x: int,
            y:int,
            x_lower: int,
            x_upper: int,
            y_lower: int,
            y_upper: int,
            crisis_id: int
        ):
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
        """
        Bind mouse for drag and drop interaction
        """
        self.canvas.tag_bind(self.image, "<ButtonPress-1>", self.move_start)
        self.canvas.tag_bind(self.image, "<ButtonRelease-1>", self.move_stop)
        self.canvas.tag_bind(self.image, "<B1-Motion>", self.move)

    def move_start(self, event):
        """
        event: Parameter from Tkinter's API
            Contains mouse positions
        Begin moving and store mouse positions
        """
        self.object_is_moving = True

        self.current_x_position = event.x
        self.current_y_position = event.y
        self.original_x_position = event.x
        self.original_y_position = event.y

    def move_stop(self, event):
        """
        Return the object to original position
        Calls a callback if within rectangular bounds
        """
        self.object_is_moving = False

        # print(f"self.current_x_position: {self.current_x_position:}, self.x_lower: {self.x_lower}, self.x_upper: {self.x_upper}")
        # print(f"self.current_y_position: {self.current_y_position:}, self.y_lower: {self.y_lower}, self.y_upper: {self.y_upper}")

        # The position is within the bounds, x_lower < (current x) < x_upper and y_lower < (current y) < y_upper
        if self.current_x_position > self.x_lower and \
            self.current_x_position < self.x_upper and \
            self.current_y_position > self.y_lower and \
            self.current_y_position < self.y_upper:
            self.callback()
        self.x_diff = self.original_x_position - self.current_x_position
        self.y_diff = self.original_y_position - self.current_y_position
        self.canvas.move(self.image, self.x_diff, self.y_diff)

        self.current_x_position = 0
        self.current_y_position = 0

    def move(self, event):
        """
        Move object to current mouse position
        """
        if self.object_is_moving:
            dx = event.x - self.current_x_position
            dy = event.y - self.current_y_position

            self.canvas.move(self.image, dx, dy)

            self.current_x_position = event.x
            self.current_y_position = event.y

class Fablab_Phone:
    '''
    The phone to call the fablab staff
    Resolves all crisis in the game controller file
    '''

    def __init__(self, canvas: tk.Canvas, image: tk.Image | ImageTk.PhotoImage, x: int, y: int):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image: int = self.canvas.create_image(x, y, image=image)
        self.on_click = lambda: None
        self.canvas.tag_bind(self.image, "<ButtonPress-1>",
            lambda event: (self.on_click()))


class PowerupDisplay:
    '''
    Logic for powerups that show in the left corner
    '''
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
            font=("Comic Sans MS", 12),
            background="grey",
            foreground="white",
            justify='left'
        )

        self.hide()
    def show(self):
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
        """
        Initializes window, assets, and all frames
        """
        # Setup
        self.root = tk.Tk()
        self.root.minsize(width=900, height=600)
        self.root.title("Jo's 3D Printing Adventure")
        self.root.iconbitmap("bamboo.ico")
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
        self.GFX_fablab_phone = tk.PhotoImage(file=os.path.join(assets, 'FabLab Hotline.png'))
        self.GFX_printer_screen_error = tk.PhotoImage(file=os.path.join(assets, 'Printer Screen (Error).png'))
        
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
        image = ImageTk.Image.open(os.path.join(assets, 'Fablab Staff.png')).resize(POWERUP_SIZE)
        self.GFX_fablab_staff = ImageTk.PhotoImage(image)

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
        self.update_score_frame()
    
    def create_menu_frame(self):
        """
        Main Menu initialiser
        Split out from __init__ for code organisation purposes
        """
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
        self.play_button.place(x=450,y=300, anchor='center')
        self.scoreboard_button = ttk.Button(
            master,
            text="Scoreboard",
            command=lambda: self.change_frame(self.score_frame),
            width=32,
            style='my.TButton'
            )
        self.scoreboard_button.place(x=450,y=350, anchor='center')
        self.exit_button = ttk.Button(
            master,
            text="Exit",
            command=self.root.destroy,
            width=32,
            style='my.TButton'
            )
        self.exit_button.place(x=450,y=400, anchor='center')
        
        s.configure('my.TButton', font=('Comic Sans MS', 18))
    
    def create_score_frame(self):
        """
        Scorescreen initialiser
        Split out from __init__ for code organisation purposes
        """
        self.scoreobject = Leaderboard(self.root)
        self.score_frame = self.scoreobject.root
        self.scoreobject.gomenu = lambda: self.change_frame(self.menu_frame)

    def update_score_frame(self):
        self.scoreobject.clear_widgets()
        self.scoreobject.startup()
        self.scoreobject.display_data()
        self.scoreobject.exit_button()


    def create_name_frame(self):
        """
        Enter name screen initialiser
        Split out from __init__ for code organisation purposes
        """
        self.loginobject = Login(self.root)
        self.name_frame = self.loginobject.root
        self.loginobject.play_callback = self.on_play
        self.loginobject.gomenu = lambda: self.change_frame(self.menu_frame)

    def create_game_frame(self):
        """
        Create game elements
        Split out from __init__ for code organisation purposes
        Most elements depend on canvas to enable transparency support
        """
        master = self.game_frame
        self.background = tk.Canvas(master, width=900, height=600)
        self.background.create_image(450, 300, image=self.GFX_background)
        self.background.create_image(450, 300, image=self.GFX_printer )
        self.filament_static = self.background.create_image(350, 18, image=self.GFX_filament_static)
        self.printer_bed_static = self.background.create_image(447, 486, image=self.GFX_printer_bed)

        # Error alert is hidden at game start
        self.error_alert = self.background.create_image(344, 189, image=self.GFX_printer_screen_error)
        self.background.itemconfigure(self.error_alert, state='hidden')

        self.background.pack()

        self.printer_head = Print_Head(self.background, self.GFX_printer_head, 340, 430)
        self.clicker = Clicker_Button(self.background, self.GFX_main_clicker, 450, 325)
        self.filament = Moving_Object(self.background, self.GFX_filament, 800, 500, 295, 408, 2, 115, 1)
        self.printer_bed = Moving_Object(self.background, self.GFX_printer_bed, 800, 600, 321, 566, 458, 514, 2)
        self.fablab_phone = Fablab_Phone(self.background, self.GFX_fablab_phone, 841, 250)

        # Username display
        self.test_username = tk.StringVar()
        display = tk.Label(
            master,
            textvariable=self.test_username,
            font=("Comic Sans MS", 20),
            background="grey",
            foreground="white"
        )
        display.place(anchor = "nw")

        # Time display
        self.time_remaining = tk.StringVar()
        display = tk.Label(
            master,
            textvariable=self.time_remaining,
            font=("Comic Sans MS", 20),
            background="grey",
            foreground="white"
        )
        display.place(x = 0, y = 40)
        # Time till fablab staff intervenes
        self.time_intervention = tk.StringVar()
        display = tk.Label(
            master,
            textvariable=self.time_intervention,
            font=("Comic Sans MS", 20),
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
            font=("Comic Sans MS", 20),
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
            font=("Comic Sans MS", 14),
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
            font=("Comic Sans MS", 12),
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
    
    def register_callbacks(self, play, name, clicker, resolve_filament, resolve_bed, call_fablab):
        """
        Setter function for game.py to pass all callbacks without navigating
        children of this class
        """
        self.play_callback = play
        self.loginobject.get_name = name
        self.clicker.on_click(clicker)
        self.filament.callback = resolve_filament
        self.printer_bed.callback = resolve_bed
        self.fablab_phone.on_click = call_fablab

    def update_print_display(self, prints_per_click, prints_per_sec):
        self.ppc_display.set(f"Prints per click: {prints_per_click}")
        self.pps_display.set(f"Auto Prints/sec: {prints_per_sec}")
    
    def update_time_display(self, time, time_crisis_start):
        """
        Update text for countdown timers
        """
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
                powerup_string = "You got a free\nAnyQuadratic printer!"
                image = self.GFX_anyquadratic
            case Powerup.Bamboo:
                powerup_string = "You got a free\nB4MBOO printer!"
                image = self.GFX_bamboo
            case Powerup.DouyinIonThrusters:
                powerup_string = "Douyin Ion Thrusters are\npowering your printer"
                image = self.GFX_douyin
            case Powerup.November:
                powerup_string = "Jovan is coming to help you"
                image = self.GFX_november

        self.powerup_display.show()
        self.powerup_string.set(powerup_string)
        self.powerup_display.change_image(image=image)
        
    def create_crisis(self, crisis_index):
        """
        Code to display and notify user that a crisis has occurred
        """
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
            self.background.itemconfigure(self.error_alert, state='normal')
    
    # Used to re-show elements that have been hidden by crisises
    def show_filament(self):
        self.background.itemconfigure(self.filament_static, state='normal')

    def show_plate(self):
        self.background.itemconfigure(self.printer_bed_static, state='normal')

    def hide_error(self):
        self.background.itemconfigure(self.error_alert, state='hidden')

    def user_resolved(self):
        self.printer_head.enabled = True

    def popup_fablab(self):
        """
        Code to display fablab intervention
        """
        messagebox.askquestion(
            "Crisis Resolved",
            "Fablab staff have come to fix your problems",
            type=messagebox.OK,
            icon=messagebox.WARNING
        )
        self.printer_head.enabled = True
        self.powerup_display.show()
        self.powerup_string.set("Fablab staff")
        self.powerup_display.update_text("")
        self.powerup_display.change_image(image=self.GFX_fablab_staff)
        self.root.after(5000, self.powerup_display.hide)

    def change_frame(self, new_frame: ttk.Frame | tk.Frame):
        """
        Change all elements in window
        """
        if new_frame is self.game_frame:
            self.loginobject.button.configure(state=tk.DISABLED)
        else:
            self.loginobject.button.configure(state=tk.NORMAL)
        
        if new_frame is self.score_frame:
            self.update_score_frame()
        
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