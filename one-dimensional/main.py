import tkinter as tk
from utils import ProgramTimer
from ui import UserInterface

if __name__ == "__main__":
    root = tk.Tk()
    timer = ProgramTimer()
    app = UserInterface(root, timer)
    root.mainloop()
