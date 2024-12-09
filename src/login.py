import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Login:

    def __init__(self, master):
        self.root = ttk.Frame(master)

        self.label = ttk.Label(self.root, text = "Play", font =('Arial', 18))
        self.label.pack(padx=10, pady=10)

        self.name = tk.StringVar()
        self.textbox = ttk.Entry(self.root, font=('Arial', 16), textvariable=self.name)
        self.textbox.bind("<KeyPress>", self.shortcut)
        self.textbox.pack(padx=10, pady=10)

        self.check_state = tk.IntVar()

        self.check = ttk.Checkbutton(self.root, text = "Show Messagebox", variable=self.check_state)
        self.check.pack(padx=10, pady=10)

        self.button = ttk.Button(self.root, text ="Show Username", command = self.show_message)
        self.button.pack(padx = 10, pady=10)

        self.clearbtn = ttk.Button(self.root, text="Clear", command=self.clear)
        self.clearbtn.pack(padx=10, pady=10)
        
        self.play_callback = lambda: None
        self.name_callback = lambda: None

    def show_message(self):
        if self.check_state.get() == 0:
            print(self.name.get())
        else:
            messagebox.showinfo(title = "Message", message=self.name.get())
        self.play_callback()
        self.name_callback()

    def shortcut(self, event):
        if event.state ==12 and event.keysym == "Return":
            self.show_message()

    def clear(self):
        self.name.set("")

if __name__ == "__main__":
    root = tk.Tk()
    menu = Login(root)
    menu.root.pack()
    root.mainloop()