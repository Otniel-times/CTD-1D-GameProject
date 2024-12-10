import dbHandler
import tkinter as tk
from tkinter import ttk

## TODO: nicholas
class Leaderboard:
    def __init__(self, master) -> None:
        self.root = ttk.Frame(master)
        self.CSfont = 'Comic Sans MS'

        ## display "High Scores" + "Rank" + "Username" + "Score"
        self.high_score = ttk.Label(self.root, text = "HIGH SCORES!", font =(self.CSfont, 28))
        self.high_score.grid(row = 0, column = 1, pady = 2)

        self.R = ttk.Label(self.root, text = "Rank", font =(self.CSfont, 18))
        self.R.grid(row = 1, column = 0, pady = 10)

        name_txt = "                                      Name                                      "

        self.R = ttk.Label(self.root, text = name_txt, font =(self.CSfont, 18))
        self.R.grid(row = 1, column = 1, pady = 10)

        self.R = ttk.Label(self.root, text = "Score", font =(self.CSfont, 18))
        self.R.grid(row = 1, column = 2, pady = 10)

        self.gomenu = lambda: None

    def get_data(self): ## Data is already sorted by score, descending (list)s
        data = dbHandler.getall_username_and_score_sorted()
        return data
    
    def display_data(self):
        data = self.get_data()
        data_len = len(data)
        if data_len > 10:
            data_len = 10
        
        # to display data
        for i in range(2, data_len+2):
            self.rank = ttk.Label(self.root, text = str(i-1), font =(self.CSfont, 18))
            self.rank.grid(row = i, column = 0, pady = 2)
            self.name = ttk.Label(self.root, text = str(data[i-2][0]), font =(self.CSfont, 18))
            self.name.grid(row = i, column = 1, sticky = tk.W, pady = 2)
            self.score = ttk.Label(self.root, text = str(data[i-2][1]), font =(self.CSfont, 18))
            self.score.grid(row = i, column = 2, pady = 2)


    def exit_btn(self):
        self.button = ttk.Button(self.root, text ="Exit", command = self.exit)
        self.button.grid(row = 100, column = 1, pady = 10)

    def exit(self):
        self.gomenu()



if __name__ == "__main__":
    root = tk.Tk()
    menu = Leaderboard(root)
    menu.root.grid()
    menu.display_data()
    menu.exit_btn()
    root.mainloop()


