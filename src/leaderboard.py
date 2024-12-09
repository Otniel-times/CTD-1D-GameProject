import dbHandler
import tkinter as tk
from tkinter import ttk

## TODO: nicholas
class Leaderboard:
    def __init__(self, master) -> None:
        self.root = ttk.Frame(master)

        ## Data is already sorted by score, descending (list)
        data = dbHandler.getall_username_and_score_sorted()

        ## display leaderboard table
        self.label = ttk.Label(self.root, text = "High Scores", font =('Arial', 18))
        self.label.pack(padx=10, pady=10)

        # to display data
        for i in range(10):
            self.label = ttk.Label(self.root, text = data[i], font =('Arial', 18))
            self.label.pack(padx=10, pady=10)

        self.button = ttk.Button(self.root, text ="Exit", command = self.root.destroy)
        self.button.pack(padx = 10, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    menu = Leaderboard(root)
    menu.root.pack()
    root.mainloop()