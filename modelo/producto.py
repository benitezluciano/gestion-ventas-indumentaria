class Producto:
    def __init__(self, id, nombre, categoria_id, precio_costo,
                 precio_venta, talle, color, stock, stock_minimo=0, activo=1):
        self.id = id
        self.nombre = nombre
        self.categoria_id = categoria_id
        self.precio_costo = precio_costo
        self.precio_venta = precio_venta
        self.talle = talle
        self.color = color
        self.stock = stock
        self.stock_minimo = stock_minimo
        self.activo = activo

    def __repr__(self):
        return f"Producto({self.id} | {self.nombre} | Talle {self.talle} | Stock: {self.stock})"