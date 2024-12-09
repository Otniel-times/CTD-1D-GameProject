from gui import *
import dbHandler
import random

class GameController:
    def __init__(self) -> None:
        self.rng = random.Random()
        self.rng.seed(random.randint(0, 2**16))

        self.score = 0

        ## crises dict contains {<number>:<crisis name>}
        self.crises = {1:"No filament",
                       2:"No printer bed",
                       3:"Error code FILLTHISIN"}
        self.crisis = None

        self.CRISIS_COUNT = len(self.crises)
        self.powerup_timer = -1

        # TODO: Finalize values
        # parameters for function
        # perclick bonus, persec bonus, time(ms) until disabled
        self.POWERUP_ACTIONS = [
            (1, 1, 10000), #Anyquadratic
            (4, 2, 10000), #Bamboo
            (4, 25, 3000), #Douyin Ion Thrusters
            (20, 5, 15000), #November
        ]

        self.username = ""
        self.uid = 0

        # Setup values
        self.prints_per_click = 1
        self.prints_per_sec = 0
        self.clicks_since_last_crisis = 0
        
        self.gui = Main_GUI()
        # Function to initialize game logic after button pressed
        def play():
            self.gui.root.after(1000, self.per_sec)
            #Schedule crises here
            #self.gui.root.after(2000, self.generate_crisis)
            #self.gui.root.after(6000, self.generate_crisis)
            #self.gui.root.after(6000, self.generate_crisis)
        def name_callback():
            self.username = self.gui.loginobject.name.get()
            if self.username[-1].lower() == 's':
                self.gui.test_username.set(f"{self.username}' 3D Printer")
            else:
                self.gui.test_username.set(f"{self.username}'s 3D Printer")
        
        self.gui.register_callbacks(
            play,
            name_callback,
            self.earn,
            self.resolve_no_filament,
            self.resolve_no_plate,
            self.resolve_print_error
        )

        # time limit - value in seconds
        self.time = 200
        self.time_crisis_start = 0
        self.gui.update_time_display(self.time, self.time_crisis_start)

        # GUI setup
        self.gui.update_print_display(self.prints_per_click, self.prints_per_sec)

        self.gui.mainloop()

    """
    Periodically called function to update score over time
    Also used for displaying countdown
    """
    def per_sec(self):
        self.score += self.prints_per_sec
        if self.powerup_timer >= 0:
            self.powerup_timer -= 1
            self.gui.powerup_display.update_text(self.powerup_timer)
        # using <= in case of overrun - even if its not really possible
        if self.time <= 0:
            self.save()
            self.gui.change_frame(self.gui.score_frame)
            # break the "loop"
            return
        
        # reset click count every 15s
        if self.time % 15 == 0:
            self.clicks_since_last_crisis = 0
        #if self.time % 10 == 0:
        #    self.resolve_crisis(True)
        if self.time_crisis_start - self.time >= FABLAB_TIMEOUT and \
            self.crisis is not None:
            self.crisis = None
            self.call_staff()
        
        self.time -= 1
        self.gui.update_time_display(self.time, self.time_crisis_start)
        
        
        self.gui.score.set(self.score)
        self.gui.root.after(1000, self.per_sec)

    """
    Function for clicker button press
    """
    def earn(self):
        self.score += self.prints_per_click
        self.gui.score.set(self.score)
        self.gui.printer_head.animation_check()
        # printing too much causes crises
        self.clicks_since_last_crisis += 1
        # 5 clicks per second
        if self.clicks_since_last_crisis > 5 * 15:
            self.generate_crisis()

    def powerup_action(self, moreclick, moresec, time):
        self.prints_per_click += moreclick
        self.prints_per_sec += moresec
        self.powerup_timer = time // 1000
        self.gui.powerup_display.update_text(self.powerup_timer)
        self.gui.update_print_display(self.prints_per_click, self.prints_per_sec)

        def reverse():
            self.prints_per_click -= moreclick
            self.prints_per_sec -= moresec
            self.gui.update_print_display(self.prints_per_click, self.prints_per_sec)
            self.gui.powerup_display.hide()
        self.gui.root.after(time, reverse)

    def use_powerup(self, powerup: Powerup):
        # prevent activating multiple powerups at the same time
        if self.powerup_timer != -1:
            return
        # unpack tuple into arguments
        self.powerup_action(*self.POWERUP_ACTIONS[powerup])
        time = self.POWERUP_ACTIONS[powerup][2]
        self.gui.show_powerup_popup(powerup, time)

    def save(self) -> None:
        dbHandler.new_entry(self.username, self.uid, self.score)

    def generate_crisis(self):
        """
        This function generates crisis and starts timer, calls self.call_staff()
        after timer runs out, once timer starts, self.prints_per_click and self.prints_per_sec are set to 0.
        """
        # Do not generate multiple crises at the same time
        if self.crisis != None:
            return
        #crisis_index, crisis_name = self.rng.choice(list(self.crises.items()))
        crisis_index, crisis_name = list(self.crises.items())[0]
        self.gui.create_crisis(crisis_index)
        self.crisis = crisis_name

        ##Crisis starts
        self.original_click = self.prints_per_click
        self.original_sec = self.prints_per_sec
        self.prints_per_click = 0
        self.prints_per_sec = 0
        self.gui.update_print_display(self.prints_per_click, self.prints_per_sec)
        self.time_crisis_start = self.time

    def resolve_no_filament(self):
        """
        Checks if "no filament" crisis and resolves if it is
        """
        if self.crisis == "No filament":
            self.gui.show_filament()
            self.resolve_crisis(True)

        else:
            print("Wrong resolution")

    def resolve_no_plate(self):
        """
        Checks if "no plate" crisis and resolves if it is
        """
        if self.crisis == "No printer bed":
            self.resolve_crisis(True)

        else:
            print("Wrong resolution")

    def resolve_print_error(self):
        """
        Checks if "print error" crisis and resolves if it is
        """
        if self.crisis == 'Error code FILLTHISIN':
            self.resolve_crisis(True)

        else:
            print("Wrong resolution")

    def call_staff(self):
        ## GUI TO CALL STAFF
        self.resolve_crisis(False)
        self.gui.popup_fablab()
        
    def resolve_crisis(self, userResolved: bool):
        """
        Sets crisis state to None, and determines whether 

        userResolved: True if crisis was resolved by the player, False if crisis was resolved by staff
        """
        self.crisis = None
        self.time_crisis_start = 0
        self.prints_per_click = self.original_click
        self.prints_per_sec = self.original_sec
        self.gui.update_print_display(self.prints_per_click, self.prints_per_sec)
        # 66% chance of reward
        #should_reward = random.choice((False, True, True))
        should_reward = True
        if userResolved and should_reward:
            reward = random.choice(list(Powerup))
            print(f"You got the {reward.name}")
            self.use_powerup(reward)
        if userResolved:
            self.gui.user_resolved()

GameController()