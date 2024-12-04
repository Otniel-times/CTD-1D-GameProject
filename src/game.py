from enum import IntEnum
from gui import *
import dbHandler
import random

# Powerups.Anyquadratic for 0
# list(Powerups) will give you a list of all Powerups
# access name string by .name
# int value used by default
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

        ## 1. Spaghetti print
        ## 2. Broken Head
        ## 3. Someone stopped print
        self.crises = {1:"Spaghetti",
                       2:"Broken Head",
                       3:"Stopped Print"}
        self.crisis = None

        self.CRISIS_COUNT = len(self.crises)
        # array of powerup counts
        self.powerups = [0] * self.POWERUP_COUNT
        self.powerup_timer = -1

        # TODO: Finalize values
        # parameters for function
        # perclick bonus, persec bonus, time(ms) until disabled
        self.POWERUP_ACTIONS = [
            (1, 1, 5000), #Anyquadratic
            (4, 2, 5000), #Bamboo
            (4, 500, 2000), #Douyin Ion Thrusters
            (499, 5, 5000), #November
        ]

        # TODO:implement userid
        self.uid = 0

        # Setup values
        self.prints_per_click = 1
        self.prints_per_sec = 0
        self.per_sec_malus_scale = 1
        
        self.gui = Main_GUI()
        self.gui.clicker.on_click(self.earn)
        def play():
            self.gui.root.after(1000, self.per_sec)
        self.gui.play_callback = play

        # time limit - value in seconds
        self.time = 200
        self.time_remaining_minutes = self.time // 60
        self.time_remaining_seconds = self.time % 60
        self.gui.time_remaining.set(f"{self.time_remaining_minutes :02d}:{self.time_remaining_seconds :02d}")

        # temporary user name for the purposes of the thing
        self.test_username = 'GaS'
        if self.test_username[-1].lower() == 's':
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
        if self.powerup_timer >= 0:
            self.powerup_timer -= 1
            self.gui.powerup_display.update_text(self.powerup_timer)
        # using <= in case of overrun - even if its not really possible
        if self.time <= 0:
            self.save()
            self.gui.change_frame(self.gui.name_frame)
            # break the "loop"
            return
        # TODO: Remove this, only for testing getting powerups
        if self.time % 20 == 0:
            self.resolve_crisis()
        self.time -= 1
        self.time_remaining_minutes = self.time // 60
        self.time_remaining_seconds = self.time % 60
        self.gui.time_remaining.set(f"{self.time_remaining_minutes :02d}:{self.time_remaining_seconds :02d}")
        
        print(f"{self.time}, {self.time_remaining_minutes :02d}:{self.time_remaining_seconds :02d}")
        self.gui.score.set(self.score)
        self.gui.root.after(1000, self.per_sec)

    def earn(self):
        self.score += self.prints_per_click
        self.gui.score.set(self.score)
        self.gui.printer_head.animation_check()

    def powerup_action(self, moreclick, moresec, time):
        self.prints_per_click += moreclick
        self.prints_per_sec += moresec
        self.powerup_timer = time // 1000
        self.gui.powerup_display.update_text(self.powerup_timer)
        self.gui.ppc_display.set(f"Prints per click: {self.prints_per_click}")
        self.gui.pps_display.set(f"Auto Prints/sec: {self.prints_per_sec}")
        def reverse():
            self.prints_per_click -= moreclick
            self.prints_per_sec -= moresec
            self.gui.ppc_display.set(f"Prints per click: {self.prints_per_click}")
            self.gui.pps_display.set(f"Auto Prints/sec: {self.prints_per_sec}")
            self.gui.powerup_display.hide()
        self.gui.root.after(time, reverse)

    def get_powerup(self, powerup: Powerups):
        self.powerups[powerup] += 1
        self.gui.powerup_display.appear()

    def use_powerup(self, powerup: Powerups):
        # prevent activating multiple powerups at the same time
        if self.powerup_timer != -1 or self.powerups[powerup] == 0:
            return
        self.powerups[powerup] -= 1
        # TODO: Select image for active powerup
        # OR Decide to show powerups at the same time
        if powerup == Powerups.DouyinIonThrusters:
            self.gui.powerup_display.change_image(image=self.gui.GFX_douyin)
        else:
            self.gui.powerup_display.change_image(image=self.gui.GFX_november)
        # unpack tuple into arguments
        self.powerup_action(*self.POWERUP_ACTIONS[powerup])

    def save(self):
        dbHandler.update_score_by_id(self.uid, self.score)
        
    def generate_crisis(self):
        pass
        #self.gui.create_crisis(crisis_name, crisis_text)
    def resolve_crisis(self):
        self.crisis = None
        should_reward = random.choice((False, True))
        if should_reward:
            reward = random.choice(list(Powerups))
            self.get_powerup(reward)
            print(f"You got the {reward.name}")
            self.use_powerup(reward)

GameController()