import os
import glob
import shutil
import logging
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDButton, MDButtonText

# Configuración de logging
log_path = os.path.join(os.path.dirname(__file__), '..', 'app.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()]
)

class DownloadReportsScreen(Screen):
    """Pantalla para descargar informes generados."""

    def __init__(self, **kwargs):
        """Inicializa la pantalla de descarga de informes."""
        super(DownloadReportsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Área de scroll para los informes
        self.scroll_view = ScrollView(size_hint=(1, 0.9))
        self.grid_layout = GridLayout(cols=1, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)
        layout.add_widget(self.scroll_view)

        # Botón de "Atrás"
        back_button = MDButton(
            MDButtonText(text='Atrás'),
            size_hint=(1, 0.1)
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(1, 0.713, 0.757, 1)  # #FFB6C1
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_bg_rect, size=self._update_bg_rect)

    def _update_bg_rect(self, *args):
        """Actualiza el fondo de la pantalla."""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_enter(self):
        """Acciones al entrar en la pantalla."""
        try:
            self.display_reports()
            logging.info('Entrando a pantalla de descarga de informes')
        except Exception as e:
            logging.error(f'Error al entrar a pantalla de descarga de informes: {e}')

    def display_reports(self):
        """Muestra los informes disponibles para descargar."""
        try:
            self.grid_layout.clear_widgets()
            informes_dir = os.path.join(os.path.dirname(__file__), '..', 'informes')
            excel_files = glob.glob(os.path.join(informes_dir, '*.xlsx'))
            if not excel_files:
                self.grid_layout.add_widget(Label(text="No hay informes disponibles.", size_hint_y=None, height=40))
                logging.warning('No hay informes disponibles para descargar')
            else:
                for file in excel_files:
                    file_name = os.path.basename(file)
                    file_button = MDButton(
                        MDButtonText(text=file_name),
                        size_hint_y=None, height=40
                    )
                    file_button.bind(on_press=lambda instance, f=file: self.download_file(f))
                    self.grid_layout.add_widget(file_button)
                logging.info('Lista de informes para descarga mostrada')
        except Exception as e:
            logging.critical(f'Error crítico al mostrar informes para descarga: {e}')

    def download_file(self, file_path):
        """Descarga el archivo seleccionado."""
        try:
            downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            shutil.copy(file_path, downloads_dir)
            logging.info(f'Archivo descargado: {file_path}')
        except Exception as e:
            logging.error(f'Error al descargar archivo {file_path}: {e}')

    def go_back(self, instance):
        """Vuelve a la pantalla de informes."""
        try:
            self.manager.current = 'reports'
            logging.info('Volviendo a Informes desde descarga de informes')
        except Exception as e:
            logging.error(f'Error al volver a Informes desde descarga de informes: {e}')