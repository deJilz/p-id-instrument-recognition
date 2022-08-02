
# built in
import os

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
            circles = circles1 [0 , : , :]
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