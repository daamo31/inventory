from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from camera import CameraWidget
from inventory import Inventory
from kivy.clock import Clock

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.info_label = Label(text='Información de la etiqueta:')
        layout.add_widget(self.info_label)

        self.info_input = TextInput(hint_text='Fecha de caducidad, lote')
        layout.add_widget(self.info_input)

        capture_button = Button(text='Capturar Imagen')
        capture_button.bind(on_press=self.go_to_camera)
        layout.add_widget(capture_button)

        save_button = Button(text='Guardar')
        save_button.bind(on_press=self.save_info)
        layout.add_widget(save_button)

        list_button = Button(text='Listar Productos')
        list_button.bind(on_press=self.list_products)
        layout.add_widget(list_button)

        self.add_widget(layout)

    def go_to_camera(self, instance):
        self.manager.current = 'camera'

    def save_info(self, instance):
        info = self.info_input.text.split(',')
        if len(info) == 2:
            fecha_caducidad, lote = info
            if fecha_caducidad.strip() and lote.strip():
                self.manager.inventory.add_product(fecha_caducidad.strip(), lote.strip())
                self.info_label.text = 'Información guardada'
            else:
                self.info_label.text = 'Todos los campos son obligatorios.'
        else:
            self.info_label.text = 'Formato incorrecto. Use: fecha, lote'

    def list_products(self, instance):
        products = self.manager.inventory.list_products()
        self.info_label.text = '\n'.join(str(product) for product in products)

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.info_label = Label(text='Información de la etiqueta:')
        layout.add_widget(self.info_label)

        self.info_input = TextInput(hint_text='Fecha de caducidad, lote')
        layout.add_widget(self.info_input)

        self.camera_widget = CameraWidget(size_hint=(1, 0.7))
        layout.add_widget(self.camera_widget)

        button_layout = BoxLayout(size_hint=(1, 0.1))
        back_button = Button(text='Atrás')
        back_button.bind(on_press=self.go_back)
        button_layout.add_widget(back_button)

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
        Clock.schedule_once(self.process_image, 2)  # Esperar 2 segundos antes de capturar la imagen

    def process_image(self, dt):
        image_path = self.camera_widget.capture_image()
        if not image_path:
            self.info_label.text = "Error al capturar la imagen"
            return

        text = self.camera_widget.extract_text(image_path)
        data = self.camera_widget.extract_data(text)

        if data:
            self.info_input.text = f"{data.get('fecha_caducidad', '')}, {data.get('lote', '')}"
            self.info_label.text = f"Datos extraídos: {data.get('fecha_caducidad', 'N/A')}, {data.get('lote', 'N/A')}"
            Clock.schedule_once(lambda dt: self.force_update(), 0)  # Forzar actualización
        else:
            self.info_label.text = "No se pudieron extraer datos de la imagen"

    def force_update(self):
        self.info_input.focus = True
        self.info_input.focus = False

    def save_info(self, instance):
        info = self.info_input.text.split(',')
        if len(info) == 2:
            fecha_caducidad, lote = info
            if fecha_caducidad.strip() and lote.strip():
                self.manager.inventory.add_product(fecha_caducidad.strip(), lote.strip())
                self.info_label.text = 'Información guardada'
            else:
                self.info_label.text = 'Todos los campos son obligatorios.'
        else:
            self.info_label.text = 'Formato incorrecto. Use: fecha, lote'

    def go_back(self, instance):
        self.manager.current = 'main_menu'

class MainApp(App):
    def build(self):
        self.title = 'Inventario'
        self.inventory = Inventory()

        sm = ScreenManager()
        sm.inventory = self.inventory

        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(CameraScreen(name='camera'))

        return sm

if __name__ == '__main__':
    MainApp().run()