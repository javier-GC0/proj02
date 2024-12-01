import tkinter as tk
from tkinter import ttk
import os
import csv
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


def load_file(root, header):
    file = tk.filedialog.askopenfilename(
        title="Select file",
        filetypes=[("CSV", "*.csv")]
    )
    if file:
        load_file.df = pd.read_csv(file)
        if all(hasattr(load_file, attr) for attr in ["name_file", "path_file"]):  
            load_file.name_file.grid_forget() 
            load_file.path_file.grid_forget()

        file_info = tk.Frame(root)
        file_info.grid(row=1, column=0, columnspan=1, sticky="nsew", pady=20)

        tk.Label(file_info, text="File information:", font=("Times New Roman", 15, "bold")).grid(row=0, column=0, sticky="w", padx=20)

        load_file.info_label = tk.Label(
            file_info, 
            text=f"- Name: {os.path.basename(file)}\n- Path: {os.path.dirname(file)}\n- Size: {os.path.getsize(file)/ (1024 * 1024):.2f} MB", 
            font=("Times New Roman", 13),
            justify="left"
        )
        load_file.info_label.grid(row=1, column=0, sticky="w", padx=20)

        data_frame = tk.Frame(root)
        data_frame.grid(row=2, column=0, sticky="nsew", padx=20)
        tk.Label(data_frame, text="Data:", font=("Times New Roman", 15, "bold")).grid(row=0, column=0, sticky="w")
        data_content = tk.Text(data_frame)
        data_content.grid(row=1, column=0, sticky="nsew", pady=8)
        scrollbar = tk.Scrollbar(data_frame, command=data_content.yview)
        scrollbar.grid(row=1, column=1, sticky="nsw")

        data_content.config(yscrollcommand=scrollbar.set)
        try: 
            with open(file, "r") as f:
                reader = csv.reader(f)  
                rows = [", ".join(row) for row in reader]
                columns = list(load_file.df.columns) 
                content = "\n".join(rows)
                data_content.insert("1.0", content)
            data_content.config(state="disabled")

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error reading file: {e}")

        axis_frame = tk.Frame(root)
        axis_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=12)

        x_axis_label = tk.Label(axis_frame, text="X-axis:", font=("Times New Roman", 15, "bold"))
        x_axis_label.grid(row=0, column=0, sticky="e")
        x_axis = ttk.Combobox(axis_frame, state="readonly", values=columns)
        x_axis.grid(row=0, column=1, sticky="w")
        y_axis_label = tk.Label(axis_frame, text=f"{' '*46}Y-axis:", font=("Times New Roman", 15, "bold"))
        y_axis_label.grid(row=0, column=2, sticky="e")
        y_axis = ttk.Combobox(axis_frame, state="readonly", values=columns)
        y_axis.grid(row=0, column=3, sticky="w")

        plot = tk.Button(header, text="Plot", font=("Courier", 13), command=lambda: plot_data(data_frame, header, x_axis.get(), y_axis.get()), width=20, bg="#F7F7F7")
        plot.grid(row=0, column=3, padx=5, pady=10)

    else:
        tk.messagebox.showwarning("Warning", "No file selected")


def plot_data(data_frame, header, x_axis, y_axis):
    if not x_axis or not y_axis:
        tk.messagebox.showwarning("Warning", "Please select both X and Y axes")
        return

    try:
        df = load_file.df
        x_data = df[x_axis]
        y_data = df[y_axis]

        tk.Label(data_frame, text="Plot:", font=("Times New Roman", 15, "bold")).grid(row=0, column=2, sticky="w", padx=20)
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x_data, y_data, "o", label=f"{y_axis} vs. {x_axis}")
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=data_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=2, columnspan=3, padx=20, pady=8)

        plot = tk.Button(header, text="Save plot", font=("Courier", 13), command=lambda: save_plot(fig), width=20, bg="#F7F7F7")
        plot.grid(row=0, column=4, padx=5, pady=10)

    except Exception as e:
        tk.messagebox.showerror("Error", f"Error generating plot: {e}")


def save_plot(fig):
    try:
        file_path = tk.filedialog.asksaveasfilename(
            defaultextension=".png", 
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])

        if file_path:  
            fig.savefig(file_path)
            tk.messagebox.showinfo("Success", "Plot saved successfully!")

    except Exception as e:
        tk.messagebox.showerror("Error", f"Error saving plot: {e}")