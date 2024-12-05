import tkinter as tk
from tkinter import ttk
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
# config
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import FONT_BUTTON, FONT_SIZE_BUTTON, WIDTH_BUTTON, BG_BUTTON, FONT_TEXT, FONT_SIZE_MED_TEXT, FONT_SIZE_SMALL_TEXT


class Functions:
    @staticmethod
    def load_file(root, header):
        file = tk.filedialog.askopenfilename(
            title="Select file",
            filetypes=[("CSV", "*.csv")]
        )
        if file:
            df = pd.read_csv(file)
            if hasattr(Functions, "save_btn"):
                Functions.save_btn.destroy() # when a new file is loaded, the save button disappers (no plot yet)
            Functions.file_info(root, file, df)
            Functions.plot_options(root, header, df)
        else:
            tk.messagebox.showwarning("Warning", "No file selected")

    @staticmethod
    def file_info(root, file, df):
        file_info = tk.Frame(root)
        file_info.grid(row=1, column=0, columnspan=1, sticky="nsew", pady=20)

        tk.Label(file_info, text="File information:", font=(FONT_TEXT, FONT_SIZE_MED_TEXT, "bold")).grid(
            row=0, column=0, sticky="w", padx=20
        )
        tk.Label(
            file_info,
            text=f"- Name: {os.path.basename(file)}\n"
                 f"- Path: {os.path.dirname(file)}\n"
                 f"- Size: {os.path.getsize(file) / (1024 * 1024):.2f} MB",
            font=(FONT_TEXT, FONT_SIZE_SMALL_TEXT),
            justify="left"
        ).grid(row=1, column=0, sticky="w", padx=20)

        Functions.raw_data(root, df)

    @staticmethod
    def raw_data(root, df):
        data_frame = tk.Frame(root)
        Functions.raw_data.data_frame = data_frame
        data_frame.grid(row=2, column=0, sticky="nsew", padx=20)

        tk.Label(data_frame, text="Data:", font=(FONT_TEXT, FONT_SIZE_MED_TEXT, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        data_content = tk.Text(data_frame)
        data_content.grid(row=1, column=0, sticky="nsew", pady=8)
        scrollbar = tk.Scrollbar(data_frame, command=data_content.yview)
        scrollbar.grid(row=1, column=1, sticky="nsw")

        data_content.config(yscrollcommand=scrollbar.set)
        content = df.to_csv(index=False)
        data_content.insert("1.0", content)
        data_content.config(state="disabled")

    @staticmethod
    def plot_options(root, header, df):
        columns = list(df.columns)
        axis_frame = tk.Frame(root)
        axis_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=12)

        tk.Label(axis_frame, text="X-axis:", font=(FONT_TEXT, FONT_SIZE_MED_TEXT, "bold")).grid(row=0, column=0, sticky="e")
        x_axis = ttk.Combobox(axis_frame, state="readonly", values=columns)
        x_axis.grid(row=0, column=1, sticky="w")

        tk.Label(axis_frame, text=f"{' '*46}Y-axis:", font=(FONT_TEXT, FONT_SIZE_MED_TEXT, "bold")).grid(row=0, column=2, sticky="e")
        y_axis = ttk.Combobox(axis_frame, state="readonly", values=columns)
        y_axis.grid(row=0, column=3, sticky="w")

        tk.Button(
            header, text="Plot",
            command=lambda: Functions.plot_data(header, df, x_axis.get(), y_axis.get()),
            font=(FONT_BUTTON, FONT_SIZE_BUTTON), width=WIDTH_BUTTON, bg=BG_BUTTON
        ).grid(row=0, column=3, padx=5, pady=10)

    @staticmethod
    def plot_data(header, df, x_axis, y_axis):
        if not x_axis or not y_axis:
            tk.messagebox.showwarning("Warning", "Please select both X and Y axes")
            return

        try:
            x_data = df[x_axis]
            y_data = df[y_axis]

            data_frame = Functions.raw_data.data_frame 
            tk.Label(data_frame, text="Plot:", font=(FONT_TEXT, FONT_SIZE_MED_TEXT, "bold")).grid(
                row=0, column=2, sticky="w", padx=20)

            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            ax.plot(x_data, y_data, "o", label=f"{y_axis} vs. {x_axis}")
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.legend()

            canvas = FigureCanvasTkAgg(fig, master=data_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, column=2, columnspan=3, padx=20, pady=8)

            Functions.save_btn = tk.Button(
                header, text="Save plot",
                command=lambda: Functions.save_plot(fig),
                font=(FONT_BUTTON, FONT_SIZE_BUTTON), width=WIDTH_BUTTON, bg=BG_BUTTON
            )
            Functions.save_btn.grid(row=0, column=4, padx=5, pady=10)

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error generating plot: {e}")

    @staticmethod
    def save_plot(fig):
        try:
            file_path = tk.filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
            )
            if file_path:
                fig.savefig(file_path)
                tk.messagebox.showinfo("Success", "Plot saved successfully!")
            else:
                tk.messagebox.showwarning("Warning", "Plot was not saved")

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error saving plot: {e}")