from enum import IntEnum

# How to use:
# Powerups.Anycubic for 0
class Powerups(IntEnum):
    Anycubic = 0
    Bambu = 1
    November = 31
    

class GameController:
    def __init__(self) -> None:
        # To store:
        # Click count
        self.coins = 0
        # array of powerup counts
        # temporarily set to 32 entries until we decide how many we want
        # or if we want to use dictionary for this instead
        # but probably better as array for ease of entry into database
        self.powerups = [0] * 32
    def earn(self):
        self.coins += 1
    def get_powerup(self, powerup: Powerups):
        self.powerups[powerup] += 1
    def use_powerup(self, powerup: Powerups):
        # validation here? or maybe ui
        self.powerups[powerup] -= 1
    def get_data(self):
        return self.coins, self.powerups
    def generate_crisis(self):
    #TODO
        pass

