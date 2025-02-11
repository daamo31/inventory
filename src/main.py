from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from camera import Camera
from inventory import Inventory

class MainApp(App):
    def build(self):
        self.title = 'Inventario de Chuches'
        layout = BoxLayout(orientation='vertical')

        self.camera = Camera()
        self.inventory = Inventory()

        self.info_label = Label(text='Información de la etiqueta:')
        layout.add_widget(self.info_label)

        self.info_input = TextInput(hint_text='Fecha de caducidad, lote, precio, proveedor')
        layout.add_widget(self.info_input)

        capture_button = Button(text='Capturar Imagen')
        capture_button.bind(on_press=self.capture_image)
        layout.add_widget(capture_button)

        save_button = Button(text='Guardar')
        save_button.bind(on_press=self.save_info)
        layout.add_widget(save_button)

        list_button = Button(text='Listar Productos')
        list_button.bind(on_press=self.list_products)
        layout.add_widget(list_button)

        return layout

    def capture_image(self, instance):
        image_path = self.camera.capture_image()
        if image_path:
            text = self.camera.process_image(image_path)
            data = self.camera.extract_data(text)
            self.info_input.text = f"{data.get('fecha_caducidad', '')}, {data.get('lote', '')}, {data.get('precio', '')}, {data.get('proveedor', '')}"
            self.info_label.text = f"Imagen capturada: {image_path}"
        else:
            self.info_label.text = "Error al capturar la imagen"

    def save_info(self, instance):
        info = self.info_input.text.split(',')
        if len(info) == 4:
            fecha_caducidad, lote, precio, proveedor = info
            self.inventory.add_product(fecha_caducidad.strip(), lote.strip(), float(precio.strip()), proveedor.strip())
            self.info_label.text = 'Información guardada'
        else:
            self.info_label.text = 'Formato incorrecto. Use: fecha, lote, precio, proveedor'

    def list_products(self, instance):
        products = self.inventory.list_products()
        self.info_label.text = '\n'.join(str(product) for product in products)

if __name__ == '__main__':
    MainApp().run()