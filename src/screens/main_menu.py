from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Añadir imagen al menú principal
        logo_image = Image(source='images/morrico.jpeg', size_hint=(1, 1))
        layout.add_widget(logo_image)

        inventory_button = Button(text='Inventario', size_hint=(1, 0.2))
        inventory_button.bind(on_press=self.go_to_inventory)
        layout.add_widget(inventory_button)

        sales_button = Button(text='Ventas', size_hint=(1, 0.2))
        sales_button.bind(on_press=self.go_to_sales)
        layout.add_widget(sales_button)

        reports_button = Button(text='Informes', size_hint=(1, 0.2))
        reports_button.bind(on_press=self.go_to_reports)
        layout.add_widget(reports_button)

        self.add_widget(layout)

    def go_to_inventory(self, instance):
        self.manager.current = 'inventory'

    def go_to_sales(self, instance):
        self.manager.current = 'sales'

    def go_to_reports(self, instance):
        self.manager.current = 'reports'
