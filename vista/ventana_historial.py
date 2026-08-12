from tkinter import *
from tkinter import messagebox
from vista.ventana_base import VentanaBase
from servicio import venta_servicio


class VentanaHistorial(VentanaBase):
    def __init__(self, master, log_callback):
        super().__init__(master, "Historial de Ventas")
        self.geometry("600x480+100+20")
        self.log = log_callback
        self.crear_widgets()
        self.actualizar_lista()

    def crear_widgets(self):
        Label(self, text="Historial de ventas:", fg="white",
              bg="#1A477A", font=("sans", 10, "bold")).pack(pady=(15, 5))

        frame_lista = Frame(self, bg="#1A477A")
        frame_lista.pack(fill="both", expand=True, padx=20)

        scrollbar = Scrollbar(frame_lista)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(frame_lista, bg="#d6d4d9",
                               yscrollcommand=scrollbar.set,
                               selectmode=SINGLE, width=70, height=12)
        self.listbox.pack(side=LEFT, fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        # ── Cancelación ────────────────────────────────────────
        Label(self, text="Motivo de cancelación:", fg="white",
              bg="#1A477A", font=("sans", 10, "bold")).pack(pady=(10, 5))

        self.motivo_var = StringVar()
        Entry(self, textvariable=self.motivo_var,
              bg="#d6d4d9", width=40).pack()

        self.msg_var = StringVar()
        Label(self, textvariable=self.msg_var, fg="white",
              bg="#1A477A", wraplength=500).pack(pady=(5, 0))

        Button(self, text="Cancelar venta seleccionada", font="sans",
               bg="#99999B", command=self.cancelar).pack(pady=10)

    def actualizar_lista(self):
        self.listbox.delete(0, END)
        self.ventas = venta_servicio.obtener_historial()
        for v in self.ventas:
            self.listbox.insert(
                END,
                f"#{v.id}  |  {v.fecha}  |  "
                f"${v.total:.2f}  |  {v.estado}"
            )

    def cancelar(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            self.msg_var.set("Seleccioná una venta de la lista.")
            return

        venta = self.ventas[seleccion[0]]

        if venta.estado == "Cancelada":
            self.msg_var.set("Esa venta ya está cancelada.")
            return

        motivo = self.motivo_var.get().strip()
        if not motivo:
            self.msg_var.set("Ingresá el motivo de cancelación.")
            return

        confirmacion = messagebox.askyesno(
            "Confirmar cancelación",
            f"¿Cancelar la venta #{venta.id} por ${venta.total:.2f}?\n"
            f"Motivo: {motivo}\n\n"
            "El stock de los productos será reintegrado."
        )
        if not confirmacion:
            return

        try:
            venta_servicio.cancelar_venta(venta.id, motivo)
            self.msg_var.set(f"Venta #{venta.id} cancelada correctamente.")
            self.log(f"VENTA CANCELADA: #{venta.id} | Motivo: {motivo}")
            self.motivo_var.set("")
            self.actualizar_lista()
        except ValueError as e:
            self.msg_var.set(str(e))