import tkinter as tk
from tkinter import messagebox

class SimuladorPila:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Didáctico de Pila (Stack)")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Pila interna (máximo 6 elementos para ajuste visual)
        self.pila = []
        self.capacidad_maxima = 6

        # --- Interfaz de Usuario ---
        self.crear_widgets()

    def crear_widgets(self):
        # Título
        lbl_titulo = tk.Label(self.root, text="Simulador Didáctico de Operaciones de Pila", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=10)

        # Panel de Entrada y Operaciones Básicas
        frame_entrada = tk.Frame(self.root)
        frame_entrada.pack(pady=5)

        tk.Label(frame_entrada, text="Valor (Entero):", font=("Arial", 11)).grid(row=0, column=0, padx=5)
        self.entry_valor = tk.Entry(frame_entrada, font=("Arial", 11), width=10)
        self.entry_valor.grid(row=0, column=1, padx=5)

        btn_push = tk.Button(frame_entrada, text="PUSH", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.push)
        btn_push.grid(row=0, column=2, padx=5)

        btn_pop = tk.Button(frame_entrada, text="POP", bg="#f44336", fg="white", font=("Arial", 10, "bold"), command=self.pop)
        btn_pop.grid(row=0, column=3, padx=5)

        # Panel de Operaciones ALU (Aritméticas y Lógicas)
        frame_alu = tk.LabelFrame(self.root, text=" Operaciones ALU (Procesa los 2 últimos elementos) ", font=("Arial", 10, "bold"), padx=10, pady=10)
        frame_alu.pack(pady=10)

        btn_add = tk.Button(frame_alu, text="ADD (+)", width=8, command=lambda: self.operar_alu("ADD"))
        btn_add.grid(row=0, column=0, padx=5)

        btn_sub = tk.Button(frame_alu, text="SUB (-)", width=8, command=lambda: self.operar_alu("SUB"))
        btn_sub.grid(row=0, column=1, padx=5)

        btn_and = tk.Button(frame_alu, text="AND (&)", width=8, command=lambda: self.operar_alu("AND"))
        btn_and.grid(row=0, column=2, padx=5)

        btn_or = tk.Button(frame_alu, text="OR (|)", width=8, command=lambda: self.operar_alu("OR"))
        btn_or.grid(row=0, column=3, padx=5)

        # Canvas para la Pila Visual
        self.canvas = tk.Canvas(self.root, width=220, height=250, bg="#f0f0f0", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=10)

        # Etiqueta de Estado / Explicación Didáctica
        self.lbl_estado = tk.Label(self.root, text="Estado: Pila vacía. Ingresa un valor y presiona PUSH.", font=("Arial", 10, "italic"), fg="#333333")
        self.lbl_estado.pack(pady=5)

        self.actualizar_grafico()

    def actualizar_grafico(self):
        """Redibuja la pila visualmente en el Canvas."""
        self.canvas.delete("all")
        
        # Dibujar bordes de la estructura de la pila (LIFO)
        self.canvas.create_line(30, 20, 30, 230, width=3, fill="#333")
        self.canvas.create_line(190, 20, 190, 230, width=3, fill="#333")
        self.canvas.create_line(30, 230, 190, 230, width=3, fill="#333")

        # Dibujar los elementos guardados (de abajo hacia arriba)
        ancho_bloque = 150
        alto_bloque = 30
        x_inicio = 35
        y_base = 225

        for idx, val in enumerate(self.pila):
            y1 = y_base - (idx + 1) * alto_bloque
            y2 = y1 + alto_bloque - 2
            
            # Resaltar el elemento superior (TOP)
            color_fondo = "#2196F3" if idx == len(self.pila) - 1 else "#90CAF9"
            
            self.canvas.create_rectangle(x_inicio, y1, x_inicio + ancho_bloque, y2, fill=color_fondo, outline="black")
            
            texto = f"{val}"
            if idx == len(self.pila) - 1:
                texto += "  <-- TOP"
                
            self.canvas.create_text(x_inicio + (ancho_bloque / 2), y1 + (alto_bloque / 2), text=texto, font=("Arial", 10, "bold"))

    def push(self):
        val_str = self.entry_valor.get().strip()
        # Verificar que sea un número (incluso negativo)
        if not (val_str.isdigit() or (val_str.startswith("-") and val_str[1:].isdigit())):
            messagebox.showerror("Error de entrada", "Por favor ingresa un número entero válido.")
            return

        if len(self.pila) >= self.capacidad_maxima:
            messagebox.showwarning("Stack Overflow", "La pila está llena (máximo 6 elementos).")
            return

        val = int(val_str)
        self.pila.append(val)
        self.entry_valor.delete(0, tk.END)
        self.lbl_estado.config(text=f"Operación: PUSH({val}) realizado con éxito.")
        self.actualizar_grafico()

    def pop(self):
        if not self.pila:
            messagebox.showwarning("Stack Underflow", "La pila está vacía.")
            return

        val = self.pila.pop()
        self.lbl_estado.config(text=f"Operación: POP devolvió el valor {val}.")
        self.actualizar_grafico()

    def operar_alu(self, op):
        if len(self.pila) < 2:
            messagebox.showwarning("Error de Operación", f"La operación {op} requiere al menos 2 elementos en la pila.")
            return

        b = self.pila.pop()  # El de arriba
        a = self.pila.pop()  # El segundo arriba

        if op == "ADD":
            res = a + b
            explicacion = f"{a} + {b} = {res}"
        elif op == "SUB":
            res = a - b
            explicacion = f"{a} - {b} = {res}"
        elif op == "AND":
            res = a & b
            explicacion = f"{a} AND {b} = {res}"
        elif op == "OR":
            res = a | b
            explicacion = f"{a} OR {b} = {res}"

        self.pila.append(res)
        self.lbl_estado.config(text=f"ALU ({op}): Se extrajeron {b} y {a}. Resultado pushed: {res} ({explicacion})")
        self.actualizar_grafico()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorPila(root)
    root.mainloop()