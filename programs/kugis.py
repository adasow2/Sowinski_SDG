from src.menu_operations.close_program import close_program
from src.create_window import create_window
from src.create_menu_option import create_menu_option
from src.layers.load_file import load_data
from src.layers.show_layers import show_layers

def main_window():
    window, canvas = create_window()

    create_menu_option(canvas, 465, "Zamknij program", lambda: close_program(window))
    # Przekazujemy okno do zamknięcia, zanim otworzymy nowe!
    create_menu_option(canvas, 485, "wczytaj warstwę", lambda: load_data())
    create_menu_option(canvas, 505, 'pokaż warstwy', lambda: show_layers(window))
    window.mainloop()

if __name__ == "__main__":
    main_window()
