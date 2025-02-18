import re
import cv2
import numpy as np
import easyocr
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from datetime import datetime

class CameraWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.image = Image(size_hint=(1, 5))
        self.add_widget(self.image)

        self.capture_button = Button(text="Capturar Imagen")
        self.capture_button.bind(on_press=self.capture)
        self.add_widget(self.capture_button)

        self.info_label = Label(text="Esperando captura...")
        self.add_widget(self.info_label)

        self.capture_device = None
        self.reader = easyocr.Reader(['es', 'en'])  # Inicializa el lector de easyocr

    def start_camera(self):
        """Inicia la captura de la cámara."""
        if self.capture_device is None:
            self.capture_device = cv2.VideoCapture(0)
            Clock.schedule_interval(self.update, 1.0 / 30.0)

    def stop_camera(self):
        """Libera el dispositivo de captura de la cámara."""
        if self.capture_device:
            self.capture_device.release()
            self.capture_device = None

    def update(self, *args):
        """Actualiza la imagen mostrada en la interfaz en tiempo real."""
        if self.capture_device:
            ret, frame = self.capture_device.read()
            if ret:
                frame = cv2.flip(frame, 0)
                buf = frame.tobytes()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = image_texture

    def capture(self, *args):
        """Captura una imagen, procesa el texto con OCR y extrae los datos."""
        if self.capture_device:
            ret, frame = self.capture_device.read()
            if not ret:
                self.info_label.text = "Error al capturar la imagen"
                return None

            image_path = 'captured_image.png'
            cv2.imwrite(image_path, frame)

            text, data = self.preprocess_and_ocr(image_path)

            if data:
                self.info_label.text = f"Fecha: {data.get('fecha_caducidad', 'N/A')}, Lote: {data.get('lote', 'N/A')}"
            else:
                self.info_label.text = "No se encontraron datos en la imagen"

            return image_path
        return None

    def preprocess_and_ocr(self, image_path):
        """Preprocesa la imagen y extrae texto con OCR."""
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Aplicar preprocesamiento
        image = self.apply_preprocessing(image)

        # Guardar la imagen preprocesada
        processed_image_path = 'processed_image.png'
        cv2.imwrite(processed_image_path, image)

        # Utilizar easyocr para extraer texto
        result = self.reader.readtext(image)
        text = " ".join([res[1] for res in result])

        data = self.extract_data(text)
        return text, data

    def apply_preprocessing(self, image):
        """Aplica filtros para mejorar la detección de texto en la imagen."""
        image = cv2.GaussianBlur(image, (5, 5), 0)  # Reducción de ruido
        image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        kernel = np.ones((2, 2), np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        return image

    def extract_data(self, text):
        """Extrae fecha de caducidad y número de lote del texto OCR."""
        data = {}

        fecha_pattern = re.compile(r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}[-/]\d{2}|\d{2}[-]\d{4})\b')
        lote_pattern = re.compile(r'\b[L]?\d+[A-Za-z]?\d*\b')

        fecha_match = fecha_pattern.search(text)
        if fecha_match:
            fecha_str = fecha_match.group(1)
            formatos = ["%d-%m-%Y", "%d/%m/%Y", "%d-%m-%y", "%d/%m-%y", "%m-%Y", "%m/%Y"]
            for fmt in formatos:
                try:
                    fecha = datetime.strptime(fecha_str, fmt).strftime("%d/%m/%Y")
                    data['fecha_caducidad'] = fecha
                    break
                except ValueError:
                    pass

        lote_match = lote_pattern.search(text)
        if lote_match:
            data['lote'] = lote_match.group(0)

        return data if data else None