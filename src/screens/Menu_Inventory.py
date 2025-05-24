from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivy.uix.label import Label
from kivy.uix.widget import Widget

class InventoryScreen(Screen):
    def __init__(self, **kwargs):
        super(InventoryScreen, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        
        # Título como texto centrado
        title_label = Label(text="Gestión de Inventario", font_size='26sp', size_hint=(1, 0.15), halign='center', valign='middle')
        title_label.bind(size=title_label.setter('text_size'))
        layout.add_widget(title_label)

        # Contenedor centrado para los botones principales
        center_box = MDBoxLayout(orientation='vertical', spacing=50, size_hint=(1, 0.7), padding=[0,60,0,60])
        center_box.add_widget(Widget(size_hint_y=0.2))  # Espaciador superior
        buttons_info = [
            ("Ver Inventario", self.view_inventory),
            ("Añadir nuevo producto", self.add_product),
            ("Añadir Lote a Producto Existente", self.add_existing_product_lote)
        ]
        for text, callback in buttons_info:
            btn = MDButton(
                MDButtonText(text=text),
                size_hint=(0.7, None),
                height=80,
                pos_hint={"center_x": 0.5}
            )
            btn.bind(on_press=callback)
            center_box.add_widget(btn)
        center_box.add_widget(Widget(size_hint_y=0.2))  # Espaciador inferior
        layout.add_widget(center_box)

        # Botón 'Atrás' abajo a la izquierda
        bottom_box = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        btn_back = MDButton(
            MDButtonText(text="Atrás"),
            size_hint=(None, 1),
            width=120,
            pos_hint={"x": 0}
        )
        btn_back.bind(on_press=self.go_back)
        bottom_box.add_widget(btn_back)
        bottom_box.add_widget(Widget())
        layout.add_widget(bottom_box)

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
        self.expanded_groups = {}
        self.original_lotes = []  # Lista para guardar los lotes originales

        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        search_layout = MDBoxLayout(size_hint=(1, 0.1), spacing=10)
        self.search_input = TextInput(hint_text='Buscar producto...', size_hint=(0.8, 1))
        search_button = MDButton(
            MDButtonText(text="Buscar"),
            size_hint=(0.2, 1)
        )
        search_button.bind(on_press=self.search_product)
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_button)
        layout.add_widget(search_layout)

        self.scroll_view = ScrollView(size_hint=(1, 0.7))
        self.grid_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)
        layout.add_widget(self.scroll_view)

        # Botones de abajo
        btn_back = MDButton(
            MDButtonText(text="Atrás"),
            size_hint=(1, 0.1)
        )
        btn_back.bind(on_press=self.go_back)

        btn_save = MDButton(
            MDButtonText(text="Guardar Cambios"),
            size_hint=(1, 0.1)
        )
        btn_save.bind(on_press=self.save_changes)

        layout.add_widget(btn_back)
        layout.add_widget(btn_save)

        self.add_widget(layout)

    def on_enter(self):
        self.display_products(self.inventory.list_products())

    def group_products_by_name(self, products):
        grouped = {}
        for product in products:
            name = product[0]
            if name not in grouped:
                grouped[name] = []
            grouped[name].append(product)
        return grouped

    def display_products(self, products):
        self.grid_layout.clear_widgets()
        self.original_lotes = []  # Limpiar la lista cada vez que se muestran productos
        grouped_products = self.group_products_by_name(products)

        for name, items in grouped_products.items():
            header_button = MDButton(
                MDButtonText(text=f"{name} ({len(items)})"),
                size_hint_y=None, height=50
            )
            header_button.bind(on_press=lambda instance, n=name: self.toggle_group(n))
            self.grid_layout.add_widget(header_button)

            if self.expanded_groups.get(name, False):
                for product in items:
                    product_layout = GridLayout(cols=8, size_hint_y=None, height=100)

                    image = Image(source=product[6] if product[6] else "default_image.png", size_hint_y=None, height=100)
                    product_layout.add_widget(image)

                    for detail in product[:6]:
                        text_input = TextInput(text=str(detail), size_hint_y=None, height=40, multiline=False)
                        product_layout.add_widget(text_input)
                    # Guardar el lote original (posición 3 de product)
                    self.original_lotes.append(product[3])

                    delete_button = MDButton(
                        MDButtonText(text="Eliminar"),
                        size_hint_y=None, height=40
                    )
                    delete_button.bind(on_press=lambda instance, lote=product[3]: self.delete_product(lote))
                    product_layout.add_widget(delete_button)

                    self.grid_layout.add_widget(product_layout)

    def toggle_group(self, name):
        self.expanded_groups[name] = not self.expanded_groups.get(name, False)
        self.display_products(self.inventory.list_products())

    def search_product(self, instance):
        query = self.search_input.text.lower()
        filtered_products = [p for p in self.inventory.list_products() if query in p[0].lower()]
        self.display_products(filtered_products)

    def delete_product(self, lote):
        self.inventory.remove_product(lote)
        self.display_products(self.inventory.list_products())

    def go_back(self, instance):
        # Al volver, recargar productos actualizados desde la base de datos
        self.display_products(self.inventory.list_products())
        self.manager.current = 'main_menu'

    def save_changes(self, instance):
        idx = 0
        for widget in reversed(self.grid_layout.children):
            if isinstance(widget, GridLayout) and len(widget.children) == 8:
                image_widget, nombre_input, proveedor_input, fecha_input, lote_input, coste_input, pvp_input, delete_button = widget.children[::-1]
                try:
                    self.inventory.update_product(
                        image_widget.source,
                        nombre_input.text.strip(),
                        proveedor_input.text.strip(),
                        fecha_input.text.strip(),
                        self.original_lotes[idx],  # Usar el lote original guardado al crear los widgets
                        lote_input.text.strip(),
                        float(coste_input.text.strip()),
                        float(pvp_input.text.strip())
                    )
                except ValueError as e:
                    print(f"Error al guardar cambios: {e}")
                idx += 1
        print("Cambios guardados correctamente")