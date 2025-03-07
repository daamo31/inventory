from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserIconView
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
        download_button = Button(text='Descargar Informe', size_hint=(1, 0.1))
        download_button.bind(on_press=self.download_report)
        layout.add_widget(download_button)

        # Botón de "Atrás"
        back_button = Button(text='Atrás', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_enter(self):
        self.load_dates()
        self.display_reports(self.date_spinner.text)

    def load_dates(self):
        try:
            df = pd.read_excel('sales_report.xlsx')
            dates = df['Fecha y Hora'].apply(lambda x: x.split()[0]).unique()
            self.date_spinner.values = list(dates)
        except FileNotFoundError:
            self.grid_layout.add_widget(Label(text="No hay informes disponibles.", size_hint_y=None, height=40))

    def display_reports(self, date):
        self.grid_layout.clear_widgets()
        try:
            df = pd.read_excel('sales_report.xlsx')
            filtered_df = df[df['Fecha y Hora'].str.contains(date)]
            if 'Imagen' in filtered_df.columns:
                filtered_df = filtered_df.drop(columns=['Imagen'])
            if 'Coste' in filtered_df.columns:
                filtered_df = filtered_df.drop(columns=['Coste'])
            for index, row in filtered_df.iterrows():
                report_label = Label(text=str(row.to_dict()), size_hint_y=None, height=40)
                self.grid_layout.add_widget(report_label)
        except FileNotFoundError:
            self.grid_layout.add_widget(Label(text="No hay informes disponibles.", size_hint_y=None, height=40))

    def download_report(self, instance):
        filechooser = FileChooserIconView()
        filechooser.path = './'
        filechooser.filters = ['*.xlsx']
        self.add_widget(filechooser)

    def go_back(self, instance):
        self.manager.current = 'main_menu'