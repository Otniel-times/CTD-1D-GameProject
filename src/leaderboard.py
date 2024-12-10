# leaderboard.py is to generate a leaderboard frame for the game

# library import
import dbHandler
import tkinter as tk
from tkinter import ttk

## TODO: nicholas
class Leaderboard:
    def __init__(self, master) -> None:
        # initialises frame, font, and gomenu callback
        self.root = ttk.Frame(master)
        self.CSfont = 'Comic Sans MS'
        self.gomenu = lambda: None
    
    # startup display for "High Scores" + "Rank" + "Username" + "Score"
    def startup(self):
        # HIGH SCORE! Label
        self.high_score = ttk.Label(self.root, text = "HIGH SCORES!", font =(self.CSfont, 28))
        self.high_score.grid(row = 0, column = 1, pady = 2)

        # Rank Label
        self.R = ttk.Label(self.root, text = "Rank", font =(self.CSfont, 18))
        self.R.grid(row = 1, column = 0, pady = 10)

        # Name Label
        # name_txt variable as there is too many spaces needed (for cleaner view)
        name_txt = "                                      Name                                      "
        self.R = ttk.Label(self.root, text = name_txt, font =(self.CSfont, 18))
        self.R.grid(row = 1, column = 1, pady = 10)

        # Score Label
        self.R = ttk.Label(self.root, text = "Score", font =(self.CSfont, 18))
        self.R.grid(row = 1, column = 2, pady = 10)

    # fetches data form db
    def get_data(self): 
        # uses DBHandler functions to get sorted data, returns data in list with tuples
        data = dbHandler.getall_username_and_score_sorted()
        return data
    
    # uses for-loop to display scores of previous users (up to 10)
    def display_data(self):
        data = self.get_data()
        data_len = len(data)

        # if statement to ensure the displayed data is only 10 rows
        if data_len > 10:
            data_len = 10
        
        # to display data row by row
        for i in range(2, data_len+2):
            # displays rank of player in column 0
            self.rank = ttk.Label(self.root, text = str(i-1), font =(self.CSfont, 18))
            self.rank.grid(row = i, column = 0, pady = 2)
            # displays name of player in column 1
            self.name = ttk.Label(self.root, text = str(data[i-2][0]), font =(self.CSfont, 18))
            self.name.grid(row = i, column = 1, sticky = tk.W, pady = 2)
            # displays score of player in column 2
            self.score = ttk.Label(self.root, text = str(data[i-2][1]), font =(self.CSfont, 18))
            self.score.grid(row = i, column = 2, pady = 2)

    # creates exit button to go to main menu
    def exit_btn(self):
        self.button = ttk.Button(self.root, text ="Exit", command = self.exit)
        self.button.grid(row = 100, column = 1, pady = 10)

    # callback to change_frame function to change to main menu frame
    def exit(self):
        self.gomenu()
    
    # clears all widgets inside frame
    def clr_wgt(self): 
        for wgt in self.root.winfo_children():
            wgt.destroy()

# if statement to allow for individual testing of above code within this .py file
# if name = main is to check if the current file is being run directly
if __name__ == "__main__":
    root = tk.Tk()
    menu = Leaderboard(root)
    menu.root.grid()
    menu.startup()
    menu.display_data()
    menu.exit_btn()
    root.mainloop()