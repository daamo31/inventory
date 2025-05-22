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

class ReportsScreen(Screen):
    def __init__(self, **kwargs):
        super(ReportsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Desplegable para seleccionar la fecha
        self.date_spinner = Spinner(text='Seleccionar Fecha', size_hint=(1, 0.1))
        self.date_spinner.bind(text=self.display_reports)
        layout.add_widget(self.date_spinner)

        # Área de scroll para los informes
        self.scroll_view = ScrollView(size_hint=(1, 0.7))
        self.grid_layout = GridLayout(cols=1, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)
        layout.add_widget(self.scroll_view)

        # Botón para descargar el archivo Excel
        download_button = MDButton(
            MDButtonText(text='Descargar Informe'),
            size_hint=(1, 0.1)
        )
        download_button.bind(on_press=self.go_to_download_screen)
        layout.add_widget(download_button)

        # Botón de "Atrás"
        back_button = MDButton(
            MDButtonText(text='Atrás'),
            size_hint=(1, 0.1)
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_enter(self):
        self.load_dates()
        if self.date_spinner.values:
            self.display_reports(self.date_spinner, self.date_spinner.text)

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
        except FileNotFoundError:
            self.grid_layout.add_widget(Label(text="No hay informes disponibles.", size_hint_y=None, height=40))

    def download_report(self, instance):
        informes_dir = os.path.join(os.path.dirname(__file__), '..', 'informes')
        filechooser = FileChooserIconView(path=informes_dir, filters=['*.xlsx'], dirselect=False)
        filechooser.bind(on_submit=self.on_file_selected)
        self.add_widget(filechooser)
        
    def go_to_download_screen(self, instance):
        self.manager.current = 'download_reports'

    def on_file_selected(self, filechooser, selection, *args):
        if selection:
            selected_file = selection[0]
            downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            shutil.copy(selected_file, downloads_dir)
            print(f"Archivo descargado en: {downloads_dir}")
        self.remove_widget(filechooser)
        print('Infome descargado', selected_file)

    def go_back(self, instance):
        self.manager.current = 'main_menu'