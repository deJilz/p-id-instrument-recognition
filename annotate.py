# built in 
import os
import sys
import argparse
import shutil

# 3rd party imports
from pdf_annotate import PdfAnnotator, Appearance, Location

# import other modules from this project



'''
from pdf_annotate import PdfAnnotator, Appearance, Location

annotator = PdfAnnotator('test.pdf')
annotator.add_annotation(
  'square',
  Location=Location(x1=10, y1=20, x2=100, y2=100, page=0),
  Appearance=Appearance(fill=(1, 0, 0))
)
annotator.write('annotated.pdf')

'''

def draw_circles():
    pass