#Backend (reads and processes the brailled from webcamera input)
import numpy as np
import cv2
import copy
import os

def startCam():
    cam=cv2.VideoCapture(0)
    while True:
        ret, frame=cam.read()
       # ret=cam.set(3,200)
        #ret=cam.set(4,200)
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #print(frame.shape[:2])
        #hsv hue saturation value
        lowerB=np.array([0,0,0])#blue hsv=0 ,140,0 , black hsv=0,0,0
        upperB=np.array([180,255,80])#black hsv=180,255,80, blue hsv=255,255,255
        mask=cv2.inRange(hsv,lowerB,upperB)
        cv2.rectangle(frame,(100,200),(540,400),(255,0,0),2)
        cv2.putText(frame,"Place Braille in the box and press Space to Process. \"ESC\" to quit",(10,50),\
                    cv2.FONT_HERSHEY_SIMPLEX,0.55,(105,105,105),2,cv2.CV_AA)
        #kernel1=np.ones((2,2),np.uint8)                #Experimentation filters that were 
        #erosion=cv2.erode(mask,kernel1,iterations=1)   #not needed 
        #dilation=cv2.dilate(mask,kernel1,iterations=1) #
        #kernel=np.ones((2,2),np.float32)/4             #
        #smoothed=cv2.filter2D(mask,-1,kernel)          #
        #cv2.imshow('frame',frame)                      #
        #cv2.imshow('mask',mask)                        #
        cv2.imshow('camera',frame)
     
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

def findCircles(image):# passes image through a series of filters so that the contour function has a higher success rate
    #a variety of sources helped me implement these series of filters
    allCoord=[]
    #im[im == 255] = 1
    #im[im == 0] = 255
    #im[im == 1] = 0
    im2 = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    grayBlur = cv2.medianBlur(im2, 1)

     # Remove noise before laplacian
    grayLap = cv2.Laplacian(grayBlur, cv2.CV_8UC1, ksize=5)
    dilateLap = cv2.dilate(grayLap, (3, 3))  # Fill in gaps from blurring. fill circles with broken edges

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
           if((h>10 and w>10) and (h<80 and w<80)):#removes obvious noise
                allCoord.append((x,y,w,h))
                #cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                #cv2.imshow('Features', im)
                #cv2.imwrite(str(i)+'.png', im)
        
    return allCoord #list of coords of (upperleft x pos, upper left y pos, width and height) for each dot

def rectIntersection(allCoord):#if bounding boxes overlap get rid of one (avoids double counting)
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

