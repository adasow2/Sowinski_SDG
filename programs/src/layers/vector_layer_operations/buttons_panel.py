import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from ..state import active_layers
from ..vector_layer import VectorLayer
from .table import LayerTableWidget
from .operations_dialog import SimpleOperationsDialog

class LayerButtonsPanel(ttk.Frame):
    def __init__(self, parent, table_widget: LayerTableWidget):
        super().__init__(parent, padding=10)
        self.table_widget = table_widget
        self.parent_window = parent

        # Przycisk wczytywania warstwy
        btn_load = ttk.Button(
            self,
            text="Wczytaj warstwę",
            command=self.load_data
        )
        btn_load.pack(fill=tk.X, pady=5)

        # Przycisk do wyświetlania mapy
        btn_show = ttk.Button(
            self,
            text="Pokaż zaznaczone",
            command=self.plot_selected_layers
        )
        btn_show.pack(fill=tk.X, pady=5)

        # Przycisk usuwania
        btn_remove = ttk.Button(
            self,
            text="Usuń zaznaczone",
            command=self.remove_selected_layers
        )
        btn_remove.pack(fill=tk.X, pady=5)

        # Przycisk zapisu
        btn_save = ttk.Button(
            self,
            text="Zapisz zaznaczoną",
            command=self.save_selected_layer
        )
        btn_save.pack(fill=tk.X, pady=5)

        # Przycisk prostych operacji
        btn_operations = ttk.Button(
            self,
            text="Proste operacje",
            command=self.open_operations_dialog
        )
        btn_operations.pack(fill=tk.X, pady=5)

    def open_operations_dialog(self):
        selected_items = self.table_widget.get_selected_layer_ids()
        if not selected_items:
            messagebox.showwarning("Brak zaznaczenia", "Zaznacz dokładnie jedną warstwę do wykonania operacji.")
            return

        if len(selected_items) > 1:
            messagebox.showwarning("Zbyt wiele zaznaczeń", "Proste operacje można wykonać tylko na jednej warstwie naraz.")
            return

        layer_id = selected_items[0]
        if layer_id not in active_layers:
            return

        layer_obj = active_layers[layer_id]
        SimpleOperationsDialog(self.parent_window, layer_id, layer_obj, self.table_widget.load_layers)

    def load_data(self):
        path = filedialog.askopenfilename(title='Wybierz warstwę')
        if not path:
            return

        vector_files = ['shp', 'geojson', 'gpkg']
        if path.split('.')[-1].lower() in vector_files:
            try:
                VectorLayer.load_vector(path)
                self.table_widget.load_layers()
                # Zamknij okno warstw (self.parent_window to okno Toplevel LayerWindow)
                if hasattr(self, 'parent_window') and self.parent_window:
                    self.parent_window.destroy()
            except Exception as e:
                messagebox.showwarning(
                    "Błąd wczytywania",
                    f"Nie udało się wczytać wybranego pliku:\n{e}"
                )

    def plot_selected_layers(self):
        selected_items = self.table_widget.get_selected_layer_ids()
        if not selected_items:
            return

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_title("Wybrane warstwy")

        plotted_count = 0
        for layer_id in selected_items:
            if layer_id in active_layers:
                layer_obj = active_layers[layer_id]
                if layer_obj.df is not None:
                    layer_obj.df.plot(
                        ax=ax,
                        alpha=0.6,
                        edgecolor='k',
                        label=layer_obj.name
                    )
                    plotted_count += 1

        if plotted_count > 0:
            ax.legend()
            plt.tight_layout()
            plt.show()
        else:
            plt.close(fig)

    def remove_selected_layers(self):
        selected_items = self.table_widget.get_selected_layer_ids()
        if not selected_items:
            return

        for item_id in selected_items:
            if item_id in active_layers:
                del active_layers[item_id]
            self.table_widget.tree.delete(item_id)

    def save_selected_layer(self):
        selected_items = self.table_widget.get_selected_layer_ids()
        if not selected_items:
            messagebox.showwarning("Brak zaznaczenia", "Zaznacz warstwę do zapisu.")
            return

        if len(selected_items) > 1:
            messagebox.showwarning("Zbyt wiele zaznaczeń", "Wybierz tylko jedną warstwę do zapisu.")
            return

        layer_id = selected_items[0]
        if layer_id not in active_layers:
            return

        layer_obj = active_layers[layer_id]

        file_path = filedialog.asksaveasfilename(
            title="Zapisz warstwę jako",
            defaultextension=".geojson",
            filetypes=[
                ("GeoJSON", "*.geojson"),
                ("Shapefile", "*.shp"),
                ("GeoPackage", "*.gpkg"),
                ("CSV", "*.csv"),
                ("Wszystkie pliki", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            ext = file_path.split('.')[-1].lower()
            if ext == 'csv':
                sep = simpledialog.askstring(
                    "Separator CSV",
                    "Podaj separator dla pliku CSV (np. ',', ';', '\t'):",
                    initialvalue=","
                )
                if sep is None:
                    return

                df_to_save = layer_obj.df.copy()
                if 'geometry' in df_to_save.columns:
                    df_to_save['geometry'] = df_to_save['geometry'].astype(str)
                df_to_save.to_csv(file_path, index=False, sep=sep)
            else:
                layer_obj.df.to_file(file_path)
            messagebox.showinfo("Sukces", f"Pomyślnie zapisano warstwę do:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Błąd zapisu", f"Nie udało się zapisać pliku:\n{e}")
