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

'''

def draw_circles(pandidfname):
    circ_fldr = os.path.join(os.getcwd(),"images/", "circles/")
    stem_fname = pathlib.Path(pandidfname).stem
    
    savefname = os.getcwd() + "/outs/" + stem_fname +" - inst marked.pdf"
    annotator = PdfAnnotator(pandidfname)
    annotator.set_page_dimensions((1684,2384),180)
    
    for root, dirs, files in os.walk(circ_fldr):
        for f in files:
            if not f.endswith(".txt"):
                continue # if not a txt file go to next
            
            #page_num
            try:
                page_num = int(pathlib.Path(f).stem.split(" ")[-1]) - 1# get last element of filename of form: "pdfname N.txt"
            except:
                page_num = int(pathlib.Path(f).stem[-1]) - 1# get last element of filename of form: "pdfname N.txt"
            
            
            with open(os.path.join(circ_fldr,f)) as fi: # open txt file
                for line in fi: # loop through each line
                    if line.find("x y r:") > 0: continue # ignore the first line
                    # read in lines
                    try:
                        tag, x, y, r, sheet = line.strip().split(" ")#[-3:-1] ** deal with if theres a spcae in the tag
                        # do math with read in coordinates
                        x, y, r = int(x), int(y), int(r)
                        
                        # adjust coordinates from png to pdf
                        x1m = (x - r)/3
                        x2m = (x + r)/3
                        y1m = (-y+r+5050)/3
                        y2m = (-y-r+5050)/3
                        
                    except:
                        print("issue drawing", line)
                        continue
                    annotator.add_annotation('circle', Location(x1=x1m, y1=y1m-36, x2=x1m+36, 
                                             y2=y1m, page=page_num), 
                                             Appearance(stroke_color=(1, 0, 0),
                                             stroke_width=1))
                    
                    
    #annotator.write(savefname)
    try:
        annotator.write(savefname) # save annotated pdf
    except PermissionError:
        print("[*] Close or delete the old document before running again to annotate.")
        quit()
    return savefname