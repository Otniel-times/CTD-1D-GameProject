# login.py is to generate a name input frame for the game

# library import
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

## TODO: Clarence
class Login:
    def __init__(self, master):
        # initialises frame and variable to check if empty name was inputted
        self.root = ttk.Frame(master)
        self.has_clicked_with_empty_username = False

        # "How to play" label
        self.label = ttk.Label(self.root, text = "How to play", font =('Comic Sans MS', 18))
        self.label.pack(padx=10, pady=10)

        # how to play txt label
        # how_to_play_txt is to declare the text variable as it is too long
        how_to_play_txt = '''

        Your goal is to get as many prints as possible within the alloted time of 03:20.
        Familiarize yourself with the 3D Printer as you are expected to fix any problems that you may encounter.
        Solve problems with your prints to earn upgrades that temporarily increases your print capacity by a certain amount.
        If you fail to solve the problems, a member of the staff will come and resolve it for you without getting any bonus upgrades.
        Note that sometimes, there will be problems where the solution is to call lab staff.
        To begin the game, enter your username and press play.

        '''

        self.label = ttk.Label(self.root, text = how_to_play_txt, font =('Comic Sans MS', 12), justify="center")
        self.label.pack()

        # Entry box to input username + declared variable to store name for future use
        self.name = tk.StringVar()
        self.textbox = ttk.Entry(self.root, font=('Comic Sans MS', 16), textvariable=self.name)
        self.textbox.bind("<KeyPress>", self.shortcut)
        self.textbox.pack(padx=10, pady=10)

        # play button to run play function to store name and change frame to main game
        self.button = ttk.Button(self.root, text ="Play", command = self.play)
        self.button.pack(padx = 10, pady=10)

        # clear button to run clear function to clear text in entry box
        self.clearbtn = ttk.Button(self.root, text="Clear", command=self.clear)
        self.clearbtn.pack(padx=10, pady=10)
        self.play_callback = lambda: None
        self.name_callback = lambda: None

        # back button to run exit function to go back to main menu frame
        self.button = ttk.Button(self.root, text ="Back", command = self.exit)
        self.button.pack(padx = 10, pady=10)
        self.gomenu = lambda: None

    # play function checks if name empty and either runs game or 
    def play(self):
        # uses console to check if name variable is stored correctly
        print(self.name.get())

        # checks if name is not empty, then runs play and name callback functions in game.py
        if self.name.get() != "":
            self.play_callback()
            self.name_callback()
        
        # checks if name is empty, then tells user that username cannot be empty in red text
        elif not self.has_clicked_with_empty_username:
            self.emptytext = ttk.Label(self.root, text="Username field cannot be empty. Please enter a username to continue.", foreground="red")
            self.emptytext.pack()
            self.has_clicked_with_empty_username = True

    def shortcut(self, event):
        if event.state ==12 and event.keysym == "Return":
            self.play()

    # function to clear the text within the text entry box
    def clear(self):
        self.name.set("")

    # function to allow change frame back to main menu
    def exit(self):
        self.gomenu()

# if statement to allow for individual testing of above code within this .py file
# if name = main is to check if the current file is being run directly
if __name__ == "__main__":
    root = tk.Tk()
    menu = Login(root)
    menu.root.pack()
    root.mainloop()