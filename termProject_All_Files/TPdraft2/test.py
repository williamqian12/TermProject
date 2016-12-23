#Using hough circle transformation
#so far doesnt work too well
#pros: works well for very clear pictures (usually online .jpgs or .pngs)
#cons: usually a bit of noise, requires a lot of calibration
import cv2
import cv2.cv
import numpy as np
def draw_circles(img, circles):
    #img = cv2.imread(img,0)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    for i in circles[0,:]:
    # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
        cv2.putText(cimg,str(i[0])+str(',')+str(i[1]), (i[0],i[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, 255)
    return cimg

def detect_circles(image_path):
    gray = cv2.imread(image_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    
    gray_blur = cv2.medianBlur(gray, 13)  # Remove noise before laplacian
    gray_lap = cv2.Laplacian(gray_blur, cv2.CV_8UC1, ksize=5)
    dilate_lap = cv2.dilate(gray_lap, (3, 3))  # Fill in gaps from blurring. This helps to detect circles with broken edges.
    # Furture remove noise introduced by laplacian. This removes false pos in space between the two groups of circles.
    lap_blur = cv2.bilateralFilter(dilate_lap, 5, 9, 9)
    
    # Fix the resolution to 16. This helps it find more circles. Also, set distance between circles to 55 by measuring dist in image.
    # Minimum radius and max radius are also set by examining the image.
    circles = cv2.HoughCircles(gray,cv2.cv.CV_HOUGH_GRADIENT,1,20,
                            param1=50,param2=40,minRadius=0,maxRadius=0)
    print(circles)
    cimg = draw_circles(gray, circles)

    print("{} circles detected.".format(circles[0].shape[0]))
    # There are some false positives left in the regions containing the numbers.
    # They can be filtered out based on their y-coordinates if your images are aligned to a canonical axis.
    # I'll leave that to you.
    return cimg
    #cv2.imshow('image',lap_blur)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
im=cv2.imread("test4.jpg")
cv2.imshow('image',im)
cv2.waitKey(0)
cv2.destroyAllWindows()
cimg = detect_circles('test4.jpg')
cv2.imshow('image',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()