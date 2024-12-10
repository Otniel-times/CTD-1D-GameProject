import dbHandler
import tkinter as tk
from tkinter import ttk
import gui

## TODO: nicholas
class Leaderboard:
    def __init__(self, master) -> None:
        self.root = ttk.Frame(master)

        ## display leaderboard table
        self.label = ttk.Label(self.root, text = "High Scores", font =('Comic Sans MS', 18))
        self.label.pack(padx=10, pady=10)

        data = self.get_data()
        if data is None:
            data_len = 0
        else:
            data_len = len(data)
        if data_len > 9:
            data_len = 9
        
        # to display data
        for i in range(data_len):
            self.label = ttk.Label(self.root, text = data[i], font =('Comic Sans MS', 18))
            self.label.pack(padx=10, pady=10)

        self.callback = lambda: None

        self.button = ttk.Button(self.root, text ="Exit", command = self.exit)
        self.button.pack(padx = 10, pady=10)

    def get_data(self): ## Data is already sorted by score, descending (list)s
        data = dbHandler.getall_username_and_score_sorted()
        return data

    def exit(self):
        self.callback()


if __name__ == "__main__":
    root = tk.Tk()
    menu = Leaderboard(root)
    menu.root.pack()
    root.mainloop()