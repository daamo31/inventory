from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
import cv2
import pytesseract

class CameraWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.image = Image()
        self.add_widget(self.image)

        self.capture_button = Button(text='Capturar')
        self.capture_button.bind(on_press=self.capture)
        self.add_widget(self.capture_button)

        self.info_label = Label(text='Información de la etiqueta:')
        self.add_widget(self.info_label)

        self.capture = cv2.VideoCapture(0)
        self.update()

    def update(self, *args):
        ret, frame = self.capture.read()
        if ret:
            buf = cv2.flip(frame, 0).tobytes()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = image_texture
        self.image.canvas.ask_update()

    def capture(self, *args):
        ret, frame = self.capture.read()
        if ret:
            image_path = 'captured_image.png'
            cv2.imwrite(image_path, frame)
            text = self.process_image(image_path)
            data = self.extract_data(text)
            self.info_label.text = f"Fecha: {data.get('fecha_caducidad', 'N/A')}, Lote: {data.get('lote', 'N/A')}, Precio: {data.get('precio', 'N/A')}, Proveedor: {data.get('proveedor', 'N/A')}"

    def process_image(self, image_path):
        # Lee la imagen desde el archivo
        image = cv2.imread(image_path)
        # Convierte la imagen a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Aplica un umbral para binarizar la imagen
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        # Usa pytesseract para extraer texto de la imagen
        text = pytesseract.image_to_string(binary)
        return text

    def extract_data(self, text):
        # Extrae datos como fecha de caducidad, lote, precio y proveedor del texto procesado
        lines = text.split('\n')
        data = {}
        for line in lines:
            if 'fecha' in line.lower():
                data['fecha_caducidad'] = line.split(':')[-1].strip()
            elif 'lote' in line.lower():
                data['lote'] = line.split(':')[-1].strip()
            elif 'precio' in line.lower():
                data['precio'] = line.split(':')[-1].strip()
            elif 'proveedor' in line.lower():
                data['proveedor'] = line.split(':')[-1].strip()
        return data

class Camera:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)

    def capture_image(self):
        ret, frame = self.capture.read()
        if ret:
            image_path = 'captured_image.png'
            cv2.imwrite(image_path, frame)
            return image_path
        return None