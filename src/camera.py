import re
import cv2
import easyocr
import logging
import numpy as np
from PIL import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from datetime import datetime

class CameraWidget(BoxLayout):
    """
    Widget de cámara para captura y procesamiento de imágenes con OCR.
    """

    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(1, 0.713, 0.757, 1)  # #FFB6C1
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_bg_rect, size=self._update_bg_rect)

        self.image = KivyImage(size_hint=(1, 5))
        self.add_widget(self.image)

        # Botón con color personalizado
        self.capture_button = Button(
            text="Capturar Imagen",
            background_color=(0.2, 0.5, 0.9, 1),  # Azul vibrante
            color=(1, 1, 1, 1),  # Texto blanco
            font_size='18sp',
            size_hint=(1, None),
            height=50
        )
        self.capture_button.bind(on_press=self.capture)
        self.add_widget(self.capture_button)

        self.info_label = Label(text="Esperando captura...", color=(1,1,1,1), font_size='16sp')
        self.add_widget(self.info_label)

        self.capture_device = None
        self.reader = easyocr.Reader(['es', 'en'])  # Inicializa el lector de easyocr
        logging.info('CameraWidget inicializado')

    def _update_bg_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def start_camera(self):
        """Inicia la cámara y comienza a actualizar la imagen."""
        try:
            if self.capture_device is None:
                self.capture_device = cv2.VideoCapture(0)
                Clock.schedule_interval(self.update, 1.0 / 30.0)
            logging.info('Cámara iniciada')
        except Exception as e:
            logging.error(f'Error al iniciar la cámara: {e}')

    def stop_camera(self):
        """Detiene la cámara si está en funcionamiento."""
        try:
            if self.capture_device:
                self.capture_device.release()
                self.capture_device = None
            logging.info('Cámara detenida')
        except Exception as e:
            logging.error(f'Error al detener la cámara: {e}')

    def update(self, *args):
        """Actualiza la imagen de la cámara en el widget."""
        try:
            if self.capture_device:
                ret, frame = self.capture_device.read()
                if ret:
                    frame = cv2.flip(frame, 0)
                    buf = frame.tobytes()
                    image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                    image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                    self.image.texture = image_texture
        except Exception as e:
            logging.error(f'Error al actualizar la imagen de la cámara: {e}')

    def capture(self, *args):
        """Captura una imagen y extrae datos usando OCR."""
        try:
            if self.capture_device:
                ret, frame = self.capture_device.read()
                if not ret:
                    self.info_label.text = "Error al capturar la imagen"
                    logging.error('Error al capturar la imagen')
                    return None
                image_path = 'captured_image.png'
                cv2.imwrite(image_path, frame)

                text, data = self.preprocess_and_ocr(image_path)

                if data:
                    self.info_label.text = f" {data.get('fecha_caducidad', 'N/A')}, {data.get('lote', 'N/A')}"
                    if self.parent.__class__.__name__ == 'AddProductLoteScreen':
                        self.parent.update_info_input(data)
                    logging.info('Datos extraídos correctamente de la imagen')
                else:
                    self.info_label.text = "No se encontraron datos en la imagen"
                    logging.warning('No se encontraron datos en la imagen')

                return image_path
            return None
        except Exception as e:
            logging.error(f'Error al capturar imagen y extraer datos: {e}')
            return None

    def capture_product_image(self, *args):
        """Captura una imagen del producto."""
        try:
            if self.capture_device:
                ret, frame = self.capture_device.read()
                if not ret:
                    self.info_label.text = "Error al capturar la imagen"
                    logging.error('Error al capturar la imagen de producto')
                    return None

                image_path = 'captured_product_image.png'
                cv2.imwrite(image_path, frame)
                self.info_label.text = "Imagen del producto capturada"
                logging.info('Imagen del producto capturada')
                return image_path
            return None
        except Exception as e:
            logging.error(f'Error al capturar imagen de producto: {e}')
            return None

    def preprocess_and_ocr(self, image_path):
        """Preprocesa la imagen y aplica OCR para extraer texto."""
        try:
            image_cv = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            image_cv = self.apply_preprocessing(image_cv)

            processed_image_path_cv = 'processed_image_cv.png'
            cv2.imwrite(processed_image_path_cv, image_cv)

            image_pil = Image.fromarray(image_cv)

            result = self.reader.readtext(np.array(image_pil))  # Usa la imagen procesada
            text = " ".join([res[1] for res in result])
            logging.info(f"Texto OCR (EasyOCR): {text}")  # Imprime el texto para depuración

            data = self.extract_data(text)
            return text, data
        except Exception as e:
            logging.error(f'Error en el preprocesamiento y OCR: {e}')
            return '', None

    def apply_preprocessing(self, image_cv):
        """Aplica técnicas de preprocesamiento a la imagen para mejorar el OCR."""
        try:
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
        except Exception as e:
            logging.error(f'Error en el preprocesamiento de la imagen: {e}')
            return image_cv

    def extract_data(self, text):
        """Extrae datos relevantes del texto usando expresiones regulares."""
        data = {}
        try:
            # Patrón de fecha mejorado para detectar diferentes formatos, incluyendo letras
            fecha_pattern = re.compile(r'\b(\d{1,2}[-/](?:\d{1,2}|\w{3})[-/]\d{2,4}|\d{1,2}[-/]\d{2}|\d{2}[-/]\d{4})\b')
            lote_pattern = re.compile(r'\b[L]?\d+[A-Za-z]?\d*[A-Za-z]?\d*\b')

            fecha_match = fecha_pattern.search(text)
            if fecha_match:
                fecha_str = fecha_match.group(1)
                formatos = ["%d-%m-%Y", "%d/%m/%Y", "%d-%m-%y", "%d/%m/%y", "%m-%Y", "%m/%Y", "%d-%b-%Y", "%d/%b/%Y"]
                for fmt in formatos:
                    try:
                        fecha = datetime.strptime(fecha_str, fmt).strftime("%d/%m/%Y")
                        data['fecha_caducidad'] = fecha
                        break
                    except ValueError:
                        pass

                # Buscar el lote antes y después de la fecha
                lote_match_before = lote_pattern.search(text, 0, fecha_match.start())
                lote_match_after = lote_pattern.search(text, fecha_match.end())
                if lote_match_before:
                    data['lote'] = lote_match_before.group(0)
                elif lote_match_after:
                    data['lote'] = lote_match_after.group(0)

            logging.info(f"Fecha de caducidad: {data.get('fecha_caducidad', 'N/A')}, Lote: {data.get('lote', 'N/A')}")
            return data if data else None
        except Exception as e:
            logging.error(f'Error al extraer datos del texto OCR: {e}')
            return None

    def update_info_input(self, data):
        """Actualiza el campo de entrada de información en el padre."""
        try:
            self.parent.update_info_input(data)
            logging.info('Campo de entrada de información actualizado')
        except Exception as e:
            logging.error(f'Error al actualizar campo de entrada de información: {e}')