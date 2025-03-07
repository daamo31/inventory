from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
import pandas as pd
from datetime import datetime

class SalesScreen(Screen):
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
        finalize_button = Button(text='Finalizar Ventas', size_hint=(1, 0.1))
        finalize_button.bind(on_press=self.finalize_sales)
        layout.add_widget(finalize_button)

        # Botón de "Atrás"
        back_button = Button(text='Atrás', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        # Etiqueta para mostrar la facturación total
        self.total_label = Label(text='Total: 0', size_hint=(1, 0.1))
        layout.add_widget(self.total_label)

        self.add_widget(layout)

    def on_enter(self):
        self.display_products()

    def display_products(self):
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
        grouped = {}
        for product in products:
            name = product[0]  # Suponiendo que el nombre está en la posición 0
            if name not in grouped:
                grouped[name] = []
            grouped[name].append(product)
        return grouped

    def sell_product(self, product):
        nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path = product
        self.inventory.remove_product(lote)
        self.sales.append(product)
        self.total_sales += pvp
        self.total_label.text = f'Total: {self.total_sales}'
        self.display_products()

    def finalize_sales(self, instance):
        # Guardar las ventas y la facturación en un archivo Excel
        sales_data = [(nombre, proveedor, fecha_caducidad, lote, pvp) for nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path in self.sales]
        df = pd.DataFrame(sales_data, columns=['Nombre', 'Proveedor', 'Fecha de Caducidad', 'Lote', 'PVP'])
        fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        df['Fecha y Hora'] = fecha_hora

        # Añadir una fila para el total de facturación
        total_row = pd.DataFrame([['', '', '', 'Total', self.total_sales, '', '']], columns=df.columns)
        df = pd.concat([df, total_row], ignore_index=True)

        df.to_excel(f'sales_report_{fecha_hora}.xlsx', index=False)

        # Reiniciar las ventas
        self.sales = []
        self.total_sales = 0
        self.total_label.text = 'Total: 0'
        self.manager.current = 'main_menu'

    def go_back(self, instance):
        self.manager.current = 'main_menu'
