import os
import glob
import shutil
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

class DownloadReportsScreen(Screen):
    def __init__(self, **kwargs):
        super(DownloadReportsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Área de scroll para los informes
        self.scroll_view = ScrollView(size_hint=(1, 0.9))
        self.grid_layout = GridLayout(cols=1, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)
        layout.add_widget(self.scroll_view)

        # Botón de "Atrás"
        back_button = Button(text='Atrás', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_enter(self):
        self.display_reports()

    def display_reports(self):
        self.grid_layout.clear_widgets()
        informes_dir = os.path.join(os.path.dirname(__file__), '..', 'informes')
        excel_files = glob.glob(os.path.join(informes_dir, '*.xlsx'))
        if not excel_files:
            self.grid_layout.add_widget(Label(text="No hay informes disponibles.", size_hint_y=None, height=40))
        else:
            for file in excel_files:
                file_name = os.path.basename(file)
                file_button = Button(text=file_name, size_hint_y=None, height=40)
                file_button.bind(on_press=lambda instance, f=file: self.download_file(f))
                self.grid_layout.add_widget(file_button)

    def download_file(self, file_path):
        downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        shutil.copy(file_path, downloads_dir)
        print(f"Archivo descargado en: {downloads_dir}")

    def go_back(self, instance):
        self.manager.current = 'reports'
