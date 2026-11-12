from src.menu_operations.close_program import close_program
from src.create_window import create_window
from src.create_menu_option import create_menu_option
from src.layers.show_layers import show_layers

def main_window():
    window, canvas = create_window()

    create_menu_option(canvas, 465, "Zamknij program", lambda: close_program(window))
    create_menu_option(canvas, 485, "Warstwy", lambda: show_layers(window))
    window.mainloop()

if __name__ == "__main__":
    main_window()
