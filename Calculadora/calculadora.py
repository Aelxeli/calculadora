import tkinter as tk
from tkinter import messagebox
import os
import sys

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CyberCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberCalc v1.0")
        self.root.geometry("350x500")
        self.root.configure(bg="#0a0a0c")
        self.root.resizable(False, False)

        # Configurar Ícone
        try:
            icon_path = resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

        # Cores Cyberpunk
        self.neon_green = "#2CFF05"
        self.dark_bg = "#0a0a0c"
        self.btn_bg = "#121214"
        self.text_color = "#e0e0e0"

        # Variáveis
        self.equation = ""
        self.display_var = tk.StringVar(value="0")

        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        # Visor
        display_frame = tk.Frame(self.root, bg=self.dark_bg, bd=0, highlightthickness=1, highlightbackground=self.neon_green)
        display_frame.pack(padx=15, pady=(25, 15), fill="both")

        self.display_label = tk.Label(
            display_frame, 
            textvariable=self.display_var, 
            font=("Consolas", 32, "bold"), 
            bg=self.dark_bg, 
            fg=self.neon_green,
            anchor="e",
            padx=15,
            pady=20
        )
        self.display_label.pack(fill="both")

        # Container de botões
        btn_frame = tk.Frame(self.root, bg=self.dark_bg)
        btn_frame.pack(padx=15, pady=10, fill="both", expand=True)

        # Configuração da grade
        for i in range(4):
            btn_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            btn_frame.grid_rowconfigure(i, weight=1)

        # Lista de botões: (texto, linha, coluna, span_coluna)
        buttons = [
            ("AC", 0, 0, 2), ("DEL", 0, 2, 1), ("/", 0, 3, 1),
            ("7", 1, 0, 1), ("8", 1, 1, 1), ("9", 1, 2, 1), ("X", 1, 3, 1),
            ("4", 2, 0, 1), ("5", 2, 1, 1), ("6", 2, 2, 1), ("-", 2, 3, 1),
            ("1", 3, 0, 1), ("2", 3, 1, 1), ("3", 3, 2, 1), ("+", 3, 3, 1),
            ("0", 4, 0, 2), (".", 4, 2, 1), ("=", 4, 3, 1)
        ]

        for (text, row, col, span) in buttons:
            self.create_button(btn_frame, text, row, col, span)

    def create_button(self, parent, text, row, col, span):
        # Botões com bordinhas sutis
        btn = tk.Button(
            parent, 
            text=text, 
            font=("Consolas", 14, "bold"),
            bg=self.btn_bg,
            fg=self.neon_green if not text.isdigit() and text != "." else self.text_color,
            activebackground=self.neon_green,
            activeforeground="black",
            bd=0,
            highlightthickness=1,
            highlightbackground="#222", # Borda sutil por padrão
            relief="flat",
            command=lambda t=text: self.on_click(t)
        )
        
        # Efeito de hover
        btn.bind("<Enter>", lambda e, b=btn: b.config(highlightbackground=self.neon_green))
        btn.bind("<Leave>", lambda e, b=btn: b.config(highlightbackground="#222"))
        
        btn.grid(row=row, column=col, columnspan=span, sticky="nsew", padx=3, pady=3)

    def on_click(self, char):
        if char == "AC":
            self.equation = ""
            self.display_var.set("0")
        elif char == "DEL":
            self.equation = self.equation[:-1]
            self.display_var.set(self.equation if self.equation else "0")
        elif char == "=":
            try:
                # Troca os símbolos visuais pelos matemáticos do Python
                calc_eq = self.equation.replace("X", "*").replace("/", "/")
                result = eval(calc_eq)
                # Formata o resultado para evitar números muito longos
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.equation = str(result)
                self.display_var.set(self.equation)
            except ZeroDivisionError:
                messagebox.showerror("Erro", "Divisão por zero não permitida.")
                self.on_click("AC")
            except Exception:
                messagebox.showerror("Erro", "Expressão inválida.")
                self.on_click("AC")
        else:
            # Prevenir múltiplos pontos decimais no mesmo número
            if char == "." and self.equation and "." in self.equation.split()[-1]:
                return
            
            # Limite de caracteres no visor
            if len(self.equation) > 15:
                return

            if self.equation == "0" and char != ".":
                self.equation = str(char)
            else:
                self.equation += str(char)
            self.display_var.set(self.equation)

    def bind_keys(self):
        # Suporte ao teclado físico
        self.root.bind("<Key>", self.key_press)

    def key_press(self, event):
        key = event.char
        if key in "0123456789.+-/":
            self.on_click(key)
        elif key in "*xX":
            self.on_click("X")
        elif event.keysym == "Return":
            self.on_click("=")
        elif event.keysym == "BackSpace":
            self.on_click("DEL")
        elif event.keysym == "Escape":
            self.on_click("AC")


if __name__ == "__main__":
    root = tk.Tk()
    app = CyberCalc(root)
    # Adicionando um pequeno rodapé de status estilo terminal
    status_bar = tk.Label(root, text="STATUS: SYSTEM READY...", bd=0, bg="#0a0a0c", fg="#444", font=("Consolas", 8), anchor="w", padx=15)
    status_bar.pack(side="bottom", fill="x")
    root.mainloop()
