from repositorio.database import get_connection

def guardar(nombre: str) -> int:
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO categorias (nombre) VALUES (?)", (nombre,)
    )
    conn.commit()
    categoria_id = cursor.lastrowid
    conn.close()
    return categoria_id

def obtener_todas():
    conn = get_connection()
    filas = conn.execute(
        "SELECT * FROM categorias ORDER BY nombre"
    ).fetchall()
    conn.close()
    return [dict(f) for f in filas]

def obtener_por_id(id: int):
    conn = get_connection()
    fila = conn.execute(
        "SELECT * FROM categorias WHERE id = ?", (id,)
    ).fetchone()
    conn.close()
    return dict(fila) if fila else None

def eliminar(id: int):
    conn = get_connection()
    conn.execute(
        "DELETE FROM categorias WHERE id = ?", (id,)
    )
    conn.commit()
    conn.close()