from tkinter import filedialog, messagebox
import tkinter as tk
import os
import csv

def load_file(root, title):
    file = filedialog.askopenfilename(
        title="Select file",
        filetypes=[("CSV", "*.csv")]
    )
    if file:
        title.grid_forget()
        file_name = os.path.basename(file)
        if hasattr(load_file, "label"):  
            load_file.label.grid_forget()  

        load_file.label = tk.Label(root, text=f"Selected file: {file_name}", font=("Times New Roman", 13))
        load_file.label.grid(row=1, column=0, columnspan=2)
        data_content = tk.Text(root)
        data_content.grid(row=2, column=1)

        scrollbar = tk.Scrollbar(root, command=data_content.yview)
        scrollbar.grid(row=2, column=2, sticky="nse")
        data_content.config(yscrollcommand=scrollbar.set)
        try: 
            with open(file, "r") as f:
                reader = csv.reader(f)  
                rows = [", ".join(row) for row in reader]
                content = "\n".join(rows)

                data_content.insert("1.0", content)
            data_content.config(state="disabled")

        except Exception as e:
            print(f"Error reading file: {e}")

        plot = tk.Button(root, text="Plot", font=("Times New Roman", 13), command=plot_data)
        plot.grid(row=3, column=1)

    else:
        messagebox.showwarning("Alert", "No file selected")


def plot_data():
    pass