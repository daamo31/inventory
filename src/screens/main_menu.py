import logging
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDButton, MDButtonText  # KivyMD 2.x

# Configuración de logging
log_path = os.path.join(os.path.dirname(__file__), '..', 'app.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()]
)

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        
        # Imagen
        logo_image = Image(source='images/morrico.jpeg', size_hint=(1, 0.5))
        layout.add_widget(logo_image)

        # Botones
        button_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 0.4))

        inventory_button = MDButton(
            MDButtonText(text="Inventario"),
            pos_hint={"center_x": 0.5},
            on_release=self.go_to_inventory,
        )
        button_layout.add_widget(inventory_button)

        sales_button = MDButton(
            MDButtonText(text="Ventas"),
            pos_hint={"center_x": 0.5},
            on_release=self.go_to_sales,
        )
        button_layout.add_widget(sales_button)

        reports_button = MDButton(
            MDButtonText(text="Informes"),
            pos_hint={"center_x": 0.5},
            on_release=self.go_to_reports,
        )
        button_layout.add_widget(reports_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)
        logging.info('MainMenuScreen inicializado correctamente')

    def go_to_inventory(self, instance):
        try:
            logging.info('Navegando a Inventario')
            self.manager.current = 'inventory'
        except Exception as e:
            logging.error(f'Error al navegar a Inventario: {e}')

    def go_to_sales(self, instance):
        try:
            logging.info('Navegando a Ventas')
            self.manager.current = 'sales'
        except Exception as e:
            logging.error(f'Error al navegar a Ventas: {e}')

    def go_to_reports(self, instance):
        try:
            logging.info('Navegando a Informes')
            self.manager.current = 'reports'
        except Exception as e:
            logging.critical(f'Error crítico al navegar a Informes: {e}')