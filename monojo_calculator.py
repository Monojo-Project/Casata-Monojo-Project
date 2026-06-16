#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox
import os

ICON_PATH = os.path.join(os.path.dirname(__file__), "monojo_naranja.png")

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__(className="monojo_calculator_main")

        self.title("Monojo Calculator")
        self.geometry("360x520")
        self.resizable(False, False)

        try:
            icon = tk.PhotoImage(file=ICON_PATH)
            self.iconphoto(False, icon)
        except:
            pass

        self.expression = ""
        self.create_widgets()

        # Activar teclado
        self.bind_all("<Key>", self.key_input)

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ========== IMAGEN (a la izquierda del resultado) ==========
        try:
            img_original = tk.PhotoImage(file=ICON_PATH)
            self.img = img_original.subsample(
                max(1, img_original.width() // 90),
                max(1, img_original.height() // 90)
            )
        except:
            self.img = None

        img_label = ttk.Label(main_frame, image=self.img if self.img else None)
        img_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="n")

        # ========== BOTÓN DE AYUDA DEBAJO DEL MONOJO ==========
        help_btn = tk.Button(
            main_frame,
            text="Controles del teclado",
            font=("Arial", 10),
            command=self.show_help
        )
        help_btn.grid(row=1, column=0, padx=5, pady=5)

        # ========== PANTALLA (a la derecha del Monojo) ==========
        self.display = tk.Label(
            main_frame,
            text="",
            font=("Arial", 28),
            anchor="e",
            relief="sunken",
            bg="white",
            width=14
        )
        self.display.grid(row=0, column=1, columnspan=5, rowspan=2,
                          padx=5, pady=5, sticky="nsew")

        # ========== BOTONERA ==========
        botones = [
            ["", "7", "8", "9", "÷"],
            ["", "4", "5", "6", "×"],
            ["", "1", "2", "3", "-"],
            ["C", ".", "0", "^", "+"]
        ]

        for i, fila in enumerate(botones, start=2):
            for j, txt in enumerate(fila):
                if txt == "":
                    continue
                tk.Button(
                    main_frame,
                    text=txt,
                    font=("Arial", 18),
                    bg="#e6e6e6",
                    activebackground="#cccccc",
                    command=lambda t=txt: self.on_button(t)
                ).grid(row=i, column=j, padx=4, pady=4, sticky="nsew")

        # "=" gigante
        eq_button = tk.Button(
            main_frame,
            text="=",
            font=("Arial", 22),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.on_button("=")
        )
        eq_button.grid(row=6, column=0, columnspan=6,
                       padx=4, pady=4, sticky="nsew")

        # Ajustes de tamaño
        for col in range(6):
            main_frame.columnconfigure(col, weight=1)
        for row in range(2, 7):
            main_frame.rowconfigure(row, weight=1)

    # ========== TECLADO ==========
    def key_input(self, event):
        key = event.keysym
        char = event.char

        # Reset si hay error
        if self.expression == "Error":
            self.expression = ""

        # 1) NÚMEROS
        if char.isdigit():
            self.on_button(char)
            return

        # 2) PUNTO
        if char == ".":
            self.on_button(".")
            return

        # 3) SUMA
        if char == "+":
            self.on_button("+")
            return

        # 4) RESTA
        if char == "-":
            self.on_button("-")
            return

        # 5) MULTIPLICAR: Shift + X
        if key == "X":
            self.on_button("×")
            return

        # 6) DIVISIÓN: Shift + punto (→ ":")
        if key == "colon":
            self.on_button("÷")
            return

        # 7) PARÉNTESIS
        if char in "()":
            self.on_button(char)
            return

        # 8) DELETE / BACKSPACE
        if key in ("BackSpace", "Delete"):
            self.expression = self.expression[:-1]
            self.update_display()
            return

        # 9) IGUAL
        if char == "=" or key == "Return":
            self.calculate()
            return

    # ========== LÓGICA ==========
    def on_button(self, char):
        if self.expression == "Error":
            self.expression = ""

        if char == "C":
            self.clear()
        elif char == "=":
            self.calculate()
        else:
            self.expression += str(char)
            self.update_display()

    def update_display(self):
        self.display.config(text=self.expression)

    def clear(self):
        self.expression = ""
        self.update_display()

    def calculate(self):
        expr = (
            self.expression
            .replace("×", "*")
            .replace("÷", "/")
            .replace("^", "**")
        )

        try:
            result = str(eval(expr))
            self.expression = result
        except:
            self.expression = "Error"

        self.update_display()

    # ========== AYUDA ==========
    def show_help(self):
        msg = (
            "➤ CONTROLES DEL TECLADO\n\n"
            "• Números → escribir normalmente\n"
            "• . → punto decimal\n"
            "• + → sumar\n"
            "• - → restar\n"
            "• Shift + X → multiplicar (×)\n"
            "• Shift + . (:) → dividir (÷)\n"
            "• Shift + 8 → (\n"
            "• Shift + 9 → )\n"
            "• Backspace / Delete → borrar último\n"
            "• = o Enter → calcular\n"
        )
        messagebox.showinfo("Controles del teclado", msg)


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
