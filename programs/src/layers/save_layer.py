from .state import active_layers
from tkinter import filedialog, messagebox, simpledialog

def save_selected_layer(tree):
    selected_items = tree.selection()
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
                return  # Anulowano

            df_to_save = layer_obj.df.copy()
            if 'geometry' in df_to_save.columns:
                df_to_save['geometry'] = df_to_save['geometry'].astype(str)
            df_to_save.to_csv(file_path, index=False, sep=sep)
        else:
            layer_obj.df.to_file(file_path)
        messagebox.showinfo("Sukces", f"Pomyślnie zapisano warstwę do:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Błąd zapisu", f"Nie udało się zapisać pliku:\n{e}")
