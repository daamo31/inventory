import os
import logging
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText

# Configuración de logging
log_path = os.path.join(os.path.dirname(__file__), '..', 'app.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()]
)

class InventoryScreen(Screen):
    """Pantalla principal de gestión de inventario."""
    def __init__(self, **kwargs):
        super(InventoryScreen, self).__init__(**kwargs)
        with self.canvas.before:
            from kivy.graphics import Rectangle
            self.bg_rect = Rectangle(source='images/chuches.png', pos=self.pos, size=self.size)
            self.bind(pos=self._update_bg_rect, size=self._update_bg_rect)

        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        
        # Título como texto centrado con fondo negro
        from kivy.uix.boxlayout import BoxLayout
        title_box = BoxLayout(size_hint=(1, 0.15), padding=0)
        from kivy.uix.label import Label
        from kivy.graphics import Color, Rectangle
        title_label = Label(text="Gestión de Inventario", font_size='26sp', halign='center', valign='middle', color=(1,1,1,1))
        title_label.bind(size=title_label.setter('text_size'))
        def update_title_bg(*args):
            title_bg.pos = title_box.pos
            title_bg.size = title_box.size
        with title_box.canvas.before:
            Color(0, 0, 0, 1)
            title_bg = Rectangle(pos=title_box.pos, size=title_box.size)
        title_box.bind(pos=update_title_bg, size=update_title_bg)
        title_box.add_widget(title_label)
        layout.add_widget(title_box)

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
        logging.info('InventoryScreen inicializado correctamente')

    def _update_bg_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def view_inventory(self, instance):
        try:
            logging.info('Navegando a Ver Inventario')
            self.manager.current = 'view_inventory'
        except Exception as e:
            logging.error(f'Error al navegar a Ver Inventario: {e}')

    def add_product(self, instance):
        try:
            logging.info('Navegando a Añadir nuevo producto')
            self.manager.current = 'add_product_photo'
        except Exception as e:
            logging.error(f'Error al navegar a Añadir nuevo producto: {e}')

    def add_existing_product_lote(self, instance):
        try:
            logging.info('Navegando a Añadir Lote a Producto Existente')
            self.manager.current = 'add_existing_product_lote'
        except Exception as e:
            logging.error(f'Error al navegar a Añadir Lote a Producto Existente: {e}')

    def go_back(self, instance):
        try:
            logging.info('Volviendo al menú principal desde Inventario')
            self.manager.current = 'main_menu'
        except Exception as e:
            logging.error(f'Error al volver al menú principal: {e}')


