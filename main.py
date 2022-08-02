#!/usr/bin/env python

# built in 
import os
import sys
import argparse
import shutil

# 3rd party imports


# import other modules from this project
from cut_surroundings import crop_image
from recognition import recognize_instruments, recognize_sheet_numbers_for_document
import file_conversions
import annotate

__author__ = "Connor DeJohn"
"""
August 2022 

program to look at instruments in p&ids

1. add circles to current pdf (https://github.com/plangrid/pdf-annotate)
2. get txt file of tags
3. get excel file of tags
4. get txt file of sheet -> page relation
"""

def main():
    # instantiate arg parser
    parser = argparse.ArgumentParser(description='command line script to parse p&id')
    parser.add_argument('--source', type=str,
                        help='pdf p&id in working directory that will be parsed')
    parser.add_argument('--flag_inst', action='store_true',
                        help='draw circles around p&id instrument circles in a new pdf')
    parser.add_argument('--sheet2page', action='store_true',
                        help='create sheet and page number listing')
    parser.add_argument('--open', action='store_true',
                        help='open pdf file after generating')
    parser.add_argument('--keep', action='store_true',
                        help='dont delete image files')
                        
    args = parser.parse_args()
    cur_dir = os.getcwd()
    
    # validate input for input file
    if not args.source: # source must be included
        print("[*] A source in the current directory is required")
        quit()
    elif not os.path.splitext(args.source)[1]: # needs file extention - could add handling for this
        print("[*] Please include a file extension on the source")
        quit()
    elif not args.source in [f for f in os.listdir(cur_dir) if os.path.isfile(os.path.join(cur_dir,f))]: # file must exist
        print("[*] The source was not found in the current working directory.")
        quit()
    
    # parse options
    if not args.flag_inst and not args.sheet2page: # some option must be chosen - THIS SHOULD LIST ALL
        print("[*] Please choose an option to execute. Check -h for help")
        quit()
    
    # declare some variables and fld names
    image_source_fldr = os.path.join(cur_dir,"images/") # allows customization and deletion afterwards
    cut_fldr = os.path.join(image_source_fldr, "results/")
    circ_fldr = os.path.join(image_source_fldr, "circles/")
    
    # mkdir if not there, suppresses error if there
    os.makedirs(image_source_fldr, exist_ok=True)
    os.makedirs(cut_fldr, exist_ok=True)
    os.makedirs(circ_fldr, exist_ok=True)
        
    if args.flag_inst:
        # flag instruments in new document
        
        file_conversions.pdf2im(args.source, image_source_fldr) # convert each sheet to an image
        crop_image(image_source_fldr, cut_fldr) # crop each image - will probably be something opposite for 
        recognize_instruments(image_source_fldr, cut_fldr, circ_fldr)
        #circle_file = file_conversions.im2pdf(circ_fldr, args.source) # convert new images to pdf
        circle_file = annotate.draw_circles(circ_fldr, args.source) # annotate original pdf
        
        # delete image folders
        if not args.keep:
            shutil.rmtree(image_source_fldr) 
        
        # open new pdf
        if args.open:
            os.startfile(circle_file)
    elif args.sheet2page:
        
        file_conversions.pdf2im(args.source, image_source_fldr) # convert each sheet to an image
        recognize_sheet_numbers_for_document(image_source_fldr, circ_fldr, args.source) #img_fldr, cut_surroundings_fldr, circle_fldr, ):

    else:
        print("welp nothing else is implemented sooooo")
        quit()
    print("[:)] done") #✓
    
    
    
if __name__ == "__main__":
	# try:
        # main()
    # except:
        # print("[*] Error running")
        # quit()
    main()
    