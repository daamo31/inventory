from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from camera import CameraWidget
import logging
import os

# Configuración de logging
log_path = os.path.join(os.path.dirname(__file__), '..', 'app.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()]
)

class AddProductPhotoScreen(Screen):
    def __init__(self, **kwargs):
        super(AddProductPhotoScreen, self).__init__(**kwargs)
        self.captured_image_path = None
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.info_label = Label(text='Capturar Foto del Producto:', size_hint=(1, 0.05), font_size='16sp')
        layout.add_widget(self.info_label)

        # La cámara ocupa casi toda la pantalla (más del 80%)
        self.camera_widget = CameraWidget(size_hint=(1, 0.9))
        layout.add_widget(self.camera_widget)

        # Botones en una fila pequeña abajo, alineados: Atrás (izq), Capturar (centro), Siguiente (der)
        from kivy.uix.widget import Widget
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), spacing=10)

        # Botón Salir alineado a la izquierda
        salir_button = MDButton(
            MDButtonText(text='Salir'),
            size_hint=(None, 1),
            width=90
        )
        salir_button.bind(on_press=self.go_exit)
        button_layout.add_widget(salir_button)

        # Espaciador flexible
        button_layout.add_widget(Widget())

        # Botón Capturar centrado
        capture_button = MDButton(
            MDButtonText(text='Capturar'),
            size_hint=(None, 1),
            width=140
        )
        capture_button.bind(on_press=self.capture_image)
        button_layout.add_widget(capture_button)

        # Espaciador flexible
        button_layout.add_widget(Widget())

        # Botón Siguiente alineado a la derecha
        next_button = MDButton(
            MDButtonText(text='Siguiente'),
            size_hint=(None, 1),
            width=120
        )
        next_button.bind(on_press=self.go_to_next)
        button_layout.add_widget(next_button)

        # Botón Atrás alineado a la derecha
        back_button = MDButton(
            MDButtonText(text='Atrás'),
            size_hint=(None, 1),
            width=120
        )
        back_button.bind(on_press=self.go_back)
        button_layout.add_widget(back_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)
        logging.info('AddProductPhotoScreen inicializado correctamente')

    def on_enter(self):
        self.camera_widget.start_camera()
        self.manager.get_screen('add_product_name').clear_fields()

    def on_leave(self):
        self.camera_widget.stop_camera()

    def capture_image(self, instance):
        try:
            image_path = self.camera_widget.capture_product_image()
            if image_path:
                self.manager.get_screen('add_product_name').update_image_preview(image_path)
                self.captured_image_path = image_path
                logging.info('Imagen de producto capturada correctamente')
        except Exception as e:
            logging.error(f'Error al capturar imagen de producto: {e}')

    def go_to_next(self, instance):
        try:
            self.manager.current = 'add_product_name'
            logging.info('Navegando a pantalla de nombre de producto')
        except Exception as e:
            logging.error(f'Error al navegar a pantalla de nombre de producto: {e}')

    def go_back(self, instance):
        try:
            self.manager.current = 'inventory'
            logging.info('Volviendo a inventario desde foto producto')
        except Exception as e:
            logging.error(f'Error al volver a inventario desde foto producto: {e}')

    def go_exit(self, instance):
        try:
            self.manager.current = 'main_menu'
            logging.info('Saliendo al menú principal desde foto producto')
        except Exception as e:
            logging.error(f'Error al salir al menú principal desde foto producto: {e}')


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

       
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        # Botón Salir alineado a la izquierda
        salir_button = MDButton(
            MDButtonText(text='Salir'),
            size_hint=(None, 1),
            width=90
        )
        salir_button.bind(on_press=self.go_exit)
        button_layout.add_widget(salir_button)
        button_layout.add_widget(Widget())
        next_button = MDButton(
            MDButtonText(text='Siguiente'),
            size_hint=(None, 1),
            width=120
        )
        next_button.bind(on_press=self.go_to_next)
        button_layout.add_widget(next_button)

        # Botón Atrás alineado a la derecha
        back_button = MDButton(
            MDButtonText(text='Atrás'),
            size_hint=(None, 1),
            width=120
        )
        back_button.bind(on_press=self.go_back)
        button_layout.add_widget(back_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)
        logging.info('AddProductNameScreen inicializado correctamente')

    def update_image_preview(self, image_path):
        self.image_preview.source = image_path

    def go_to_next(self, instance):
        self.manager.get_screen('add_product_proveedor').update_info_input({
            'nombre': self.nombre_input.text.strip()
        })
        self.manager.current = 'add_product_proveedor'
        logging.info('Navegando a pantalla de proveedor de producto')

    def go_back(self, instance):
        self.manager.current = 'add_product_photo'
        logging.info('Volviendo a la pantalla de foto de producto')

    def go_exit(self, instance):
        self.manager.current = 'main_menu'
        logging.info('Saliendo al menú principal desde nombre producto')

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

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        # Botón Salir alineado a la izquierda
        salir_button = MDButton(
            MDButtonText(text='Salir'),
            size_hint=(None, 1),
            width=90
        )
        salir_button.bind(on_press=self.go_exit)
        button_layout.add_widget(salir_button)
        button_layout.add_widget(Widget())
        next_button = MDButton(
            MDButtonText(text='Siguiente'),
            size_hint=(None, 1),
            width=120
        )
        next_button.bind(on_press=self.go_to_next)
        button_layout.add_widget(next_button)

        # Botón Atrás alineado a la derecha
        back_button = MDButton(
            MDButtonText(text='Atrás'),
            size_hint=(None, 1),
            width=120
        )
        back_button.bind(on_press=self.go_back)
        button_layout.add_widget(back_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)
        logging.info('AddProductProveedorScreen inicializado correctamente')

    def go_to_next(self, instance):
        self.manager.get_screen('add_product_lote').update_info_input({
            'proveedor': self.proveedor_input.text.strip()
        })
        self.manager.current = 'add_product_lote'
        logging.info('Navegando a pantalla de lote de producto')

    def go_back(self, instance):
        self.manager.current = 'add_product_name'
        logging.info('Volviendo a la pantalla de nombre de producto')

    def go_exit(self, instance):
        self.manager.current = 'main_menu'
        logging.info('Saliendo al menú principal desde proveedor producto')

    def update_info_input(self, data):
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

        self.info_label = Label(text='Capturar Lote y Fecha de Caducidad:', size_hint=(1, 0.05), font_size='16sp')
        layout.add_widget(self.info_label)

        self.camera_widget = CameraWidget(size_hint=(1, 1))
        layout.add_widget(self.camera_widget)

        self.fecha_input = TextInput(hint_text='Fecha de Caducidad (dd/mm/yyyy)', size_hint=(1, 0.2))
        layout.add_widget(self.fecha_input)

        self.lote_input = TextInput(hint_text='Lote', size_hint=(1, 0.1))
        layout.add_widget(self.lote_input)

    
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), spacing=10)
        # Botón Salir alineado a la izquierda
        salir_button = MDButton(
            MDButtonText(text='Salir'),
            size_hint=(None, 1),
            width=90
        )
        salir_button.bind(on_press=self.go_exit)
        button_layout.add_widget(salir_button)
        button_layout.add_widget(Widget())
        capture_button = MDButton(
            MDButtonText(text='Capturar Lote'),
            size_hint=(None, 1),
            width=90
        )
        capture_button.bind(on_press=self.capture_lote_image)
        button_layout.add_widget(capture_button)
        button_layout.add_widget(Widget())
        next_button = MDButton(
            MDButtonText(text='Siguiente'),
            size_hint=(None, 1),
            width=90
        )
        next_button.bind(on_press=self.go_to_next)
        button_layout.add_widget(next_button)

        # Botón Atrás alineado a la derecha
        back_button = MDButton(
            MDButtonText(text='Atrás'),
            size_hint=(None, 1),
            width=90
        )
        back_button.bind(on_press=self.go_back)
        button_layout.add_widget(back_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)
        logging.info('AddProductLoteScreen inicializado correctamente')

    def on_enter(self):
        self.camera_widget.start_camera()
        self.manager.get_screen('add_product_price').clear_fields()

    def on_leave(self):
        self.camera_widget.stop_camera()

    def capture_lote_image(self, instance):
        image_path = self.camera_widget.capture()
        if image_path:
            data = {
                'fecha_caducidad': self.camera_widget.info_label.text.split(',')[0].strip() if len(self.camera_widget.info_label.text.split(',')) > 1 else '',
                'lote': self.camera_widget.info_label.text.split(',')[1].strip() if len(self.camera_widget.info_label.text.split(',')) > 1 else ''
            }
            self.update_info_input(data)
            logging.info('Imagen de lote capturada correctamente')

    def go_to_next(self, instance):
        fecha_caducidad = self.fecha_input.text.strip() or self.camera_widget.info_label.text.split(',')[0].strip()
        lote = self.lote_input.text.strip() or self.camera_widget.info_label.text.split(',')[1].strip()
        data = {'fecha_caducidad': fecha_caducidad, 'lote': lote}
        self.manager.get_screen('add_product_price').update_info_input(data)
        self.manager.current = 'add_product_price'
        logging.info('Navegando a pantalla de precio de producto')

    def go_back(self, instance):
        self.manager.current = 'add_product_proveedor'
        logging.info('Volviendo a la pantalla de proveedor de producto')

    def go_exit(self, instance):
        self.manager.current = 'main_menu'
        logging.info('Saliendo al menú principal desde lote producto')

    def update_info_input(self, data):
        if data:
            self.fecha_input.text = data.get('fecha_caducidad', '')
            self.lote_input.text = data.get('lote', '')
            self.camera_widget.info_label.text = f"{data.get('fecha_caducidad', '')}, {data.get('lote', '')}"


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

        
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        # Botón Salir alineado a la izquierda
        salir_button = MDButton(
            MDButtonText(text='Salir'),
            size_hint=(None, 1),
            width=90
        )
        salir_button.bind(on_press=self.go_exit)
        button_layout.add_widget(salir_button)
        button_layout.add_widget(Widget())
        save_button = MDButton(
            MDButtonText(text='Guardar'),
            size_hint=(None, 1),
            width=120
        )
        save_button.bind(on_press=self.save_product)
        button_layout.add_widget(save_button)

        # Botón Atrás alineado a la derecha
        back_button = MDButton(
            MDButtonText(text='Atrás'),
            size_hint=(None, 1),
            width=120
        )
        back_button.bind(on_press=self.go_back)
        button_layout.add_widget(back_button)
        layout.add_widget(button_layout)

        self.add_widget(layout)
        logging.info('AddProductPriceScreen inicializado correctamente')

    def save_product(self, instance):
        nombre = self.manager.get_screen('add_product_name').nombre_input.text.strip()
        proveedor = self.manager.get_screen('add_product_proveedor').proveedor_input.text.strip()
        fecha_caducidad = self.manager.get_screen('add_product_lote').fecha_input.text.strip() or self.manager.get_screen('add_product_lote').camera_widget.info_label.text.split(',')[0].strip()
        lote = self.manager.get_screen('add_product_lote').lote_input.text.strip() or self.manager.get_screen('add_product_lote').camera_widget.info_label.text.split(',')[1].strip()
        coste = self.coste_input.text.strip().replace(',', '.')
        pvp = self.pvp_input.text.strip().replace(',', '.')
        image_path = self.manager.get_screen('add_product_photo').captured_image_path

        if image_path and nombre and proveedor and fecha_caducidad and lote and coste and pvp:
            self.manager.inventory.add_product(image_path, nombre, proveedor, fecha_caducidad, lote, float(coste), float(pvp))
            self.info_label.text = 'Producto añadido'
            self.manager.current = 'inventory'
            logging.info('Producto guardado correctamente')
        else:
            self.info_label.text = 'Todos los campos son obligatorios.'
            logging.warning('Intento de guardar producto fallido, campos incompletos')

    def go_back(self, instance):
        self.manager.current = 'add_product_lote'
        logging.info('Volviendo a la pantalla de lote de producto')

    def go_exit(self, instance):
        self.manager.current = 'main_menu'
        logging.info('Saliendo al menú principal desde precio producto')

    def update_info_input(self, data):
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

        save_button = MDButton(
            MDButtonText(text='Guardar Cambios'),
            size_hint=(1, 0.2)
        )
        save_button.bind(on_press=self.modify_product)
        layout.add_widget(save_button)

        back_button = MDButton(
            MDButtonText(text='Atrás'),
            size_hint=(1, 0.2)
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)
        logging.info('ModifyProductScreen inicializado correctamente')

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
                logging.info('Producto modificado correctamente')
            except Exception as e:
                self.info_label.text = f'Error al modificar el producto: {str(e)}'
                logging.error(f'Error al modificar el producto: {str(e)}')
        else:
            self.info_label.text = 'Todos los campos son obligatorios.'
            logging.warning('Intento de modificar producto fallido, campos incompletos')

    def go_back(self, instance):
        self.manager.current = 'inventory'
        logging.info('Volviendo a la pantalla de inventario')

