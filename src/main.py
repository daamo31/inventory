from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from inventory import Inventory
from screens.main_menu import MainMenuScreen
from screens.Menu_Inventory import InventoryScreen, ViewInventoryScreen
from screens.product import (
    AddProductPhotoScreen, AddProductNameScreen, AddProductProveedorScreen,
    AddProductLoteScreen, AddProductPriceScreen, AddExistingProductLoteScreen,
    ModifyProductScreen, DeleteProductScreen
)
from screens.camera_screen import CameraScreen

class MainApp(MDApp):
    def build(self):
    
        self.title = 'Inventario'
        self.inventory = Inventory()

        sm = ScreenManager()
        sm.inventory = self.inventory

        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(CameraScreen(name='camera'))
        sm.add_widget(InventoryScreen(name='inventory'))
        sm.add_widget(ViewInventoryScreen(inventory=self.inventory, name='view_inventory'))
        sm.add_widget(AddProductPhotoScreen(name='add_product_photo'))
        sm.add_widget(AddProductNameScreen(name='add_product_name'))
        sm.add_widget(AddProductProveedorScreen(name='add_product_proveedor'))
        sm.add_widget(AddProductLoteScreen(name='add_product_lote'))
        sm.add_widget(AddProductPriceScreen(name='add_product_price'))
        sm.add_widget(AddExistingProductLoteScreen(inventory=self.inventory, name='add_existing_product_lote'))
        sm.add_widget(ModifyProductScreen(name='modify_product'))
        sm.add_widget(DeleteProductScreen(name='delete_product'))

        return sm

    def on_stop(self):
        self.inventory.close()

if __name__ == '__main__':
    MainApp().run()


