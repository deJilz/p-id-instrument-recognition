import fitz
from absl import app
import os

def pdf_image ( pdfPath , imgPath , zoom_x , zoom_y , rotation_angle ) :
    # open pdf file
    pdf = fitz.open ( pdfPath )

    dir_path_obj = 'Dataset/images/'
    files = os.listdir ( dir_path_obj )
    # read each page
    for pg in range (0 , pdf.page_count ) :
        page = pdf [ pg ]
        # zoom_x = zoom_y =3 -> use 3 * original resolution
        trans = fitz.Matrix ( zoom_x , zoom_y ).prerotate (rotation_angle)
        pm = page.get_pixmap ( matrix = trans , alpha = False )
        rename = pg + len ( files )
        # write the image
        pm.save(imgPath +str ( rename ) +".png")
    pdf.close ()

def main ( _argv ) :
    # folder storing the PDF files
    dir_path = 'Dataset/'
    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path,f))]
    print("files",files)
    for file in files :
        pdfPath = dir_path +'/'+ file
        # print ( pdfPath )
        pdf_image ( pdfPath , 'Dataset/images/', 3 , 3 , 0)
    print (" finished ")

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit :
        pass