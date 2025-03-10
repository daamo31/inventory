from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from camera import CameraWidget

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 📸 La cámara ocupa la mayor parte de la pantalla
        self.camera_widget = CameraWidget(size_hint=(1, 2))  # Aumentar el tamaño de la cámara
        layout.add_widget(self.camera_widget)

        # 📌 Etiqueta de información (solo una vez)
        self.info_label = Label(text='Información de la etiqueta:', size_hint=(1, 0.1))
        layout.add_widget(self.info_label)

        # 📌 Campo de entrada
        self.info_input = TextInput(hint_text='Fecha de caducidad, lote', size_hint=(1, 0.1))
        layout.add_widget(self.info_input)

        # 📍 Botones alineados en la parte inferior
        button_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)

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
