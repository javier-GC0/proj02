from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import ttk
import os
import csv
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


def load_file(root, title):
    file = filedialog.askopenfilename(
        title="Select file",
        filetypes=[("CSV", "*.csv")]
    )
    if file:
        load_file.df = pd.read_csv(file)
        title.grid_forget()
        file_name = os.path.basename(file)
        if all(hasattr(load_file, attr) for attr in ["name_file", "path_file"]):  
            load_file.name_file.grid_forget() 
            load_file.path_file.grid_forget()

        load_file.name_file = tk.Label(root, text=f"Name of the file: {file_name}", font=("Times New Roman", 13))
        load_file.name_file.grid(row=1, column=2)
        load_file.path_file = tk.Label(root, text=f"Path of the file: {os.path.dirname(file)}", font=("Times New Roman", 13))
        load_file.path_file.grid(row=2, column=2)
        data_content = tk.Text(root)
        data_content.grid(row=3, column=2)

        scrollbar = tk.Scrollbar(root, command=data_content.yview)
        scrollbar.grid(row=3, column=3, sticky="nsw")
        data_content.config(yscrollcommand=scrollbar.set)
        try: 
            with open(file, "r") as f:
                reader = csv.reader(f)  
                rows = [", ".join(row) for row in reader]
                columns = list(load_file.df.columns) #rows[0].split(",")
                content = "\n".join(rows)
                data_content.insert("1.0", content)
            data_content.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")

        x_axis = ttk.Combobox(root, state="readonly", values=columns)
        x_axis.grid(row=5, column=1, sticky="w")
        x_axis_label = tk.Label(root, text="X-axis:")
        x_axis_label.grid(row=5, column=0, sticky="e")
        y_axis = ttk.Combobox(root, state="readonly", values=columns)
        y_axis.grid(row=5, column=4, sticky="w")
        y_axis_label = tk.Label(root, text="Y-axis:")
        y_axis_label.grid(row=5, column=3, sticky="e")

        plot = tk.Button(root, text="Plot", font=("Times New Roman", 13), command=lambda: plot_data(root, x_axis.get(), y_axis.get()))
        plot.grid(row=4, column=2)

    else:
        messagebox.showwarning("Warning", "No file selected")


def plot_data(root, x_axis, y_axis):
    if not x_axis or not y_axis:
        messagebox.showwarning("Warning", "Please select both X and Y axes")
        return

    try:
        df = load_file.df
        x_data = df[x_axis]
        y_data = df[y_axis]

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x_data, y_data, "o", label=f"{y_axis} vs. {x_axis}")
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=7, column=0, columnspan=6)

    except Exception as e:
        messagebox.showerror("Error", f"Error generating plot: {e}")