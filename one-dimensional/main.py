import tkinter as tk
from utils import ProgramTimer, ReportTarget
from ui import UserInterface

if __name__ == "__main__":
    root = tk.Tk()
    timer = ProgramTimer(targets=[ReportTarget.CONSOLE, ReportTarget.FILE])
    app = UserInterface(root, timer)
    root.mainloop()
