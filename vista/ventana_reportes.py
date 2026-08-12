from tkinter import *
from tkinter import ttk, messagebox
from vista.ventana_base import VentanaBase
from repositorio.database import get_connection
import datetime


class VentanaReportes(VentanaBase):
    def __init__(self, master, log_callback):
        super().__init__(master, "Reportes")
        self.geometry("600x500+100+20")
        self.log = log_callback
        self.crear_widgets()

    def crear_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # ── Pestaña 1: Ventas del día ──────────────────────────
        tab_dia = Frame(notebook, bg="#1A477A")
        notebook.add(tab_dia, text="Ventas del día")
        self._tab_ventas_dia(tab_dia)

        # ── Pestaña 2: Ventas por período ──────────────────────
        tab_periodo = Frame(notebook, bg="#1A477A")
        notebook.add(tab_periodo, text="Por período")
        self._tab_ventas_periodo(tab_periodo)

        # ── Pestaña 3: Productos más vendidos ──────────────────
        tab_ranking = Frame(notebook, bg="#1A477A")
        notebook.add(tab_ranking, text="Más vendidos")
        self._tab_mas_vendidos(tab_ranking)

        # ── Pestaña 4: Valor del inventario ────────────────────
        tab_inventario = Frame(notebook, bg="#1A477A")
        notebook.add(tab_inventario, text="Inventario")
        self._tab_inventario(tab_inventario)

    # ── TAB 1: Ventas del día ───────────────────────────────────────────────
    def _tab_ventas_dia(self, parent):
        Label(parent, text="Resumen de ventas de hoy",
              fg="white", bg="#1A477A",
              font=("sans", 11, "bold")).pack(pady=(15, 10))

        self.txt_dia = Text(parent, bg="#d6d4d9", height=14, width=60)
        self.txt_dia.pack(padx=15)
        self.txt_dia.config(state="disabled")

        Button(parent, text="Actualizar", font="sans",
               bg="#99999B", command=self._cargar_ventas_dia).pack(pady=8)

        self._cargar_ventas_dia()

    def _cargar_ventas_dia(self):
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        conn = get_connection()
        filas = conn.execute("""
            SELECT v.id, v.fecha, v.total, v.estado
            FROM ventas v
            WHERE v.fecha LIKE ? AND v.estado = 'Completada'
            ORDER BY v.fecha DESC
        """, (f"{hoy}%",)).fetchall()

        total_dia = sum(f["total"] for f in filas)
        conn.close()

        self.txt_dia.config(state="normal")
        self.txt_dia.delete("1.0", END)
        self.txt_dia.insert(END, f"Fecha: {hoy}\n")
        self.txt_dia.insert(END, f"Ventas completadas: {len(filas)}\n")
        self.txt_dia.insert(END, f"Total recaudado:    ${total_dia:.2f}\n")
        self.txt_dia.insert(END, "\n─────────────────────────────────────\n\n")

        if not filas:
            self.txt_dia.insert(END, "No hay ventas registradas hoy.")
        else:
            for f in filas:
                self.txt_dia.insert(
                    END, f"  Venta #{f['id']}  |  {f['fecha']}  |  ${f['total']:.2f}\n"
                )
        self.txt_dia.config(state="disabled")
        self.log("REPORTE: ventas del día consultado.")

    # ── TAB 2: Ventas por período ───────────────────────────────────────────
    def _tab_ventas_periodo(self, parent):
        Label(parent, text="Filtrar por rango de fechas",
              fg="white", bg="#1A477A",
              font=("sans", 11, "bold")).pack(pady=(15, 5))

        frame_filtro = Frame(parent, bg="#1A477A")
        frame_filtro.pack()

        Label(frame_filtro, text="Desde (YYYY-MM-DD):",
              fg="white", bg="#1A477A").grid(row=0, column=0, padx=5, pady=5)
        self.desde_var = StringVar()
        Entry(frame_filtro, textvariable=self.desde_var,
              bg="#d6d4d9", width=14).grid(row=0, column=1)

        Label(frame_filtro, text="Hasta (YYYY-MM-DD):",
              fg="white", bg="#1A477A").grid(row=1, column=0, padx=5, pady=5)
        self.hasta_var = StringVar()
        Entry(frame_filtro, textvariable=self.hasta_var,
              bg="#d6d4d9", width=14).grid(row=1, column=1)

        self.msg_periodo = StringVar()
        Label(parent, textvariable=self.msg_periodo,
              fg="white", bg="#1A477A").pack()

        Button(parent, text="Consultar", font="sans",
               bg="#99999B",
               command=self._cargar_periodo).pack(pady=5)

        self.txt_periodo = Text(parent, bg="#d6d4d9", height=10, width=60)
        self.txt_periodo.pack(padx=15, pady=5)
        self.txt_periodo.config(state="disabled")

    def _cargar_periodo(self):
        desde = self.desde_var.get().strip()
        hasta = self.hasta_var.get().strip()

        if not desde or not hasta:
            self.msg_periodo.set("Completá ambas fechas.")
            return

        try:
            datetime.datetime.strptime(desde, "%Y-%m-%d")
            datetime.datetime.strptime(hasta, "%Y-%m-%d")
        except ValueError:
            self.msg_periodo.set("Formato incorrecto. Usá YYYY-MM-DD.")
            return

        conn = get_connection()
        filas = conn.execute("""
            SELECT id, fecha, total, estado
            FROM ventas
            WHERE fecha BETWEEN ? AND ?
            ORDER BY fecha DESC
        """, (f"{desde} 00:00:00", f"{hasta} 23:59:59")).fetchall()

        completadas = [f for f in filas if f["estado"] == "Completada"]
        total = sum(f["total"] for f in completadas)
        conn.close()

        self.txt_periodo.config(state="normal")
        self.txt_periodo.delete("1.0", END)
        self.txt_periodo.insert(END, f"Período: {desde} → {hasta}\n")
        self.txt_periodo.insert(END, f"Ventas completadas: {len(completadas)}\n")
        self.txt_periodo.insert(END, f"Total recaudado:    ${total:.2f}\n")
        self.txt_periodo.insert(END, "\n─────────────────────────────────\n\n")

        if not filas:
            self.txt_periodo.insert(END, "No hay ventas en ese período.")
        else:
            for f in filas:
                self.txt_periodo.insert(
                    END,
                    f"  #{f['id']}  |  {f['fecha']}  |  "
                    f"${f['total']:.2f}  |  {f['estado']}\n"
                )
        self.txt_periodo.config(state="disabled")
        self.msg_periodo.set("")
        self.log(f"REPORTE: período {desde} → {hasta} consultado.")

    # ── TAB 3: Productos más vendidos ───────────────────────────────────────
    def _tab_mas_vendidos(self, parent):
        Label(parent, text="Productos más vendidos",
              fg="white", bg="#1A477A",
              font=("sans", 11, "bold")).pack(pady=(15, 10))

        self.txt_ranking = Text(parent, bg="#d6d4d9", height=14, width=60)
        self.txt_ranking.pack(padx=15)
        self.txt_ranking.config(state="disabled")

        Button(parent, text="Actualizar", font="sans",
               bg="#99999B",
               command=self._cargar_ranking).pack(pady=8)

        self._cargar_ranking()

    def _cargar_ranking(self):
        conn = get_connection()
        filas = conn.execute("""
            SELECT p.nombre, p.talle, p.color,
                   SUM(dv.cantidad) as total_vendido
            FROM detalle_venta dv
            JOIN productos p ON dv.producto_id = p.id
            JOIN ventas v ON dv.venta_id = v.id
            WHERE v.estado = 'Completada'
            GROUP BY dv.producto_id
            ORDER BY total_vendido DESC
            LIMIT 10
        """).fetchall()
        conn.close()

        self.txt_ranking.config(state="normal")
        self.txt_ranking.delete("1.0", END)

        if not filas:
            self.txt_ranking.insert(END, "No hay ventas registradas aún.")
        else:
            self.txt_ranking.insert(END, f"  {'#':<4} {'Producto':<25} {'Talle':<8} {'Color':<12} {'Vendido'}\n")
            self.txt_ranking.insert(END, "  " + "─" * 58 + "\n")
            for i, f in enumerate(filas, 1):
                self.txt_ranking.insert(
                    END,
                    f"  {i:<4} {f['nombre']:<25} {str(f['talle']):<8} "
                    f"{str(f['color']):<12} {f['total_vendido']} uds.\n"
                )
        self.txt_ranking.config(state="disabled")
        self.log("REPORTE: ranking de productos consultado.")

    # ── TAB 4: Valor del inventario ─────────────────────────────────────────
    def _tab_inventario(self, parent):
        Label(parent, text="Valor del inventario actual",
              fg="white", bg="#1A477A",
              font=("sans", 11, "bold")).pack(pady=(15, 10))

        self.txt_inventario = Text(parent, bg="#d6d4d9", height=14, width=60)
        self.txt_inventario.pack(padx=15)
        self.txt_inventario.config(state="disabled")

        Button(parent, text="Actualizar", font="sans",
               bg="#99999B",
               command=self._cargar_inventario).pack(pady=8)

        self._cargar_inventario()

    def _cargar_inventario(self):
        conn = get_connection()
        filas = conn.execute("""
            SELECT p.nombre, p.talle, p.color,
                   p.stock, p.precio_costo,
                   p.stock * p.precio_costo as valor_total
            FROM productos p
            WHERE p.activo = 1
            ORDER BY valor_total DESC
        """).fetchall()
        conn.close()

        valor_total = sum(f["valor_total"] for f in filas)

        self.txt_inventario.config(state="normal")
        self.txt_inventario.delete("1.0", END)
        self.txt_inventario.insert(END, f"  Valor total del inventario: ${valor_total:.2f}\n")
        self.txt_inventario.insert(END, f"  Productos activos: {len(filas)}\n\n")
        self.txt_inventario.insert(END, "  " + "─" * 58 + "\n")

        if not filas:
            self.txt_inventario.insert(END, "No hay productos en el inventario.")
        else:
            self.txt_inventario.insert(
                END,
                f"  {'Producto':<22} {'T':<5} {'Color':<10} "
                f"{'Stock':<7} {'P.Costo':<10} {'Valor'}\n"
            )
            self.txt_inventario.insert(END, "  " + "─" * 58 + "\n")
            for f in filas:
                self.txt_inventario.insert(
                    END,
                    f"  {f['nombre']:<22} {str(f['talle']):<5} "
                    f"{str(f['color']):<10} {f['stock']:<7} "
                    f"${f['precio_costo']:<9.2f} ${f['valor_total']:.2f}\n"
                )
        self.txt_inventario.config(state="disabled")
        self.log("REPORTE: inventario consultado.")