import tkinter as tk
from tkinter import ttk
from .state import active_layers
from .remove import remove_selected_layers
from .plot_layers import plot_selected_layers
from .save_layer import save_selected_layer
from .change_crs import change_layer_crs


def load_layers(tree):
    for item in tree.get_children():
        tree.delete(item)

    for layer_id, layer in active_layers.items():
        tree.insert("", tk.END, iid=layer_id, values=(layer.name, layer.geometry, layer.crs))

def create_buttons_panel(parent, tree):
    """2. Dodawanie panelu i przycisków sterujących."""
    frame_buttons = ttk.Frame(parent, padding=10)

    # Przycisk do wyświetlania mapy
    btn_show = ttk.Button(
        frame_buttons,
        text="Pokaż zaznaczone",
        command=lambda: plot_selected_layers(tree)
    )
    btn_show.pack(fill=tk.X, pady=5)

    # Przycisk usuwania
    btn_remove = ttk.Button(
        frame_buttons,
        text="Usuń zaznaczone",
        command=lambda: remove_selected_layers(tree)
    )
    btn_remove.pack(fill=tk.X, pady=5)

    # Przycisk zapisu
    btn_save = ttk.Button(
        frame_buttons,
        text="Zapisz zaznaczoną",
        command=lambda: save_selected_layer(tree)
    )
    btn_save.pack(fill=tk.X, pady=5)

    # Przycisk zmiany CRS
    btn_crs = ttk.Button(
        frame_buttons,
        text="Zmień CRS",
        command=lambda: change_layer_crs(tree, load_layers)
    )
    btn_crs.pack(fill=tk.X, pady=5)

    return frame_buttons


def show_layers(parent):
    window = tk.Toplevel(parent)
    window.title("Warstwy")

    # Główne ramki
    frame_table = ttk.Frame(window)
    frame_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Konfiguracja kolumn i tabeli
    col_widths = {
        "nazwa": 150,
        "geometria": 230,
        "crs": 230
    }
    columns = list(col_widths.keys())

    tree = ttk.Treeview(frame_table, columns=columns, show="headings")
    for col, width in col_widths.items():
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor="w")

    # Pasek przewijania
    scrollbar = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    load_layers(tree)

    frame_buttons = create_buttons_panel(window, tree)
    frame_buttons.pack(side=tk.RIGHT, fill=tk.Y)

    window.update_idletasks()

    required_width = window.winfo_reqwidth()

    window.geometry(f"{required_width}x700")

    window.minsize(required_width, 500)
