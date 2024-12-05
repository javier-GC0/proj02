import tkinter as tk
from funs import Functions
# config
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import BG_HEADER, HEIGHT_HEADER, FONT_HEADER, FONT_SIZE_HEADER, FONT_BUTTON, FONT_SIZE_BUTTON, WIDTH_BUTTON, BG_BUTTON


class GUI:
    def __init__(self, root):
        self.root = root
        self.window()
        self.header()

    def window(self):
        self.root.title("Python in the Enterprise")
        self.root.geometry("800x500")
        self.root.columnconfigure(0, weight=1)

    def header(self):
        header = tk.Frame(self.root, bg=BG_HEADER, height=HEIGHT_HEADER)
        header.grid(row=0, column=0, columnspan=2, sticky="nsew")
        header.columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Title
        tk.Label(header, text="GUI application using Tkinter", font=(FONT_HEADER, FONT_SIZE_HEADER), bg=BG_HEADER).grid(
            row=0, column=0, padx=5, pady=10
        )
        # 'Select file' button
        tk.Button(
            header, text="Select file",
            command=lambda: Functions.load_file(self.root, header),
            font=(FONT_BUTTON, FONT_SIZE_BUTTON), width=WIDTH_BUTTON, bg=BG_BUTTON
        ).grid(row=0, column=1, padx=5, pady=10)
        # 'Quit' button
        tk.Button(
            header, text="Quit",
            command=self.root.destroy,
            font=(FONT_BUTTON, FONT_SIZE_BUTTON), width=WIDTH_BUTTON, bg=BG_BUTTON
        ).grid(row=0, column=2, padx=5, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()