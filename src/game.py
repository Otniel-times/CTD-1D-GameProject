from gui import *
import dbHandler
import random
from common import *

class GameController:
    def __init__(self) -> None:
        self.rng = random.Random()
        self.rng.seed(random.randint(0, 2**16))

        self.score = 0

        ## crises dict contains number:tuple(<crisis_name>, <crisis text>)
        ## Please insert crisis text
        self.crises = {1:("No filament",""),
                       2:("No printer bed",""),
                       3:("Error code FILLTHISIN","")}
        self.crisis = None

        self.CRISIS_COUNT = len(self.crises)
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
            self.score += self.prints_per_sec
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
            self.resolve_crisis(True)
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

    def use_powerup(self, powerup: Powerup):
        # prevent activating multiple powerups at the same time
        if self.powerup_timer != -1:
            return
        # TODO: Select image for active powerup
        if powerup == Powerup.DouyinIonThrusters:
            self.gui.powerup_display.change_image(image=self.gui.GFX_douyin)
        else:
            self.gui.powerup_display.change_image(image=self.gui.GFX_november)
        # unpack tuple into arguments
        self.powerup_action(*self.POWERUP_ACTIONS[powerup])
        time = self.POWERUP_ACTIONS[powerup][2]
        self.gui.show_powerup_popup(powerup, time)

    def save(self) -> None:
        dbHandler.update_score_by_id(self.uid, self.score)

    def generate_crisis(self) -> None:
        """
        This function generates crisis and starts timer, calls self.call_staff() after timer runs out, once timer starts, self.prints_per_click and self.prints_per_sec are set to 0.
        Original print rates are stored locally.
        """
        self.crisis_index = self.rng.randint(0, self.CRISIS_COUNT)
        self.gui.create_crisis(self.crisis_index)

        ##Crisis starts
        resolved = False
        print_rate_click = self.prints_per_click
        print_rate_base = self.prints_per_sec
        self.prints_per_click = 0
        self.prints_per_sec = 0

        self.crisis_timer = 60

        ## Insert 60s timer
        ## Basic logic, will need help implementing this with timer
        if resolved:
            self.prints_per_click = print_rate_click
            self.prints_per_sec = print_rate_base
            self.resolve_crisis(True)

        else:
            self.call_staff()
            self.prints_per_click = print_rate_click
            self.prints_per_sec = print_rate_base

    def call_staff(self):
        ## GUI TO CALL STAFF
        self.resolve_crisis(False)
        
    def resolve_crisis(self, userResolved: bool):
        """
        Sets crisis state to None, and determines whether 

        userResolved: True if crisis was resolved by the player, False if crisis was resolved by staff
        """
        self.crisis = None
        #should_reward = random.choice((False, True))
        should_reward = True
        if userResolved and should_reward:
            reward = random.choice(list(Powerup))
            print(f"You got the {reward.name}")
            self.use_powerup(reward)

GameController()