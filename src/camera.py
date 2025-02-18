import re
import cv2  # Usaremos OpenCV para preprocesamiento
import easyocr
from PIL import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from datetime import datetime
import numpy as np

class CameraWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.image = KivyImage(size_hint=(1, 5))
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
                self.parent.parent.update_info_input(data)
            else:
                self.info_label.text = "No se encontraron datos en la imagen"

            return image_path
        return None

    def preprocess_and_ocr(self, image_path):
        """Preprocesa la imagen y extrae texto con OCR."""
        # 1. Abre la imagen con OpenCV (para mejor manejo de escala de grises)
        image_cv = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # 2. Preprocesamiento MEJORADO con OpenCV
        image_cv = self.apply_preprocessing(image_cv)

        # 3. Guarda la imagen preprocesada (para depuración)
        processed_image_path_cv = 'processed_image_cv.png'
        cv2.imwrite(processed_image_path_cv, image_cv)

        # 4. Convierte la imagen de OpenCV a PIL (EasyOCR usa PIL)
        image_pil = Image.fromarray(image_cv)

        # 5. OCR con EasyOCR
        result = self.reader.readtext(np.array(image_pil))  # Usa la imagen procesada
        text = " ".join([res[1] for res in result])
        print(f"Texto OCR (EasyOCR): {text}")  # Imprime el texto para depuración

        data = self.extract_data(text)
        return text, data

    def apply_preprocessing(self, image_cv):
        """Preprocesamiento ROBUSTO con OpenCV."""

        # 1. Aumento de contraste (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        image_cv = clahe.apply(image_cv)

        # 2. Binarización adaptativa (THRESH_OTSU para imágenes con iluminación variable)
        _, image_cv = cv2.threshold(image_cv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 3. Eliminación de ruido (morfología - OPEN para eliminar puntos blancos)
        kernel = np.ones((3, 3), np.uint8)
        image_cv = cv2.morphologyEx(image_cv, cv2.MORPH_OPEN, kernel, iterations=1)

        # 4. Inversión de colores (si es necesario)
        image_cv = cv2.bitwise_not(image_cv)  # Invierte los colores

        return image_cv

    def extract_data(self, text):
        """Extrae fecha de caducidad y número de lote del texto OCR."""
        data = {}

        # Patrón de fecha mejorado para detectar diferentes formatos
        fecha_pattern = re.compile(r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}[-/]\d{2}|\d{2}[-/]\d{4})\b')
        lote_pattern = re.compile(r'\b[L]?\d+[A-Za-z]?\d*[A-Za-z]?\d*\b')

        fecha_match = fecha_pattern.search(text)
        if fecha_match:
            fecha_str = fecha_match.group(1)
            formatos = ["%d-%m-%Y", "%d/%m/%Y", "%d-%m-%y", "%d/%m/%y", "%m-%Y", "%m/%Y"]
            for fmt in formatos:
                try:
                    fecha = datetime.strptime(fecha_str, fmt).strftime("%d/%m/%Y")
                    data['fecha_caducidad'] = fecha
                    break
                except ValueError:
                    pass

            # Buscar el lote después de la fecha
            lote_match = lote_pattern.search(text, fecha_match.end())
            if lote_match:
                data['lote'] = lote_match.group(0)

        # Imprime los datos para depuración
        print(f"Fecha de caducidad: {data.get('fecha_caducidad', 'N/A')}, Lote: {data.get('lote', 'N/A')}")

        return data if data else None

    def update_info_input(self, data):
        """Actualiza el campo de entrada de información en la interfaz de usuario."""
        self.parent.parent.update_info_input(data)