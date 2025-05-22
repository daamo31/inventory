import sqlite3
import os
import shutil

class Inventory:
    def __init__(self, db_path=None, images_dir=None):
        # Obtener la ruta absoluta de la carpeta donde está este archivo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = db_path or os.path.join(base_dir, 'inventory.db')
        self.images_dir = images_dir or os.path.join(base_dir, 'images')
        # Solo usar el directorio de imágenes si existe
        if not os.path.isdir(self.images_dir):
            raise FileNotFoundError(f"El directorio de imágenes '{self.images_dir}' no existe. Por favor, créalo manualmente.")
        # Solo conectar a la base de datos si existe
        if not os.path.isfile(self.db_path):
            raise FileNotFoundError(f"La base de datos '{self.db_path}' no existe. Por favor, créala manualmente.")
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
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
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_lote ON products (lote)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_nombre ON products (nombre)')

    def add_product(self, image_path, nombre, proveedor, fecha_caducidad, lote, coste, pvp):
        # Guarda la imagen con el nombre del producto
        image_filename = f"{nombre.replace(' ', '_')}.png"
        image_dest_path = os.path.join(self.images_dir, image_filename)
        shutil.copy(image_path, image_dest_path)

        try:
            with self.conn:
                self.conn.execute('''
                    INSERT INTO products (nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (nombre.upper(), proveedor.upper(), fecha_caducidad.upper(), lote.upper(), coste, pvp, image_dest_path))
        except sqlite3.IntegrityError:
            raise ValueError(f"El producto con el lote {lote} ya existe.")

    def update_product(self, image_path, nombre, proveedor, fecha_caducidad, lote, nuevo_lote, coste, pvp):
        # Verificar si el producto existe
        product = self.find_product(lote.strip().upper())
        if not product:
            raise ValueError(f"Producto con lote {lote} no encontrado")

        # Mantener la imagen existente si no se ha cambiado
        image_dest_path = product[0][6] if image_path is None else image_path

        with self.conn:
            self.conn.execute('''
                UPDATE products
                SET nombre = ?, proveedor = ?, fecha_caducidad = ?, lote = ?, coste = ?, pvp = ?, image_path = ?
                WHERE lote = ?
            ''', (nombre.upper(), proveedor.upper(), fecha_caducidad.upper(), nuevo_lote.strip().upper(), coste, pvp, image_dest_path, lote.strip().upper()))

        print(f"Producto {nombre} actualizado correctamente en la base de datos.")

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