class DeleteProductScreen(Screen):
    def __init__(self, **kwargs):
        super(DeleteProductScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.info_label = Label(text='Eliminar Producto:')
        layout.add_widget(self.info_label)

        self.product_spinner = Spinner(text='Seleccionar Producto', size_hint=(1, 0.1))
        layout.add_widget(self.product_spinner)

        delete_button = MDButton(
            MDButtonText(text='Eliminar'),
            size_hint=(1, 0.2)
        )
        delete_button.bind(on_press=self.delete_product)
        layout.add_widget(delete_button)

        back_button = MDButton(
            MDButtonText(text='Atrás'),
            size_hint=(1, 0.2)
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)
        logging.info('DeleteProductScreen inicializado correctamente')

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
                logging.info('Producto eliminado correctamente')
            else:
                self.info_label.text = 'Producto no encontrado'
                logging.warning('Intento de eliminar producto fallido, producto no encontrado')
        else:
            self.info_label.text = 'El campo es obligatorio.'
            logging.warning('Intento de eliminar producto fallido, campo vacío')

    def go_back(self, instance):
        self.manager.current = 'inventory'
        logging.info('Volviendo a la pantalla de inventario')


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

        self.fecha_input = TextInput(hint_text='Fecha de Caducidad (dd/mm/yyyy)', size_hint=(1, 0.2))
        layout.add_widget(self.fecha_input)

        self.lote_input = TextInput(hint_text='Lote', size_hint=(1, 0.1))
        layout.add_widget(self.lote_input)

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), spacing=10)
        # Botón Salir alineado a la izquierda
        salir_button = MDButton(
            MDButtonText(text='Salir'),
            size_hint=(None, 1),
            width=90
        )
        salir_button.bind(on_press=self.go_exit)
        button_layout.add_widget(salir_button)
        button_layout.add_widget(Widget())
        capture_button = MDButton(
            MDButtonText(text='Capturar Lote y Fecha'),
            size_hint=(None, 1),
            width=110
        )
        capture_button.bind(on_press=self.capture_lote_image)
        button_layout.add_widget(capture_button)
        button_layout.add_widget(Widget())
        save_button = MDButton(
            MDButtonText(text='Guardar'),
            size_hint=(None, 1),
            width=90
        )
        save_button.bind(on_press=self.save_product)
        button_layout.add_widget(save_button)

        # Botón Atrás alineado a la derecha
        back_button = MDButton(
            MDButtonText(text='Atrás'),
            size_hint=(None, 1),
            width=90
        )
        back_button.bind(on_press=self.go_back)
        button_layout.add_widget(back_button)
        layout.add_widget(button_layout)

        self.add_widget(layout)
        logging.info('AddExistingProductLoteScreen inicializado correctamente')

    def on_enter(self):
        products = self.inventory.list_products()
        # Mostrar solo un producto por nombre
        unique_names = {}
        for p in products:
            if p[0] not in unique_names:
                unique_names[p[0]] = p
        self.product_spinner.values = [f"{p[0]} ({p[1]})" for p in unique_names.values()]
        self.camera_widget.start_camera()

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
            logging.info('Imagen de lote y fecha capturada correctamente')

    def save_product(self, instance):
        selected_product = self.product_spinner.text
        if selected_product:
            product_name = selected_product.split(' (')[0]
            product = self.inventory.find_product(product_name)[0]
            nombre, proveedor, _, _, coste, pvp, image_path = product
            # Usar primero los campos manuales si están rellenados
            fecha_caducidad = self.fecha_input.text.strip() or self.camera_widget.info_label.text.split(',')[0].strip()
            lote = self.lote_input.text.strip() or self.camera_widget.info_label.text.split(',')[1].strip()
            try:
                if not image_path or not os.path.isfile(image_path):
                    self.product_info_label.text = f"Error: Imagen original no encontrada para este producto."
                    logging.warning('Imagen original no encontrada para el producto seleccionado')
                    return
                self.inventory.add_product(image_path, nombre, proveedor, fecha_caducidad, lote, coste, pvp)
                self.manager.current = 'inventory'
                logging.info('Producto existente agregado correctamente con nueva información de lote y fecha')
            except Exception as e:
                self.product_info_label.text = f"Error: {str(e)}"
                logging.error(f"Error al agregar producto existente con nueva información de lote y fecha: {str(e)}")

    def go_back(self, instance):
        self.manager.current = 'inventory'
        logging.info('Volviendo a la pantalla de inventario')

    def go_exit(self, instance):
        self.manager.current = 'main_menu'
        logging.info('Saliendo al menú principal desde agregar lote de producto existente')