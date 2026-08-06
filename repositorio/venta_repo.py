import datetime
from repositorio.database import get_connection
from modelo.venta import Venta, DetalleVenta

def guardar(venta: Venta) -> int:
    conn = get_connection()
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = conn.execute("""
        INSERT INTO ventas (fecha, total, descuento, estado)
        VALUES (?, ?, ?, ?)
    """, (fecha, venta.total, venta.descuento, venta.estado))

    venta_id = cursor.lastrowid

    for detalle in venta.detalles:
        conn.execute("""
            INSERT INTO detalle_venta
            (venta_id, producto_id, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
        """, (venta_id, detalle.producto_id, detalle.cantidad,
              detalle.precio_unitario, detalle.subtotal))

    conn.commit()
    conn.close()
    return venta_id

def obtener_todos():
    conn = get_connection()
    filas = conn.execute(
        "SELECT * FROM ventas ORDER BY fecha DESC"
    ).fetchall()
    conn.close()
    return [Venta(**dict(f)) for f in filas]

def cancelar(venta_id: int, motivo: str):
    conn = get_connection()
    conn.execute("""
        UPDATE ventas
        SET estado = 'Cancelada', motivo_cancelacion = ?
        WHERE id = ?
    """, (motivo, venta_id))
    conn.commit()
    conn.close()