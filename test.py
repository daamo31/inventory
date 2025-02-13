import pytesseract
from PIL import Image

img = Image.open("captured_image.png")
text = pytesseract.image_to_string(img)

print("Texto detectado:", text)