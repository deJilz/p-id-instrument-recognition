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

def _pdf_image (pandidfname, zoom_x , zoom_y , rotation_angle) :
    # get image folder
    im_dir = os.path.join(os.getcwd(), "images/")
    #print("",im_dir)
    #quit()
    # open pdf file
    pdf = fitz.open (pandidfname)

    # read each page
    for pg in range (0 , pdf.page_count ) :
        page = pdf [ pg ]
        # zoom_x = zoom_y =3 -> use 3 * original resolution
        trans = fitz.Matrix ( zoom_x , zoom_y ).prerotate (rotation_angle)
        pm = page.get_pixmap ( matrix = trans , alpha = False )
        rename = pathlib.Path(pandidfname).stem + " " + str(pg+1)
        # write the image
        pm.save(im_dir +str ( rename ) +".png")
    pdf.close ()

def pdf2im(pandidfname):
    # try:
        # #app.run(main)
        # cur_dir = os.getcwd()
        # _pdf_image(cur_dir, pandidfname, 3 , 3 , 0)
    # except:
        # #pass
        # raise ValueError("problem in pdf2image")
    _pdf_image(pandidfname, 3 , 3 , 0)