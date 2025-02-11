from camera import Camera
from inventory import Inventory

def main():
    # Inicializar la cámara
    camera = Camera()
    
    # Inicializar el inventario
    inventory = Inventory()
    
    while True:
        print("Opciones:")
        print("1. Capturar imagen")
        print("2. Agregar producto al inventario")
        print("3. Listar productos en el inventario")
        print("4. Salir")
        
        choice = input("Seleccione una opción: ")
        
        if choice == '1':
            image_path = camera.capture_image()
            # Aquí se procesaría la imagen para extraer datos
            print(f"Imagen capturada: {image_path}")
        
        elif choice == '2':
            # Aquí se agregarían los datos del producto al inventario
            # Se asume que se obtienen de la imagen procesada
            fecha_caducidad = input("Ingrese la fecha de caducidad: ")
            lote = input("Ingrese el lote: ")
            precio = float(input("Ingrese el precio: "))
            proveedor = input("Ingrese el proveedor: ")
            inventory.add_product(fecha_caducidad, lote, precio, proveedor)
        
        elif choice == '3':
            products = inventory.list_products()
            for product in products:
                print(product)
        
        elif choice == '4':
            print("Saliendo de la aplicación.")
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()