import os
import logging
from datetime import datetime
import pandas as pd
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDButton, MDButtonText

# Configuración de logging
log_path = os.path.join(os.path.dirname(__file__), '..', 'app.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()]
)

class SalesScreen(Screen):
    """Clase que representa la pantalla de ventas."""

    def __init__(self, inventory, **kwargs):
        super(SalesScreen, self).__init__(**kwargs)
        self.inventory = inventory
        self.sales = []
        self.total_sales = 0
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Área de scroll para las imágenes de los productos
        self.scroll_view = ScrollView(size_hint=(1, 0.7))
        self.grid_layout = GridLayout(cols=3, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)
        layout.add_widget(self.scroll_view)

        # Botón para finalizar ventas
        finalize_button = MDButton(
            MDButtonText(text='Finalizar Ventas'),
            size_hint=(1, 0.1)
        )
        finalize_button.bind(on_press=self.finalize_sales)
        layout.add_widget(finalize_button)

        # Botón de "Atrás"
        back_button = MDButton(
            MDButtonText(text='Atrás'),
            size_hint=(1, 0.1)
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        # Etiqueta para mostrar la facturación total
        self.total_label = Label(text='Total: 0', size_hint=(1, 0.1))
        layout.add_widget(self.total_label)

        self.add_widget(layout)
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(1, 0.713, 0.757, 1)  # #FFB6C1
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_bg_rect, size=self._update_bg_rect)

    def _update_bg_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_enter(self):
        """Acciones a realizar al entrar en la pantalla de ventas."""
        try:
            self.display_products()
            logging.info('Entrando a Ventas')
        except Exception as e:
            logging.error(f'Error al entrar a Ventas: {e}')

    def display_products(self):
        """Mostrar los productos disponibles en el inventario."""
        self.grid_layout.clear_widgets()
        products = self.inventory.list_products()
        grouped_products = self.group_products_by_name(products)

        for name, items in grouped_products.items():
            product = items[0]  # Tomar el primer producto del grupo
            image_path = product[6] if product[6] else "default_image.png"
            product_image = Image(source=image_path, size_hint_y=None, height=200)
            product_image.bind(on_touch_down=lambda instance, touch, p=product: self.sell_product(p) if instance.collide_point(*touch.pos) else None)
            self.grid_layout.add_widget(product_image)

    def group_products_by_name(self, products):
        """Agrupar productos por nombre."""
        grouped = {}
        for product in products:
            name = product[0]  # Suponiendo que el nombre está en la posición 0
            if name not in grouped:
                grouped[name] = []
            grouped[name].append(product)
        return grouped

    def sell_product(self, product):
        """Vender un producto del inventario."""
        try:
            nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path = product
            self.inventory.remove_product(lote)
            self.sales.append(product)
            self.total_sales += pvp
            self.total_label.text = f'Total: {self.total_sales}'
            self.display_products()
            logging.info(f'Producto vendido: {nombre} (lote: {lote})')
        except Exception as e:
            logging.error(f'Error al vender producto: {e}')

    def finalize_sales(self, instance):
        """Finalizar las ventas y generar un reporte en Excel."""
        try:
            # Guardar las ventas y la facturación en un archivo Excel
            sales_data = [(nombre, proveedor, fecha_caducidad, lote, pvp) for nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path in self.sales]
            df = pd.DataFrame(sales_data, columns=['Nombre', 'Proveedor', 'Fecha de Caducidad', 'Lote', 'PVP'])
            fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            df['Fecha y Hora'] = fecha_hora

            # Añadir una fila para el total de facturación
            total_row = pd.DataFrame([['', '', '', 'Total', self.total_sales, fecha_hora]], columns=df.columns)
            df = pd.concat([df, total_row], ignore_index=True)

            # Crear la carpeta 'informes' si no existe
            informes_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'informes')
            os.makedirs(informes_dir, exist_ok=True)

            # Guardar el archivo Excel en la carpeta 'informes'
            df.to_excel(os.path.join(informes_dir, f'sales_report_{fecha_hora}.xlsx'), index=False)

            # Reiniciar las ventas
            self.sales = []
            self.total_sales = 0
            self.total_label.text = 'Total: 0'
            self.manager.current = 'main_menu'
            logging.info('Ventas finalizadas y reporte generado')
        except Exception as e:
            logging.critical(f'Error crítico al finalizar ventas: {e}')

    def go_back(self, instance):
        """Volver al menú principal."""
        try:
            self.manager.current = 'main_menu'
            logging.info('Volviendo al menú principal desde Ventas')
        except Exception as e:
            logging.error(f'Error al volver al menú principal desde Ventas: {e}')