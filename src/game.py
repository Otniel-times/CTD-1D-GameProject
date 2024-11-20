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
        # Powerups
        self.coins = 0
        # store as bitflags
        self.powerups = 0
    def earn(self):
        self.coins += 1
    def get_powerup(self, powerup: Powerups):
        self.powerups |= 1 << powerup.value
    def use_powerup(self, powerup: Powerups):
        self.powerups &= ~(1 << powerup.value)
    def get_data(self):
        return self.coins, self.powerups
    def generate_crisis(self):
    #TODO
        pass

