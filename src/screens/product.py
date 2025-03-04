from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from camera import CameraWidget

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
        self.product_spinner.bind(text=self.update_fields)
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

    def update_fields(self, spinner, text):
        product = self.manager.inventory.find_product(text)[0]
        nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path = product
        self.foto_input.text = image_path
        self.nombre_input.text = nombre
        self.proveedor_input.text = proveedor
        self.fecha_input.text = fecha_caducidad
        self.lote_input.text = lote
        self.coste_input.text = str(coste)
        self.pvp_input.text = str(pvp)

    def modify_product(self, instance):
        lote = self.product_spinner.text
        foto = self.foto_input.text.strip()
        nombre = self.nombre_input.text.strip()
        proveedor = self.proveedor_input.text.strip()
        fecha_caducidad = self.fecha_input.text.strip()
        nuevo_lote = self.lote_input.text.strip()
        coste = self.coste_input.text.strip()
        pvp = self.pvp_input.text.strip()

        if nombre and proveedor and fecha_caducidad and nuevo_lote and coste and pvp:
            try:
                self.manager.inventory.update_product(foto, nombre, proveedor, fecha_caducidad, lote, nuevo_lote, float(coste), float(pvp))
                self.info_label.text = 'Producto modificado'
            except Exception as e:
                self.info_label.text = f'Error al modificar el producto: {str(e)}'
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
        self.camera_widget.start_camera()  # Asegurarse de que la cámara se inicia al entrar en la pantalla

    def on_leave(self):
        self.camera_widget.stop_camera()

    def update_product_info(self, spinner, text):
        product_name = text.split(' (')[0]
        product = self.inventory.find_product(product_name)[0]
        nombre, proveedor, fecha_caducidad, lote, coste, pvp, image_path = product
        self.product_info_label.text = f"Nombre: {nombre}, Proveedor: {proveedor}"

    def capture_lote_image(self, instance):
        image_path = self.camera_widget.capture()
        if image_path:
            self.captured_image_path = image_path

    def save_product(self, instance):
        selected_product = self.product_spinner.text
        if selected_product and hasattr(self, 'captured_image_path'):
            product_name = selected_product.split(' (')[0]
            product = self.inventory.find_product(product_name)[0]
            nombre, proveedor, _, _, coste, pvp, _ = product
            fecha_caducidad = self.camera_widget.info_label.text.split(',')[0].strip()
            lote = self.camera_widget.info_label.text.split(',')[1].strip()
            self.inventory.add_product(self.captured_image_path, nombre, proveedor, fecha_caducidad, lote, coste, pvp)
            self.manager.current = 'inventory'

    def go_back(self, instance):
        self.manager.current = 'inventory'