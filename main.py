#!/usr/bin/env python

# built in 
import os
import sys
import argparse
import shutil

# 3rd party imports


# import other modules from this project
# import p_id_recognition.file_conversions
# import p_id_recognition.recognition
# import p_id_recognition.cut_surroundings
# import p_id_recognition.annotate
from p_id_recognition import file_conversions, recognition, cut_surroundings, annotate

__author__ = "Connor DeJohn"
"""
August 2022 

program to look at instruments in p&ids

1. add circles to current pdf
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
    parser.add_argument('--noannot', action='store_true',
                        help='do not create an annoted pdf, only create an excel report. annotation takes a much longer time')
    parser.add_argument('--sheet2page', action='store_true',
                        help='create sheet and page number listing')
    parser.add_argument('--noexcel', action='store_true',
                        help='dont generate an excel sheet of instruments')
    parser.add_argument('--open', action='store_true',
                        help='open pdf file after generating')
    parser.add_argument('--keep', action='store_true',
                        help='dont delete image files')
                        
    args = parser.parse_args()
    cur_dir = os.getcwd()
    f_dir = os.path.join(cur_dir,"p-ids")
    
    # validate input for input file
    if not args.source: # source must be included
        print("[*] A source in the current directory or p-ids/ is required")
        quit()
    elif not os.path.splitext(args.source)[1]: # needs file extention - could add handling for this
        print("[*] Please include a file extension on the source")
        quit()
    
    # check on pdf file
    pandid_wholefile = ""
    if args.source in [f for f in os.listdir(cur_dir) if os.path.isfile(os.path.join(cur_dir,f))]: # file must exist in cur dir
        # file is in cur_dir
        pandid_wholefile = args.source
    elif args.source in [f for f in os.listdir(f_dir) if os.path.isfile(os.path.join(f_dir,f))]: # check file dir
        # file is in p-ids
        pandid_wholefile = os.path.join(cur_dir,"p-ids",args.source)
    else:
        print("[*] The source was not found in the current working directory or in p-ids.")
        quit()
    
    # parse options
    if not args.flag_inst and not args.sheet2page: # some option must be chosen - THIS SHOULD LIST ALL RECOGNITION OPTIONS
        print("[*] Please choose an option to execute. Check -h for help")
        quit()
    
    # declare some variables and fld names
    image_source_fldr = os.path.join(cur_dir,"images/") # allows customization and deletion afterwards
    crop_fldr = os.path.join(cur_dir,"images/", "cropped/")
    circ_fldr = os.path.join(cur_dir,"images/", "circles/")
    out_fldr = os.path.join(cur_dir, "outs/")
    
    # mkdir if not there, suppresses error if there
    os.makedirs(image_source_fldr, exist_ok=True)
    os.makedirs(crop_fldr, exist_ok=True)
    os.makedirs(circ_fldr, exist_ok=True)
    os.makedirs(out_fldr, exist_ok=True)
    
    # recognition options
    if args.flag_inst: # flag instruments in new document
        
        # convert each pdf sheet to individual images
        file_conversions.pdf2im(pandid_wholefile)
        
        # crop notes out
        #cut_surroundings.crop_image(image_source_fldr, crop_fldr)
        
        # recognize the little circles and and create txt files with their coordinates
        recognition.recognize_instruments(pandid_wholefile, args.noexcel, args.noannot)
        
        # annotation is that longest thing, so give option to just get report
        if not args.noannot:
            # draw little circles around the instruments using the coodinates created in recognize_instruments
            circle_file = annotate.draw_circles(pandid_wholefile) # annotate original pdf
        
        # delete image folders
        if not args.keep:
            shutil.rmtree(image_source_fldr) 
        
        # open new pdf
        if args.open and not args.noannot:
            os.startfile(circle_file)
    elif args.sheet2page: # create a report about the sheet numbers and the page numbers
        
        # convert each pdf sheet to individual images
        file_conversions.pdf2im(pandid_wholefile)
        
        # create either txt or excel report about the sheet to page number linkings
        recognition.recognize_sheet_numbers_for_document(pandid_wholefile, args.noexcel)
        
        # delete image folders
        if not args.keep:
            shutil.rmtree(image_source_fldr) 
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
    