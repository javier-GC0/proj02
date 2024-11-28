import tkinter as tk
import funs

root = tk.Tk()
root.title("Project #2")
root.geometry("800x500")


title = tk.Label(root, text="Welcome to the application", font=("Candara", 18))
title.grid(row=0, column=1)
open_file_btn = tk.Button(root, text="Select file", command=lambda: funs.load_file(root, title), font=("Times New Roman", 13)).grid(row=1, column=0)
quit_btn = tk.Button(root, text="Quit", command=root.destroy, font=("Times New Roman", 13)).grid(row=4, column=1)
root.mainloop()