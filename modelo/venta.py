class DetalleVenta:
    def __init__(self, producto_id, cantidad, precio_unitario):
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = cantidad * precio_unitario


class Venta:
    def __init__(self, id=None, fecha=None, total=0,
                 descuento=0, estado="Completada", motivo_cancelacion=None):
        self.id = id
        self.fecha = fecha
        self.total = total
        self.descuento = descuento
        self.estado = estado
        self.motivo_cancelacion = motivo_cancelacion
        self.detalles = []  # lista de DetalleVenta

    def agregar_detalle(self, detalle: DetalleVenta):
        self.detalles.append(detalle)

    def calcular_total(self):
        subtotal = sum(d.subtotal for d in self.detalles)
        self.total = subtotal - self.descuento
        return self.total