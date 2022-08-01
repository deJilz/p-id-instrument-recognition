import os
import cv2

def crop_image ( file_path , dest_path ) :
    files = os . listdir ( file_path ) # list all the files ' names
    counter = 0
    for file in files :
        # print ( file )
         original_image_name = os . path . join ( file_path , file )
         # dest_image_name = os. path . join ( dest_path , file )
        dest_image_name = dest_path + str( counter ) + '. png '
        if os . path . isfile ( original_image_name ) :
            print ( original_image_name )
            original_image = cv2 . imread ( original_image_name )
            shape = original_image . shape
            h = shape [0] # Y ( height ) = 1786
            w = shape [1] # X ( width ) = 2526
            print ("h = ", h )
            print ("w = ", w )
            cropped_y_start = int( h * 0.3) # y start
            cropped_y_end = int( h * 0.85) # y end
            cropped_x_start = int( w * 0.05) # x start
            cropped_x_end = int( w * 0.95) # x end
            cropped_img = original_image [ cropped_y_start :
            cropped_y_end , cropped_x_start : cropped_x_end ] # crop
            # print ( dest_image_name )
            # cv2. imshow ( ' cropped ', cropped_img )
            # cv2. waitKey ()

            cv2 . imwrite ( dest_image_name , cropped_img ) #
            counter +=1
            # print ( dest_image_name )

if __name__ == '__main__':
    crop_image ('./ Dataset / images /', './ Dataset / images / results /')