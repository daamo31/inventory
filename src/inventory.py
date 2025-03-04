import sqlite3
import os
import shutil

class Inventory:
    def __init__(self, db_path='inventory.db', images_dir='images'):
        self.db_path = db_path
        self.images_dir = images_dir
        os.makedirs(self.images_dir, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            # Crea una nueva tabla solo si no existe
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    proveedor TEXT NOT NULL,
                    fecha_caducidad TEXT NOT NULL,
                    lote TEXT NOT NULL UNIQUE,
                    coste REAL NOT NULL,
                    pvp REAL NOT NULL,
                    image_path TEXT
                )
            ''')

    def add_product(self, image_path, nombre, proveedor, fecha_caducidad, lote, coste, pvp):
        # Guarda la imagen con el nombre del producto
        image_filename = f"{nombre.replace(' ', '_')}.png"
        image_dest_path = os.path.join(self.images_dir, image_filename)
        shutil.copy(image_path, image_dest_path)

        with self.conn:
            self.conn.execute('''
                INSERT INTO products (nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nombre.upper(), proveedor.upper(), fecha_caducidad.upper(), lote.upper(), coste, pvp, image_dest_path))
    def update_product(self, image_path, nombre, proveedor, fecha_caducidad, lote, nuevo_lote, coste, pvp):
        # Guarda la nueva imagen si se ha proporcionado una nueva ruta
        if image_path:
            image_filename = f"{nombre.replace(' ', '_')}.png"
            image_dest_path = os.path.join(self.images_dir, image_filename)
            shutil.copy(image_path, image_dest_path)
        else:
            image_dest_path = self.find_product(lote)[0][6]  # Mantener la ruta de la imagen existente

        with self.conn:
            self.conn.execute('''
                UPDATE products
                SET nombre = ?, proveedor = ?, fecha_caducidad = ?, lote = ?, coste = ?, pvp = ?, image_path = ?
                WHERE lote = ?
            ''', (nombre.upper(), proveedor.upper(), fecha_caducidad.upper(), nuevo_lote.upper(), coste, pvp, image_dest_path, lote.upper()))

    def remove_product(self, lote):
        with self.conn:
            self.conn.execute('''
                DELETE FROM products WHERE lote = ?
            ''', (lote.upper(),))

    def list_products(self):
        with self.conn:
            cursor = self.conn.execute('''
                SELECT nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path FROM products
            ''')
            return cursor.fetchall()

    def find_product(self, search_term):
        search_term = f"%{search_term.upper()}%"
        with self.conn:
            cursor = self.conn.execute('''
                SELECT nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path FROM products
                WHERE nombre LIKE ? OR proveedor LIKE ? OR fecha_caducidad LIKE ? OR lote LIKE ?
            ''', (search_term, search_term, search_term, search_term))
            return cursor.fetchall()

    def save_to_file(self):
        # Este método no es necesario para SQLite, ya que los cambios se guardan automáticamente.
        # Sin embargo, si se requiere alguna acción adicional, se puede implementar aquí.
        pass

    def close(self):
        self.conn.close()