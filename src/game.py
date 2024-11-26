from enum import IntEnum
from gui import *
import dbHandler

# How to use:
# Powerups.Anycubic for 0
class Powerups(IntEnum):
    Anycubic = 0
    Bambu = 1
    DouyinIonThrusters = 30
    November = 31
    

class GameController:
    def __init__(self) -> None:
        POWERUP_COUNT = 32
        ITEM_COUNT = 5

        # To store:
        # Click count
        self.score = 0

        # array of powerup counts
        self.powerups = [0] * POWERUP_COUNT

        # TODO: Write powerup actions
        # return new per click and per sec
        self.powerup_actions = [lambda x,y: (0,0)] * POWERUP_COUNT

        self.items = [0] * ITEM_COUNT

        # TODO:implement userid
        self.uid = 0

        # Setup values
        self.prints_per_click = 2
        # set at 1 for testing
        self.prints_per_sec = 1
        # self.gui.ppc_display.set("Prints per click: {}".format(self.prints_per_click))
        
        self.gui = Main_GUI()
        self.gui.clicker.configure(command=self.earn)
        self.gui.root.after(1000, self.per_sec)

        # GUI setup
        self.gui.pps_display.set("Auto Prints/sec: {}".format(self.prints_per_sec))
        self.gui.ppc_display.set("Prints per click: {}".format(self.prints_per_click))

        self.gui.mainloop()
    
    def per_sec(self):
        self.score += self.prints_per_sec
        self.gui.score.set(self.score)
        self.gui.pps_display.set("Auto Prints/sec: {}".format(self.prints_per_sec))
        self.gui.root.after(1000, self.per_sec)

    def earn(self):
        self.score += self.prints_per_click
        self.gui.ppc_display.set("Prints per click: {}".format(self.prints_per_click))
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
    #TODO
        pass

GameController()