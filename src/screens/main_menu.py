from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDButton, MDButtonText  # KivyMD 2.x

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Título del menú principal
        title_label = Label(text="Menú Principal", font_size='24sp', size_hint=(1, 0.1), halign='center')
        layout.add_widget(title_label)

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

    def go_to_inventory(self, instance):
        self.manager.current = 'inventory'

    def go_to_sales(self, instance):
        self.manager.current = 'sales'

    def go_to_reports(self, instance):
        self.manager.current = 'reports'