class ViewInventoryScreen(Screen):
    """Pantalla para visualizar y editar el inventario."""
    def __init__(self, inventory, **kwargs):
        super(ViewInventoryScreen, self).__init__(**kwargs)
        with self.canvas.before:
            from kivy.graphics import Rectangle
            self.bg_rect = Rectangle(source='images/chuches.png', pos=self.pos, size=self.size)
            self.bind(pos=self._update_bg_rect, size=self._update_bg_rect)

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

        # Botones de abajo alineados: Atrás a la izquierda, Guardar Cambios a la derecha
        bottom_buttons = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=[0,0,0,0], spacing=10)
        btn_back = MDButton(
            MDButtonText(text="Atrás"),
            size_hint=(None, 1),
            width=140,
            pos_hint={"x": 0}
        )
        btn_back.bind(on_press=self.go_back)
        bottom_buttons.add_widget(btn_back)
        bottom_buttons.add_widget(Widget())
        btn_save = MDButton(
            MDButtonText(text="Guardar Cambios"),
            size_hint=(None, 1),
            width=180,
            pos_hint={"right": 1}
        )
        btn_save.bind(on_press=self.save_changes)
        bottom_buttons.add_widget(btn_save)
        layout.add_widget(bottom_buttons)

        self.add_widget(layout)
        logging.info('ViewInventoryScreen inicializado correctamente')

    def on_enter(self):
        try:
            self.display_products(self.inventory.list_products())
            logging.info('Entrando a Ver Inventario')
        except Exception as e:
            logging.error(f'Error al mostrar productos en Ver Inventario: {e}')

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
        # Ordenar alfabéticamente por nombre
        for name in sorted(grouped_products.keys()):
            items = grouped_products[name]
            header_button = MDButton(
                MDButtonText(text=f"{name} ({len(items)})"),
                size_hint_y=None, height=70
            )
            header_button.bind(on_press=lambda instance, n=name: self.toggle_group(n))
            self.grid_layout.add_widget(header_button)

            if self.expanded_groups.get(name, False):
                # Tabla de cabecera (Imagen, Nombre, Proveedor, Fecha, Lote, Coste, PVP)
                
                header_table = GridLayout(cols=7, size_hint_y=None, height=55, padding=[0,0,0,0], spacing=2)
                headers = [
                    ("Imagen", 180),
                    ("Nombre", 200),
                    ("Proveedor", 200),
                    ("Fecha", 200),
                    ("Lote", 200),
                    ("Coste", 160),
                    ("PVP", 160)
                ]
                for col, w in headers:
                    header_lbl = Label(text=col, bold=True, size_hint_y=None, height=55, size_hint_x=None, width=w, color=(0,0,0,1), font_size=22)
                    with header_lbl.canvas.before:
                        Color(1, 0.713, 0.757, 1)  # #FFB6C1
                        Rectangle(pos=header_lbl.pos, size=header_lbl.size)
                    def update_bg(instance, *args):
                        for instr in instance.canvas.before.children:
                            if isinstance(instr, Rectangle):
                                instr.pos = instance.pos
                                instr.size = instance.size
                    header_lbl.bind(pos=update_bg, size=update_bg)
                    header_table.add_widget(header_lbl)
                self.grid_layout.add_widget(header_table)
                for product in items:
                    product_layout = GridLayout(cols=8, size_hint_y=None, height=120, spacing=2)
                    # Imagen
                    image = Image(source=product[6] if product[6] else "default_image.png", size_hint_y=None, height=110, size_hint_x=None, width=180)
                    product_layout.add_widget(image)
                    # Campos editables en el orden correcto y con el mismo ancho que la cabecera
                    nombre_input = TextInput(text=str(product[0]), size_hint_y=None, height=70, size_hint_x=None, width=200, multiline=False, font_size=26)
                    proveedor_input = TextInput(text=str(product[1]), size_hint_y=None, height=70, size_hint_x=None, width=200, multiline=False, font_size=26)
                    fecha_input = TextInput(text=str(product[2]), size_hint_y=None, height=70, size_hint_x=None, width=200, multiline=False, font_size=26)
                    lote_input = TextInput(text=str(product[3]), size_hint_y=None, height=70, size_hint_x=None, width=200, multiline=False, font_size=26)
                    coste_input = TextInput(text=str(product[4]), size_hint_y=None, height=70, size_hint_x=None, width=160, multiline=False, font_size=26)
                    pvp_input = TextInput(text=str(product[5]), size_hint_y=None, height=70, size_hint_x=None, width=160, multiline=False, font_size=26)
                    product_layout.add_widget(nombre_input)
                    product_layout.add_widget(proveedor_input)
                    product_layout.add_widget(fecha_input)
                    product_layout.add_widget(lote_input)
                    product_layout.add_widget(coste_input)
                    product_layout.add_widget(pvp_input)
                    self.original_lotes.append(product[3])
                    delete_button = MDButton(
                        MDButtonText(text="Eliminar"),
                        size_hint_y=None, height=70, size_hint_x=None, width=180
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
        try:
            self.inventory.remove_product(lote)
            self.display_products(self.inventory.list_products())
            logging.info(f'Producto eliminado: {lote}')
        except Exception as e:
            logging.error(f'Error al eliminar producto {lote}: {e}')

    def go_back(self, instance):
        try:
            self.display_products(self.inventory.list_products())
            self.manager.current = 'main_menu'
            logging.info('Volviendo al menú principal desde Ver Inventario')
        except Exception as e:
            logging.error(f'Error al volver al menú principal desde Ver Inventario: {e}')

    def save_changes(self, instance):
        idx = 0
        try:
            for widget in reversed(self.grid_layout.children):
                if isinstance(widget, GridLayout) and len(widget.children) == 8:
                    image_widget, nombre_input, proveedor_input, fecha_input, lote_input, coste_input, pvp_input, delete_button = widget.children[::-1]
                    try:
                        self.inventory.update_product(
                            image_widget.source,
                            nombre_input.text.strip(),
                            proveedor_input.text.strip(),
                            fecha_input.text.strip(),
                            self.original_lotes[idx],
                            lote_input.text.strip(),
                            float(coste_input.text.strip()),
                            float(pvp_input.text.strip())
                        )
                        logging.info(f'Producto actualizado: {nombre_input.text.strip()} (lote original: {self.original_lotes[idx]})')
                    except ValueError as e:
                        logging.warning(f'Error de valor al guardar cambios: {e}')
                    idx += 1
            logging.info('Cambios guardados correctamente en inventario')
        except Exception as e:
            logging.critical(f'Error crítico al guardar cambios en inventario: {e}')

    def _update_bg_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

        # Fondo de inventario: imagen chuches.png con opacidad baja
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(1, 1, 1, 0.5)  # Opacidad 0.5 sobre la imagen
            self.bg_img = Rectangle(source='images/chuches.png', pos=self.pos, size=self.size)
            self.bind(pos=self._update_bg_img, size=self._update_bg_img)
    def _update_bg_img(self, *args):
        self.bg_img.pos = self.pos
        self.bg_img.size = self.size