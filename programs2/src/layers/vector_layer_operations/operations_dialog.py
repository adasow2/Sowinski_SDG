import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from ..state import active_layers
from ..vector_layer import VectorLayer
from .. import state

class SimpleOperationsDialog(tk.Toplevel):
    """
    Okno wyboru i parametryzacji prostych operacji GIS na pojedynczej warstwie.
    """
    def __init__(self, parent, layer_id, layer_obj, callback_refresh):
        super().__init__(parent)
        self.title("Proste operacje GIS")
        self.geometry("400x250")
        self.resizable(False, False)
        
        self.layer_id = layer_id
        self.layer_obj = layer_obj
        self.callback_refresh = callback_refresh

        self.operations = [
            "zmień układ współrzędnych",
            "bufor",
            "centroid",
            "convex hull",
            "simplify"
        ]

        self.create_widgets()

    def create_widgets(self):
        lbl = ttk.Label(self, text=f"Wybrana warstwa: {self.layer_obj.name}", font=("Arial", 10, "bold"))
        lbl.pack(pady=10)

        lbl_op = ttk.Label(self, text="Wybierz operację:")
        lbl_op.pack(anchor="w", padx=20)

        self.op_combobox = ttk.Combobox(self, values=self.operations, state="readonly", width=35)
        self.op_combobox.pack(padx=20, pady=5)
        if self.operations:
            self.op_combobox.set(self.operations[0])

        btn_execute = ttk.Button(self, text="Wykonaj", command=self.execute_operation)
        btn_execute.pack(pady=20)

    def execute_operation(self):
        selected_op = self.op_combobox.get()
        if not selected_op:
            messagebox.showwarning("Brak operacji", "Wybierz operację z listy.", parent=self)
            return

        try:
            if selected_op == "zmień układ współrzędnych":
                epsg_str = simpledialog.askstring(
                    "Układ współrzędnych (EPSG)",
                    "Podaj docelowy kod EPSG (np. 4326, 2180):",
                    parent=self
                )
                if not epsg_str:
                    return
                try:
                    epsg_code = int(epsg_str)
                except ValueError:
                    messagebox.showerror("Błąd", "Kod EPSG musi być liczbą całkowitą.", parent=self)
                    return

                # inplace = True
                self.layer_obj.df.to_crs(epsg=epsg_code, inplace=True)
                self.layer_obj.crs = self.layer_obj.df.crs.to_string()
                messagebox.showinfo("Sukces", f"Zmieniono układ współrzędnych warstwy na EPSG:{epsg_code}", parent=self)
                self.callback_refresh()
                self.destroy()

            else:
                # Operacje tworzące nowy obiekt
                new_gdf = self.layer_obj.df.copy()
                
                if selected_op == "bufor":
                    dist_str = simpledialog.askstring(
                        "Bufor",
                        "Podaj odległość bufora (w jednostkach układu warstwy):",
                        parent=self
                    )
                    if dist_str is None:
                        return
                    try:
                        distance = float(dist_str)
                    except ValueError:
                        messagebox.showerror("Błąd", "Odległość musi być liczbą.", parent=self)
                        return
                    
                    new_gdf['geometry'] = new_gdf.geometry.buffer(distance)
                    func_prefix = "bufor"

                elif selected_op == "centroid":
                    new_gdf['geometry'] = new_gdf.geometry.centroid
                    func_prefix = "centroid"

                elif selected_op == "convex hull":
                    new_gdf['geometry'] = new_gdf.geometry.convex_hull
                    func_prefix = "convex_hull"

                elif selected_op == "simplify":
                    tol_str = simpledialog.askstring(
                        "Simplify",
                        "Podaj tolerancję uproszczenia (tolerance):",
                        parent=self
                    )
                    if tol_str is None:
                        return
                    try:
                        tolerance = float(tol_str)
                    except ValueError:
                        messagebox.showerror("Błąd", "Tolerancja musi być liczbą.", parent=self)
                        return

                    new_gdf['geometry'] = new_gdf.geometry.simplify(tolerance)
                    func_prefix = "simplify"

                else:
                    return

                # Tworzenie nowego obiektu VectorLayer
                new_name = f"{func_prefix}_{self.layer_obj.name}"
                new_vec = VectorLayer(
                    name=new_name,
                    crs=new_gdf.crs.to_string() if new_gdf.crs else self.layer_obj.crs,
                    geometry=new_gdf.geom_type.iloc[0] if not new_gdf.empty else "Unknown",
                    df=new_gdf
                )

                # Dodanie do aktywnych warstw
                new_id = f"{state.layer_id}"
                state.active_layers[new_id] = new_vec
                state.layer_id += 1

                messagebox.showinfo("Sukces", f"Utworzono nową warstwę: {new_name}", parent=self)
                self.callback_refresh()
                self.destroy()

        except Exception as e:
            messagebox.showerror("Błąd wykonania", f"Wystąpił błąd podczas operacji:\n{e}", parent=self)