def showCircles(image,finalCoord):# important for debugging and determining accuracy of backend
    
    for i in (finalCoord):
        cv2.rectangle(image,(i[0],i[1]),(i[0]+i[2],i[1]+i[3]),(0,255,0),2)
        cv2.imshow("1",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def merge(left, right,val):#merge sort was implemented from the notes but altered 
    #to be able to sort based on all values in a specific pos in the tuples
    if ((len(left) == 0) or (len(right) == 0)):
        return left+right
    else:
        #print(left[0][val])
        if (int(left[0][val]) < int(right[0][val])):
            return [left[0]] + merge(left[1:], right,val)
        else:
            return [right[0]] + merge(left, right[1:],val)

def mergesort(finalCoord,val): #see above       
    if (len(finalCoord) < 2):
        return finalCoord
    else:
        mid = len(finalCoord)//2
        left = mergesort(finalCoord[:mid],val)
        right = mergesort(finalCoord[mid:],val)
        return merge(left, right,val)

def swap(L,a,b):#basic destructive swap function

    L[a],L[b]=L[b],L[a]

def orderBrailleCorrectly(brailleCoord,refCoords):#has multiple cases if len(hold)==6 easy to process
    #else depending on if there exists a dot with a full set, the ones with imcomplete can be determined 
    #relative to that one otherwise mostlikely user needs to interfere
    hold=mergesort(brailleCoord,1)
    if(len(hold)==6):
        for i in range(0,len(hold),2):
            if(hold[i][0]>hold[i+1][0]):
                swap(hold,i,i+1) 
        return hold
    else:
        for i in range(0,len(hold),2):
            if(i==len(hold)-1):
                break
            if(abs(hold[i][1]-hold[i+1][1])<15):
                
                if(hold[i][0]>hold[i+1][0]):
                    swap(hold,i,i+1)   
                    
       # print(hold,"after proper sorting(should be relatively correct)")
        if(refCoords==None):
            for i in range(6-len(hold)):
                hold.append((-1000,-1000,-1000,-1000))
               
        else:
            hold=orderWithRefCoord(hold,refCoords)    
            #print(hold,"after widthRefCoord")        
    return hold

def orderWithRefCoord(hold,refCoords):#if there exists a set of 6 dots, incomplete sets can be guessed with more accuracy
    #print(refCoords,"refCOords")
    #print(hold,"hold")
    row=[[None],[None],[None]]
    for i in range(len(hold)):
        for j in range(0,3):
            
            if((hold[i][1]-refCoords[2*j][1])<=12):
               # print(refCoords[j][1],j,"refCoords")
                row[j].append(hold[i])
                    
                break
    #print(row,"row")
    for i in range(3):
        if(len(row[i])==3):
            if(row[i][1][0]>row[i][2][0]):
                swap(row[i],1,2)

        elif(len(row[i])==2):
            row[i].append((-1000,-1000,-1000,-1000)) 

        else:
            row[i].append((-1000,-1000,-1000,-10000)) 
            row[i].append((-1000,-1000,-1000,-10000))
        #print(row[i],"row[i]") 
    #print(row,"row")
    return row[0][1:]+row[1][1:]+row[2][1:]

def getPixelValue(image,x,y):
    pixVal=image[y,x]
    return pixVal

def convCoordToStr(image,brailleCoord):
    brailleStrList=[]
    tempstr=''
    refCoords=None
    for i in range(len(brailleCoord)):
        if(len(brailleCoord[i])==6):
            refCoords=copy.deepcopy(brailleCoord[i])
            break
    if(refCoords!=None):
        refCoords=orderBrailleCorrectly(refCoords,None)
    #print()
    for i in range(len(brailleCoord)):
        brailleCoord[i]=orderBrailleCorrectly(brailleCoord[i],refCoords)
        #print(brailleCoord[i],"BrailleCoord[i]")
        for brDot in range(6):
            x,y,width,height=brailleCoord[i][brDot]
            #print(brailleCoord[i][brDot])
            if(x==-1000):
                tempstr+="F"
                
            else:
                
                midx=x+(width/2)
                midy=y+(height/2)
                
                if(getPixelValue(image,midx,midy)[0]==255):
                    tempstr+="T"
                else:
                    tempstr+="F"
            #print(tempstr)
        brailleStrList.append(tempstr)
        tempstr=''

    return brailleStrList

def mapStrToBraille(brailleStrList,constBrailleDict):#debugging purposes
    tempstr=""
    for s in brailleStrList:
        if(s in constBrailleDict):
            tempstr+= constBrailleDict[s]
        else:

            tempstr+= "not a word"
    return tempstr

def splitIntoBraille(finalCoord):#Takes original list and splits it into lists that contain 1 braille char
    splitCoord=[]
    avgdiff=15
    hold=[]
    counter=1
    #print(counter)
    for i in range(1,len(finalCoord)):
        #print(hold)
        if(abs(finalCoord[i][0]-finalCoord[i-1][0])<avgdiff):
            hold.append(finalCoord[i-1])
                
        else:
            #print(counter)
            hold.append(finalCoord[i-1])
            if(counter==2):
                    
                splitCoord.append(hold)
                hold=[]
                counter=1
            else:
                counter+=1


    if(abs(finalCoord[-1][0]-finalCoord[-2][0])<=avgdiff):
        hold.append(finalCoord[-1])
        splitCoord.append(hold)

    else:
        
        hold.append(finalCoord[-1])
        splitCoord.append(hold)
    return splitCoord

def removeFloatingPoints(brailleCoordXSorted):#theory is dots should be arranged pretty much like a grid
    #thus those not on the grid are removed

    brailleCoordXSortedHold=copy.deepcopy(brailleCoordXSorted)
    if(len(brailleCoordXSortedHold)<=1):
        return []
    else:
        hold=[]
        avgdiff=15 #allowable 
        for i in xrange(len(brailleCoordXSortedHold)):
            #print(1)
            if(i==0):
                if(abs(brailleCoordXSortedHold[i+1][0]-brailleCoordXSortedHold[i][0])>avgdiff):
                    if(not checkYCoordsMatch(brailleCoordXSortedHold[i],brailleCoordXSortedHold)):
                        brailleCoordXSortedHold[i]=(-1000,-1000,-1000,-1000)#nondestrucively removes contents
            elif(i==len(brailleCoordXSortedHold)-1):
                if(abs(brailleCoordXSortedHold[i-1][0]-brailleCoordXSortedHold[i][0])>avgdiff):
                    if(not checkYCoordsMatch(brailleCoordXSortedHold[i],brailleCoordXSortedHold)):
                        brailleCoordXSortedHold[i]=(-1000,-1000,-1000,-1000)
            else:
                if(abs(brailleCoordXSortedHold[i-1][0]-brailleCoordXSortedHold[i][0])>avgdiff\
                    and abs(brailleCoordXSortedHold[i+1][0]-brailleCoordXSortedHold[i][0])>avgdiff):
                    if(not checkYCoordsMatch(brailleCoordXSortedHold[i],brailleCoordXSortedHold)):
                         brailleCoordXSortedHold[i]=(-1000,-1000,-1000,-1000)
            #print(brailleCoordXSorted)
    
        #print("hello")
        for i in range(len(brailleCoordXSortedHold)):
            #print("hi")
            if(brailleCoordXSortedHold[i]==(-1000,-1000,-1000,-1000)):
                continue

            else:
                hold.append(brailleCoordXSortedHold[i])
        return hold

def checkYCoordsMatch(checkCoords,brailleCoordXSorted):#checks if dots are aligned on X axis
    avgYDiff=12
    for i in brailleCoordXSorted:
        if(i==checkCoords):
            continue
        else:

            if(abs(i[1]-checkCoords[1])<=avgYDiff and i[1]!=-1000):
                return True
    return False

def removeNoise(brailleCoords):#gets rid of random huge boxes
    hold=[]
    for i in range(len(brailleCoords)):
        if(brailleCoords[i][2]/float(brailleCoords[i][3])>1.6 or brailleCoords[i][3]/float(brailleCoords[i][2])>1.6):
            continue
        else:
            hold.append(brailleCoords[i])
    return hold


#constBrailleDict={"TFFFFF":"A","TFTFFF":"B","TTFFFF":"C","TTFTFF":"D","TFFTFF":"E","TTTFFF":"F",\
#                  "TTTTFF":"G","TFTTFF":"H","FTTFFF":"I","FTTTFF":"J","TFFFTF":"K", "TFTFTF":"L",\
#                  "TTFFTF":"M","TTTTTT":"N","TFFTTF":"O","TTTFTF":"P","TTTTTF":"Q", "TFTTTF":"R",\
#                  "FTTFTF":"S","FTTTTF":"T","TFFFTT":"U","TFTFTT":"V","FTTTFT":"W","TTFFTT":"X",\
#                  "TTFTTT":"Y","TFFTTT":"Z"}
def getText():
    startCam()
    try:
        countW=0
        countB=0
        image=cv2.imread("foo.png")
        image=image[210:390,110:530]
        print("imread")

        cv2.imshow("image",image)
        print("imshow")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("destroyallwindows")
        
        #print('waitkey')

        


        allCoord=findCircles(image)
        finalCoord=rectIntersection(allCoord)
        brailleCoord=mergesort(finalCoord,0)
        #print(brailleCoord)
        brailleCoord=removeFloatingPoints(brailleCoord)
        #print(brailleCoord)
        brailleCoord=removeNoise(brailleCoord)
        #print(brailleCoord)
        #got to get rid of noise check
        splitCoord=(splitIntoBraille(brailleCoord))
        #print(splitCoord)
        #determine if parts are missing
        #showCircles(image,brailleCoord)
        brailleStrList=(convCoordToStr(image,splitCoord))
        #tempstr=mapStrToBraille(convCoordToStr(image,splitCoord),constBrailleDict)

        os.remove("foo.png")
        return brailleStrList
    except:
        print("failed") 
        return None

print(getText())




