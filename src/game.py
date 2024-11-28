from enum import IntEnum
from gui import *
import dbHandler
import random

# How to use:
# Powerups.Anycubic for 0
class Powerups(IntEnum):
    Anycubic = 0
    Bambu = 1
    DouyinIonThrusters = 30
    November = 31
    

class GameController:
    def __init__(self) -> None:
        self.POWERUP_COUNT = 32
        self.ITEM_COUNT = 5
        
        self.rng = random.Random()
        self.rng.seed(random.randint(0, 2**16))

        # To store:
        # Click count
        self.score = 0

        ## 1. Spaghetti print
        ## 2. Broken Head
        ## 3. Someone stopped print
        self.crises = {1:"Spaghetti",
                       2:"Broken Head",
                       3:"Stopped Print"}

        self.CRISIS_COUNT = len(self.crises)
        # array of powerup counts
        self.powerups = [0] * self.POWERUP_COUNT

        # TODO: Write powerup actions
        # return new per click and per sec
        self.powerup_actions = [lambda x,y: (0,0)] * self.POWERUP_COUNT

        self.items = [0] * self.ITEM_COUNT

        # TODO:implement userid
        self.uid = 0

        # Setup values
        self.prints_per_click = 1
        self.prints_per_sec = 0
        self.per_sec_malus_scale = 1
        
        self.gui = Main_GUI()
        self.gui.clicker.configure(command=self.earn)
        self.gui.root.after(1000, self.per_sec)

        # GUI setup
        self.gui.pps_display.set(f"Auto Prints/sec: {self.prints_per_sec}")
        self.gui.ppc_display.set(f"Prints per click: {self.prints_per_click}")

        self.gui.mainloop()
    
    def per_sec(self):
        if self.crisis is not None:
            # TODO: lookup for crisis scale factors
            # use match?
            self.score += self.prints_per_sec // self.per_sec_malus_scale
        else:
            self.score += self.prints_per_sec
        self.gui.score.set(self.score)
        self.gui.pps_display.set(f"Auto Prints/sec: {self.prints_per_sec}")
        self.gui.root.after(1000, self.per_sec)

    def earn(self):
        self.score += self.prints_per_click
        self.gui.ppc_display.set(f"Prints per click: {self.prints_per_click}")
        self.gui.score.set(self.score)

    def get_powerup(self, powerup: Powerups):
        self.powerups[powerup] += 1

    def use_powerup(self, powerup: Powerups):
        # validation here? or maybe ui
        self.powerups[powerup] -= 1
        self.prints_per_click, self.prints_per_sec = \
            self.powerup_actions[powerup](self.prints_per_click, self.prints_per_sec)


    def save(self):
        dbHandler.update_score_by_id(self.uid, self.score)
        
    def generate_crisis(self):
        crisis_index = self.rng.randint(0, self.CRISIS_COUNT)
        self.crisis = self.crises[crisis_index]
    def resolve_crisis(self):
        self.crisis = None


GameController()