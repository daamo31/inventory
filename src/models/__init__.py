class Product:
    def __init__(self, fecha_caducidad, lote, precio, proveedor):
        self.fecha_caducidad = fecha_caducidad
        self.lote = lote
        self.precio = precio
        self.proveedor = proveedor

    def __repr__(self):
        return f"Product(lote={self.lote}, fecha_caducidad={self.fecha_caducidad}, precio={self.precio}, proveedor={self.proveedor})"