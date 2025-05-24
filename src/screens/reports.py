import os
import glob
import shutil
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserIconView
from kivymd.uix.button import MDButton, MDButtonText
import pandas as pd
import logging
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

# Configuración de logging
log_path = os.path.join(os.path.dirname(__file__), '..', 'app.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()]
)

class ReportsScreen(Screen):
    def __init__(self, **kwargs):
        super(ReportsScreen, self).__init__(**kwargs)
        self.date_spinner = None  # Inicializa el atributo para evitar errores
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.date_spinner = Spinner(text='Seleccionar Fecha', size_hint=(1, 0.1))
        self.date_spinner.bind(text=self.display_reports)
        layout.add_widget(self.date_spinner)
        # Botón de "Atrás" al final del layout
        back_button = MDButton(
            MDButtonText(text='Atrás'),
            size_hint=(1, 0.1)
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)
        logging.info('ReportsScreen inicializado correctamente')
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(1, 0.713, 0.757, 1)  # #FFB6C1
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_bg_rect, size=self._update_bg_rect)

    def _update_bg_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_enter(self):
        try:
            self.load_dates()
            if self.date_spinner and self.date_spinner.values:
                self.display_reports(self.date_spinner, self.date_spinner.text)
            logging.info('Entrando a Informes')
        except Exception as e:
            logging.error(f'Error al entrar a Informes: {e}')
        # Añadir botón para ver errores del sistema solo si el layout existe
        if not hasattr(self, 'error_button') and len(self.children) > 0:
            from kivymd.uix.button import MDButton, MDButtonText
            self.error_button = MDButton(
                MDButtonText(text='Ver Errores del Sistema'),
                size_hint=(1, 0.1)
            )
            self.error_button.bind(on_press=self.show_errors)
            self.children[0].add_widget(self.error_button, index=0)

    def load_dates(self):
        try:
            informes_dir = os.path.join(os.path.dirname(__file__), '..', 'informes')
            excel_files = glob.glob(os.path.join(informes_dir, 'sales_report_*.xlsx'))
            dates = [os.path.basename(file).split('_')[2] for file in excel_files]
            if dates:
                self.date_spinner.values = dates
                self.date_spinner.text = dates[0]  # Seleccionar la primera fecha por defecto
            else:
                self.date_spinner.values = ['No hay informes disponibles']
                self.date_spinner.text = 'No hay informes disponibles'
        except FileNotFoundError:
            self.grid_layout.add_widget(Label(text="No hay informes disponibles.", size_hint_y=None, height=40))

    def display_reports(self, spinner, date):
        self.grid_layout.clear_widgets()
        try:
            informes_dir = os.path.join(os.path.dirname(__file__), '..', 'informes')
            excel_files = glob.glob(os.path.join(informes_dir, f'sales_report_{date}_*.xlsx'))
            if not excel_files:
                raise FileNotFoundError
            df = pd.read_excel(excel_files[0])
            if 'Imagen' in df.columns:
                df = df.drop(columns=['Imagen'])
            if 'Coste' in df.columns:
                df = df.drop(columns=['Coste'])

            # Crear encabezados de columna
            headers = df.columns.tolist()
            header_layout = GridLayout(cols=len(headers), size_hint_y=None, height=40)
            for header in headers:
                header_label = Label(text=header, size_hint_y=None, height=40, bold=True)
                header_layout.add_widget(header_label)
            self.grid_layout.add_widget(header_layout)

            # Crear filas de datos
            for index, row in df.iterrows():
                row_layout = GridLayout(cols=len(headers), size_hint_y=None, height=40)
                for item in row:
                    item_text = '' if pd.isna(item) else str(item)
                    item_label = Label(text=item_text, size_hint_y=None, height=40)
                    row_layout.add_widget(item_label)
                self.grid_layout.add_widget(row_layout)
            logging.info(f'Mostrando informe para fecha: {date}')
        except FileNotFoundError:
            self.grid_layout.add_widget(Label(text="No hay informes disponibles.", size_hint_y=None, height=40))
            logging.warning('No hay informes disponibles para mostrar')
        except Exception as e:
            logging.critical(f'Error crítico al mostrar informes: {e}')

    def download_report(self, instance):
        informes_dir = os.path.join(os.path.dirname(__file__), '..', 'informes')
        filechooser = FileChooserIconView(path=informes_dir, filters=['*.xlsx'], dirselect=False)
        filechooser.bind(on_submit=self.on_file_selected)
        self.add_widget(filechooser)
        
    def go_to_download_screen(self, instance):
        try:
            self.manager.current = 'download_reports'
            logging.info('Navegando a pantalla de descarga de informes')
        except Exception as e:
            logging.error(f'Error al navegar a pantalla de descarga de informes: {e}')

    def on_file_selected(self, filechooser, selection, *args):
        if selection:
            selected_file = selection[0]
            downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            shutil.copy(selected_file, downloads_dir)
            print(f"Archivo descargado en: {downloads_dir}")
        self.remove_widget(filechooser)
        print('Infome descargado', selected_file)

    def go_back(self, instance):
        try:
            self.manager.current = 'main_menu'
            logging.info('Volviendo al menú principal desde Informes')
        except Exception as e:
            logging.error(f'Error al volver al menú principal desde Informes: {e}')

    def show_errors(self, instance):
        
        log_path = os.path.join(os.path.dirname(__file__), '..', 'informes', 'errores.log')
        # Si no existe, copiar los errores recientes de app.log
        if not os.path.exists(log_path):
            app_log = os.path.join(os.path.dirname(__file__), '..', 'app.log')
            if os.path.exists(app_log):
                with open(app_log, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                error_lines = [l for l in lines if '[ERROR]' in l or '[CRITICAL]' in l]
                with open(log_path, 'w', encoding='utf-8') as f:
                    f.writelines(error_lines)
        # Mostrar el contenido
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                error_text = f.read()
        else:
            error_text = 'No hay errores registrados.'
        # Layout del popup con botón de descarga
        box = BoxLayout(orientation='vertical')
        textinput = TextInput(text=error_text, readonly=True, multiline=True, font_size='14sp', size_hint=(1, 0.85))
        box.add_widget(textinput)
        download_btn = MDButton(MDButtonText(text='Descargar Errores'), size_hint=(1, 0.15))
        def download_errors(instance):
            import shutil
            downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            shutil.copy(log_path, downloads_dir)
        download_btn.bind(on_press=download_errors)
        box.add_widget(download_btn)
        popup = Popup(title='Errores del Sistema', content=box, size_hint=(0.9, 0.7))
        popup.open()