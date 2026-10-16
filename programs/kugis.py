from src.create_window import create_window
from src.create_menu_option import create_menu_option
from src.menu_operations.close_program import close_program

window, canvas = create_window()

create_menu_option(canvas, 465, "Zamknij program", lambda: close_program(window))

window.mainloop()