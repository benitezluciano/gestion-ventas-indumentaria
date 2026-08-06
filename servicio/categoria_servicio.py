from repositorio import categoria_repo

def agregar_categoria(nombre: str) -> int:
    nombre = nombre.strip()
    if not nombre or len(nombre) < 2:
        raise ValueError("El nombre de la categoría debe tener al menos 2 caracteres.")
    existentes = [c["nombre"].lower() for c in categoria_repo.obtener_todas()]
    if nombre.lower() in existentes:
        raise ValueError(f"La categoría '{nombre}' ya existe.")
    return categoria_repo.guardar(nombre)

def obtener_categorias():
    return categoria_repo.obtener_todas()

def eliminar_categoria(id: int):
    from repositorio.database import get_connection
    conn = get_connection()
    tiene_productos = conn.execute(
        "SELECT COUNT(*) FROM productos WHERE categoria_id = ? AND activo = 1", (id,)
    ).fetchone()[0]
    conn.close()
    if tiene_productos > 0:
        raise ValueError("No se puede eliminar una categoría que tiene productos asociados.")
    categoria_repo.eliminar(id)