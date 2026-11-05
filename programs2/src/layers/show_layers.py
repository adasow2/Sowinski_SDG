import tkinter as tk
from .vector_layer_operations.table import LayerTableWidget
from .vector_layer_operations.buttons_panel import LayerButtonsPanel

class LayerWindow(tk.Toplevel):
    """
    Główne okno warstw oparte na OOP, łączące tabelę i panel przycisków.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Warstwy")

        # Tabela warstw
        self.table_widget = LayerTableWidget(self)
        self.table_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Panel przycisków
        self.buttons_panel = LayerButtonsPanel(self, self.table_widget)
        self.buttons_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.update_idletasks()
        required_width = self.winfo_reqwidth()
        self.geometry(f"{required_width}x700")
        self.minsize(required_width, 500)


def show_layers(parent):
    """Funkcja kompatybilna wstecznie, uruchamiająca okno OOP."""
    return LayerWindow(parent)
