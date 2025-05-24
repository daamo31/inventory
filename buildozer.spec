[app]
title = Morrico inventario
package.name = chuchesinventario
package.domain = org.chuches.inventario
source.dir = src
source.include_exts = py,png,jpg,jpeg,kv,atlas,db
version = 1.0
requirements = python3,kivy==2.3.0,kivymd==2.0.1,opencv-python,pillow,pytesseract,numpy,requests,easyocr,flask
orientation = portrait
fullscreen = 1
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.minapi = 21
android.arch = armeabi-v7a,arm64-v8a
android.entrypoint = main.py
android.icon = ../src/images/morrico.jpeg
# (Opcional) Si tienes un archivo .kv principal, descomenta y pon el nombre
#kv = main.kv
# (Opcional) Si usas dependencias nativas, puedes añadirlas aquí
#android.add_src = src/inventory.db
# (Opcional) Si usas tesseract, puedes necesitar incluir el binario y los datos de idioma
#android.add_assets = src/tessdata

# (Opcional) Si usas Flask solo para pruebas, puedes quitarlo para producción
# (Opcional) Si usas EasyOCR, asegúrate de que los modelos estén en assets o descargados en runtime

[buildozer]
log_level = 2
warn_on_root = 1

[python]
# (Opcional) Si tienes módulos Cython, agrégalos aquí
#cython_compile_all = 1

[android]
# (Opcional) Si usas OpenCV, Pillow, etc., Buildozer los maneja automáticamente
#android.add_jars =
#android.add_src =
#android.add_assets =
#android.gradle_dependencies =
#android.api = 33
#android.ndk = 23b
#android.accept_sdk_license = True
#android.enable_androidx = True
#android.extra_args =

# (Opcional) Si tienes problemas con dependencias, puedes forzar versiones aquí
#requirements = kivy==2.3.0,kivymd==2.0.1,opencv-python,pillow,pytesseract,numpy,requests,easyocr,flask

# (Opcional) Si usas tesseract, puedes necesitar añadir los datos de idioma
#android.add_assets = src/tessdata

# (Opcional) Si usas archivos de base de datos
#android.add_assets = src/inventory.db

# (Opcional) Si usas imágenes
#android.add_assets = src/images
