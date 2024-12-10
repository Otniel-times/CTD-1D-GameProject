from gui import *
import dbHandler
import random

class GameController:
    """
    Maintains game state and passes information to GUI for display
    """
    def __init__(self) -> None:
        ## Initialise local db for leaderboard
        try: # to check if DB file exists
            db = open("index.db")
            db.close()

        except FileNotFoundError:
            dbHandler.on_init() # creates file if it does not exist

        # create random number to be used in crisis events and powerup generation
        self.rng = random.Random()

        ## crises dict contains {<number>:<crisis name>}
        self.crises = {1:"No filament",
                       2:"No printer bed",
                       3:"Error code HMS_0500-0100-0003-0005"}

        # powerup_actions declares parameters to be attributed to each powerup
        # in order: perclick bonus, persec bonus, time(ms) until disabled
        self.POWERUP_ACTIONS = [
            (2, 1, 10000), #Anyquadratic
            (5, 2, 10000), #Bamboo
            (5, 25, 3000), #Douyin Ion Thrusters
            (20, 5, 15000), #November
        ]

        # Initialised setup values to prevent undefined
        self.username = ""
        self.score = 0
        self.crisis = None
        self.powerup_timer = -1
        self.prints_per_click = 1
        self.prints_per_sec = 0
        self.clicks_since_last_crisis = 0
        # time limit - value in seconds
        self.time = 200
        self.time_crisis_start = 0

        
        self.gui = Main_GUI()

        # function to allow for playing of game
        def play():
            """
            Setup values for initialization of game
            """
            self.score = 0
            self.crisis = None
            self.powerup_timer = -1
            self.prints_per_click = 1
            self.prints_per_sec = 0
            self.clicks_since_last_crisis = 0
            self.time = 200
            self.time_crisis_start = 0

            # Assigns value to gui.py objects
            self.gui.update_print_display(self.prints_per_click, self.prints_per_sec)
            self.gui.update_time_display(self.time, self.time_crisis_start)
            
            # Begin gameloop
            self.gui.root.after(1000, self.gameloop)
            # Schedule crises here
            self.gui.root.after(6000, self.generate_crisis)

        # callback function to display name on top left of game
        def name_callback():
            self.username = self.gui.loginobject.name.get()
            # if else statement assign correct apostrophe to displayed name text
            if self.username[-1].lower() == 's':
                self.gui.test_username.set(f"{self.username}' 3D Printer")
            else:
                self.gui.test_username.set(f"{self.username}'s 3D Printer")
        
        # callback functions to be assigned to gui.py objects
        self.gui.register_callbacks(
            play,
            name_callback,
            self.earn,
            self.resolve_no_filament,
            self.resolve_no_plate,
            self.call_staff
        )


        self.gui.mainloop()

    # main game function
    def gameloop(self):
        """
        Periodically called function to update score over time
        Also used for displaying countdowns and general loop based logic
        Yes this means tickrate of the game is technically 1 Hz
        """
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
        # time_crisis start should always be greater than self.time
        # earlier times are greater since self.time is a countdown
        # automatically call staff once timeout is reached
        if self.time_crisis_start - self.time >= FABLAB_TIMEOUT and \
            self.crisis is not None:
            self.call_staff()
        
        self.time -= 1
        self.gui.update_time_display(self.time, self.time_crisis_start)
        
        
        self.gui.score.set(self.score)
        self.gui.root.after(1000, self.gameloop)

    def earn(self):
        """
        Function for clicker button press
        """
        self.score += self.prints_per_click
        self.gui.score.set(self.score)
        self.gui.printer_head.animation_check()
        # printing too much causes crises
        self.clicks_since_last_crisis += 1
        # 3 clicks per second
        if self.clicks_since_last_crisis > 3 * 15:
            self.generate_crisis()
            self.clicks_since_last_crisis = 0

    def powerup_action(self, moreclick, moresec, time):
        """
        Overrides current print per click and print per sec values
        Schedules a function to restore values to default
        """
        self.prints_per_click = moreclick
        self.prints_per_sec = moresec
        self.powerup_timer = time // 1000
        self.gui.powerup_display.update_text(self.powerup_timer)
        self.gui.update_print_display(self.prints_per_click, self.prints_per_sec)

        def reverse():
            """
            Restore stats to default
            """
            if self.crisis is not None:
                self.prints_per_click = 0
            else:
                self.prints_per_click = 1
            self.prints_per_sec = 0
            self.gui.update_print_display(self.prints_per_click, self.prints_per_sec)
            self.gui.powerup_display.hide()
            self.powerup_timer = -1
        #Schedule stat restoration
        self.gui.root.after(time, reverse)

    def use_powerup(self, powerup: Powerup):
        """
        Powerup action 
        """
        # prevent activating multiple powerups at the same time
        if self.powerup_timer != -1:
            return
        # unpack tuple into arguments
        self.powerup_action(*self.POWERUP_ACTIONS[powerup])
        time = self.POWERUP_ACTIONS[powerup][2]
        self.gui.show_powerup_popup(powerup, time)

    # saves username and score to db through DBHander function
    def save(self) -> None:
        dbHandler.new_entry(self.username, self.score)

    def generate_crisis(self):
        """
        This function generates crisis and starts timer, calls self.call_staff()
        after timer runs out, once timer starts, self.prints_per_click and self.prints_per_sec are set to 0.
        """
        # Do not generate multiple crises at the same time
        if self.crisis != None:
            return
        crisis_index, crisis_name = self.rng.choice(list(self.crises.items()))
        self.gui.create_crisis(crisis_index)
        self.crisis = crisis_name

        # Crisis starts
        # Store current stats to restore when the crisis ends
        self.prints_per_click = 0
        self.prints_per_sec = 0
        self.gui.update_print_display(self.prints_per_click, self.prints_per_sec)
        # Timestamp
        # Note that self.time counts down
        self.time_crisis_start = self.time

    """
    Callback functions for moving objects
    """
    def resolve_no_filament(self):
        '''
        Checks if "no filament" crisis and resolves if it is
        '''
        if self.crisis == "No filament":
            self.gui.show_filament()
            self.resolve_crisis(True)

        else:
            print("Wrong resolution")

    def resolve_no_plate(self):
        '''
        Checks if "no plate" crisis and resolves if it is
        '''
        if self.crisis == "No printer bed":
            self.gui.show_plate()
            self.resolve_crisis(True)

        else:
            print("Wrong resolution")

    def call_staff(self):
        """
        Resolve all possible crises
        Do not reward the player
        """
        if self.crisis is None:
            return
        ## GUI TO CALL STAFF
        self.resolve_crisis(False)
        self.gui.show_filament()
        self.gui.show_plate()
        self.gui.hide_error()
        self.gui.popup_fablab()
        
    def resolve_crisis(self, userResolved: bool):
        """
        Sets crisis state to None, and determines whether 

        userResolved: True if crisis was resolved by the player
            False if crisis was resolved by staff
        """
        self.crisis = None
        self.time_crisis_start = 0
        self.prints_per_click = 1
        self.prints_per_sec = 0
        self.gui.update_print_display(self.prints_per_click, self.prints_per_sec)
        # 66% chance of reward
        should_reward = random.choice((False, True, True))
        if userResolved and should_reward:
            reward = random.choice(list(Powerup))
            print(f"You got the {reward.name}")
            self.use_powerup(reward)
        if userResolved:
            self.gui.user_resolved()

GameController()