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
            # Elimina la tabla existente si ya existe
            self.conn.execute('DROP TABLE IF EXISTS products')
            # Crea una nueva tabla sin la columna `foto`
            self.conn.execute('''
                CREATE TABLE products (
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
        # Copia la imagen al directorio de imágenes
        image_filename = os.path.basename(image_path)
        image_dest_path = os.path.join(self.images_dir, image_filename)
        shutil.copy(image_path, image_dest_path)

        with self.conn:
            self.conn.execute('''
                INSERT INTO products (nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nombre.upper(), proveedor.upper(), fecha_caducidad.upper(), lote.upper(), coste, pvp, image_dest_path))

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

    def find_product(self, lote):
        with self.conn:
            cursor = self.conn.execute('''
                SELECT nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path FROM products WHERE lote = ?
            ''', (lote.upper(),))
            return cursor.fetchone()

    def close(self):
        self.conn.close()