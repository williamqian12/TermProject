#exploits masking/thresholding to create clear binary images
#uses boundboxes which seem to be more accurate than hough circle transformation
#some noise but can easily be taken out
#calibration required 
#file dedicated to all the backend stuff
#IMPROVEMENTS: BACKEND MAIN ALGORITHM FAIRLY CLOSE TO BEING COMPLETED
#SOME ADJUSTMENTS MAY BE NEEDED LATER ON IN THE PROJECT
#IF THERES EXTRA TIME COULD ATTEMPT TO SELF RIGHT SOME OF THE FILTERS ETC
#TRY TO MAKE IT VIDEO RATHER THAN SNAPSHOTS
#ALSO COULD CONVERT TO BINARY IMAGE FROM THE START
#ALSO IF READING IN THE DOTS ISNT TOO ACCURATE COULD HAVE MANUAL FILL INS
import numpy as np
import cv2
import copy
import os
cam=cv2.VideoCapture(0)
while True:
    ret, frame=cam.read()
   # ret=cam.set(3,200)
    #ret=cam.set(4,200)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #print(frame.shape[:2])
    #hsv hue saturation value
    lowerB=np.array([0,107,0])#blue hsv=0 ,107,0 , black hsv=0,0,0
    upperB=np.array([255,255,255])#black hsv=180,255,80, blue hsv=255,255,255
    mask=cv2.inRange(hsv,lowerB,upperB)
    cv2.rectangle(mask,(100,200),(540,400),(255,0,0),2)
    #kernel1=np.ones((2,2),np.uint8)
    #erosion=cv2.erode(mask,kernel1,iterations=1)
    #dilation=cv2.dilate(mask,kernel1,iterations=1)
    #kernel=np.ones((2,2),np.float32)/4
    #smoothed=cv2.filter2D(mask,-1,kernel)    
    #cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    cv2.imshow('camera',mask)
 
    k=cv2.waitKey(5)& 0xFF

    if (k%256==27):#esc key
        break
    elif (k%256 == 32):
        # space key
        imagePath = "foo.png"
        cv2.imwrite(imagePath, mask)
        print("written!")
        break
        
cv2.destroyAllWindows()
cam.release()
def findCircles(image):
    allCoord=[]
    #im[im == 255] = 1
    #im[im == 0] = 255
    #im[im == 1] = 0
    im2 = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    grayBlur = cv2.medianBlur(im2, 1)

     # Remove noise before laplacian
    grayLap = cv2.Laplacian(grayBlur, cv2.CV_8UC1, ksize=5)
    dilateLap = cv2.dilate(grayLap, (3, 3))  # Fill in gaps from blurring. fill circles with broken edges

    # Furture remove noise introduced by laplacian. This removes false pos in space between the two groups of circles DONT NEED THIS
    #lap_blur = cv2.bilateralFilter(dilate_lap, 5, 9, 9)
    ret,thresh = cv2.threshold(dilateLap,127,255,cv2.THRESH_BINARY)

    #gaus=cv2.adaptiveThreshold(im2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,115,1)
    #cv2.imshow("1",thresh)
    #cv2.imshow('2',gaus)
    #cv2.waitKey(0)
    #

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #print(hierarchy)
    allCoord=[]
    for i in range(len(contours)):
        if (i % 2 == 0):#otherwise cant extract boundingRect
           count = contours[i]
           #print(len(count))
           #mask = np.zeros(im2.shape,np.uint8)
           #cv2.drawContours(mask,[cnt],0,255,-1)
           x,y,w,h = cv2.boundingRect(count)
           if(h>10 and w>10):
                allCoord.append((x,y,w,h))
                #cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                #cv2.imshow('Features', im)
                #cv2.imwrite(str(i)+'.png', im)
        
    return allCoord
#TODO:improve getting rid of noise function
def rectIntersection(allCoord):
    hold=[]
    for i in range(len(allCoord)):
        if(allCoord[i]!=None):
            for j in range(i+1,len(allCoord)):
                if((allCoord[i][0]<=allCoord[j][0]  and allCoord[i][0]+allCoord[i][2]>=allCoord[j][0]+allCoord[j][2]) and\
                   (allCoord[i][1]<=allCoord[j][1]  and allCoord[i][1]+allCoord[i][3]>=allCoord[j][1]+allCoord[j][3])):
                    allCoord[j]=None #deletes coord w/out affecting size of list
                    
                elif((allCoord[i][0]>=allCoord[j][0]  and allCoord[i][0]+allCoord[i][2]<=allCoord[j][0]+allCoord[j][2]) and\
                     (allCoord[i][1]>=allCoord[j][1]  and allCoord[i][1]+allCoord[i][3]<=allCoord[j][1]+allCoord[j][3])):
                    allCoord[i]=None

                    
    for i in range(len(allCoord)):
        if(allCoord[i]!=None):
            hold.append(allCoord[i])
    return ((hold))

