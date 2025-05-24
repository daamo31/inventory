from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from camera import CameraWidget


class CameraScreen(MDScreen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle

            Color(1, 0.713, 0.757, 1)  # #FFB6C1
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_bg_rect, size=self._update_bg_rect)

    def _update_bg_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

        # Layout principal
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # 📸 La cámara ocupa la mayor parte de la pantalla
        self.camera_widget = CameraWidget(size_hint=(1, 2))
        layout.add_widget(self.camera_widget)

        # 📌 Etiqueta de información
        self.info_label = MDLabel(
            text="Información de la etiqueta:",
            halign="center",
            size_hint=(1, 0.1),
        )
        layout.add_widget(self.info_label)

        # 📌 Campo de entrada
        self.info_input = MDTextField(
            hint_text="Fecha de caducidad, lote",
            size_hint=(1, 0.1),
        )
        layout.add_widget(self.info_input)

        # 📍 Botones alineados en la parte inferior
        button_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)

        back_button = MDButton(
            MDButtonText(text="Atrás"),
            pos_hint={"center_x": 0.5},
            on_release=self.go_back,
        )
        button_layout.add_widget(back_button)

        capture_button = MDButton(
            MDButtonText(text="Capturar"),
            pos_hint={"center_x": 0.5},
            on_release=self.capture_image,
        )
        button_layout.add_widget(capture_button)

        save_button = MDButton(
            MDButtonText(text="Guardar"),
            pos_hint={"center_x": 0.5},
            on_release=self.save_info,
        )
        button_layout.add_widget(save_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def on_enter(self):
        self.camera_widget.start_camera()

    def on_leave(self):
        self.camera_widget.stop_camera()

    def capture_image(self, instance):
        image_path = self.camera_widget.capture()

        if image_path:
            self.process_image(image_path)
        else:
            self.info_label.text = "Error al capturar la imagen"

    def process_image(self, image_path):
        text, data = self.camera_widget.preprocess_and_ocr(image_path)

        if data:
            self.update_info_input(data)
            self.info_label.text = f"Datos extraídos: {data.get('fecha_caducidad', 'N/A')}, {data.get('lote', 'N/A')}"
        else:
            self.info_label.text = "No se pudieron extraer datos de la imagen"

    def save_info(self, instance):
        # Manejo seguro si el usuario no pone coma
        partes = self.info_input.text.split(",")
        fecha = partes[0].strip() if len(partes) > 0 else ""
        lote = partes[1].strip() if len(partes) > 1 else ""
        self.manager.get_screen("add_product_lote").update_info_input(
            {
                "fecha_caducidad": fecha,
                "lote": lote,
            }
        )
        self.manager.current = "add_product_lote"

    def go_back(self, instance):
        self.manager.current = "add_product_lote"

    def update_info_input(self, data):
        if data:
            self.info_input.text = f"{data.get('fecha_caducidad', 'N/A')}, {data.get('lote', 'N/A')}"
        else:
            self.info_label.text = "No se pudieron extraer datos de la imagen"