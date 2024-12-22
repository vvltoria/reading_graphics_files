import os
from PIL import Image
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def get_image_info(file_path):
    try:
        with Image.open(file_path) as img:
            dpi = img.info.get('dpi', (0, 0))
            if dpi == (0, 0) or dpi == "Unknown":
                dpi_text = "Не указано"
            else:
                dpi_text = f"{dpi[0]} x {dpi[1]}"

            img_info = {
                'File Name': os.path.basename(file_path),
                'Size (px)': f"{img.size[0]} x {img.size[1]}",
                'Resolution (DPI)': dpi_text,
                'Color Depth': img.mode,
                'Compression': img.info.get('compression', 'None'),
                'Format': img.format
            }
            return img_info
    except Exception as e:
        return {'File Name': os.path.basename(file_path), 'Error': str(e)}

def process_images(folder):
    image_info_list = []
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tif')

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(supported_formats):
                file_path = os.path.join(root, file)
                info = get_image_info(file_path)
                image_info_list.append(info)

    return pd.DataFrame(image_info_list)

def choose_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        df = process_images(folder_selected)
        if not df.empty:
            display_table(df)
            adjust_window_size(df)
        else:
            messagebox.showwarning("Нет изображений", "В выбранной папке нет поддерживаемых файлов изображений.")
    else:
        messagebox.showwarning("Папка не выбрана", "Пожалуйста, выберите папку.")

def display_table(df):
    for widget in table_frame.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(table_frame)
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(fill="both", expand=True)


def adjust_window_size(df):
    columns_count = len(df.columns)
    window_width = 150 * columns_count
    rows_count = len(df)
    window_height = min(25 * rows_count, 600)

    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)

root = tk.Tk()
root.title("Image Info Extractor")

root.geometry("300x100")
root.resizable(False, False)

btn_select_folder = tk.Button(root, text="Выбрать папку с изображениями", command=choose_folder)
btn_select_folder.pack(pady=20)

table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True)

root.mainloop()