def showCircles(image,finalCoord):
    
    for i in (finalCoord):
        cv2.rectangle(image,(i[0],i[1]),(i[0]+i[2],i[1]+i[3]),(0,255,0),2)
        cv2.imshow("1",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def merge(left, right,val):
    if ((len(left) == 0) or (len(right) == 0)):
        return left+right
    else:
        #print(left[0][val])
        if (int(left[0][val]) < int(right[0][val])):
            return [left[0]] + merge(left[1:], right,val)
        else:
            return [right[0]] + merge(left, right[1:],val)

def mergesort(finalCoord,val):        
    if (len(finalCoord) < 2):
        return finalCoord
    else:
        mid = len(finalCoord)//2
        left = mergesort(finalCoord[:mid],val)
        right = mergesort(finalCoord[mid:],val)
        return merge(left, right,val)
#merge sort
#interleave
def splitIntoBraille(finalCoord):
    splitCoord=[]
    numOfChar=len(finalCoord)/6
    for i in range(1,numOfChar+1):
        splitCoord.append(finalCoord[(i-1)*6:i*6])
    return splitCoord

def swap(L,a,b):
    L[a],L[b]=L[b],L[a]

def orderBrailleCorrectly(brailleCoord):
    hold=mergesort(brailleCoord,1)
    for i in range(0,len(hold),2):
        if(hold[i][0]>hold[i+1][0]):
            swap(hold,i,i+1)
    return hold

def getPixelValue(image,x,y):
    pixVal=image[y,x]
    return pixVal


def convCoordToStr(image,brailleCoord):
    brailleStrList=[]
    tempstr=''
    for i in range(len(brailleCoord)):
        brailleCoord[i]=orderBrailleCorrectly(brailleCoord[i])
        for brDot in range(6):
            x,y,width,height=brailleCoord[i][brDot]
            midx=x+(width/2)
            midy=y+(height/2)
            #print(midx,midy)
            if(getPixelValue(image,midx,midy)[0]==255):
                tempstr+="T"
            else:
                tempstr+="F"
        brailleStrList.append(tempstr)
        tempstr=''
    return brailleStrList



def mapStrToBraille(brailleStrList,constBrailleDict):
    for s in brailleStrList:
        if(s in constBrailleDict):
            print constBrailleDict[s],
        else:
            print "not a word",
#def checkStr(brailleCoord)
#    convCoordToStr(brailleCoord)
#    check in dictionary
#    return the letter


constBrailleDict={"TFFFFF":"A","TFTFFF":"B","TTFFFF":"C","TTFTFF":"D","TFFTFF":"E","TTTFFF":"F",\
                  "TTTTFF":"G","TFTTFF":"H","FTTFFF":"I","FTTTFF":"J","TFFFTF":"K", "TFTFTF":"L",\
                  "TTFFTF":"M","TTTTTT":"N","TFFTTF":"O","TTTFTF":"P","TTTTTF":"Q", "TFTTTF":"R",\
                  "FTTFTF":"S","FTTTTF":"T","TFFFTT":"U","TFTFTT":"V","FTTTFT":"W","TTFFTT":"X",\
                  "TTFTTT":"Y","TFFTTT":"Z"}
try:
    countW=0
    countB=0
    image=cv2.imread("foo.png")
    for i in range(210,390):
        for j in range(110,530):
            if(image[i,j][0]==255):
                countW+=1
            else:
                countB+=1
    print(countW/float(countB))#NOTE: doesnt seem to be a useful
    image=image[210:390,110:530]

    cv2.imshow("1",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    allCoord=findCircles(image)
    finalCoord=rectIntersection(allCoord)
    brailleCoord=mergesort(finalCoord,0)
    splitCoord=(splitIntoBraille(brailleCoord))

    (mapStrToBraille(convCoordToStr(image,splitCoord),constBrailleDict))

    showCircles(image,brailleCoord)

    try: 
        os.remove("foo.png")
    except: pass
except: pass


#'''


#TODO
#,run tests on noise to see approx the ratio of white to black at which point i should ignore the thing completely




