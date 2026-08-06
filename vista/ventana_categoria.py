from tkinter import *
from tkinter import messagebox
from vista.ventana_base import VentanaBase
from servicio import categoria_servicio


class VentanaCategorias(VentanaBase):
    def __init__(self, master, log_callback):
        super().__init__(master, "Gestión de Categorías")
        self.geometry("420x480+100+20")
        self.log = log_callback
        self.crear_widgets()
        self.actualizar_lista()

    def crear_widgets(self):
        # ── Alta ───────────────────────────────────────────────
        Label(self, text="Nueva categoría:", fg="white",
              bg="#1A477A", font=("sans", 10, "bold")).pack(
            pady=(15, 5))

        self.nombre_var = StringVar()
        Entry(self, textvariable=self.nombre_var,
              bg="#d6d4d9", width=28).pack()

        self.msg_var = StringVar()
        Label(self, textvariable=self.msg_var,
              fg="white", bg="#1A477A",
              wraplength=360).pack(pady=(5, 0))

        Button(self, text="Agregar categoría", font="sans",
               bg="#99999B", command=self.agregar).pack(pady=10)

        # ── Lista ──────────────────────────────────────────────
        Label(self, text="Categorías existentes:", fg="white",
              bg="#1A477A", font=("sans", 10, "bold")).pack(pady=(10, 5))

        frame_lista = Frame(self, bg="#1A477A")
        frame_lista.pack(fill="both", expand=True, padx=20)

        scrollbar = Scrollbar(frame_lista)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(frame_lista, bg="#d6d4d9",
                               yscrollcommand=scrollbar.set,
                               selectmode=SINGLE, width=40, height=10)
        self.listbox.pack(side=LEFT, fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        Button(self, text="Eliminar seleccionada", font="sans",
               bg="#99999B", command=self.eliminar).pack(pady=10)

    def actualizar_lista(self):
        self.listbox.delete(0, END)
        self.categorias = categoria_servicio.obtener_categorias()
        for cat in self.categorias:
            self.listbox.insert(END, f"[{cat['id']}]  {cat['nombre']}")

    def agregar(self):
        try:
            nombre = self.nombre_var.get()
            categoria_servicio.agregar_categoria(nombre)
            self.msg_var.set(f"Categoría '{nombre.strip()}' agregada.")
            self.log(f"CATEGORÍA AGREGADA: {nombre.strip()}")
            self.nombre_var.set("")
            self.actualizar_lista()
        except ValueError as e:
            self.msg_var.set(str(e))

    def eliminar(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            self.msg_var.set("Seleccioná una categoría de la lista.")
            return
        cat = self.categorias[seleccion[0]]
        confirmacion = messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar la categoría '{cat['nombre']}'?\n"
            "Esta acción no se puede deshacer."
        )
        if not confirmacion:
            return
        try:
            categoria_servicio.eliminar_categoria(cat["id"])
            self.msg_var.set(f"Categoría '{cat['nombre']}' eliminada.")
            self.log(f"CATEGORÍA ELIMINADA: {cat['nombre']}")
            self.actualizar_lista()
        except ValueError as e:
            self.msg_var.set(str(e))