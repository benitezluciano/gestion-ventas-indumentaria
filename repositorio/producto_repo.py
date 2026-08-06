from repositorio.database import get_connection
from modelo.producto import Producto

def guardar(producto: Producto):
    conn = get_connection()
    conn.execute("""
        INSERT INTO productos
        (id, nombre, categoria_id, precio_costo, precio_venta,
         talle, color, stock, stock_minimo, activo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (producto.id, producto.nombre, producto.categoria_id,
          producto.precio_costo, producto.precio_venta,
          producto.talle, producto.color, producto.stock,
          producto.stock_minimo, producto.activo))
    conn.commit()
    conn.close()

def obtener_todos():
    conn = get_connection()
    filas = conn.execute(
        "SELECT * FROM productos WHERE activo = 1"
    ).fetchall()
    conn.close()
    return [Producto(**dict(f)) for f in filas]

def obtener_por_id(id: str):
    conn = get_connection()
    fila = conn.execute(
        "SELECT * FROM productos WHERE id = ?", (id,)
    ).fetchone()
    conn.close()
    return Producto(**dict(fila)) if fila else None

def actualizar_stock(id: str, nuevo_stock: int):
    conn = get_connection()
    conn.execute(
        "UPDATE productos SET stock = ? WHERE id = ?", (nuevo_stock, id)
    )
    conn.commit()
    conn.close()

def desactivar(id: str):
    conn = get_connection()
    conn.execute(
        "UPDATE productos SET activo = 0 WHERE id = ?", (id,)
    )
    conn.commit()
    conn.close()