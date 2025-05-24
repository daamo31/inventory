from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout

from camera import CameraWidget


class CameraScreen(MDScreen):
    """
    Pantalla principal que muestra la cámara y permite al usuario capturar y guardar información sobre productos.
    """

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

    def on_enter(self):
        """Inicia la cámara al entrar en la pantalla."""
        self.camera_widget.start_camera()

    def on_leave(self):
        """Detiene la cámara al salir de la pantalla."""
        self.camera_widget.stop_camera()

    def capture_image(self, instance):
        """Captura una imagen y procesa los datos de la etiqueta."""
        image_path = self.camera_widget.capture()

        if image_path:
            self.process_image(image_path)
        else:
            self.info_label.text = "Error al capturar la imagen"

    def process_image(self, image_path):
        """Procesa la imagen capturada y extrae los datos de la etiqueta."""
        text, data = self.camera_widget.preprocess_and_ocr(image_path)

        if data:
            self.update_info_input(data)
            self.info_label.text = f"Datos extraídos: {data.get('fecha_caducidad', 'N/A')}, {data.get('lote', 'N/A')}"
        else:
            self.info_label.text = "No se pudieron extraer datos de la imagen"

    def save_info(self, instance):
        """Guarda la información de la etiqueta en la pantalla de añadir producto."""
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
        """Vuelve a la pantalla anterior."""
        self.manager.current = "add_product_lote"

    def update_info_input(self, data):
        """Actualiza el campo de entrada de información con los datos extraídos."""
        if data:
            self.info_input.text = f"{data.get('fecha_caducidad', 'N/A')}, {data.get('lote', 'N/A')}"
        else:
            self.info_label.text = "No se pudieron extraer datos de la imagen"