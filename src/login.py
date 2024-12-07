import tkinter as tk
from tkinter import messagebox

class MyGUI:

    def __init__(self):
        self.win = tk.Tk()

        self.root = tk.Frame()
        self.root.pack()

        self.label = tk.Label(self.root, text = "Enter your username", font =('Arial', 18))
        self.label.pack(padx=10, pady=10)

        self.textbox = tk.Text(self.root, height=5, font=('Arial', 16))
        self.textbox.bind("<KeyPress>", self.shortcut)
        self.textbox.pack(padx=10, pady=10)

        self.check_state = tk.IntVar()

        self.check = tk.Checkbutton(self.root, text = "Show Messagebox", font=('Arial', 16), variable=self.check_state)
        self.check.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text ="Show Username", font=('Arial', 18), command = self.show_message)
        self.button.pack(padx = 10, pady=10)

        self.clearbtn = tk.Button(self.root, text="Clear", font=('Arial', 18), command=self.clear)
        self.clearbtn.pack(padx=10, pady=10)


        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.win.mainloop()

    def show_message(self):
        if self.check_state.get() == 0:
            #print(self.textbox.get('1.0', tk.END))
            name = self.textbox.get('1.0', tk.END)
            print(name)
        else:
            messagebox.showinfo(title = "Message", message=self.textbox.get('1.0', tk.END))

    def shortcut(self, event):
        if event.state ==12 and event.keysym == "Return":
            self.show_message()

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()

    def clear(self):
        self.textbox.delete('1.0', tk.END)

MyGUI()