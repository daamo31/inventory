# Chuches Inventario

Este proyecto es una aplicación móvil y de escritorio desarrollada en Python para gestionar el inventario de una tienda de chuches. Permite capturar imágenes de las etiquetas de los productos y almacenar información relevante como la fecha de caducidad, lote, precio y proveedor. Incluye cámara, OCR, informes y exportación de base de datos.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
chuches-inventario
├── src
│   ├── main.py          # Punto de entrada de la aplicación
│   ├── camera.py        # Manejo de la funcionalidad de la cámara y OCR
│   ├── inventory.py     # Gestión del inventario de chuches
│   ├── models           # Definiciones de modelos de datos
│   ├── utils            # Funciones utilitarias
│   ├── images/          # Imágenes de productos y fondos
│   ├── informes/        # Informes y logs generados
│   └── screens/         # Todas las pantallas de la app (KivyMD)
├── requirements.txt     # Dependencias del proyecto
├── buildozer.spec       # Configuración para empaquetar APK Android
├── README.md            # Documentación del proyecto
└── .gitignore           # Archivos y directorios a ignorar por Git
```

## Instalación en Escritorio (Windows/Mac/Linux)

1. Instala Python 3.8+ y pip.
2. Instala las dependencias:

```sh
pip install -r requirements.txt
```

3. Ejecuta la aplicación:

```sh
python src/main.py
```

## Instalación en Android (APK)

1. Instala [Buildozer](https://github.com/kivy/buildozer) y dependencias:

```sh
pip install --user buildozer cython
brew install autoconf automake libtool pkg-config
```

2. Inicializa Buildozer (solo la primera vez):

```sh
buildozer init
```

3. Asegúrate de que el archivo `buildozer.spec` esté correctamente configurado (ya incluido en este repo).

4. Conecta tu móvil Android por USB (con depuración USB activada) o usa un emulador.

5. Compila e instala el APK:

```sh
buildozer -v android debug deploy run
```

El APK se instalará automáticamente en tu móvil. El archivo generado estará en la carpeta `bin/`.

**Notas:**
- Si usas OCR (EasyOCR, pytesseract), asegúrate de tener conexión a internet la primera vez para descargar los modelos.
- Si tienes problemas con dependencias, revisa la sección `requirements` en `buildozer.spec`.
- Para iOS, consulta la documentación de Kivy (requiere Mac y cuenta de desarrollador Apple).

## Funcionalidades principales

- Gestión de productos y lotes con imágenes.
- Captura de etiquetas y OCR automático/manual.
- Visualización y edición de inventario.
- Informes de ventas y exportación a Excel.
- Exportación de la base de datos a la carpeta Descargas.
- Visualización y descarga de logs de errores.
- Interfaz moderna y adaptada a móvil (KivyMD 2.x).

## Requisitos

- Python 3.8+
- Android 5.0+ (API 21+) para APK
- Dependencias: kivy, kivymd, opencv-python, pillow, pytesseract, numpy, requests, easyocr, flask

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
