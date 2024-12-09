import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Login:

    def __init__(self, master):
        self.root = ttk.Frame(master)
        self.has_clicked_with_empty_username = False

        self.label = ttk.Label(self.root, text = "How to play", font =('Arial', 18))
        self.label.pack(padx=10, pady=10)

        self.label = ttk.Label(self.root, text = "Your goal is to get as many prints as possible within the alloted time of 03:20.\n\nFamiliarize yourself with the 3D Printer as you are expected to fix any problems that you may encounter.\nSolve problems with your prints to earn upgrades that temporarily increases your print capacity by a certain amount.\n\nIf you fail to solve the problems, a member of the staff will come and resolve it for you without getting any bonus upgrades.\nNote that sometimes, there will be problems where the solution is to call lab staff.\n\nTo begin the game, enter your username and press play.", font =('Arial', 12), justify="center")
        self.label.pack()

        self.name = tk.StringVar()
        self.textbox = ttk.Entry(self.root, font=('Arial', 16), textvariable=self.name)
        self.textbox.bind("<KeyPress>", self.shortcut)
        self.textbox.pack(padx=10, pady=10)

        self.button = ttk.Button(self.root, text ="Play", command = self.play)
        self.button.pack(padx = 10, pady=10)

        self.clearbtn = ttk.Button(self.root, text="Clear", command=self.clear)
        self.clearbtn.pack(padx=10, pady=10)
        self.play_callback = lambda: None
        self.name_callback = lambda: None

    def play(self):
        print(self.name.get())
        if self.name.get() != "":
            self.play_callback()
            self.name_callback()
        elif not self.has_clicked_with_empty_username:
            self.emptytext = ttk.Label(self.root, text="Username field cannot be empty. Please enter a username to continue.", foreground="red")
            self.emptytext.pack()
            self.has_clicked_with_empty_username = True

    def shortcut(self, event):
        if event.state ==12 and event.keysym == "Return":
            self.play()

    def clear(self):
        self.name.set("")

if __name__ == "__main__":
    root = tk.Tk()
    menu = Login(root)
    menu.root.pack()
    root.mainloop()