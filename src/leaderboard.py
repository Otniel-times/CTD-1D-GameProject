import dbHandler
import tkinter as tk
from tkinter import ttk

class Leaderboard:
    def __init__(self, master) -> None:
        self.root = ttk.Frame(master)

    def show_table(self):
        ## display leaderboard table
        data = dbHandler.getall_username_and_score()
        pass


if __name__ == "__main__":
    root = tk.Tk()
    menu = Leaderboard(root)
    menu.root.pack()
    root.mainloop()