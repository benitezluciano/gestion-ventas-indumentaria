from modelo.venta import Venta, DetalleVenta
from repositorio import producto_repo, venta_repo

def realizar_venta(items: list[tuple]):
    """
    items: lista de tuplas (producto_id, cantidad)
    """
    if not items:
        raise ValueError("La venta debe incluir al menos un producto.")

    venta = Venta()

    for producto_id, cantidad in items:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        producto = producto_repo.obtener_por_id(producto_id)
        if not producto:
            raise ValueError(f"Producto '{producto_id}' no encontrado.")
        if producto.stock < cantidad:
            raise ValueError(
                f"Stock insuficiente para '{producto.nombre}'. "
                f"Disponible: {producto.stock} unidades."
            )

        detalle = DetalleVenta(producto_id, cantidad, producto.precio_venta)
        venta.agregar_detalle(detalle)

    venta.calcular_total()
    venta_id = venta_repo.guardar(venta)

    # Actualizar stock de cada producto vendido
    for producto_id, cantidad in items:
        producto = producto_repo.obtener_por_id(producto_id)
        producto_repo.actualizar_stock(producto_id, producto.stock - cantidad)

    return venta_id, venta.total

def obtener_historial():
    return venta_repo.obtener_todos()

def cancelar_venta(venta_id: int, motivo: str):
    if not motivo or not motivo.strip():
        raise ValueError("El motivo de cancelación es obligatorio.")

    # Recuperar los detalles para reintegrar stock
    conn = __import__('repositorio.database', fromlist=['get_connection']).get_connection()
    detalles = conn.execute(
        "SELECT producto_id, cantidad FROM detalle_venta WHERE venta_id = ?",
        (venta_id,)
    ).fetchall()
    conn.close()

    for detalle in detalles:
        producto = producto_repo.obtener_por_id(detalle["producto_id"])
        if producto:
            producto_repo.actualizar_stock(
                detalle["producto_id"],
                producto.stock + detalle["cantidad"]
            )

    venta_repo.cancelar(venta_id, motivo)