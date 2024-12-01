import tkinter as tk
import funs

root = tk.Tk()
root.title("Project #2")
root.geometry("800x500")

root.columnconfigure(0, weight=1)

header = tk.Frame(root, bg="#C7DA34", height=50)
header.grid(row=0, column=0, columnspan=2, sticky="nsew")
header.columnconfigure((0, 1, 2, 3, 4), weight=1)

title = tk.Label(header, text="GUI application using Tkinter", font=("Candara", 20), bg="#C7DA34")
title.grid(row=0, column=0, padx=5, pady=10)

open_file = tk.Button(header, text="Select file", command=lambda: funs.load_file(root, header), font=("Courier", 13), width=20, bg="#F7F7F7")
open_file.grid(row=0, column=1, padx=5, pady=10)

quit = tk.Button(header, text="Quit", command=root.destroy, font=("Courier", 13), width=20, bg="#F7F7F7")
quit.grid(row=0, column=2, padx=5, pady=10)

root.mainloop()