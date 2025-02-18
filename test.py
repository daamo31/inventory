import pytesseract
from PIL import Image

img = Image.open("captured_image.png")
img2 = Image.open("processed_image_cv.png")
text = pytesseract.image_to_string(img)
text2 = pytesseract.image_to_string(img2)
print("Texto detectado:", text2)
print("Texto detectado:", text)


  