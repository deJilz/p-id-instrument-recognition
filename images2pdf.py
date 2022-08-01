import os
from fpdf import FPDF
from PIL import Image


image_folder = "Dataset/images/circles/"
pdf = FPDF('L', 'pt', (5052,7152)) # specific for 17x11 paper
pdf.set_auto_page_break(0)


for root, dirs, files in os.walk(image_folder):
    for f in files:
        if f.endswith(".png"):
            pdf.add_page()
            img = Image.open(os.path.join(root,f))
            print("size",img.size)
            pdf.image(os.path.join(root,f),type='PNG')#,w=img.width,h=img.height

pdf.output(image_folder+"wrapped.pdf", "F")