#FrontEnd for Braille Program

from Tkinter import *
import tkFont
import math
import random
from backendDraft2 import *
import decimal
from PIL import ImageTk,Image
#from PIL import Image
#from gameMode import*
################################################
#Functions to be used by entire program 
################################################

def constInit(data):
    data.statsDictPracticeRead={"Best Score":0,"Worst Score":10000,"Average Score":0,"Easy":0,"Med":0,"Hard":0}
    data.totalNumOfPracticeRead=0
    data.totalScoreRead=0
    data.statsDictPracticeTrans={"Best Score":0,"Worst Score":10000,"Average Score":0,"Easy":0,"Med":0,"Hard":0}
    data.totalNumOfPracticeTrans=0
    data.totalScoreTrans=0
    data.statsDictGame={"Games Played":0,"Wins":0,"Losses":0,"Least Guesses":10000,"Char Solved Per Guess":0}
    data.totalChar=0
    data.totalTriesNeg=0  
    data.constBrailleDict={"TFFFFF":"A","TFTFFF":"B","TTFFFF":"C","TTFTFF":"D","TFFTFF":"E","TTTFFF":"F",\
                           "TTTTFF":"G","TFTTFF":"H","FTTFFF":"I","FTTTFF":"J","TFFFTF":"K", "TFTFTF":"L",\
                           "TTFFTF":"M","TTFTTF":"N","TFFTTF":"O","TTTFTF":"P","TTTTTF":"Q", "TFTTTF":"R",\
                           "FTTFTF":"S","FTTTTF":"T","TFFFTT":"U","TFTFTT":"V","FTTTFT":"W","TTFFTT":"X",\
                           "TTFTTT":"Y","TFFTTT":"Z","FFFFFF":" "}
    data.backgroundStr=''
    data.backgroundCounter=0
    HelpInit(data)
    
    
    #image.resize

def init(data):
    TranslateInit(data)
    PracticeInit(data)
    GameInit(data)
    data.webcamBraille=''
    data.tempBrailleStr="FFFFFF"
    data.mode="MainMenu"
    data.str=""
    data.check=True
    data.webcamBrailleList=[]
    
def mutableInit(data):

    data.MainBox=(data.width/30,data.height/50,data.width*15/100,data.height/10)

def roundHalfUp(d):#taken from notes
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def sizeChanged(event,data):#scaling of the window, taken from tkinterdemos

    data.width = event.width - 4
    data.height = event.height - 4

def checkBounds(coords,pointX,pointY):
    if((coords[0]<=pointX and pointX<=coords[2]) and (coords[1]<=pointY and \
        pointY<=coords[3])):
        return True
    else:
        return False #determines of mouse is in given bounds

def drawButton(canvas,coords,text,fill):
    (XS,YS,XE,YE)=coords
    width=XE-XS
    height=YE-YS
    canvas.create_rectangle(XS,YS,XE,YE,outline="black",fill="gray30",width=0)
    canvas.create_rectangle(XS+width/15,YS,XE-width/15,YE,fill=fill,width=0)
    canvas.create_text((XS+XE)/2,(YS+YE)/2,text=text,font="Calibri %d"%(0.4*(YE-YS)))#draws a button given specific text. also scalable

def checkInCircle(cx,cy,radius,x,y):#returns true if in circle, else false
    if(distanceOfPoints(cx,cy,x,y)<=radius):
        return True
    else:
        return False

def distanceOfPoints(x1,y1,x2,y2): #return distance between two points

    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def drawBraille(canvas,brailleStr,coords):
    (XS,YS,XE,YE)=coords
    width=XE-XS
    height=YE-YS
    if(3/(2.0)*width>=height):
        width=roundHalfUp(height*(0.8))
    else:
        height=roundHalfUp((1.6)*width)
    dotCoord=templateBraille(XS,YS,XS+width,YS+height)
    if((3/(2.0))*width>=height):
        radius=height//8
    else:
        radius=width/6
    #print(dotCoord,1)
    for i in range(6):
        if(brailleStr[i]=="T"):
            fill="black"
        else:
            fill="white"
        canvas.create_oval(dotCoord[i][0]-radius,dotCoord[i][1]-radius,\
            dotCoord[i][0]+radius,dotCoord[i][1]+radius,fill=fill,width=1.5)

def checkManualBrailleInput(data,coords,pointx,pointy):#universal function when there is mouseinput it will update the tempbraillestr
    (XS,YS,XE,YE)=coords
    width=XE-XS
    height=YE-YS
    if(3/(2.0)*width>=height):
        width=roundHalfUp(height*(0.8))
    else:
        height=roundHalfUp((1.6)*width)
    dotCoord=templateBraille(XS,YS,XS+width,YS+height)   
    if((3/(2.0))*width>=height):
        radius=height//8

    else:
        radius=width/6
    
    #print(dotCoord,2)
    for circle in range(6):
        if(checkInCircle(dotCoord[circle][0],dotCoord[circle][1],radius,pointx,pointy)):
            if(data.tempBrailleStr[circle]=="T"):

                data.tempBrailleStr=data.tempBrailleStr[:circle]+"F"+data.tempBrailleStr[circle+1:]

            else:
                data.tempBrailleStr=data.tempBrailleStr[:circle]+"T"+data.tempBrailleStr[circle+1:]

def drawBrailleString(canvas,data,stringList,coords):
    (XS,YS,XE,YE)=coords
    width=XE-XS
    height=YE-YS

    for i in range(len(stringList)):
        bounds=(XS+width*(i+1)/(len(stringList)+2),YS+height/10,XS+width*(i+2)/((len(stringList)+2)),YE)
        drawBraille(canvas,stringList[i],bounds)

def findBrailleStr(data,char):#finds the brailleStr given the char

    for key in data.constBrailleDict:
        if(data.constBrailleDict[key]==char.upper()):
            return key
    return "FFFFFF"#goes through the dictionary to map char to its key

def drawManualBrailleUI(canvas,data,coords):

    drawBraille(canvas,data.tempBrailleStr,coords)#replace with variables#the circles

