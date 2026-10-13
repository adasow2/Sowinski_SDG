import tkinter as tk

# Definicje metod:

def close_program():
    window.destroy()


# Utworzenie głównego okna + canvas:

window = tk.Tk()
window.title("KUGIS")
window.resizable(False, False)

# Ustawienie białego tła głównego okna
window.configure(bg="#ffffff")

canvas = tk.Canvas(
    window,
    width=1280,
    height=720,
    highlightthickness=0,
    bg="#ffffff"  # Ustawienie białego tła płótna
)

canvas.pack()


# Grafika tła (musi mieć przezroczystość w miejscach, gdzie ma być widać biały kolor tła okna):
background_screen = tk.PhotoImage(file="ekran.png")

canvas.create_image(
    0,
    0,
    image=background_screen,
    anchor="nw"
)





# Menu:

canvas.create_text(
    180,
    420,
    text="Wybierz operację:",
    font=("Arial", 16, "bold"),
    fill="black"
)


# Przycisk zamknięcia:

canvas.create_text(
    180,
    465,
    text="Zamknij program",
    font=("Arial", 11, "bold"),
    fill="#FF00FF",
    tags="zamknij"
)

canvas.tag_bind(
    "zamknij",
    "<Button-1>",
    lambda event: close_program()
)

canvas.tag_bind(
    "zamknij",
    "<Enter>",
    lambda event: canvas.itemconfig(
        "zamknij",
        fill="black"
    )
)

canvas.tag_bind(
    "zamknij",
    "<Leave>",
    lambda event: canvas.itemconfig(
        "zamknij",
        fill="pink"
    )
)

# Główna pętla programu:

window.mainloop()