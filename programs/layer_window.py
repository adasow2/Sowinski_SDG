# layer_window.py
from src.create_window import create_window
from src.create_menu_option import create_menu_option
from src.layers.load_file import load_data
from src.layers.show_layers import show_layers

def layer_window():
    from kugis import main_window
    window, canvas = create_window()

    # Niszczymy okno warstw i wracamy do menu głównego
    create_menu_option(canvas, 465, "powrót", lambda: [window.destroy(), main_window()])
    create_menu_option(canvas, 485, "wczytaj warstwę", lambda: load_data())
    create_menu_option(canvas, 505, 'pokaż warstwy', lambda: show_layers(window))
    window.mainloop()