import re
import cv2
import pytesseract
import numpy as np
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.clock import Clock

class CameraWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.image = Image(size_hint=(1, 5))
        self.add_widget(self.image)

        self.capture_button = Button()
        self.capture_button.bind(on_press=self.capture)
        self.add_widget(self.capture_button)

        self.info_label = Label()  # Asegurarse de que info_label esté definido
        self.add_widget(self.info_label)

        self.capture_device = None

    def start_camera(self):
        if self.capture_device is None:
            self.capture_device = cv2.VideoCapture(0)
            Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, *args):
        if self.capture_device:
            ret, frame = self.capture_device.read()
            if ret:
                frame = cv2.flip(frame, 0)
                buf = frame.tobytes()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = image_texture

    def capture(self, *args):
        if self.capture_device:
            ret, frame = self.capture_device.read()
            if not ret:
                self.info_label.text = "Error al capturar la imagen"
                return None
            
            image_path = 'captured_image.png'
            cv2.imwrite(image_path, frame)
            
            text = self.extract_text(image_path)
            data = self.extract_data(text)

            if data:
                self.info_label.text = f"Fecha: {data.get('fecha_caducidad', 'N/A')}, Lote: {data.get('lote', 'N/A')}"
            else:
                self.info_label.text = "No se encontraron datos en la imagen"
            
            return image_path
        return None

    def capture_image(self):
        if self.capture_device:
            ret, frame = self.capture_device.read()
            if not ret:
                self.info_label.text = "Error al capturar la imagen"
                return None
            
            image_path = 'captured_image.png'
            cv2.imwrite(image_path, frame)
            
            text = self.extract_text(image_path)
            data = self.extract_data(text)

            if data:
                self.info_label.text = f"Fecha: {data.get('fecha_caducidad', 'N/A')}, Lote: {data.get('lote', 'N/A')}"
            else:
                self.info_label.text = "No se encontraron datos en la imagen"
            
            return image_path
        return None

    def stop_camera(self):
        if self.capture_device:
            self.capture_device.release()
            self.capture_device = None

    def preprocess_image(self, image_path):
        image = cv2.imread(image_path)

        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Reducir ruido
        denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)

        # Ecualizar histograma
        equalized = cv2.equalizeHist(denoised)

        # Binarización adaptativa
        binary = cv2.adaptiveThreshold(equalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 11, 2)

        # Aplicar morfología para mejorar la forma de los caracteres
        kernel = np.ones((2,2), np.uint8)
        morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        cv2.imwrite("processed_image.png", morph)
        return morph

    def extract_text(self, image_path):
        processed_image = self.preprocess_image(image_path)

        # Configuración mejorada de Tesseract
        custom_config = r'--psm 6 --oem 3 -c tessedit_char_whitelist="0123456789L/-"'

        text = pytesseract.image_to_string(processed_image, config=custom_config)

        return text.strip()

    def extract_data(self, text):
        fecha_pattern = re.compile(r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b')  # Formato 12/12/2025
        lote_pattern = re.compile(r'\bL\d+\b')  # Formato L12345
        
        data = {}
        
        fecha_match = fecha_pattern.search(text)
        if fecha_match:
            data['fecha_caducidad'] = fecha_match.group(1)

        lote_match = lote_pattern.search(text)
        if lote_match:
            data['lote'] = lote_match.group(0)

        return data if data else None

class Camera:
    def __init__(self):
        self.capture_device = None

    def start_camera(self):
        if self.capture_device is None:
            self.capture_device = cv2.VideoCapture(0)

    def capture_image(self):
        if self.capture_device is None:
            self.start_camera()
        ret, frame = self.capture_device.read()
        if ret:
            image_path = 'captured_image.png'
            cv2.imwrite(image_path, frame)
            return image_path
        return None

    def stop_camera(self):
        if self.capture_device:
            self.capture_device.release()
            self.capture_device = None

    def preprocess_image(self, image_path):
        # Cargar la imagen
        image = cv2.imread(image_path)

        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Aplicar reducción de ruido
        denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)

        # Aumentar el contraste con ecualización de histograma
        equalized = cv2.equalizeHist(denoised)

        # Aplicar binarización adaptativa
        binary = cv2.adaptiveThreshold(equalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 11, 2)

        # Guardar imagen preprocesada para depuración
        cv2.imwrite("processed_image.png", binary)

        return binary

    def extract_text(self, image_path):
        # Preprocesar la imagen
        processed_image = self.preprocess_image(image_path)

        # Configurar Tesseract OCR
        custom_config = r'--psm 6 -c tessedit_char_whitelist="0123456789/L"'

        # Extraer texto con Tesseract
        text = pytesseract.image_to_string(processed_image, config=custom_config)

        return text.strip()

    def extract_data(self, text):
        # Extrae datos como fecha de caducidad y lote del texto procesado
        lines = text.split('\n')
        data = {}

        # Expresiones regulares para buscar patrones específicos
        fecha_pattern = re.compile(r'\b(\d{1,2}/\d{1,2}/\d{2,4})\b')
        lote_pattern = re.compile(r'\bL\d+\b')
        
        for line in lines:
            # Buscar fecha
            fecha_match = fecha_pattern.search(line)
            if fecha_match:
                data['fecha_caducidad'] = fecha_match.group(1)

            # Buscar lote
            lote_match = lote_pattern.search(line)
            if lote_match:
                data['lote'] = lote_match.group(0)

        return data if data else None

# Prueba con una imagen
if __name__ == '__main__':
    image_path = "/mnt/data/Captura de pantalla 2025-02-12 a las 10.57.40.png"
    widget = CameraWidget()
    detected_text = widget.extract_text(image_path)
    extracted_data = widget.extract_data(detected_text)

    print("Texto detectado:", detected_text)
    print("Datos extraídos:", extracted_data)