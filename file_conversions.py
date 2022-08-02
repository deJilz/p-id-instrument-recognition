#!/usr/bin/env python

# built in
import os
import pathlib

# 3rd party
import fitz
from absl import app
from fpdf import FPDF
from PIL import Image

'''
    includes methods for both
    image -> pdf
    pdf -> images

'''

def _pdf_image ( cur_dir, pandidfname, zoom_x , zoom_y , rotation_angle, image_source_fld) :
    
    im_dir = os.path.join(cur_dir, image_source_fld)
    # open pdf file
    pdf = fitz.open ( os.path.join(cur_dir, pandidfname))

    # read each page
    for pg in range (0 , pdf.page_count ) :
        page = pdf [ pg ]
        # zoom_x = zoom_y =3 -> use 3 * original resolution
        trans = fitz.Matrix ( zoom_x , zoom_y ).prerotate (rotation_angle)
        pm = page.get_pixmap ( matrix = trans , alpha = False )
        rename = pandidfname.split(".")[0] + " " + str(pg+1)
        # write the image
        pm.save(im_dir +str ( rename ) +".png")
    pdf.close ()

def pdf2im(pandidfname, image_source_fld):
    try:
        #app.run(main)
        cur_dir = os.getcwd()
        _pdf_image(cur_dir, pandidfname, 3 , 3 , 0, image_source_fld)
    except:
        #pass
        raise ValueError("problem in pdf2image")




def im2pdf(image_folder, pandidfname):
    
    pdf = FPDF('L', 'pt', (5052,7152)) # specific for 17x11 paper
    pdf.set_auto_page_break(0)
    savefname = os.getcwd() + "/" + pandidfname +" - MARKED INST.pdf"

    for root, dirs, files in os.walk(image_folder):
        for f in files:
            if f.endswith(".png"):
                pdf.add_page()
                img = Image.open(os.path.join(root,f))
                #print("size",img.size)
                pdf.image(os.path.join(root,f),type='PNG')#,w=img.width,h=img.height

    pdf.output(savefname, "F")
    return savefname