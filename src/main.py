from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from camera import CameraWidget
from inventory import Inventory
from datetime import datetime
from kivymd.app import MDApp
from kivy.metrics import dp

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Añadir imagen al menú principal
        logo_image = Image(source='images/morrico.jpeg', size_hint=(1, 1))
        layout.add_widget(logo_image)

        inventory_button = Button(text='Inventario', size_hint=(1, 0.2))
        inventory_button.bind(on_press=self.go_to_inventory)
        layout.add_widget(inventory_button)

        sales_button = Button(text='Ventas', size_hint=(1, 0.2))
        sales_button.bind(on_press=self.go_to_sales)
        layout.add_widget(sales_button)

        reports_button = Button(text='Informes', size_hint=(1, 0.2))
        reports_button.bind(on_press=self.go_to_reports)
        layout.add_widget(reports_button)

        self.add_widget(layout)

    def go_to_inventory(self, instance):
        self.manager.current = 'inventory'

    def go_to_sales(self, instance):
        self.manager.current = 'sales'

    def go_to_reports(self, instance):
        self.manager.current = 'reports'


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
        self.headers = ['Foto', 'Nombre', 'Proveedor', 'Fecha', 'Lote', 'Coste', 'PVP', 'Acciones']
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        search_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.search_input = TextInput(hint_text='Buscar por nombre, proveedor, fecha de caducidad o lote', size_hint=(0.8, 1))
        search_button = Button(text='Buscar', size_hint=(0.2, 1))
        search_button.bind(on_press=self.search_product)
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_button)
        layout.add_widget(search_layout)

        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.grid_layout = GridLayout(cols=8, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)
        layout.add_widget(self.scroll_view)

        back_button = Button(text='Atrás', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        save_button = Button(text='Guardar Cambios', size_hint=(1, 0.1))
        save_button.bind(on_press=self.save_changes)
        layout.add_widget(save_button)

        self.add_widget(layout)
        self.sort_order = {
            'Nombre': True,
            'Proveedor': True,
            'Fecha': True,
            'Lote': True,
            'Coste': True,
            'PVP': True
        }

    def on_enter(self):
        self.display_products(self.inventory.list_products())

    def display_products(self, products):
        self.grid_layout.clear_widgets()
        for header in self.headers:
            self.grid_layout.add_widget(Button(text=header, size_hint_y=None, height=40, on_press=self.sort_by_column))

        for product in products:
            image = Image(source=product[6], size_hint_y=None, height=100)
            self.grid_layout.add_widget(image)
            for detail in product[:6]:
                text_input = TextInput(text=str(detail), size_hint_y=None, height=40, multiline=False)
                self.grid_layout.add_widget(text_input)
            delete_button = Button(text='Eliminar', size_hint_y=None, height=40)
            delete_button.bind(on_press=lambda instance, lote=product[3]: self.delete_product(lote))
            self.grid_layout.add_widget(delete_button)

    def sort_by_column(self, instance):
        column = instance.text
        products = self.inventory.list_products()
        if column == 'Fecha':
            products.sort(key=lambda x: datetime.strptime(x[2], "%d/%m/%Y"), reverse=not self.sort_order[column])
        elif column == 'Coste':
            products.sort(key=lambda x: x[4], reverse=not self.sort_order[column])
        elif column == 'PVP':
            products.sort(key=lambda x: x[5], reverse=not self.sort_order[column])
        else:
            products.sort(key=lambda x: x[self.headers.index(column)], reverse=not self.sort_order[column])
        self.sort_order[column] = not self.sort_order[column]
        self.display_products(products)

    def search_product(self, instance):
        query = self.search_input.text.strip().upper()
        if query:
            filtered_products = self.inventory.find_product(query)
            self.display_products(filtered_products)
        else:
            self.display_products(self.inventory.list_products())

    def save_changes(self, instance):
        children = self.grid_layout.children[:]
        children.reverse()
        for i in range(0, len(children), 8):
            image_widget = children[i]
            if isinstance(image_widget, Image):
                image_path = image_widget.source
            else:
                continue
            nombre = children[i + 1].text.strip()
            proveedor = children[i + 2].text.strip()
            fecha_caducidad = children[i + 3].text.strip()
            lote = children[i + 4].text.strip()
            coste = float(children[i + 5].text.strip())
            pvp = float(children[i + 6].text.strip())
            self.inventory.update_product(image_path, nombre, proveedor, fecha_caducidad, lote, coste, pvp)
        self.display_products(self.inventory.list_products())

    def delete_product(self, lote):
        self.inventory.remove_product(lote)
        self.display_products(self.inventory.list_products())

    def go_back(self, instance):
        self.manager.current = 'inventory'

class AddProductPhotoScreen(Screen):
    def __init__(self, **kwargs):
        super(AddProductPhotoScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.info_label = Label(text='Capturar Foto del Producto:')
        layout.add_widget(self.info_label)

        self.camera_widget = CameraWidget(size_hint=(1, 0.5))
        layout.add_widget(self.camera_widget)

        capture_button = Button(text='Capturar', size_hint=(1, 0.2))
        capture_button.bind(on_press=self.capture_image)
        layout.add_widget(capture_button)

        next_button = Button(text='Siguiente', size_hint=(1, 0.2))
        next_button.bind(on_press=self.go_to_next)
        layout.add_widget(next_button)

        back_button = Button(text='Atrás', size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_enter(self):
        self.camera_widget.start_camera()
        self.manager.get_screen('add_product_name').clear_fields()

    def on_leave(self):
        self.camera_widget.stop_camera()

    def capture_image(self, instance):
        image_path = self.camera_widget.capture()
        if image_path:
            self.manager.get_screen('add_product_name').update_image_preview(image_path)
            self.manager.get_screen('add_product_photo').captured_image_path = image_path

    def go_to_next(self, instance):
        self.manager.current = 'add_product_name'

    def go_back(self, instance):
        self.manager.current = 'inventory'


class AddProductNameScreen(Screen):
    def __init__(self, **kwargs):
        super(AddProductNameScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.info_label = Label(text='Nombre del Producto:')
        layout.add_widget(self.info_label)

        self.nombre_input = TextInput(hint_text='Nombre del producto', size_hint=(1, 0.1))
        layout.add_widget(self.nombre_input)

        self.image_preview = Image(size_hint=(1, 0.5))
        layout.add_widget(self.image_preview)

        next_button = Button(text='Siguiente', size_hint=(1, 0.2))
        next_button.bind(on_press=self.go_to_next)
        layout.add_widget(next_button)

        back_button = Button(text='Atrás', size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def update_image_preview(self, image_path):
        self.image_preview.source = image_path

    def go_to_next(self, instance):
        self.manager.get_screen('add_product_proveedor').update_info_input({
            'nombre': self.nombre_input.text.strip()
        })
        self.manager.current = 'add_product_proveedor'

    def go_back(self, instance):
        self.manager.current = 'add_product_photo'

    def clear_fields(self):
        self.nombre_input.text = ''
        self.image_preview.source = ''


class AddProductProveedorScreen(Screen):
    def __init__(self, **kwargs):
        super(AddProductProveedorScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.info_label = Label(text='Proveedor del Producto:')
        layout.add_widget(self.info_label)

        self.proveedor_input = TextInput(hint_text='Proveedor del producto', size_hint=(1, 0.1))
        layout.add_widget(self.proveedor_input)

        next_button = Button(text='Siguiente', size_hint=(1, 0.2))
        next_button.bind(on_press=self.go_to_next)
        layout.add_widget(next_button)

        back_button = Button(text='Atrás', size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_to_next(self, instance):
        self.manager.get_screen('add_product_lote').update_info_input({
            'proveedor': self.proveedor_input.text.strip()
        })
        self.manager.current = 'add_product_lote'

    def go_back(self, instance):
        self.manager.current = 'add_product_name'

    def update_info_input(self, data):
        """Actualiza los campos de entrada de información en la interfaz de usuario."""
        if data:
            if 'nombre' in data:
                self.manager.get_screen('add_product_name').nombre_input.text = data['nombre']
            if 'proveedor' in data:
                self.proveedor_input.text = data['proveedor']

    def clear_fields(self):
        self.proveedor_input.text = ''


class AddProductLoteScreen(Screen):
    def __init__(self, **kwargs):
        super(AddProductLoteScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.info_label = Label(text='Capturar Lote y Fecha de Caducidad:')
        layout.add_widget(self.info_label)

        self.camera_widget = CameraWidget(size_hint=(1, 0.5))
        layout.add_widget(self.camera_widget)

        capture_button = Button(text='Capturar Lote', size_hint=(1, 0.2))
        capture_button.bind(on_press=self.capture_lote_image)
        layout.add_widget(capture_button)

        next_button = Button(text='Siguiente', size_hint=(1, 0.2))
        next_button.bind(on_press=self.go_to_next)
        layout.add_widget(next_button)

        back_button = Button(text='Atrás', size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_enter(self):
        self.camera_widget.start_camera()
        self.manager.get_screen('add_product_price').clear_fields()

    def on_leave(self):
        self.camera_widget.stop_camera()

    def capture_lote_image(self, instance):
        image_path = self.camera_widget.capture()
        if image_path:
            self.manager.get_screen('add_product_price').update_info_input({
                'fecha_caducidad': self.camera_widget.info_label.text.split(',')[0].strip() if len(self.camera_widget.info_label.text.split(',')) > 1 else 'N/A',
                'lote': self.camera_widget.info_label.text.split(',')[1].strip() if len(self.camera_widget.info_label.text.split(',')) > 1 else 'N/A'
            })

    def go_to_next(self, instance):
        self.manager.current = 'add_product_price'

    def go_back(self, instance):
        self.manager.current = 'add_product_proveedor'

    def update_info_input(self, data):
        """Actualiza los campos de entrada de información en la interfaz de usuario."""
        if data:
            self.camera_widget.info_label.text = f"{data.get('fecha_caducidad', 'N/A')}, {data.get('lote', 'N/A')}"


class AddProductPriceScreen(Screen):
    def __init__(self, **kwargs):
        super(AddProductPriceScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.info_label = Label(text='Precio de Coste y PVP:')
        layout.add_widget(self.info_label)

        self.coste_input = TextInput(hint_text='Coste', size_hint=(1, 0.1))
        layout.add_widget(self.coste_input)

        self.pvp_input = TextInput(hint_text='PVP', size_hint=(1, 0.1))
        layout.add_widget(self.pvp_input)

        save_button = Button(text='Guardar', size_hint=(1, 0.2))
        save_button.bind(on_press=self.save_product)
        layout.add_widget(save_button)

        back_button = Button(text='Atrás', size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def save_product(self, instance):
        nombre = self.manager.get_screen('add_product_name').nombre_input.text.strip()
        proveedor = self.manager.get_screen('add_product_proveedor').proveedor_input.text.strip()
        fecha_caducidad = self.manager.get_screen('add_product_lote').camera_widget.info_label.text.split(',')[0].strip() if len(self.manager.get_screen('add_product_lote').camera_widget.info_label.text.split(',')) > 1 else 'N/A'
        lote = self.manager.get_screen('add_product_lote').camera_widget.info_label.text.split(',')[1].strip() if len(self.manager.get_screen('add_product_lote').camera_widget.info_label.text.split(',')) > 1 else 'N/A'
        coste = self.coste_input.text.strip()
        pvp = self.pvp_input.text.strip()
        image_path = self.manager.get_screen('add_product_photo').captured_image_path

        if image_path and nombre and proveedor and fecha_caducidad and lote and coste and pvp:
            self.manager.inventory.add_product(image_path, nombre, proveedor, fecha_caducidad, lote, float(coste), float(pvp))
            self.info_label.text = 'Producto añadido'
            self.manager.current = 'inventory'
        else:
            self.info_label.text = 'Todos los campos son obligatorios.'

    def go_back(self, instance):
        self.manager.current = 'add_product_lote'

    def update_info_input(self, data):
        """Actualiza los campos de entrada de información en la interfaz de usuario."""
        if data:
            if 'nombre' in data:
                self.manager.get_screen('add_product_name').nombre_input.text = data['nombre']
            if 'proveedor' in data:
                self.manager.get_screen('add_product_proveedor').proveedor_input.text = data['proveedor']
            if 'fecha_caducidad' in data and 'lote' in data:
                self.manager.get_screen('add_product_lote').camera_widget.info_label.text = f"{data['fecha_caducidad']}, {data['lote']}"

    def clear_fields(self):
        self.coste_input.text = ''
        self.pvp_input.text = ''


class ModifyProductScreen(Screen):
    def __init__(self, **kwargs):
        super(ModifyProductScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.info_label = Label(text='Modificar Producto:')
        layout.add_widget(self.info_label)

        self.product_spinner = Spinner(text='Seleccionar Producto', size_hint=(1, 0.1))
        layout.add_widget(self.product_spinner)

        self.foto_input = TextInput(hint_text='Nueva ruta de la foto', size_hint=(1, 0.1))
        layout.add_widget(self.foto_input)

        self.nombre_input = TextInput(hint_text='Nuevo nombre del producto', size_hint=(1, 0.1))
        layout.add_widget(self.nombre_input)

        self.proveedor_input = TextInput(hint_text='Nuevo proveedor', size_hint=(1, 0.1))
        layout.add_widget(self.proveedor_input)

        self.fecha_input = TextInput(hint_text='Nueva fecha de caducidad', size_hint=(1, 0.1))
        layout.add_widget(self.fecha_input)

        self.lote_input = TextInput(hint_text='Nuevo lote', size_hint=(1, 0.1))
        layout.add_widget(self.lote_input)

        self.coste_input = TextInput(hint_text='Nuevo coste', size_hint=(1, 0.1))
        layout.add_widget(self.coste_input)

        self.pvp_input = TextInput(hint_text='Nuevo PVP', size_hint=(1, 0.1))
        layout.add_widget(self.pvp_input)

        save_button = Button(text='Guardar Cambios', size_hint=(1, 0.2))
        save_button.bind(on_press=self.modify_product)
        layout.add_widget(save_button)

        back_button = Button(text='Atrás', size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_enter(self):
        products = self.manager.inventory.list_products()
        self.product_spinner.values = [f"{product[3]}" for product in products]

    def modify_product(self, instance):
        lote = self.product_spinner.text
        foto = self.foto_input.text.strip()
        nombre = self.nombre_input.text.strip()
        proveedor = self.proveedor_input.text.strip()
        fecha_caducidad = self.fecha_input.text.strip()
        nuevo_lote = self.lote_input.text.strip()
        coste = self.coste_input.text.strip()
        pvp = self.pvp_input.text.strip()

        if foto and nombre and proveedor and fecha_caducidad and nuevo_lote and coste and pvp:
            product = self.manager.inventory.find_product(lote)
            if product:
                self.manager.inventory.remove_product(lote)
                self.manager.inventory.add_product(foto, nombre, proveedor, fecha_caducidad, nuevo_lote, float(coste), float(pvp))
                self.info_label.text = 'Producto modificado'
            else:
                self.info_label.text = 'Producto no encontrado'
        else:
            self.info_label.text = 'Todos los campos son obligatorios.'

    def go_back(self, instance):
        self.manager.current = 'inventory'


class DeleteProductScreen(Screen):
    def __init__(self, **kwargs):
        super(DeleteProductScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.info_label = Label(text='Eliminar Producto:')
        layout.add_widget(self.info_label)

        self.product_spinner = Spinner(text='Seleccionar Producto', size_hint=(1, 0.1))
        layout.add_widget(self.product_spinner)

        delete_button = Button(text='Eliminar', size_hint=(1, 0.2))
        delete_button.bind(on_press=self.delete_product)
        layout.add_widget(delete_button)

        back_button = Button(text='Atrás', size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_enter(self):
        products = self.manager.inventory.list_products()
        self.product_spinner.values = [f"{product[3]}" for product in products]

    def delete_product(self, instance):
        lote = self.product_spinner.text
        if lote:
            product = self.manager.inventory.find_product(lote)
            if product:
                self.manager.inventory.remove_product(lote)
                self.info_label.text = 'Producto eliminado'
            else:
                self.info_label.text = 'Producto no encontrado'
        else:
            self.info_label.text = 'El campo es obligatorio.'

    def go_back(self, instance):
        self.manager.current = 'inventory'


class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 📸 La cámara ocupa la mayor parte de la pantalla
        self.camera_widget = CameraWidget(size_hint=(1, 5))  
        layout.add_widget(self.camera_widget)

        # 📌 Etiqueta de información (solo una vez)
        self.info_label = Label(text='Información de la etiqueta:', size_hint=(1, 0.1))
        layout.add_widget(self.info_label)

        # 📌 Campo de entrada
        self.info_input = TextInput(hint_text='Fecha de caducidad, lote', size_hint=(1, 0.1))
        layout.add_widget(self.info_input)

        # 📍 Botones alineados en la parte inferior
        button_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)

        back_button = Button(text='Atrás')
        back_button.bind(on_press=self.go_back)
        button_layout.add_widget(back_button)

        capture_button = Button(text='Capturar')
        capture_button.bind(on_press=self.capture_image)
        button_layout.add_widget(capture_button)

        save_button = Button(text='Guardar')
        save_button.bind(on_press=self.save_info)
        button_layout.add_widget(save_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def on_enter(self):
        self.camera_widget.start_camera()

    def on_leave(self):
        self.camera_widget.stop_camera()

    def capture_image(self, instance):
        image_path = self.camera_widget.capture()  # Usa el método capture() de CameraWidget

        if image_path:
            self.process_image(image_path)  # Llama a process_image DIRECTAMENTE
        else:
            self.info_label.text = "Error al capturar la imagen"

    def process_image(self, image_path):  # Elimina el argumento *args
        text, data = self.camera_widget.preprocess_and_ocr(image_path)

        if data:
            self.update_info_input(data)
            self.info_label.text = f"Datos extraídos: {data.get('fecha_caducidad', 'N/A')}, {data.get('lote', 'N/A')}"
            # No es necesario force_update aquí
        else:
            self.info_label.text = "No se pudieron extraer datos de la imagen"

    def save_info(self, instance):
        self.manager.get_screen('add_product_lote').update_info_input({
            'fecha_caducidad': self.info_input.text.split(',')[0].strip(),
            'lote': self.info_input.text.split(',')[1].strip()
        })
        self.manager.current = 'add_product_lote'

    def go_back(self, instance):
        self.manager.current = 'add_product_lote'

    def update_info_input(self, data):
        """Actualiza el campo de entrada de información en la interfaz de usuario."""
        if data:
            self.info_input.text = f"{data.get('fecha_caducidad', 'N/A')}, {data.get('lote', 'N/A')}"
        else:
            self.info_label.text = "No se pudieron extraer datos de la imagen"

class AddExistingProductLoteScreen(Screen):
    def __init__(self, inventory, **kwargs):
        super(AddExistingProductLoteScreen, self).__init__(**kwargs)
        self.inventory = inventory
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.product_spinner = Spinner(text='Seleccionar Producto', size_hint=(1, 0.1))
        self.product_spinner.bind(text=self.update_product_info)
        layout.add_widget(self.product_spinner)

        self.product_info_label = Label(text='Nombre del Producto y Proveedor', size_hint=(1, 0.1))
        layout.add_widget(self.product_info_label)

        self.camera_widget = CameraWidget(size_hint=(1, 0.5))
        layout.add_widget(self.camera_widget)

        capture_button = Button(text='Capturar Lote y Fecha', size_hint=(1, 0.2))
        capture_button.bind(on_press=self.capture_lote_image)
        layout.add_widget(capture_button)

        save_button = Button(text='Guardar', size_hint=(1, 0.2))
        save_button.bind(on_press=self.save_product)
        layout.add_widget(save_button)

        back_button = Button(text='Atrás', size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_enter(self):
        products = self.inventory.list_products()
        self.product_spinner.values = [f"{product[0]} ({product[1]})" for product in products]
        

    def on_leave(self):
        self.camera_widget.stop_camera()

    def update_product_info(self, text):
        product_name = text.split(' (')[0]
        product = self.inventory.find_product(product_name)[0]
        nombre, proveedor = product
        self.product_info_label.text = f"Nombre: {nombre}, Proveedor: {proveedor}"

    def capture_lote_image(self):
        image_path = self.camera_widget.capture()
        if image_path:
            self.captured_image_path = image_path

    def save_product(self):
        selected_product = self.product_spinner.text
        if selected_product and hasattr(self, 'captured_image_path'):
            product_name = selected_product.split(' (')[0]
            product = self.inventory.find_product(product_name)[0]
            nombre, proveedor, fecha_caducidad, lote, coste, pvp = product
            fecha_caducidad = self.camera_widget.info_label.text.split(',')[0].strip()
            lote = self.camera_widget.info_label.text.split(',')[1].strip()
            self.inventory.add_product(self.captured_image_path, nombre, proveedor, fecha_caducidad, lote, coste, pvp)
            self.manager.current = 'inventory'

    def go_back(self):
        self.manager.current = 'inventory'

class MainApp(MDApp):
    def build(self):
        self.title = 'Inventario'
        self.inventory = Inventory()

        sm = ScreenManager()
        sm.inventory = self.inventory

        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(CameraScreen(name='camera'))
        sm.add_widget(InventoryScreen(name='inventory'))
        sm.add_widget(ViewInventoryScreen(inventory=self.inventory, name='view_inventory'))
        sm.add_widget(AddProductPhotoScreen(name='add_product_photo'))
        sm.add_widget(AddProductNameScreen(name='add_product_name'))
        sm.add_widget(AddProductProveedorScreen(name='add_product_proveedor'))
        sm.add_widget(AddProductLoteScreen(name='add_product_lote'))
        sm.add_widget(AddProductPriceScreen(name='add_product_price'))
        sm.add_widget(AddExistingProductLoteScreen(inventory=self.inventory, name='add_existing_product_lote'))
        sm.add_widget(ModifyProductScreen(name='modify_product'))
        sm.add_widget(DeleteProductScreen(name='delete_product'))

        return sm

    def on_stop(self):
        self.inventory.close()

if __name__ == '__main__':
    MainApp().run()


