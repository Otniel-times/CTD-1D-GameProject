from enum import IntEnum
from gui import *
import dbHandler
import random

# How to use:
# Upgrades.Anycubic for 0
class Powerups(IntEnum):
    Anyquadratic = 0
    Bamboo = 1
    DouyinIonThrusters = 2
    November = 3
    

class GameController:
    def __init__(self) -> None:
        self.POWERUP_COUNT = 4
        
        self.rng = random.Random()
        self.rng.seed(random.randint(0, 2**16))

        # To store:
        # Click count
        self.score = 0

        ## crises dict contains number:tuple(<crisis_name>, <crisis text>)
        ## Please insert crisis text
        self.crises = {1:("No filament",""),
                       2:("No printer bed",""),
                       3:("Error code FILLTHISIN","")}
        self.crisis = None

        self.CRISIS_COUNT = len(self.crises)
        # array of upgrade counts
        self.POWERUPS = [0] * self.POWERUP_COUNT

        # TODO: Finalize values
        # parameters for function
        # perclick bonus, persec bonus, time(ms) until disabled
        self.POWERUP_ACTIONS = [
            (0, 1, 2000), #Anyquadratic
            (1, 4, 5000), #Bamboo
            (1, 100, 500), #Douyin Ion Thrusters
            (500, 4, 5000), #November
        ]

        # TODO:implement userid
        self.uid = 0

        # Setup values
        self.prints_per_click = 1
        self.prints_per_sec = 0
        self.per_sec_malus_scale = 1
        # time limit
        self.time = 200 * 1000
        
        self.gui = Main_GUI()
        self.gui.clicker.on_click(self.earn)
        self.gui.root.after(1000, self.per_sec)

        # temporary user name for the purposes of the thing
        self.test_username = 'Gas'
        if self.test_username[-1] == 's' or self.test_username[-1] == 'S':
            self.gui.test_username.set(f"{self.test_username}' 3D Printer")
        else:
            self.gui.test_username.set(f"{self.test_username}'s 3D Printer")

        # GUI setup
        self.gui.pps_display.set(f"Auto Prints/sec: {self.prints_per_sec}")
        self.gui.ppc_display.set(f"Prints per click: {self.prints_per_click}")

        # TODO: Schedule crises here
        #self.gui.root.after(100, self.gui.create_crisis, "Hello", "World")
        self.gui.mainloop()
    
    def per_sec(self):
        if self.crisis is not None:
            # TODO: lookup for crisis scale factors
            # use match?
            self.score += self.prints_per_sec // self.per_sec_malus_scale
        else:
            self.score += self.prints_per_sec
        # using <= in case of overrun - even if its not really possible
        if self.time <= 0:
            # TODO: score screen and log in
            self.save()
        self.time -= 1
        self.gui.score.set(self.score)
        self.gui.pps_display.set(f"Auto Prints/sec: {self.prints_per_sec}")
        self.gui.root.after(1000, self.per_sec)

    def earn(self):
        self.score += self.prints_per_click
        self.gui.ppc_display.set(f"Prints per click: {self.prints_per_click}")
        self.gui.score.set(self.score)
        self.gui.printer_head.animation_check()

    def powerup_action(self, moreclick, moresec, time):
        self.prints_per_click += moreclick
        self.prints_per_sec += moresec
        def reverse():
            self.prints_per_click -= moreclick
            self.prints_per_sec -= moresec
        self.gui.root.after(time, reverse)

    def get_powerup(self, powerup: Powerups):
        self.POWERUPS[powerup] += 1

    def use_powerup(self, powerup: Powerups):
        # validation here? or maybe ui
        self.POWERUPS[powerup] -= 1
        # unpack tuple into arguments
        self.powerup_action(*self.POWERUP_ACTIONS[powerup])

    def save(self) -> None:
        dbHandler.update_score_by_id(self.uid, self.score)
        
    def generate_crisis(self) -> None:
        """
        This function generates crisis and starts timer, calls self.call_staff() after timer runs out, once timer starts, self.prints_per_click and self.prints_per_sec are set to 0.
        Original print rates are stored locally.


        """
        crisis_index = self.rng.randint(0, self.CRISIS_COUNT)
        self.crisis = self.crises[crisis_index]
        self.gui.create_crisis(self.crisis[0], self.crisis[1])

        ##Crisis starts
        resolved = False
        print_rate_click = self.prints_per_click
        print_rate_base = self.prints_per_sec
        self.prints_per_click = 0
        self.prints_per_sec = 0

        ## Insert 60s timer
        ## Basic logic, will need help implementing this with timer
        if resolved:
            self.prints_per_click = print_rate_click
            self.prints_per_sec = print_rate_base

        else:
            self.call_staff()
            self.prints_per_click = print_rate_click
            self.prints_per_sec = print_rate_base

    def call_staff(self):
        ## GUI TO CALL STAFF
        self.resolve_crisis()
        
    def resolve_crisis(self):
        self.crisis = None


GameController()