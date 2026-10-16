import tkinter as tk
from collections.abc import Callable

def create_menu_option(
    canvas: tk.Canvas,
    height: int,
    text: str,
    operation: Callable
):
    text_id = canvas.create_text(
        180,
        height,
        text=text,
        font=("Arial", 11, "bold"),
        fill="#FF00FF"
    )

    canvas.tag_bind(
        text_id,
        "<Button-1>",
        lambda event: operation()
    )

    canvas.tag_bind(
        text_id,
        "<Enter>",
        lambda event: canvas.itemconfig(
            text_id,
            fill="pink"
        )
    )

    canvas.tag_bind(
        text_id,
        "<Leave>",
        lambda event: canvas.itemconfig(
            text_id,
            fill="pink"
        )
    )