def templateBraille(XS,YS,XE,YE): 
    #return array with coords#returns list of 6 circles centres for each braille block
    dotCoord=[]
    for i in range(1,4):
        for j in range(1,3):
            dotCoord.append((j*(XE-XS)//3+XS,i*(YE-YS)//4+YS))
    return dotCoord

def getBrailleList(data,string): # returns list of braille strings given eng str
    temp=[]
    for i in string:
        temp.append(findBrailleStr(data,i))
    return temp

def checkCorrectingBrailleString(data,coords,stringList,pointx,pointy):
    (XS,YS,XE,YE)=coords
    width=XE-XS
    height=YE-YS

    for i in range(len(stringList)):
        bounds=(XS+width*(i+1)/(len(stringList)+2),YS+height/10,XS+width*(i+2)/\
            ((len(stringList)+2)),YE)
        data.tempBrailleStr=stringList[i]
        checkManualBrailleInput(data,bounds,pointx,pointy)
        stringList[i]=data.tempBrailleStr
    print(stringList)
    return stringList

def drawText(canvas,x,y,anchor,fontSize,text): #draws the inputed alphanum text

    canvas.create_text(x,y,text=text,anchor=anchor,font="Calibri %d"%(fontSize))#edit

def basicKeyAnalysis(data,char,cursor=0):#Analyzes keyboard input
    
    cursor+=1
    if(len(char)==1):
       data.str+=char

        #data.cursorXOffset= data.font.measure(data.str)
    if(char=="space"):
        data.str+=" "
        #data.cursorXOffset+=data.font.measure(" ")

    elif(char=="BackSpace" and len(data.str)>=1):
        #print("hi")
        #print(data.str,"Its right")
        if(data.str[-1]=="\n" and data.str[-2]==" "):
            data.str=data.str[:-2]
           # print("slash n")
        else:
            data.str=data.str[:-1]

        cursor-=2
    elif(char=="Tab"):
        data.str+="    "
        cursor+=1
    elif(char=="Return"):
        data.str+="\n"

def getAlphaString(data,brailleList):#gets alphatext from braille string
    tempstr=''
    for i in brailleList:
        if(i in data.constBrailleDict):
            tempstr+=data.constBrailleDict[i]
    return tempstr

###############################################

def moveMouse(event,data):
    print("moveMouse")
    if(data.mode=="Practice"): PracticeMoveMouse(event,data)
    else:
        pass

def mousePressed(event, data):#taken from notes but altered
    print("mousePressed")
    if(checkBounds((data.MainBox),event.x,event.y) and data.mode!="MainMenu"):
        
        data.mode="MainMenu"
    elif(data.mode=="MainMenu"):MainMenuMousePressed(event,data)
    elif(data.mode=="Translate"):TranslateMousePressed(event,data)
    elif(data.mode=="Practice"): PracticeMousePressed(event,data)
    elif(data.mode=="Stats"): StatsMousePressed(event,data)
    elif(data.mode=="Game"): GameMousePressed(event,data)
    elif(data.mode=="Help"): HelpMousePressed(event,data)
    # use event.x and event.y
    pass

def keyPressed(event, data):
    print("keypressed")
    if(data.mode=="MainMenu"):MainMenuKeyPressed(event,data)
    elif(data.mode=="Translate"):TranslateKeyPressed(event,data)
    elif(data.mode=="Practice"): PracticeKeyPressed(event,data)
    elif(data.mode=="Stats"): StatsKeyPressed(event,data)
    elif(data.mode=="Game"): GameKeyPressed(event,data)
    elif(data.mode=="Help"):  HelpTKeyPressed(event,data)
    # use event.char and event.keysym
    pass

def timerFired(data):
    print("timer")
    if(data.mode=="MainMenu" or data.mode=="Stats" or data.mode=="Help"):
        if(data.backgroundCounter<=360):
            data.backgroundStr+=chr(ord("a")+random.randint(0,25))
            
        else:
            data.backgroundStr=data.backgroundStr[:data.backgroundCounter%360]+chr(ord("a")+\
                random.randint(0,25))+data.backgroundStr[data.backgroundCounter%360+1:]
        data.backgroundCounter+=1
    if(data.mode=="MainMenu"):MainMenuTimerFired(data)
    elif(data.mode=="Translate"):TranslateTimerFired(data)
    elif(data.mode=="Practice"): PracticeTimerFired(data)
    elif(data.mode=="Stats"): StatsTimerFired(data)
    elif(data.mode=="Game"):  GameTimerFired(data)
    elif(data.mode=="Help"):  HelpTimerFired(data)
    pass

def rgbString(red, green, blue):#taken from notes

    return "#%02x%02x%02x" % (red, green, blue)

def drawBackground(canvas,data):#draws gradient background
    for i in range(35):
        canvas.create_rectangle(0,i*data.height/35,data.width,\
        (i+1)*data.height/35,width=0,fill=rgbString(154-35+i,192-35+i,205-35+i))

def redrawAll(canvas,data):
    print("draw4")

    mutableInit(data)
    drawBackground(canvas,data)
    #canvas.create_rectangle(0,0,data.width,data.height,fill="lightBlue3",width=0)

    if(data.mode=="MainMenu"  or data.mode=="Stats" or data.mode=="Help"):
       for i in range(len(data.backgroundStr)):
            backgroundBox=(data.width*(i%30)/(31), data.height*(i/30)/12,\
                    data.width*(i%30+1)/(31), data.height*(i/30+1)/10)
        #pass
            drawBraille(canvas,findBrailleStr(data,data.backgroundStr[i]),backgroundBox)
    if(data.mode!="MainMenu"):
        drawButton(canvas,(data.MainBox),"Main","beige")
    if(data.mode=="MainMenu"): 
        init(data)
        MainMenuRedrawAll(canvas,data)
    elif(data.mode=="Translate"): TranslateRedrawAll(canvas,data)
    elif(data.mode=="Practice"): PracticeRedrawAll(canvas,data)
    elif(data.mode=="Stats"): StatsRedrawAll(canvas,data)
    elif(data.mode=="Game"): GameRedrawAll(canvas,data)
    elif(data.mode=="Help"): HelpRedrawAll(canvas,data)
    print("stilldrawing 3")
   
    

###############################################
#MainMenu
###############################################

def MainMenuInit(data):
    data.transBox=(2*data.width/7,data.height*5/15,5*data.width/7,data.height*6/15)
    data.pracBox=(data.width*2/7,data.height*7/15,5*data.width/7,data.height*8/15)
    data.gameBox=(data.width*2/7,data.height*9/15,data.width*5/7,data.height*10/15)
    data.statsBox=(data.width*2/7,data.height*11/15,data.width*5/7,data.height*12/15)
    data.helpBox=(data.width*2/7,data.height*13/15,data.width*5/7,data.height*14/15)

def MainMenuMousePressed(event,data):
    if(checkBounds(data.transBox,event.x,event.y)):
        data.mode="Translate"
    elif(checkBounds(data.pracBox,event.x,event.y)):
        data.mode="Practice"
    elif(checkBounds(data.statsBox,event.x,event.y)):
        data.mode="Stats"
    elif(checkBounds(data.gameBox,event.x,event.y)):
        data.mode="Game"
    elif(checkBounds(data.helpBox,event.x,event.y)):
        data.mode="Help"
    pass

def MainMenuKeyPressed(event,data):#no keyboard input on this page

    pass

def MainMenuTimerFired(data):# no timer needed on this page

    pass

def drawMainMenuTitle(canvas,data):

    canvas.create_text(data.width/2,data.height/5,text="e-Braille!", \
                        font="Calibri %d bold"%(0.07*data.width),fill="beige")

def MainMenuRedrawAll(canvas,data):
    MainMenuInit(data)
    drawMainMenuTitle(canvas,data)
    drawButton(canvas,data.transBox,"Translate",rgbString(250,232,240))
    drawButton(canvas,data.pracBox,"Practice",rgbString(240,229,230))
    drawButton(canvas,data.gameBox,"Game",rgbString(235,226,220))
    drawButton(canvas,data.statsBox,"Stats",rgbString(230,223,210))
    
    drawButton(canvas,data.helpBox,"Help/About",rgbString(220,220,200))
    pass



###################################
#Translate
###################################


def TranslateInit(data):
    data.transMode="AlphanumToBraille"
    data.cursorYOffset=0
    data.cursorXOffset=0
    data.cursorBlink=True
    data.cursorLocation=0 #location relative to data.str index 
    data.holdStr=[] #holds the string when text goes off screen
    #edit#initialization that only needed for init page
    data.drawBrailleCheck=True
    data.transBrailleAuxStr=''
    data.transTimer=0
    
def TranslateMutable(data):
    if(data.width<data.height):
        data.fontSize=data.width/20
    else:
        data.fontSize=data.height/20

    data.font=tkFont.Font(family="Calibri",size=data.fontSize)

    data.cursorX=data.width*1/15
    data.cursorY=data.height*2/16

    data.switchButtonBox=(data.width*10/12,data.height*1/60,data.width*49/50,data.height*1/10)
    data.translateManualBrailleBox=(data.width*2/7,data.height*1/40,data.width*5/7,data.height*4/7)
 
    data.editorXS=data.width*1/20
    data.editorXE=data.width*19/20
    data.editorYS=data.height*2/17
    data.editorYE=data.height*1/2  

    data.translateContWordBox=(data.width*1/5,data.height*1/6,data.width*2/5,data.height*1/4)
    data.translateNewWordBox=(data.width*3/5,data.height*1/6,data.width*4/5,data.height*1/4)
    data.translateManualBox=(data.width*1/5,data.height*1/6,data.width*2/5,data.height*1/4)
    data.translateWebcamBox=(data.width*3/5,data.height*1/6,data.width*4/5,data.height*1/4)
    data.webcamBrailleBox=(data.width*1/5,data.height*5/18,data.width*4/5,data.height*49/100)

def drawTranslationEditorBox(canvas,data):
    canvas.create_rectangle(data.editorXS+data.width*1/8,data.height*1/15,\
                        data.editorXS+data.width*2/7,data.editorYS,width=2,fill="white")
    canvas.create_text(data.editorXS+data.width*15/100,data.height*1/11,\
                anchor="w",text="Input",font="calibri %d italic"%(data.height/30))
    canvas.create_rectangle(data.editorXS,data.editorYS,data.editorXE,\
                            data.editorYE,fill="white",width=2)
    canvas.create_line(data.editorXS+data.width*1/8+data.width*1/500,data.editorYS,\
        data.editorXS+data.width*2/7-data.width*1/500,data.editorYS,width=2,fill="white")

    if(data.cursorBlink):#edit
        canvas.create_line(data.cursorX+data.cursorXOffset,\
                        data.cursorY+data.cursorYOffset+data.height*14/10000,\
        data.cursorX+data.cursorXOffset,data.cursorY+data.fontSize+data.cursorYOffset+data.height*1/70,\
                            fill="black",width=2)

def drawTranslationBox(canvas,data): #draws the box where either translated braille or alphanum goes

    canvas.create_rectangle(data.editorXS,data.editorYS+data.height*3/7,\
        data.editorXE,data.editorYE+data.height*3/7,fill="white",width=2)

def drawTranslatedText(canvas,data):
    canvas.create_text(data.editorXS+data.width*1/80,data.editorYS+data.height*3/7, text=data.str,\
                        anchor=NW,font="Calibri %d"%(data.fontSize))
                        #for alphanum to braille will #Braille to alpha num shows result textstr

def drawTranslationBraille(canvas,data):#when theres only a couple char, they are scaled appropriately, otherwise they are drawn consistently
    editorBoxWidth=data.editorXE-data.editorXS
    editorBoxHeight=data.editorYE-data.editorYS
    if(len(data.str)>20 or data.str.find("\n")!=-1):
        data.drawBrailleCheck=False
    if(data.drawBrailleCheck==True):
        for i in range(len(data.str)):
            if(data.str[i]==" "):#no need to draw braille
                continue
            else:
                editorBox=(data.editorXS+editorBoxWidth*(i+1)/(len(data.str)+2),\
                           data.editorYS+data.height*3/7,\
                           data.editorXS+editorBoxWidth*(i+2)/((len(data.str)+2)),\
                           data.editorYE+data.height*3/7)
                drawBraille(canvas,findBrailleStr(data,data.str[i]),editorBox)
    else:
        newline=0
        tempStr=removeConsecutiveSpaces(data.str)
        auxStr=''
        if(len(tempStr)>100):
            if(len(tempStr)-len(data.transBrailleAuxStr)>=100):
                data.transBrailleAuxStr=tempStr[:len(tempStr)-80]
                tempStr=tempStr[len(tempStr)-80:]
            else:
                tempStr=tempStr[len(data.transBrailleAuxStr)-1:]
        for i in range(len(tempStr)):
            if(tempStr[i]==" "):
                continue
            else:
                editorBox=(data.editorXS+editorBoxWidth*(i%20)/(21), \
                    data.editorYS+(data.height*3/7)+editorBoxHeight*(i/20)/5,\
                    data.editorXS+editorBoxWidth*(i%20+1)/((21)),\
                    data.editorYS+(data.height*3/7)+editorBoxHeight*(i/20+1)/5)
                drawBraille(canvas,findBrailleStr(data,tempStr[i]),editorBox)

def getEndOfString(string):#gets location of last \n
    tempStr=string[::-1]
    tempStr=tempStr[:tempStr.find("\n")]
    tempStr=tempStr[::-1] 
    return tempStr

def removeConsecutiveSpaces(string):
    tempList=string.split(' ')
    tempStr=''
    for a in tempList:
        if(len(a)>0):
            tempStr+=a+" "
    return tempStr.strip() 

def getTranslatedOffsets(data):#detemines location of cursor

    if(data.str.find("\n")!=-1):
        tempStr=getEndOfString(data.str)

        data.cursorXOffset=data.font.measure(tempStr)
    else:
        data.cursorXOffset=data.font.measure(data.str)
 
    data.cursorYOffset=data.str.count("\n")*(data.fontSize+data.height/30)

    #check if text needs to be wrapped
    if(data.cursorXOffset>=(data.editorXE-data.editorXS-data.width/70)):
        tempStr=data.str[::-1]
        lastSpace=len(data.str)-tempStr.find(" ")
        tempStr=tempStr[:tempStr.find(" ")]
        if(len(tempStr)<25):
            data.str=data.str[:lastSpace]+len(tempStr)*" "+"\n"+ data.str[lastSpace:]
        else:
            data.str=data.str[:-1]+"\n"+data.str[-1]
        getTranslatedOffsets(data)

    if(data.cursorYOffset>=(data.editorYE-data.editorYS-data.fontSize*2)):
        tempStr=data.str[:data.str.find("\n")+1]
        data.holdStr.append(tempStr)#stack like object
        #print(data.holdStr,1)
        data.str=data.str[data.str.find("\n")+1:]
        getTranslatedOffsets(data)

    #check if line needs to be placed back
    if(data.cursorYOffset+data.fontSize+data.height/30<=\
    (data.editorYE-data.editorYS-2*data.fontSize) and len(data.holdStr)>0):

        data.str=data.holdStr.pop()+data.str

        getTranslatedOffsets(data)


################################################

def TranslateKeyPressed(event,data):
    if(data.transMode=="AlphanumToBraille"):
        basicKeyAnalysis(data,event.keysym,data.cursorLocation)
        #cursorAnalysis(data,event.keysym)
        #if(char=="Return"):
         #   data.str+="\n"
        getTranslatedOffsets(data)

    elif(data.transMode.find("BrailleToAlphaNum")):

        if(data.transMode.find("Manual")!=-1):
            width=data.editorXE-data.editorXS
            if(data.str.find("\n")!=-1):
                tempStr=getEndOfString(data.str)
                if(data.font.measure(tempStr)+data.fontSize>=width):
                    data.str+='\n'
            elif(data.font.measure(data.str)+data.fontSize>=width):
                data.str+='\n'
            if(event.keysym=="Return"):
                if(data.tempBrailleStr in data.constBrailleDict):
                    data.str+=data.constBrailleDict[data.tempBrailleStr]
                data.tempBrailleStr="FFFFFF"
        else:
            if(event.keysym=="Return"):
                data.str+=getAlphaString(data,data.webcamBrailleList)
                data.webcamBrailleList=[]
        if(event.keysym=="BackSpace" and len(data.str)>=1):
            data.str=data.str[:-1]

def TranslateMousePressed(event,data):
    if(checkBounds(data.switchButtonBox,event.x,event.y)):
        if(data.transMode=="AlphanumToBraille"):
            data.str=""
            data.transMode="BrailleToAlphanum"

        else:
            data.str=''
            data.transMode="AlphanumToBraille"

    elif(data.transMode.find("BrailleToAlphanum")!=-1):

        if(data.transMode.find("Manual")!=-1):
            checkManualBrailleInput(data,data.translateManualBrailleBox,event.x,event.y)

        elif(data.transMode.find("Webcam")!=-1):#needs editing
            
            if(checkBounds(data.translateContWordBox,event.x,event.y)):
                data.webcamBraille=''
                try:
                    data.webcamBrailleList+=getText()

                except:
                    print("failedstorestr")
                    
                #data.webcamBrailleList=getBrailleList(data,data.webcamBraille)
            elif(checkBounds(data.translateNewWordBox,event.x,event.y)):
                if(len(data.str)>0):
                    data.webcamBrailleList.append("FFFFFF") 
                try:
                    data.webcamBrailleList+=getText()
                    print(data.webcamBrailleList)
                    print(getAlphaString(data,data.webcamBrailleList))
                except:
                    pass
            checkCorrectingBrailleString(data,data.webcamBrailleBox,\
                                        data.webcamBrailleList,event.x,event.y)


        else:

            if(checkBounds(data.translateManualBox,event.x,event.y)):
                data.transMode="BrailleToAlphanumManual"#choose your option

            elif(checkBounds(data.translateWebcamBox,event.x,event.y)):
                
                data.transMode="BrailleToAlphanumWebcam"
              #  go to that option

def TranslateTimerFired(data):
    data.transTimer+=data.timerDelay
    if(data.transTimer%500==0):
        if(data.cursorBlink):
            data.cursorBlink=False
        else:
            data.cursorBlink=True#only needed to simulate cursor blink

def TranslateRedrawAll(canvas,data):
    print("still drawing")
    TranslateMutable(data)
    #scalability
    drawTranslationBox(canvas,data)
    drawButton(canvas,data.switchButtonBox,"","beige")
    if(data.transMode=="AlphanumToBraille"):
        drawTranslationEditorBox(canvas,data)
        drawBrailleString(canvas,data,getBrailleList(data,"AB"),data.switchButtonBox)
        drawText(canvas,data.cursorX,data.editorYS,"nw",data.fontSize,data.str)
        drawTranslationBraille(canvas,data)

    elif(data.transMode.find("BrailleToAlphanum")!=-1):
        data.cursorXOffset=0
        data.cursorYOffset=0
        drawButton(canvas,data.switchButtonBox,"ABC","beige")
        if(data.transMode.find("Manual")!=-1):


            drawManualBrailleUI(canvas,data,data.translateManualBrailleBox)

        elif(data.transMode.find("Webcam")!=-1):

            canvas.create_rectangle(data.webcamBrailleBox,fill="beige",width=2)
            drawButton(canvas,data.translateContWordBox,"ABC___","beige")#shows option for manual input
            drawBrailleString(canvas,data,data.webcamBrailleList,data.webcamBrailleBox)
            drawButton(canvas,data.translateNewWordBox,"ABC  __","beige")#shows option for webcam

        else:
            drawButton(canvas,data.translateManualBox,"Manual","beige")#shows option for manual input
            drawButton(canvas,data.translateWebcamBox,"Webcam","beige")#shows option for webcam
        

        drawTranslatedText(canvas,data)
        print("stilldrawing 2")

##################################################
#Practice
##################################################

def PracticeInit(data):
    data.timerRead=60
    data.timerTrans=120
    data.score=0
    data.countTime=0
    data.colourLeft="light green"
    data.colourRight="lightBlue3"
    data.pracMode="Practice"
    data.readBrailleEasy='A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,'
    data.readBrailleMed="HI,HE,IS,OR,TO,OF,IN,IT,GO,UP,SO,ON,DO,AT,AS,BY,MY,IF,US,OH,SHE,THE,FOR,NOR,BUT,AND,"
    data.readBrailleHard="HELLO,WORLD,WORD,NOT,BRAILLE,LOUIS,CMU,PYTHON,STRING,LIST,QUIZ,OPEN,CLOSE,STAND,SPEED,QUEUE,STACK"#make up more later
    data.ProbEasy=70
    data.ProbMed=20
    data.ProbHard=10
    data.pracTextAnsColor="white"
    data.colorTime=0
    data.pracCountdownColor="beige"

def PracticeMutable(data):
    data.practiceManualBrailleBox=(data.width*35/100,data.height*65/100,\
                                    data.width*2/3,data.height*97/100)
    data.practiceManualBox=(data.width*1/5,data.height*2/3,data.width*2/5,data.height*3/4)
    data.practiceWebcamBox=(data.width*3/5,data.height*2/3,data.width*4/5,data.height*3/4)
    data.practiceContWordBox=(data.width*1/5,data.height*2/3,data.width*2/5,data.height*3/4)
    data.practiceNewWordBox=(data.width*3/5,data.height*2/3,data.width*4/5,data.height*3/4)
    data.practiceBrailleBox=(data.width/10,data.height/6,data.width*9/10,data.height*2/4)
    data.timerCoord=(data.width*23/30,data.height/20)
    data.timerScoreBox=(data.width*45/60,data.height/31,data.width*49/50,\
                        data.height*1/15+data.height*1/20+2*data.width*1/30)
    data.scoreCoord=(data.width*23/30,data.height/30+data.height*1/20+data.width*1/35)
    data.pracBrailleDisplayBox=(data.width/8,data.height*1/2,data.width*7/8,\
                                data.height*62/100)
    
def drawPracticeChoice(canvas,data):# the menu to choose which practice mode
    canvas.create_rectangle(0,0,data.width/2,data.height,fill=data.colourLeft,width=0)
    canvas.create_rectangle(data.width/2,0,data.width,data.height,fill=data.colourRight,width=0)
    canvas.create_line(data.width/2,0,data.width/2,data.height,width=3)

def drawPracticeChoiceText(canvas,data): 
    canvas.create_text(data.width/4,data.height/2, text="Read Braille",font="Calibri %d "%(data.width/20))
    canvas.create_text(data.width*3/4,data.height/2, text="Translate Braille",font="Calibri %d"%(data.width/20))

def getNumOfWords(dictStr):#returns a num of words in the database
    counter=0
    for c in dictStr:
        if(c==","):
            counter+=1
    return counter

def findWord(dictStr,wordIndex):#returns the word in the database
    counter=0
    word=''
    for c in dictStr:
        if(counter-1==wordIndex):
            return word 
        elif(counter==wordIndex and c!=","):
            word+=c
        if(c==','):
            counter+=1
    return word

def getWord(dictStr):#gets a rando word from the database
    numCommas=getNumOfWords(dictStr)
    wordIndex=random.randint(0,numCommas-1)
    word=findWord(dictStr,wordIndex)
    
    return word

def PracticeChooseWord(data):# based on progress will choose from which database to extract from
    randNum=random.randint(0,100)
    if(randNum<data.ProbEasy):
        word=getWord(data.readBrailleEasy)
    elif(randNum<data.ProbEasy+data.ProbMed):
        word=getWord(data.readBrailleMed)
    else:   #hard
        word=getWord(data.readBrailleHard)
    print(word)
    return word

def drawPracticeBrailleWord(canvas,data,word):
    brailleStringList=getBrailleList(data,word)
    drawBrailleString(canvas,data,brailleStringList,data.practiceBrailleBox)
   
def checkIfCorrect(data):
    if(data.word==data.str.upper()):
        #data.str=''
        data.score+=1
        if(data.ProbEasy!=0):
            data.ProbEasy-=len(data.word)
            data.ProbMed+=roundHalfUp(len(data.word)*2/3)
            data.ProbHard+=len(data.word)-roundHalfUp(len(data.word)*2/3)
        else:
            data.ProbHard+=roundHalfup(len(data.word)*2/3)
            data.ProbMed-=roundHalfup(len(data.word)*2/3)
        data.check=True
        data.pracTextAnsColor="light green"
    else:
        data.pracTextAnsColor="IndianRed1"

def drawTimerAndScore(canvas,data,time):
    canvas.create_rectangle(data.timerScoreBox,fill="grey30",width=0)
    canvas.create_rectangle(data.timerScoreBox[0],data.timerScoreBox[1]+data.height*1/100,data.timerScoreBox[2],data.timerScoreBox[3]-data.height*1/100,fill=data.pracCountdownColor,width=0)
    font="Calibri %d "
    if(time%60<10):
        canvas.create_text(data.timerCoord,text="Timer: %d:0%d"%(time/60,time%60),anchor="nw",font=font%(data.width/30))
    else:
        canvas.create_text(data.timerCoord,text="Timer: %d:%d"%(time/60,time%60),anchor="nw",font=font%(data.width/30))
    if(data.score<10):
        canvas.create_text(data.scoreCoord,anchor="nw",text="Score: 0%d"%(data.score),font=font%(data.width/35))
    else:
        canvas.create_text(data.scoreCoord,anchor="nw",text="Score: %d"%(data.score),font=font%(data.width/35))

def updatePracticeRead(data):
    data.totalNumOfPracticeRead+=1
    data.totalScoreRead+=data.score
    if(data.statsDictPracticeRead["Best Score"]<data.score):
        data.statsDictPracticeRead["Best Score"]=data.score
    if(data.statsDictPracticeRead["Worst Score"]>data.score):
        data.statsDictPracticeRead["Worst Score"]=data.score
    data.statsDictPracticeRead["Average Score"]=data.totalScoreRead/float(data.totalNumOfPracticeRead)
        
def updatePracticeTrans(data):
    data.totalNumOfPracticeTrans+=1
    data.totalScoreTrans+=data.score
    if(data.statsDictPracticeTrans["Best Score"]<data.score):
        data.statsDictPracticeTrans["Best Score"]=data.score 
    if(data.statsDictPracticeTrans["Worst Score"]>data.score):
        data.statsDictPracticeTrans["Worst Score"]=data.score
    data.statsDictPracticeTrans["Average Score"]=data.totalScoreRead/float(data.totalNumOfPracticeRead)      

########################################################

def PracticeMoveMouse(event,data):
    if(data.pracMode=="Practice"):
        if(event.x<data.width/2):
            data.colourLeft="light green"
            data.colourRight="lightBlue3"
        elif(event.x>data.width/2):
            data.colourLeft="lightBlue3"
            data.colourRight="light green"

def PracticeMousePressed(event,data):
    if(data.pracMode=="Practice"):
        if(checkBounds((0,0,data.width/2,data.height),event.x,event.y)):
            data.pracMode="PracticeRead"
        elif(checkBounds((data.width/2,0,data.width,data.height),event.x,event.y)):
            data.pracMode="PracticeTranslate"

    elif(data.pracMode.find("PracticeTranslate")!=-1):
        if(data.pracMode.find("Manual")!=-1):
            checkManualBrailleInput(data,data.practiceManualBrailleBox,event.x,event.y)
            
        elif(data.pracMode.find("Webcam")!=-1):#needs editing
            if(checkBounds(data.practiceContWordBox,event.x,event.y)):
                data.webcamBrailleList+=getText()
            elif(checkBounds(data.practiceNewWordBox,event.x,event.y)):
                
                if(len(data.str)>=1):
                    data.webcamBrailleList.append("FFFFFF") 
                try:
                    data.webcamBrailleList+=getText()

                except:
                    pass
            checkCorrectingBrailleString(data,data.pracBrailleDisplayBox,data.webcamBrailleList,event.x,event.y)
            pass
        else:
            if(checkBounds(data.practiceManualBox,event.x,event.y)):
                data.pracMode="PracticeTranslateManual"#choose your option
            elif(checkBounds(data.practiceWebcamBox,event.x,event.y)):
                data.pracMode="PracticeTranslateWebcam"

def PracticeKeyPressed(event,data):
    if(data.pracMode.find("Read")!=-1):
        if(len(event.keysym)==1):
            data.str+=event.keysym
        elif(event.keysym=="BackSpace" and len(data.str)>=1):
            data.str=data.str[:-1]

        if(event.keysym=="Return"):
            checkIfCorrect(data)

    elif(data.pracMode.find("Translate")!=-1):
        if(event.keysym=="Return" ):
            if(data.pracMode.find("Webcam")!=-1):
                data.str+=getAlphaString(data,data.webcamBrailleList)
                checkIfCorrect(data)
                data.webcamBrailleList=[]
            if(data.tempBrailleStr=="FFFFFF"):
                checkIfCorrect(data)
                
            else:
                if(data.tempBrailleStr in data.constBrailleDict):
                    data.str+=data.constBrailleDict[data.tempBrailleStr]
                data.tempBrailleStr="FFFFFF"
        if(event.keysym=="BackSpace" and (len(data.str)>=1 or len(data.webcamBrailleList)>0)) :
            data.str=data.str[:-1]
            data.webcamBrailleList=data.webcamBrailleList[:-1]

def PracticeTimerFired(data):
    data.countTime+=data.timerDelay
    if(data.pracTextAnsColor!="white"):
        data.colorTime+=data.timerDelay
        
        if(data.colorTime%500==0):
            data.pracTextAnsColor="white"
        
            data.colorTime=0
        elif(data.colorTime%250==0):
            data.str=''
    if(data.countTime%1000==0):
        if(data.pracMode.find("Read")!=-1):
            if(data.timerRead==0):
                data.pracMode="Practice"
                updatePracticeRead(data)
                #data.timerRead=5
                data.score=0
                data.mode="Stats"
            else:
                if(data.timerRead<=10):
                    data.pracCountdownColor="IndianRed1"
                elif(data.timerRead<=20):
                    data.pracCountdownColor="gold2"
                data.timerRead-=1
        elif(data.pracMode.find("Translate")!=-1):
            if(data.timerTrans==0):
                data.pracMode="Practice"
                updatePracticeTrans(data)
                #data.timerTrans=10
                data.score=0
                data.mode="Stats"
            else:
                if(data.timerTrans<=10):
                    data.pracCountdownColor="IndianRed1"
                elif(data.timerTrans<=20):
                    data.pracCountdownColor="gold2"
                data.timerTrans-=1
    pass

def PracticeRedrawAll(canvas,data):
    PracticeMutable(data)
    if(data.check==True):
            data.word=PracticeChooseWord(data)
           # print(data.word)
            data.check=False

    if(data.pracMode.find("Read")!=-1):
        
        drawPracticeBrailleWord(canvas,data,data.word)
        #checkIfCorrect(canvas,word,data)
        canvas.create_rectangle(data.width/8,data.height*4/6,data.width*7/8,\
                            data.height*5/6,fill=data.pracTextAnsColor,width=2)
        drawText(canvas,data.width/2,data.height*3/4,None,data.width/15,data.str)
        drawTimerAndScore(canvas,data,data.timerRead)
        canvas.create_rectangle(data.width/8,data.height*61/100,data.width*3/10,\
            data.height*4/6,fill=data.pracTextAnsColor,width=2)
        canvas.create_line(data.width/8+data.width/500,data.height*2/3,\
            data.width*3/10-data.width/500,data.height*2/3,fill=data.pracTextAnsColor,width=2)
        canvas.create_text(data.width*16/100,data.height*127/200,anchor="w",text="Input",\
            font="Calibri %d italic"%(data.height/30))

    elif(data.pracMode.find("Translate")!=-1):
        drawTimerAndScore(canvas,data,data.timerTrans)

        drawText(canvas,data.width/2,data.height*4/14,None,data.width/10,data.word)
        canvas.create_rectangle(data.width/8,data.height*1/2,data.width*7/8,\
                        data.height*62/100,fill=data.pracTextAnsColor,width=2)
        canvas.create_rectangle(data.width/8,data.height*45/100,data.width*3/10,\
            data.height*1/2,fill=data.pracTextAnsColor,width=2)
        canvas.create_line(data.width/8+data.width/500,data.height*1/2,\
            data.width*3/10-data.width/500,data.height*1/2,fill=data.pracTextAnsColor,width=2)
        canvas.create_text(data.width*16/100,data.height*47/100,anchor="w",text="Input",\
            font="Calibri %d italic"%(data.height/30))

        if(data.pracMode.find("Manual")!=-1):
            drawBrailleString(canvas,data,getBrailleList(data,data.str),\
            (data.width/8,data.height*1/2,data.width*7/8,data.height*62/100))

            drawManualBrailleUI(canvas,data,data.practiceManualBrailleBox)

        elif(data.pracMode.find("Webcam")!=-1):
            drawBrailleString(canvas,data,data.webcamBrailleList,\
            (data.width/8,data.height*1/2,data.width*7/8,data.height*62/100))

            drawButton(canvas,data.practiceContWordBox,"AB___","white") 
            drawButton(canvas,data.practiceNewWordBox,"AB   ___","white")

        else:
            drawButton(canvas,data.practiceManualBox,"Manual","white")#need 
            drawButton(canvas,data.practiceWebcamBox,"Webcam","white")

    else:


        drawPracticeChoice(canvas,data)
        drawPracticeChoiceText(canvas,data)


#####################################################
#Stats
#####################################################

def StatsInit(data):
    data.StatsPracticeReadBox=(data.width/3,data.height/7,data.width*2/3,data.height*2/7)
    data.StatsPracticeTransBox=(data.width/3,data.height*3/7,data.width*2/3,data.height*4/7)
    data.StatsGameBox=(data.width/3,data.height*5/7,data.width*2/3,data.height*6/7)

def drawStatsPracticeRead(canvas,data):
    height=data.height/7
    canvas.create_text(data.width/6,data.height/7,anchor="w",text="Reading",font="calibri %d bold"%(data.height/27))
    canvas.create_text(data.width/6,height/3+data.height*15/100,anchor="w",text="Best Score: "+\
        str(data.statsDictPracticeRead["Best Score"]),font="calibri %d"%(data.height/32))
    if(data.statsDictPracticeRead["Worst Score"]==10000):
        canvas.create_text(data.width/6,height*2/3+data.height*15/100,anchor="w",text="Worst Score: "\
                            ,font="calibri %d"%(data.height/32))
    else:
        canvas.create_text(data.width/6,height*2/3+data.height*15/100,anchor="w",text="Worst Score: "\
                            +str(data.statsDictPracticeRead["Worst Score"])\
                            ,font="calibri %d"%(data.height/32))
    canvas.create_text(data.width/6,height+data.height*15/100,anchor="w",\
        text="Average Score: "+str(data.statsDictPracticeRead["Average Score"])\
                        ,font="calibri %d"%(data.height/32))

def drawStatsPracticeTrans(canvas,data):
    height=data.height/7
    canvas.create_text(data.width/6,data.height*42/100,anchor="w",text="Translating",\
                        font="calibri %d bold"%(data.height/29))
    canvas.create_text(data.width/6,height/3+data.height*43/100,anchor="w",text="Best Score: "+\
        str(data.statsDictPracticeTrans["Best Score"]),font="calibri %d"%(data.height/32))
    if(data.statsDictPracticeTrans["Worst Score"]==10000):
        canvas.create_text(data.width/6,height*2/3+data.height*43/100,anchor="w",text="Worst Score:",\
                            font="calibri %d"%(data.height/32))
    else:
        canvas.create_text(data.width/6,height*2/3+data.height*43/100,anchor="w",text="Worst Score: "\
                            +str(data.statsDictPracticeTrans["Worst Score"])\
                            ,font="calibri %d"%(data.height/32))
    canvas.create_text(data.width/6,height+data.height*43/100,anchor="w",text="Average Score: "\
                        +str(data.statsDictPracticeTrans["Average Score"])\
                        ,font="calibri %d"%(data.height/32))

def drawStatsGame(canvas,data):
    height=data.height/7
    canvas.create_text(data.width/6,data.height*69/100,anchor="w",text="Game Stats",\
                        font="calibri %d bold"%(data.height/29))
    canvas.create_text(data.width/6,height*15/100+data.height*72/100,anchor="w",\
                        text="Games Played: "+str(data.statsDictGame["Games Played"]),\
                        font="calibri %d"%(data.height/32))
    canvas.create_text(data.width/6,height*45/100+data.height*72/100,anchor="w",\
                        text="Wins: "+str(data.statsDictGame["Wins"])\
                        ,font="calibri %d"%(data.height/32))
    canvas.create_text(data.width/6,height*72/100+data.height*72/100,anchor="w",\
                        text="Losses: "+str(data.statsDictGame["Losses"])\
                        ,font="calibri %d"%(data.height/32))
    if(data.statsDictGame["Least Guesses"]==10000):
        canvas.create_text(data.width/6,height+data.height*72/100,anchor="w",\
                            text="Least Guesses: ",font="calibri %d"%(data.height/32))
    else:
        canvas.create_text(data.width/6,height+data.height*72/100,anchor="w",\
                            text="Least Guesses: " +str(data.statsDictGame["Least Guesses"])\
                            ,font="calibri %d"%(data.height/32))

######################################################

def StatsMousePressed(event,data):

    pass

def StatsKeyPressed(event,data):#not necessary

    pass

def StatsTimerFired(data):#not necessary

    pass

def StatsRedrawAll(canvas,data):
    canvas.create_line(data.width*38/100,data.height/44,data.width*43/100,data.height*92/1000,width=4,fill="white smoke")
    canvas.create_line(data.width*57/100,data.height/44,data.width*62/100,data.height*92/1000,width=4,fill="white smoke")
    canvas.create_text(data.width/2,data.height/18,text="Stats",font="calibri %d bold italic"%(data.height/20),fill="white smoke")
    canvas.create_rectangle((data.width/7,data.height/9,data.width*9/10,data.height*35/100),fill="beige",width=4,outline="gray30")
    canvas.create_rectangle(data.width/7,data.height*38/100,data.width*9/10,data.height*63/100,fill="beige",width=4,outline="gray30")
    canvas.create_rectangle((data.width/7,data.height*66/100,data.width*9/10,data.height*90/100),fill="beige",width=4,outline="gray30")
    drawStatsPracticeRead(canvas,data)
    drawStatsPracticeTrans(canvas,data)
    drawStatsGame(canvas,data)
    #canvas.create_text(data.width/2,data.height/2,text="Stats",font="calibri %d"%(data.height/30))
    


#################################
#Game Mode
##################################

def GameInit(data):
    data.GameMode="GameTitle"
    data.numOfPlayers=1
    data.boardSize="Easy"
    data.difficultyString=["Easy","Med","Hard","Super"]
    GameTitleInit(data)
    #Game1PlayerInit(data)
    data.gameOver=False
    #data.playerTurn=1
    
    data.tempBrailleStr="FFFFFF"
    # load data.xyz as appropriate
    pass

def make2dList(rows,cols):#taken form notes
    board=[]
    for row in range(rows): board += [[0]*cols]
    return board

def updateGame(data):
    data.totalChar=len(data.word)*6
    data.totalTriesNeg+=data.triesNeg
    
    data.statsDictGame["Games Played"]+=1
    if(data.statsDictGame["Least Guesses"]>data.triesNeg):
        data.statsDictGame["Least Guesses"]=data.triesNeg 
    if(data.tries==0):
        data.statsDictGame["Losses"]+=1
    else:
        data.statsDictGame["Wins"]+=1
    data.triesNeg=0

################################################
def GameMousePressed(event, data):
    if(data.GameMode=="GameTitle"): GameTitleMousePressed(event,data)
    elif(data.GameMode=="Game1Player"): Game1PlayerMousePressed(event,data)
    # use event.x and event.y
    pass

def GameKeyPressed(event, data):
    if(data.GameMode=="GameTitle"): GameTitleKeyPressed(event,data)
    elif(data.GameMode=="Game1Player"): Game1PlayerKeyPressed(event,data)
    pass

def GameTimerFired(data):
    if(data.GameMode=="GameTitle"): GameTitleTimerFired(data)
    elif(data.GameMode=="Game1Player"): Game1PlayerTimerFired(data)
    pass

def GameRedrawAll(canvas, data):
    if(data.gameOver==True): 
        updateGame(data)
        data.mode="Stats"
    if(data.GameMode=="GameTitle"): GameTitleRedrawAll(canvas,data)
    elif(data.GameMode=="Game1Player"): Game1PlayerRedrawAll(canvas,data)
    pass


#############################################
#Game Title
#############################################
#box to determine num of players
#box to determine easy med hard

def GameTitleInit(data):
    data.titleX=data.width/2
    data.titleY=data.height*1/9
    data.titleStr="Braille BattleShip!"
    data.playerBox=[(data.width/5,data.height/4,data.width*2/5,data.height/3),\
    ((data.width*3/5,data.height/4,data.width*4/5,data.height/3))]

    data.difficultyBox=[(data.width*5/100,data.height*6/10,data.width*20/100,data.height*7/10),\
            (data.width*30/100,data.height*6/10,data.width*45/100,data.height*7/10),\
            (data.width*55/100,data.height*6/10,data.width*70/100,data.height*7/10),\
            (data.width*80/100,data.height*6/10,data.width*95/100,data.height*7/10)]

def drawInstructions(canvas,data):

    Instructions='''
In this game a word, in braille, is hidden and scrambled 
on the grid. Like battleship. At the top a the topic of 
the hidden word is given in braille. You will have limited
attempts to reveal the tiles and to  guess the word 
                                    Good luck!
                '''
    canvas.create_text(data.width/2,data.height/3,\
                        text=Instructions,font="calibri %d"%(data.height/35))

def GameTitleMousePressed(event,data):
    #for i in range(len(data.playerBox)):
     #   if(checkBounds(data.playerBox[i],event.x,event.y)):
      #      data.numOfPlayers=i+1
    for i in range(len(data.difficultyBox)):
        if(checkBounds(data.difficultyBox[i],event.x,event.y)):
            data.boardSize=data.difficultyString[i]
        
    #print(data.numOfPlayers,data.boardSize)
    pass

def GameTitleKeyPressed(event,data):
    if(event.keysym=="Return"):
        data.GameMode="Game%dPlayer"%(data.numOfPlayers)
        Game1PlayerInit(data)
    #print(data.GameMode)
    pass

def GameTitleTimerFired(data):

    pass

def GameTitleRedrawAll(canvas,data):
    GameTitleInit(data)
    canvas.create_text(data.titleX,data.titleY,text=data.titleStr,\
                        font="Calibri %d bold" %(data.height/15)) #title

    drawInstructions(canvas,data)
    for i in range(len(data.difficultyBox)):
        if(data.boardSize==data.difficultyString[i]):
            drawButton(canvas,data.difficultyBox[i],data.difficultyString[i],"light green")
        else:
            drawButton(canvas,data.difficultyBox[i],data.difficultyString[i],"beige")    
    canvas.create_rectangle(data.width*65/100,data.height*80/100,data.width*85/100,\
                            data.height*9/10,fill="beige",width=4,outline="gray30")
    canvas.create_polygon((data.width*85/100,data.height*75/100),\
        (data.width*85/100,data.height*95/100),(data.width*97/100,data.height*85/100),\
                            fill="beige",width=4,outline="gray30")
    canvas.create_line(data.width*85/100,data.height*80/100+data.height/200,\
        data.width*85/100,data.height*90/100-data.height/200,width=4,fill="beige")
    canvas.create_text(data.width*8/10,data.height*85/100,text="\"Enter\" to start",\
                        font="Calibri %d"%(data.height/30))
    #draw arrow

################################################
#1PlayerMode
################################################
def Game1PlayerInit(data):
    if(data.boardSize=="Easy"):
        data.size=6
    elif(data.boardSize=="Med"):
        data.size=8
    elif(data.boardSize=="Hard"):
        data.size=10
    else:
        data.size=20
    data.boardWord=make2dList(data.size,data.size) #stores the backend of the board/0 is nothing/1 is unfilled circle 2 is filled circle
    data.boardShow=make2dList(data.size,data.size) #stores whether the cell has been clicked or not
    data.gameTextAnsColor="white"
    data.place=False
    data.guessStr=''
    data.Game1PlayerInput=''
    data.wordBankEasy={"PET":("CAT","DOG"),"PERSON":("DAD","MOM"),"TRAVEL":("CAR",),"COLOR":("RED","TAN")}
    data.wordBankMed={"NAMES":("ALEX","EMMA","JACK","WILL","KEVIN"),"COLOR":("BLUE","CYAN","GREY","NAVY"),"PERSON":("KING","MAID")}
    data.wordBankHard={"NAMES":("ARTHUR","JESSICA","JUSTIN","HILLARY","ANDREW"),"COLOR":("ORANGE","VIOLET","PURPLE","MAROON"),"JOB":("FARMER","LAWYER")}
    data.wordBankSuper={"SCHOOL":("CARNEGIE MELLON UNIVERSITY",)}
    data.word="DOG"
    data.hint="PET"
    data.triesNeg=0
    data.gameColorTime=0
    data.countdownColor="beige"

def Game1PlayerInitMutable(data):
    data.Game1PlayerManualBox=(data.width/5,data.height*89/100,data.width*2/5,\
                                data.height*49/50)
    data.Game1PlayerWebcamBox=(data.width*3/5,data.height*89/100,data.width*4/5,\
                                data.height*49/50)
    data.Game1PlayerInputBox=(data.width/3,data.height*89/100,data.width*2/3,\
                                data.height*49/50)
    data.Game1PlayerManualBrailleBox=(data.width*3/7,data.height*89/100,\
                                        data.width*4/7,data.height)
    data.marginY=data.height/10
    data.Game1PlayerBrailleDisplayBox=(data.width*1/5,data.height*78/100,\
                                        data.width*4/5,data.height*87/100)
 
def drawBoard(canvas,data):
    for row in range(len(data.boardShow)):
        for col in range(len(data.boardShow[0])):
            if(data.boardShow[row][col]==0):
                drawCell(canvas,data,row,len(data.boardShow),col,\
                            len(data.boardShow[0]),"grey")
            elif(data.boardShow[row][col]==1):
                drawCell(canvas,data,row,len(data.boardShow),col,\
                            len(data.boardShow[0]),"white")
                drawInCell(canvas,data,row,len(data.boardShow),col,\
                            len(data.boardShow[0]))

def convStrToList(str):#Takes "FFFFFF" makes [["F","F"],["F","F"],["F","F"]]
    temp=[]
    final=[]
    for char in str:
        temp.append(char)
        if(len(temp)==2):
            final.append(temp)
            temp=[]
    return final

def rotateList(L):#to inc randomness, braille char are rotated 
    newList=make2dList(len(L[0]),\
                    len(L))
                    
    for row in range(len(L[0])):
        for col in range(len(L)-1,-1,-1):
            newList[row][len(L)-1-col]=L[col][row]

    return newList
       
def placeWord(word,data):#places words randomly
    for char in word:
        brailleStr=findBrailleStr(data,char)
        brailleList=convStrToList(brailleStr)
        numOfRotations=random.randint(0,3)
        for i in range(numOfRotations):
            brailleList=rotateList(brailleList)
       # print(brailleList)    
        randRow=random.randint(0,len(data.boardWord)-1)
        randCol=random.randint(0,len(data.boardWord[0])-1)

        while(isLegal(randRow,randCol,brailleList,data.boardWord)==False):
            numOfRotations=random.randint(0,3)
            for i in range(numOfRotations):
                brailleList=rotateList(brailleList)
           # print(brailleList)    
            randRow=random.randint(0,len(data.boardWord)-1)
            randCol=random.randint(0,len(data.boardWord[0])-1)
        placeLetter(randRow,randCol,brailleList,data.boardWord)
       # print(randRow,randCol)
    return data.boardWord

def placeLetter(row,col,L,board):#places the braille char
    for i in range(row,row+len(L)):
        for j in range(col,col+len(L[0])):
            if(L[i-row][j-col]=="T"):
                board[i][j]=2
            else:
                board[i][j]=1

def isLegal(row,col,L,board):#checks whether braille char can be placed 
    if(row+len(L)>len(board) or col+len(L[0])>len(board[0])):
        return False
    for checkrow in range(row,row+len(L)):
        for checkcol in range(col,col+len(L[0])):
            if(board[checkrow][checkcol]!=0):
                return False

    return True

def drawInCell(canvas,data,row,rows,col,cols):#if the cell is part of a braille word u draw this
    (XS,YS,XE,YE)=getCell(data,row,rows,col,cols)
    if(data.boardWord[row][col]==1):
        canvas.create_oval(XS,YS,XE,YE,width=2)
    elif(data.boardWord[row][col]==2):
        canvas.create_oval(XS,YS,XE,YE,fill="black")

def drawCell(canvas,data,row,rows,col,cols,color):#create each cell
    (XS,YS,XE,YE)=getCell(data,row,rows,col,cols)
    width=XE-XS
    height=YE-YS
    canvas.create_rectangle(XS,YS,XE,YE,fill="black")
    canvas.create_rectangle(XS+1,YS+1,XE-1,YE-1,fill=color)
    if(color!="white"):
        canvas.create_rectangle(XS+width/10,YS+height/10,XE-width/10,YE-height/10,\
                                fill="light grey",width=0)
        #canvas.create_rectangle(XS+width/5,YS+height/5,XE-width/5,YE-height/5,fill="white smoke",width=0)

    pass

def getCell(data,row,rows,col,cols):#gets the coords for given cell
    if(data.width>=data.height):
        dimension=data.height
    else:
        dimension=data.width
    marginX=(data.width-dimension*2/3)/2
    rowHeight =  (dimension) *2/3/ rows
    columnWidth = (dimension)*2/3/ cols
    XS = marginX + col * columnWidth
    XE = marginX + (col+1) * columnWidth
    YS = data.marginY + row * rowHeight
    YE =data.marginY + (row+1) * rowHeight
    return (XS,YS,XE,YE) 

def chooseWord(data):#select word from database
    if(data.boardSize=="Easy"):
        dataBank=data.wordBankEasy
    elif(data.boardSize=="Med"):
        dataBank=data.wordBankMed
    elif(data.boardSize=="Hard"):
        dataBank=data.wordBankHard
    else:
        dataBank=data.wordBankSuper
    randint=random.randint(0,len(dataBank)-1)
    counter=0
    for key in dataBank:
        if(counter==randint):
            data.hint=key
            break
        else:
            counter+=1
    word=dataBank[data.hint][(random.randint(0,len(dataBank[data.hint])-1))]
    return word

def drawBrailleWord(canvas,data,string,coords): #draws given braille WOrd
    (XS,YS,XE,YE)=coords
    numChar=len(string)
    for i in range(len(string)):
        XSC=i*(XE-XS)/(numChar)+XS
        XEC=(i+1)*(XE-XS)/(numChar)+XS
        brailleStr=findBrailleStr(data,string[i])
        drawBraille(canvas,brailleStr,(XSC,YS,XEC,YE))

def drawTries(canvas,data):#draw remaining attempts left
    canvas.create_rectangle(data.width/100,data.height*49/50-data.height/9-data.height*1/20,\
                            data.width/6, data.height*49/50,fill="gray30")
    canvas.create_rectangle(data.width/100,data.height*49/50-data.height/9-data.height*1/20+data.height/100,\
        data.width/6, data.height*49/50-data.height/100,fill=data.countdownColor,width=0)
    
    canvas.create_text(data.width/50,data.height*49/50-data.height/40-data.height*1/20,\
        text="Attempts\nLeft:", anchor="sw",font="calibri %d bold"% (data.height/40))
    canvas.create_text(data.width/50,data.height*49/50,text=str(data.tries),\
                        anchor="sw",font="calibri %d"%(data.height/20))

##############################################

def Game1PlayerMousePressed(event,data):
    for row in range(len(data.boardWord)):
        for col in range(len(data.boardWord[0])):
            coords=getCell(data,row,len(data.boardWord),col,len(data.boardWord[0]))
            if(checkBounds(coords,event.x,event.y)):
                if(data.boardShow[row][col]==0):
                    data.tries-=1
                    data.triesNeg+=1
                data.boardShow[row][col]=1
                #print(data.boardWord[row][col])

    if(data.Game1PlayerInput=="Manual"):
        checkManualBrailleInput(data,data.Game1PlayerManualBrailleBox,event.x,event.y)
    elif(data.Game1PlayerInput=="Webcam"):
        if(checkBounds(data.Game1PlayerInputBox,event.x,event.y)):
            try:
                data.webcamBrailleList+=getText()

            except:
                pass
       # print(data.webcamBrailleList)
        checkCorrectingBrailleString(data,(data.width*1/5,data.height*77/100,data.width*4/5,data.height*87/100),data.webcamBrailleList,event.x,event.y)
    else:
        if(checkBounds(data.Game1PlayerManualBox,event.x,event.y)):
            data.Game1PlayerInput="Manual"#choose your option

        elif(checkBounds(data.Game1PlayerWebcamBox,event.x,event.y)):
                
            data.Game1PlayerInput="Webcam"
    pass

def Game1PlayerKeyPressed(event,data):

    if(event.keysym=="BackSpace" and (len(data.guessStr)>0 or \
        len(data.webcamBrailleList)>0)):
        data.guessStr=data.guessStr[:-1]
        data.webcamBrailleList=data.webcamBrailleList[:-1]

    if(data.Game1PlayerInput=="Manual"):
        if(event.keysym=="Return"):
            if(data.tempBrailleStr=="FFFFFF"):
                if(data.guessStr==data.word):
                    data.gameOver=True

                else:
                    data.tries-=1
                    data.triesNeg+=1
                   # print("hello World")
                    data.gameTextAnsColor="orange red"

            else:
                if(data.tempBrailleStr in data.constBrailleDict):
                    data.guessStr+=data.constBrailleDict[data.tempBrailleStr]
            data.tempBrailleStr="FFFFFF"
        
    elif(data.Game1PlayerInput=="Webcam" and event.keysym=="Return"):
        data.guessStr=getAlphaString(data,data.webcamBrailleList)
        if(data.guessStr==data.word):
                data.gameOver=True
        else:
            data.tries-=1
            data.triesNeg+=1
            data.gameTextAnsColor="IndianRed1"

    if(data.tries/float(data.size**2)<=0.1):
        data.countdownColor="IndianRed1"

    elif((data.tries/float(data.size**2)<=0.3)):
        data.countdownColor="gold2"

def Game1PlayerTimerFired(data):

    if(data.gameTextAnsColor!="white"):
        data.gameColorTime+=data.timerDelay

        if(data.gameColorTime%500==0):
            data.gameTextAnsColor="white"
            
            data.gameColorTime=0
        elif(data.gameColorTime%250==0):
            data.guessStr=''
            data.webcamBrailleList=[]
    
def Game1PlayerRedrawAll(canvas,data):

    Game1PlayerInitMutable(data)
    if(data.place==False):#data thats initialized only once
        data.word=chooseWord(data)
        print(data.word,data.hint)
        placeWord(data.word,data)
        data.tries=int(len(data.word*6)*1.4)
       # print(data.boardWord)
        data.place=True
        
    elif(data.tries==0):
        data.gameOver=True

    else:

        drawBoard(canvas,data)
        canvas.create_rectangle(data.Game1PlayerBrailleDisplayBox,\
                                fill=data.gameTextAnsColor)
        canvas.create_rectangle((data.width*1/5,data.height/100,data.width*4/5,data.height/11),\
                                fill="skyblue",width=0)

        drawBrailleString(canvas,data,getBrailleList(data,data.hint),\
                        (data.width*1/5,data.height/100,data.width*4/5,data.height/11))
        drawTries(canvas,data)

        if(data.Game1PlayerInput=="Manual"):
            drawBrailleString(canvas,data,getBrailleList(data,data.guessStr),\
                (data.width*1/5,data.height*77/100,data.width*4/5,data.height*87/100))
            drawManualBrailleUI(canvas,data,data.Game1PlayerManualBrailleBox)

        elif(data.Game1PlayerInput=="Webcam"):
            drawBrailleString(canvas,data,data.webcamBrailleList,\
                (data.width*1/5,data.height*77/100,data.width*4/5,data.height*87/100))
            drawButton(canvas,data.Game1PlayerInputBox,"Input","beige")

        else:
            drawButton(canvas,data.Game1PlayerManualBox,"Manual","beige")
            drawButton(canvas,data.Game1PlayerWebcamBox,"Webcam","beige")
     

############################
#Help
#################################
def HelpInit(data):
    data.BrailleDictBox=(data.width*6/10,data.height*8/10,data.width*9/10,data.height*9/10)
    data.AboutBraille='''
    Braille is a system designed to allow the visually impaired a way of 
    reading. It is named after Louis Braille, is used across the globe 
    in any language

    '''
    data.AboutProgram='''
    This is designed for the sighted to learn braille. Braille is a key method of how 
    the visually impaired interact with the world and so it offers those who are 
    sighted perspective. Braille is dictated by 6 dots, arranged 2 by 3 with each 
    either being raised or lowered. This program uses a black dot to represent 
    raised, and white for lowered.
    '''
    data.HelpStr='''
     Inputting Braille has two methods: Manual input, which will display a 
     template and the mouse can be used to input the character. If webcam 
     is chosen, follow the instructions that will be provided. In case the 
     result from the webcamera isn't accurate, anyone of the braille characters 
     can be altered using the mouse. Pressing Enter will allow the program to 
     process the braille
    '''
    data.OpenImg=False
    
def HelpMousePressed(event,data):
    if(checkBounds(data.BrailleDictBox,event.x,event.y)):
        data.OpenImg=not data.OpenImg
    pass

def HelpTimerFired(data):

    pass

def HelpKeyPressed(event,data):

    pass

def HelpRedrawAll(canvas,data):
    data.BrailleDictBox=(data.width*6/10,data.height*8/10,data.width*9/10,data.height*9/10)

    if(not data.OpenImg):
        canvas.create_rectangle(data.width/9,data.height/8,data.width*8/9,\
                                data.height*75/100,fill="beige",width=2,outline="gray30")
        canvas.create_text(data.width*13/100,data.height*16/100,anchor="w",\
                            text="About Braille",font="Calibri %d bold"%(data.height/30))
        canvas.create_text(data.width/9,data.height*4/16,anchor="w",\
                            text=data.AboutBraille,font="Calibri %d"%(data.height/50))
        canvas.create_text(data.width*13/100,data.height*34/100,anchor="w",\
                            text="About Program",font="calibri %d bold"%(data.height/30))
        canvas.create_text(data.width/9,data.height*7/16,anchor="w",\
                            text=data.AboutProgram,font="Calibri %d"%(data.height/60))
        canvas.create_text(data.width*13/100,data.height*55/100,anchor="w",\
                            text="Help",font="Calibri %d bold"%(data.height/30))
        canvas.create_text(data.width/9,data.height*66/100,anchor="w",\
                            text=data.HelpStr,font="Calibri %d" %(data.height/60))

    if(data.OpenImg):
        data.dictImg=Image.open("brailleDictionary2.jpg")
        data.dictImg = data.dictImg.resize((data.width*3/4,data.height*6/10),\
                                            Image.ANTIALIAS)
        data.dictImage =ImageTk.PhotoImage(data.dictImg)
        canvas.create_image(data.width/9,data.height/8,\
                            anchor="nw",image=data.dictImage)
    drawButton(canvas,data.BrailleDictBox,"Dictionary",fill="beige")
    canvas.create_text(data.width/2,data.height/15,text="About/Help",\
                        font="Calibri %d italic bold"%(data.height/20),fill="white smoke")
    



################################################
#Run function
################################################

def run(width=500, height=500):#run function template was taken from notes but tracking mouse movements was self implemented

    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    def sizeChangedWrapper(event,canvas,data):
        sizeChanged(event,data)
        redrawAllWrapper(canvas,data)
    def moveMouseWrapper(event,canvas,data):
        moveMouse(event,data)
        redrawAllWrapper(canvas,data)

    # Set up data and call init
    class Struct(object): pass #hold all the data w/out globals
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 50 # milliseconds
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack(fill=BOTH,expand=YES)

    constInit(data)
    init(data)
    # create the root and the canvas

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<Configure>", lambda event:
                            sizeChangedWrapper(event,canvas,data))

    root.bind("<Motion>", lambda event:
                            moveMouseWrapper(event,canvas,data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
    # create the root and the canvas#run function template was used but the 
    
run()