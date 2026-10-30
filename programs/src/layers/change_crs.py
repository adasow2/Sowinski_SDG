from .state import active_layers
from tkinter import messagebox, simpledialog

def change_layer_crs(tree, load_layers_callback):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Brak zaznaczenia", "Zaznacz warstwę do zmiany układu współrzędnych.")
        return
    
    if len(selected_items) > 1:
        messagebox.showwarning("Zbyt wiele zaznaczeń", "Wybierz tylko jedną warstwę.")
        return

    layer_id = selected_items[0]
    if layer_id not in active_layers:
        return

    layer_obj = active_layers[layer_id]

    current_crs = layer_obj.crs
    new_crs_input = simpledialog.askstring(
        "Zmiana układu współrzędnych (CRS)",
        f"Aktualny CRS: {current_crs}\n\nPodaj docelowy CRS (np. EPSG:2180, EPSG:4326):",
        initialvalue="EPSG:2180"
    )

    if not new_crs_input:
        return

    try:
        # Reprojektacja GeoDataFrame
        if layer_obj.df.crs is None:
            # Jeśli brak zdefiniowanego CRS, przypisujemy zamiast transformować, lub próbujemy ustawić
            layer_obj.df = layer_obj.df.set_crs(new_crs_input, allow_override=True)
        else:
            layer_obj.df = layer_obj.df.to_crs(new_crs_input)
        
        # Aktualizacja właściwości w obiekcie
        layer_obj.crs = layer_obj.df.crs.to_string()

        # Odświeżenie tabeli w widoku warstw
        load_layers_callback(tree)

        messagebox.showinfo("Sukces", f"Zmieniono układ współrzędnych na: {layer_obj.crs}")
    except Exception as e:
        messagebox.showerror("Błąd CRS", f"Nie udało się zmienić układu współrzędnych:\n{e}")
