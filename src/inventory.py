class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, fecha_caducidad, lote):
        product = {
            'fecha_caducidad': fecha_caducidad,
            'lote': lote
        }
        self.products.append(product)

    def remove_product(self, lote):
        self.products = [product for product in self.products if product['lote'] != lote]

    def list_products(self):
        return self.products

    def find_product(self, lote):
        for product in self.products:
            if product['lote'] == lote:
                return product
        return None

    def save_to_file(self, filename):
        import json
        with open(filename, 'w') as file:
            json.dump(self.products, file)

    def load_from_file(self, filename):
        import json
        with open(filename, 'r') as file:
            self.products = json.load(file)