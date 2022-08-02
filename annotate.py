# built in 
import os
import sys
import argparse
import shutil
import pathlib

# 3rd party imports
from pdf_annotate import PdfAnnotator, Appearance, Location

# import other modules from this project

'''
from pdf_annotate import PdfAnnotator, Appearance, Location

annotator = PdfAnnotator('test.pdf')
annotator.add_annotation('square', Location=Location(x1=10, y1=20, x2=100, y2=100, page=0), Appearance=Appearance(fill=(1, 0, 0)))
annotator.write('annotated.pdf')

---
fname: pdfname N.txt

instrument x y r:
LY1104 4698 3338 53
HC1101 3888 1162 53
'''

def draw_circles(circ_fldr, pandidfname):
    savefname = os.getcwd() + "/" + pandidfname +" - inst marked.pdf"
    annotator = PdfAnnotator(os.getcwd() + "/" + pandidfname)
    annotator.set_page_dimensions((1684,2384),180)
    annotator.add_annotation('square', Location(x1=0, y1=0, x2=50, y2=50, page=0), Appearance(stroke_color=(1, 0, 0),stroke_width=50))
    
    for root, dirs, files in os.walk(circ_fldr):
        for f in files:
            if not f.endswith(".txt"):
                continue # if not a txt file go to next
            
            page_num = int(pathlib.Path(f).stem.split(" ")[-1]) - 1# get last element of filename of form: "pdfname N.txt"
            
            with open(os.path.join(circ_fldr,f)) as fi: # open txt file
                for line in fi: # loop through each line
                    if line.find("x y r:") > 0: continue # ignore the first line
                    # read in lines
                    try:
                        tag, x, y, r = line.strip().split(" ")#[-3:-1] ** deal with if theres a spcae in the tag
                        # do math with read in coordinates
                        x, y, r = int(x), int(y), int(r)
                        
                        # adjust coordinates from png to pdf
                        x1m = (x - r)/3
                        x2m = (x + r)/3
                        y1m = (-y+r+5050)/3
                        y2m = (-y-r+5050)/3
                        
                    except:
                        print("issue with", line)
                        continue
                    annotator.add_annotation('circle', Location(x1=x1m, y1=y1m-36, x2=x1m+36, y2=y1m, page=0), Appearance(stroke_color=(1, 0, 0),stroke_width=1))
                    
                    
    #annotator.write(savefname)
    try:
        annotator.write(savefname) # save annotated pdf
    except PermissionError:
        print("[*] Close or delete the old document before running again to annotate.")
        quit()
    return savefname