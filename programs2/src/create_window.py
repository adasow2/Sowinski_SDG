import tkinter as tk

def create_window():
    # Utworzenie głównego okna + canvas:

    window = tk.Tk()
    window.title("KUGIS")
    window.resizable(False, False)
    canvas = tk.Canvas(
        window,
        width=1280,
        height=720,
        highlightthickness=0,
        bg="#ffffff"
    )

    canvas.pack()
    # Grafika tła:
    window.background_screen = tk.PhotoImage(
        file="src/img/ekran.png"
    )

    canvas.create_image(
        0,
        0,
        image=window.background_screen,
        anchor="nw"
    )

    # Menu:
    canvas.create_text(
        180,
        420,
        text="Wybierz operację:",
        font=("Arial", 16, "bold"),
        fill="#FF00FF"
    )

    return (window, canvas)