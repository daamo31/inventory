from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

class InventoryScreen(Screen):
    def __init__(self, **kwargs):
        super(InventoryScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        view_button = Button(text='Ver Inventario', size_hint=(1, 0.2))
        view_button.bind(on_press=self.view_inventory)
        layout.add_widget(view_button)

        add_button = Button(text='Añadir nuevo producto', size_hint=(1, 0.2))
        add_button.bind(on_press=self.add_product)
        layout.add_widget(add_button)

        add_existing_button = Button(text='Añadir Lote a Producto Existente', size_hint=(1, 0.2))
        add_existing_button.bind(on_press=self.add_existing_product_lote)
        layout.add_widget(add_existing_button)

        back_button = Button(text='Atrás', size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def view_inventory(self, instance):
        self.manager.current = 'view_inventory'

    def add_product(self, instance):
        self.manager.current = 'add_product_photo'

    def add_existing_product_lote(self, instance):
        self.manager.current = 'add_existing_product_lote'

    def go_back(self, instance):
        self.manager.current = 'main_menu'


class ViewInventoryScreen(Screen):
    def __init__(self, inventory, **kwargs):
        super(ViewInventoryScreen, self).__init__(**kwargs)
        self.inventory = inventory
        self.expanded_groups = {}  # Guarda el estado de los grupos

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Barra de búsqueda
        search_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.search_input = TextInput(hint_text='Buscar producto...', size_hint=(0.8, 1))
        search_button = Button(text='Buscar', size_hint=(0.2, 1))
        search_button.bind(on_press=self.search_product)
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_button)
        layout.add_widget(search_layout)

        # Área de scroll
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.grid_layout = GridLayout(cols=1, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)
        layout.add_widget(self.scroll_view)

        # Botón Atrás
        back_button = Button(text='Atrás', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        # Botón Guardar
        save_button = Button(text='Guardar Cambios', size_hint=(1, 0.1))
        save_button.bind(on_press=self.save_changes)
        layout.add_widget(save_button)

        self.add_widget(layout)

    def on_enter(self):
        self.display_products(self.inventory.list_products())

    def group_products_by_name(self, products):
        grouped = {}
        for product in products:
            name = product[0]  # Suponiendo que el nombre está en la posición 0
            if name not in grouped:
                grouped[name] = []
            grouped[name].append(product)
        return grouped

    def display_products(self, products):
        self.grid_layout.clear_widgets()
        grouped_products = self.group_products_by_name(products)

        for name, items in grouped_products.items():
            # Botón del encabezado (nombre del producto)
            header_button = Button(text=f"{name} ({len(items)})", size_hint_y=None, height=50)
            header_button.bind(on_press=lambda instance, n=name: self.toggle_group(n))
            self.grid_layout.add_widget(header_button)

            # Si el grupo está expandido, mostrar los productos
            if self.expanded_groups.get(name, False):
                for product in items:
                    product_layout = GridLayout(cols=8, size_hint_y=None, height=100)

                    # Imagen del producto
                    image = Image(source=product[6] if product[6] else "default_image.png", size_hint_y=None, height=100)
                    product_layout.add_widget(image)

                    # Datos del producto
                    for detail in product[:6]:
                        text_input = TextInput(text=str(detail), size_hint_y=None, height=40, multiline=False)
                        product_layout.add_widget(text_input)

                    # Botón de eliminar
                    delete_button = Button(text='Eliminar', size_hint_y=None, height=40)
                    delete_button.bind(on_press=lambda instance, lote=product[3]: self.delete_product(lote))
                    product_layout.add_widget(delete_button)

                    self.grid_layout.add_widget(product_layout)

    def toggle_group(self, name):
        self.expanded_groups[name] = not self.expanded_groups.get(name, False)
        self.display_products(self.inventory.list_products())  # Refresca la UI

    def search_product(self, instance):
        query = self.search_input.text.lower()
        filtered_products = [p for p in self.inventory.list_products() if query in p[0].lower()]
        self.display_products(filtered_products)

    def delete_product(self, lote):
        self.inventory.remove_product(lote)
        self.display_products(self.inventory.list_products())

    def go_back(self, instance):
        self.manager.current = 'main_menu'

    def save_changes(self, instance):
        for widget in self.grid_layout.children:
            if isinstance(widget, GridLayout) and len(widget.children) == 8:
                image_widget, nombre_input, proveedor_input, fecha_input, lote_input, coste_input, pvp_input, delete_button = widget.children[::-1]
                nombre = nombre_input.text.strip()
                proveedor = proveedor_input.text.strip()
                fecha_caducidad = fecha_input.text.strip()
                lote = lote_input.text.strip()
                nuevo_lote = lote_input.text.strip()  # Asegurarse de que el nuevo lote se toma del campo de entrada
                coste = float(coste_input.text.strip())
                pvp = float(pvp_input.text.strip())
                image_path = image_widget.source

                try:
                    self.inventory.update_product(image_path, nombre, proveedor, fecha_caducidad, lote, nuevo_lote, coste, pvp)
                except ValueError as e:
                    print(f"Error al guardar cambios: {e}")
        print("Cambios guardados correctamente")
