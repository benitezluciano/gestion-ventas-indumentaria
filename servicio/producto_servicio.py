from modelo.producto import Producto
from repositorio import producto_repo

def agregar_producto(id, nombre, categoria_id, precio_costo,
                     precio_venta, talle, color, stock, stock_minimo=0):
    if not id or not nombre:
        raise ValueError("El ID y el nombre del producto son obligatorios.")
    if precio_costo <= 0 or precio_venta <= 0:
        raise ValueError("Los precios deben ser valores positivos.")
    if stock < 0:
        raise ValueError("El stock no puede ser negativo.")
    if producto_repo.obtener_por_id(id):
        raise ValueError(f"Ya existe un producto con el ID '{id}'.")

    producto = Producto(id, nombre, categoria_id, precio_costo,
                        precio_venta, talle, color, stock, stock_minimo)
    producto_repo.guardar(producto)
    return producto

def obtener_catalogo():
    return producto_repo.obtener_todos()

def eliminar_producto(id: str):
    producto = producto_repo.obtener_por_id(id)
    if not producto:
        raise ValueError("Producto no encontrado.")
    # Baja lógica: desactiva en lugar de eliminar físicamente
    producto_repo.desactivar(id)