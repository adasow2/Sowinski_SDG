from .vector import VectorLayer
from tkinter import filedialog, messagebox

def load_data():
    path = filedialog.askopenfilename(
        title='wybierz warstwę'
    )
    if not path:
        return None

    vector_files = ['shp', 'geojson', 'gpkg']
    if path.split('.')[-1] in vector_files:
        try:
            VectorLayer.load_vector(path)
        except Exception:
            messagebox.showwarning(
                "Błąd wczytywania",
                "Nie udało się wczytać wybranego pliku.\n"
                "Upewnij się, że jest to prawidłowy plik GIS."
            )
            return None

    else: return None