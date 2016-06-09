from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Spacer
import PIL
import os

doc = SimpleDocTemplate("image.pdf", pagesize=letter)

# populate original image folder, (image, download_count)
selected_images = []
for f, c in image_d:
    if c > 0.7:
        selected_images.append(f)


# this part needs to be customized according to the system
# resize images
image_folder = './Images'
rescaled_images = './r_images'
for _file in files:
    f = image_folder +'/'+ _file
    fl = PIL.Image.open(f)
    fl = fl.resize((456, 436), PIL.Image.ANTIALIAS)
    fl.save(rescaled_images + '/' + _file)

files = os.listdir(rescaled_images)
parts = []
for _file in (files):
    f = rescaled_images + '/' + _file
    parts.append(Image(f))
doc.build(parts)

