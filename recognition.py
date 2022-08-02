
# built in
import os
import pathlib

# 3rd party
import numpy as np
import cv2
import pytesseract
import re

# textImgs_path = 'Dataset/images/'
# path_list = os.listdir ( textImgs_path )


def recognize_instruments( img_fldr, cut_surroundings_fldr, circle_fldr, ):
    # 
    all_instruments_counter = 0
    
    
    
    for img_path in [f for f in os.listdir(img_fldr) if os.path.isfile(os.path.join(img_fldr,f))]:#path_list :# [f for f in os.listdir(cur_dir) if os.path.isfile(os.path.join(cur_dir,f))]
        if img_path.split ('.') [ -1] == 'png':
            # name of the image in the folder , e.g. 20
            img_name = img_path.split ('.') [0]

            # the name of the output filefor e.g. image name is 20. png , file name is 20. txt
            #file_path = 'Dataset/images/circles_txt/'+ img_name +'.txt'
            
            file_path = os.path.join(img_fldr,"circles/"+img_name+".txt")
            file = open ( file_path , 'w')
            file.write ('instrument x y r:\n')
            img = cv2.imread ( img_fldr + img_path )
            gray = cv2.cvtColor ( img , cv2.COLOR_BGR2GRAY )

            # Hough Circle Transform with OpenCV
            circles1 = cv2.HoughCircles ( gray , cv2.HOUGH_GRADIENT , 1 , 10 , param1 =100 , param2 =60 , minRadius =40, maxRadius =60)
            try:
                circles = circles1 [0 , : , :]
            except:
                continue
            circles = np.uint16 ( np.around ( circles ) )
            counter = 0

            # draw the detected circles on the original image and show
            for i in circles [:]:
                cv2.circle ( img , ( i [0] , i [1]) , i [2] , (255 , 0 , 255) , 7)
            #cv2.imshow ('detected circles ', img )
            #cv2.waitKey ()
            #cv2.imwrite ( 'Dataset/images/circles/'+ img_name + '.png', img )
            cv2.imwrite (os.path.join(circle_fldr ,img_name + '.png'), img )
            
            for i in circles [:]:
                cv2.circle ( img , ( i [0] , i [1]) , i [2] , (255 , 255 , 255) , 7)

                # filter out the wrongly detected circles
                if i [2] >= 25:
                    counter += 1
                    # generate the candidate area
                    #cropped_image_name = 'Dataset/images/circles/id_' + img_name + '/circle_' + str( counter ) + '.png'
                    cropped_circles = img [( i [1] - i [2]) :( i [1] + i [2]) , ( i [0] - i [2]) :( i [0] + i [2]) ]

                    # use Tesseract
                    cropped_circles_rgb = cv2.cvtColor ( cropped_circles ,cv2.COLOR_BGR2RGB )
                    # Recognition is very sensitive to this configuration
                    custom_config = r'--oem 3 --psm 6'
                    text = pytesseract.image_to_string (cropped_circles_rgb , config = custom_config )
                    
                    
                    # Postprocessing Steps :
                    # 1. write in one line
                    text = text.replace ('\n', '').replace ('\r','')
                    # 2. Uppercase
                    text = text.upper ()
                    # 3. only keep the upper - case abbr and numbers
                    text = re.sub (u" ([^\ u0030 -\ u0039 \u0041 -\ u005a \ u002e])", "", text) # literall what
                    # 4. Some common problem ( specific to this dataset )
                    text = text.replace ('TL ', 'TI ')
                    text = text.replace ('POIE ', 'PDIE ')

                    #print ( text )

                    #cv2.imshow (" circles ", cropped_circles )
                    #cv2.waitKey ()
                    # print ( ' - - - - - - - - - - - - - next circle - - - - - - - - - - - - - - - - - ')
                    file.write ( text +' ') # instrument
                    file.write (str ( i [0]) +' ') # center point x
                    file.write (str ( i [1]) +' ') # center point y
                    file.write (str ( i [2]) +'\n') #r



            all_instruments_counter += counter
            # file.write ('\n')
            # file.write ('detected '+ str(len( circles ) ) + ' circles ' + '\n')
            # file.write ('recognized '+ str( counter ) + ' instruments ' + '\n')
            # file.close ()
            # print ('Image '+ str( img_name ) +' has been written in circle_txt .')
            # print ( ' recognized in this image = ' + str( counter ))

    #print (" Number of recognized instruments in all images :")
    #print ( all_instruments_counter )
    
    
    
def recognize_sheet_numbers( img_fldr, circle_fldr, pandidfname):
    files = os.listdir ( img_fldr ) # list all the files ' names
    counter = 0
    sheet2pagetxt = open ( os.path.join(os.getcwd(),pandidfname + " - SHEET2PAGE.txt") , 'w')
    sheet2pagetxt.write("sheet\t\tpage\n")
    for file in files :
        # print ( file )
        original_image_name = os.path.join ( img_fldr , file )
        # dest_image_name = os. path.join ( dest_path , file )
        # dest_image_name = dest_path + str( counter ) + ".png"
        if os.path.isfile ( original_image_name ) :
            #print ( original_image_name )
            original_image = cv2.imread ( original_image_name )
            shape = original_image.shape
            
             
            h = shape [0] # Y ( height ) = 1786
            w = shape [1] # X ( width ) = 2526
            #print ("h = ", h )
            #print ("w = ", w )
            cropped_y_start = int( h * 0.97) # y start
            cropped_y_end = int( h * 1) # y end
            cropped_x_start = int( w * 0.94) # x start
            cropped_x_end = int( w * 1) # x end
            
            cropped_img = original_image [ cropped_y_start : cropped_y_end , cropped_x_start : cropped_x_end ] # crop
            
            # throw cropped_img into pytesseract and get sheet text
            # for circle text - text = pytesseract.image_to_string (cropped_circles_rgb , config = custom_config )
            #cv2.imshow (" cropped ", cropped_img )
            #cv2.waitKey ()
            
            
            text = pytesseract.image_to_string ( cropped_img ) # get text from image
            text = text.replace (' ', '').replace ('SHEET','').replace('\n','') # replace dumb stuff
            
            page_num = int(pathlib.Path(file).stem.split(" ")[-1])# get image page number
            #sheet2pagetxt.write(text + "\t\t" + str(page_num) + "\n") # write to file
            sheet2pagetxt.write("{:<12s}{:<10s}\n".format(text, str(page_num)))