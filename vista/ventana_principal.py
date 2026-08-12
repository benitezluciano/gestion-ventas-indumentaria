import datetime
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from vista.ventana_categoria import VentanaCategorias

from servicio import producto_servicio, venta_servicio
from vista.ventana_base import VentanaBase
from vista.ventana_historial import VentanaHistorial

class VentanaPrincipal:
    def __init__(self, root):
        self.ventana = root
        self.ventana.geometry("750x800+500+50")
        self.ventana.title("Sistema de Gestión de Ventas")
        self.ventana.config(bg="#1A477A", padx=10, pady=10)
        self.ventana.resizable(False, False)
        self.crear_widgets()

    def crear_widgets(self):
        Label(self.ventana, text="Sistema de Gestión de Ventas",
              fg="white", bg="#1A477A",
              font=("sans", 16, "bold")).pack(pady=(5, 5))

        try:
            img = Image.open("Imagen/Logo.png")
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(img)
            Label(self.ventana, image=self.logo, bg="#1A477A",
                  highlightbackground="Black",
                  highlightthickness=2).place(x=1, y=5)
        except Exception:
            pass

        frame = Frame(self.ventana, bg="#1A477A")
        frame.pack(pady=(0, 10))

        botones = [
            ("Agregar producto",  self.abrir_agregar_producto,  0, 0),
            ("Ver catálogo",      self.mostrar_catalogo,        0, 1),
            ("Realizar venta",    self.abrir_realizar_venta,    1, 0),
            ("Ver historial",     self.mostrar_historial,       1, 1),
            ("Categorías", self.abrir_categorias, 0, 2),
        ]
        for texto, comando, fila, col in botones:
            Button(frame, text=texto, font="sans", width=18,
                   bg="#99999B", command=comando).grid(
                row=fila, column=col, padx=5, pady=5)

        Button(frame, text="Salir", font="sans", width=38,
               bg="#99999B", command=self.ventana.quit).grid(
            row=2, column=0, columnspan=2, pady=(10, 0))

        Label(self.ventana,
              text="Consola principal (registro de acciones):",
              bg="lightgray", anchor="w").pack(fill="x", padx=20, pady=(10, 0))

        self.consola = Text(self.ventana, bg="#d6d4d9", width=70, height=15)
        self.consola.pack(fill="x", padx=20, pady=(5, 10))
        self.consola.config(state="disabled")

        self.log("Aplicación iniciada.")

    # ── CONSOLA ────────────────────────────────────────────────────────────
    def log(self, texto):
        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.consola.config(state="normal")
        self.consola.insert(END, f"[{ahora}] {texto}\n")
        self.consola.see(END)
        self.consola.config(state="disabled")

    # ── CATÁLOGO ───────────────────────────────────────────────────────────
    def mostrar_catalogo(self):
        productos = producto_servicio.obtener_catalogo()
        self.log("CATÁLOGO:")
        if not productos:
            self.log("  No hay productos registrados.")
            return
        for p in productos:
            self.log(f"  [{p.id}] {p.nombre} | "
                     f"Talle: {p.talle} | Color: {p.color} | "
                     f"Precio: ${p.precio_venta} | Stock: {p.stock}")

    # ── HISTORIAL ──────────────────────────────────────────────────────────
    def mostrar_historial(self):
        VentanaHistorial(self.ventana, self.log)

    # ── AGREGAR PRODUCTO ───────────────────────────────────────────────────
    def abrir_agregar_producto(self):
        v = VentanaBase(self.ventana, "Agregar Producto")

        campos = [
            ("ID / SKU:",        "id"),
            ("Nombre:",          "nombre"),
            ("Categoría ID:",    "categoria_id"),
            ("Precio costo:",    "precio_costo"),
            ("Precio venta:",    "precio_venta"),
            ("Talle:",           "talle"),
            ("Color:",           "color"),
            ("Stock inicial:",   "stock"),
            ("Stock mínimo:",    "stock_minimo"),
        ]

        vars = {}
        for i, (label, key) in enumerate(campos):
            Label(v, text=label, fg="white", bg="#1A477A",
                  font=("sans", 10, "bold")).grid(
                row=i, column=0, pady=3, sticky="e", padx=5)
            var = StringVar()
            Entry(v, textvariable=var, bg="#d6d4d9").grid(
                row=i, column=1, pady=3)
            vars[key] = var

        msg_var = StringVar()

        def ejecutar():
            try:
                producto = producto_servicio.agregar_producto(
                    id             = vars["id"].get().strip(),
                    nombre         = vars["nombre"].get().strip(),
                    categoria_id   = int(vars["categoria_id"].get()),
                    precio_costo   = float(vars["precio_costo"].get()),
                    precio_venta   = float(vars["precio_venta"].get()),
                    talle          = vars["talle"].get().strip(),
                    color          = vars["color"].get().strip(),
                    stock          = int(vars["stock"].get()),
                    stock_minimo   = int(vars["stock_minimo"].get() or 0),
                )
                msg_var.set(f"Producto '{producto.nombre}' agregado.")
                self.log(f"PRODUCTO AGREGADO: {producto}")
            except ValueError as e:
                msg_var.set(str(e))

        Button(v, text="Agregar", font="sans", bg="#99999B",
               command=ejecutar).grid(
            row=len(campos), column=0, columnspan=2, pady=10)
        Label(v, textvariable=msg_var, fg="white",
              bg="#1A477A", wraplength=340).grid(
            row=len(campos) + 1, column=0, columnspan=2)

    # ── REALIZAR VENTA ─────────────────────────────────────────────────────
    def abrir_realizar_venta(self):
        v = VentanaBase(self.ventana, "Realizar Venta")
        v.geometry("420x320+100+20")

        Label(v, text="ID Producto:", fg="white", bg="#1A477A",
              font=("sans", 10, "bold")).grid(
            row=0, column=0, pady=5, sticky="e", padx=5)
        Label(v, text="Cantidad:", fg="white", bg="#1A477A",
              font=("sans", 10, "bold")).grid(
            row=1, column=0, pady=5, sticky="e", padx=5)

        id_var       = StringVar()
        cantidad_var = StringVar()
        msg_var      = StringVar()

        Entry(v, textvariable=id_var,       bg="#d6d4d9").grid(row=0, column=1)
        Entry(v, textvariable=cantidad_var, bg="#d6d4d9").grid(row=1, column=1)

        def ejecutar():
            try:
                id_p     = id_var.get().strip()
                cantidad = int(cantidad_var.get())
                venta_id, total = venta_servicio.realizar_venta(
                    [(id_p, cantidad)]
                )
                msg_var.set(f"Venta #{venta_id} registrada. Total: ${total}")
                self.log(f"VENTA #{venta_id} | Producto: {id_p} | "
                         f"Cantidad: {cantidad} | Total: ${total}")
            except ValueError as e:
                msg_var.set(str(e))


        Button(v, text="Confirmar venta", font="sans", bg="#99999B",
               command=ejecutar).grid(
            row=2, column=0, columnspan=2, pady=10)
        Label(v, textvariable=msg_var, fg="white",
              bg="#1A477A", wraplength=360).grid(
            row=3, column=0, columnspan=2, padx=10)
    def abrir_categorias(self):
            VentanaCategorias(self.ventana, self.log)