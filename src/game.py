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
        # To store:
        # Click count
        self.score = 0
        # array of powerup counts
        # temporarily set to 32 entries until we decide how many we want
        # or if we want to use dictionary for this instead
        # but probably better as array for ease of entry into database
        self.powerups = [0] * 32
        # TODO:implement userid
        self.uid = 0
        
        self.gui = Main_GUI()
        self.gui.clicker.configure(command=self.earn)
        # TODO: link to counter display once created
        self.gui.mainloop()
    def earn(self):
        self.score += 1
        self.gui.score.set(self.score)
    def get_powerup(self, powerup: Powerups):
        self.powerups[powerup] += 1
    def use_powerup(self, powerup: Powerups):
        # validation here? or maybe ui
        self.powerups[powerup] -= 1
    def save(self):
        dbHandler.update_score_by_id(self.uid, self.score)
    def generate_crisis(self):
    #TODO
        pass

GameController()