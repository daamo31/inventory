import os
import sqlite3
import shutil
import logging

class Inventory:
    """Clase para gestionar el inventario de productos con persistencia en base de datos SQLite y almacenamiento de imágenes."""

    def __init__(self, db_path=None, images_dir=None):
        """Inicializa la clase Inventory.

        Args:
            db_path (str): Ruta a la base de datos SQLite.
            images_dir (str): Ruta al directorio de imágenes de los productos.
        """
        # Obtener la ruta absoluta de la carpeta donde está este archivo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = db_path or os.path.join(base_dir, 'inventory.db')
        self.images_dir = images_dir or os.path.join(base_dir, 'images')
        # Solo usar el directorio de imágenes si existe
        if not os.path.isdir(self.images_dir):
            logging.error(f"El directorio de imágenes '{self.images_dir}' no existe.")
            raise FileNotFoundError(f"El directorio de imágenes '{self.images_dir}' no existe. Por favor, créalo manualmente.")
        # Solo conectar a la base de datos si existe
        if not os.path.isfile(self.db_path):
            logging.error(f"La base de datos '{self.db_path}' no existe.")
            raise FileNotFoundError(f"La base de datos '{self.db_path}' no existe. Por favor, créala manualmente.")
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()
        logging.info('Conexión a la base de datos y directorio de imágenes verificados')

    def create_table(self):
        """Crea la tabla de productos en la base de datos si no existe."""
        try:
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
            logging.info('Tabla de productos creada/verificada')
        except Exception as e:
            logging.critical(f'Error al crear/verificar la tabla de productos: {e}')

    def add_product(self, image_path, nombre, proveedor, fecha_caducidad, lote, coste, pvp):
        """Añade un producto nuevo a la base de datos y guarda su imagen.

        Args:
            image_path (str): Ruta de la imagen del producto.
            nombre (str): Nombre del producto.
            proveedor (str): Proveedor del producto.
            fecha_caducidad (str): Fecha de caducidad del producto.
            lote (str): Lote del producto.
            coste (float): Coste del producto.
            pvp (float): Precio de venta al público del producto.
        """
        # Guarda la imagen con el nombre del producto
        image_filename = f"{nombre.replace(' ', '_')}.png"
        image_dest_path = os.path.join(self.images_dir, image_filename)
        try:
            shutil.copy(image_path, image_dest_path)
            with self.conn:
                self.conn.execute('''
                    INSERT INTO products (nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (nombre.upper(), proveedor.upper(), fecha_caducidad.upper(), lote.upper(), coste, pvp, image_dest_path))
            logging.info(f'Producto añadido: {nombre} (lote: {lote})')
        except shutil.SameFileError:
            logging.warning(f'La imagen ya existe en el destino: {image_dest_path}')
        except Exception as e:
            logging.error(f'Error al añadir producto: {e}')
            if 'UNIQUE constraint failed' in str(e):
                raise ValueError(f"El producto con el lote {lote} ya existe.")
            else:
                raise

    def update_product(self, image_path, nombre, proveedor, fecha_caducidad, lote, nuevo_lote, coste, pvp):
        """Actualiza la información de un producto existente.

        Args:
            image_path (str): Nueva ruta de la imagen del producto (opcional).
            nombre (str): Nuevo nombre del producto.
            proveedor (str): Nuevo proveedor del producto.
            fecha_caducidad (str): Nueva fecha de caducidad del producto.
            lote (str): Lote actual del producto.
            nuevo_lote (str): Nuevo lote del producto.
            coste (float): Nuevo coste del producto.
            pvp (float): Nuevo precio de venta al público del producto.
        """
        try:
            product = self.find_product(lote.strip().upper())
            if not product:
                logging.warning(f"Producto con lote {lote} no encontrado para actualizar")
                raise ValueError(f"Producto con lote {lote} no encontrado")
            # Mantener la imagen existente si no se ha cambiado
            image_dest_path = product[0][6] if image_path is None else image_path
            with self.conn:
                self.conn.execute('''
                    UPDATE products
                    SET nombre = ?, proveedor = ?, fecha_caducidad = ?, lote = ?, coste = ?, pvp = ?, image_path = ?
                    WHERE lote = ?
                ''', (nombre.upper(), proveedor.upper(), fecha_caducidad.upper(), nuevo_lote.strip().upper(), coste, pvp, image_dest_path, lote.strip().upper()))
            logging.info(f"Producto actualizado: {nombre} (lote original: {lote})")
        except Exception as e:
            logging.error(f'Error al actualizar producto: {e}')
            raise

    def remove_product(self, lote):
        """Elimina un producto de la base de datos.

        Args:
            lote (str): Lote del producto a eliminar.
        """
        try:
            with self.conn:
                self.conn.execute('''
                    DELETE FROM products WHERE lote = ?
                ''', (lote.upper(),))
            logging.info(f'Producto eliminado: {lote}')
        except Exception as e:
            logging.error(f'Error al eliminar producto: {e}')
            raise

    def list_products(self):
        """Lista todos los productos en la base de datos.

        Returns:
            list: Lista de tuplas con la información de los productos.
        """
        try:
            with self.conn:
                cursor = self.conn.execute('''
                    SELECT nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path FROM products
                ''')
                productos = cursor.fetchall()
            logging.info(f'Se listaron {len(productos)} productos')
            return productos
        except Exception as e:
            logging.error(f'Error al listar productos: {e}')
            return []

    def find_product(self, search_term):
        """Busca productos en la base de datos que coincidan con el término de búsqueda.

        Args:
            search_term (str): Término de búsqueda (parte del nombre, proveedor, fecha de caducidad o lote).

        Returns:
            list: Lista de tuplas con la información de los productos que coinciden con la búsqueda.
        """
        search_term = f"%{search_term.upper()}%"
        try:
            with self.conn:
                cursor = self.conn.execute('''
                    SELECT nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path FROM products
                    WHERE nombre LIKE ? OR proveedor LIKE ? OR fecha_caducidad LIKE ? OR lote LIKE ?
                ''', (search_term, search_term, search_term, search_term))
                resultados = cursor.fetchall()
            logging.info(f'Búsqueda de producto: {search_term}, encontrados: {len(resultados)}')
            return resultados
        except Exception as e:
            logging.error(f'Error al buscar producto: {e}')
            return []

    def save_to_file(self):
        """Guarda los cambios en la base de datos en el archivo.

        Este método no es necesario para SQLite, ya que los cambios se guardan automáticamente.
        Sin embargo, si se requiere alguna acción adicional, se puede implementar aquí.
        """
        pass

    def close(self):
        """Cierra la conexión a la base de datos."""
        try:
            self.conn.close()
            logging.info('Conexión a la base de datos cerrada')
        except Exception as e:
            logging.error(f'Error al cerrar la base de datos: {e}')