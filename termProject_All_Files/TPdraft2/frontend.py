#Front end graphics stuff
#battleship for the end
#mainmenu
#practice
#translate need to do vice versa 
#   basic text editor Simple Frame basically done
#stats 
#animations for the end
#gotta hookup the backend
#history
#
#Style systemL: functions native to a particular splash screen will include the splash screens name in the function
#else all other functions are global
#
from Tkinter import *
import tkFont
import math
import random
from backendDraft1 import*
################################################
#Functions to be used by entire program 
################################################

def init(data):
    TranslateInit(data)
    PracticeInit(data)
    data.MainXS=data.width/15
    data.MainYS=data.height/50
    data.MainXE=data.width/5
    data.MainYE=data.height/10
    data.tempBrailleStr="FFFFFF"
    data.mode="MainMenu"
    data.str=""
    data.check=True
    data.constBrailleDict={"TFFFFF":"A","TFTFFF":"B","TTFFFF":"C","TTFTFF":"D","TFFTFF":"E","TTTFFF":"F",\
                           "TTTTFF":"G","TFTTFF":"H","FTTFFF":"I","FTTTFF":"J","TFFFTF":"K", "TFTFTF":"L",\
                           "TTFFTF":"M","TTTTTT":"N","TFFTTF":"O","TTTFTF":"P","TTTTTF":"Q", "TFTTTF":"R",\
                           "FTTFTF":"S","FTTTTF":"T","TFFFTT":"U","TFTFTT":"V","FTTTFT":"W","TTFFTT":"X",\
                           "TTFTTT":"Y","TFFTTT":"Z","FFFFFF":" "}
    
def sizeChanged(event,data):#scaling of the window

    data.width = event.width - 4
    data.height = event.height - 4

def checkBounds(XS,YS,XE,YE,pointX,pointY):
    if((XS<=pointX and pointX<=XE) and (YS<=pointY and pointY<=YE)):
        return True
    else:
        return False #determines of mouse is in given bounds

def drawButton(canvas,XS,YS,XE,YE,text):
    canvas.create_rectangle(XS,YS,XE,YE,outline="black")
    canvas.create_text((XS+XE)/2,(YS+YE)/2,text=text,font="Calibri %d"%(0.5*(YE-YS)))#draws a button given specific text. also scalable

def checkInCircle(cx,cy,radius,x,y):#returns true if in circle, else false
    if(distanceOfPoints(cx,cy,x,y)<=radius):
        return True
    else:
        return False

def distanceOfPoints(x1,y1,x2,y2): #return distance between two points

    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def drawBraille(canvas,brailleStr,XS,YS,XE,YE):#TODO optimize
    width=XE-XS
    height=YE-YS
    dotCoord=templateBraille(XS,YS,XE,YE)
    if((3/(2.0))*width>=height):
        radius=height//8
    else:
        radius=width/6
    for i in range(6):
        if(brailleStr[i]=="T"):
            fill="black"
        else:
            fill=None
        canvas.create_oval(dotCoord[i][0]-radius,dotCoord[i][1]-radius,dotCoord[i][0]+radius,dotCoord[i][1]+radius,fill=fill)

def findBrailleStr(data,char):

    for key in data.constBrailleDict:
        if(data.constBrailleDict[key]==char):
            return key
    return "FFFFFF"#goes through the dictionary to map char to its key

def drawManualBrailleUI(canvas,data,XS,YS,XE,YE):
    
    drawBraille(canvas,data.tempBrailleStr,XS,YS,XE,YE)#replace with variables#the circles

def templateBraille(XS,YS,XE,YE):    #return array with coords#returns list of 6 circles centres for each braille block
    dotCoord=[]
    for i in range(1,4):
        for j in range(1,3):
            dotCoord.append((j*(XE-XS)//3+XS,i*(YE-YS)//4+YS))
    return dotCoord

def checkManualBrailleInput(data,XS,YS,XE,YE,pointx,pointy):#universal function when there is mouseinput it will update the tempbraillestr
    width=XE-XS
    height=YE-YS
    dotCoord=templateBraille(XS,YS,XE,YE)
    if((3/(2.0))*width>=height):
        radius=height//8
    else:
        radius=width/6
    for circle in range(6):
        if(checkInCircle(dotCoord[circle][0],dotCoord[circle][1],radius,pointx,pointy)):
            if(data.tempBrailleStr[circle]=="T"):

                data.tempBrailleStr=data.tempBrailleStr[:circle]+"F"+data.tempBrailleStr[circle+1:]

            else:
                data.tempBrailleStr=data.tempBrailleStr[:circle]+"T"+data.tempBrailleStr[circle+1:]

def drawText(canvas,x,y,anchor,fontSize,text): #draws the inputed alphanum text

    canvas.create_text(x,y,text=text,anchor=anchor,font="Calibri %d"%(fontSize))#edit

def basicKeyAnalysis(data,char):
    if(len(char)==1):
        data.str+=char.upper()
        #data.cursorXOffset= data.font.measure(data.str)
    elif(char=="space"):
        data.str+=" "
        #data.cursorXOffset+=data.font.measure(" ")
    elif(char=="BackSpace" and len(data.str)>=1):
        data.str=data.str[:-1]
    elif(char=="Tab"):
        data.str+="    "


###############################################

def moveMouse(event,data):

    if(data.mode=="Practice"): PracticeMoveMouse(event,data)

def mousePressed(event, data):
    if(checkBounds(data.MainXS,data.MainYS,data.MainXE,data.MainYE,event.x,event.y) and data.mode!="MainMenu"):
        
        data.mode="MainMenu"
    elif(data.mode=="MainMenu"):MainMenuMousePressed(event,data)
    elif(data.mode=="Translate"):TranslateMousePressed(event,data)
    elif(data.mode=="Practice"): PracticeMousePressed(event,data)
    elif(data.mode=="Stats"): StatsMousePressed(event,data)
    # use event.x and event.y
    pass

def keyPressed(event, data):
    if(data.mode=="MainMenu"):MainMenuKeyPressed(event,data)
    elif(data.mode=="Translate"):TranslateKeyPressed(event,data)
    elif(data.mode=="Practice"): PracticeKeyPressed(event,data)
    elif(data.mode=="Stats"): StatsKeyPressed(event,data)

    # use event.char and event.keysym
    pass

def timerFired(data):
    if(data.mode=="MainMenu"):MainMenuTimerFired(data)
    elif(data.mode=="Translate"):TranslateTimerFired(data)
    elif(data.mode=="Practice"): PracticeTimerFired(data)
    elif(data.mode=="Stats"): StatsTimerFired(data)

    pass

def redrawAll(canvas,data):
    if(data.mode!="MainMenu"):
        drawButton(canvas,data.MainXS,data.MainYS,data.MainXE,data.MainYE,"Main Menu")
    if(data.mode=="MainMenu"): 
        init(data)
        MainMenuRedrawAll(canvas,data)
    elif(data.mode=="Translate"): TranslateRedrawAll(canvas,data)
    elif(data.mode=="Practice"): PracticeRedrawAll(canvas,data)
    elif(data.mode=="Stats"): StatsRedrawAll(canvas,data)
    pass
    












###############################################
#MainMenu
###############################################

def MainMenuInit(data):
    data.XS=2*data.width/7
    data.XE=5   *data.width/7
    data.avgX=(data.XS+data.XE)/2
    data.transYS=data.height*6/12
    data.transYE=data.height*7/12
    data.pracYS=data.height*8/12
    data.pracYE=data.height*9/12
    data.statsYS=data.height*10/12
    data.statsYE=data.height*11/12

def MainMenuMousePressed(event,data):
    if(checkBounds(data.XS,data.transYS,data.XE,data.transYE,event.x,event.y)):
        data.mode="Translate"
    elif(checkBounds(data.XS,data.pracYS,data.XE,data.pracYE,event.x,event.y)):
        data.mode="Practice"
    elif(checkBounds(data.XS,data.statsYS,data.XE,data.statsYE,event.x,event.y)):
        data.mode="Stats"
    pass

def MainMenuKeyPressed(event,data):#no keyboard input on this page

    pass

def MainMenuTimerFired(data):# no timer needed on this page

    pass

def drawMainMenuTitle(canvas,data):

    canvas.create_text(data.width/2,data.height/3,text="Learn Braille", font="Calibri %d bold"%(0.07*data.width))

def MainMenuRedrawAll(canvas,data):
    MainMenuInit(data)
    drawMainMenuTitle(canvas,data)
    drawButton(canvas,data.XS,data.transYS,data.XE,data.transYE,"Translate")
    drawButton(canvas,data.XS,data.pracYS,data.XE,data.pracYE,"Practice")
    drawButton(canvas,data.XS,data.statsYS,data.XE,data.statsYE,"Stats")
    pass



###################################
#Translate
###################################

#Translate has several components
#   Alphanum to braille which is essentially works as a google translate
#   Braille to alphanum which has 2 modes of input
#       manual in case webcam doesnt work
#       webcam 


#PROBLEMS WITH TRANSLATE
#Need to wrap text if its really long
#on alphanum to braille need to properly display braille in editors text box
#on manual need more buttons to switch between displays
#backend needs more work
#

def TranslateInit(data):
    data.transMode="AlphanumToBraille"
    data.cursorYOffset=0
    data.cursorXOffset=0
    data.cursorBlink=True
    
    #edit#initialization that only needed for init page

def TranslateMutable(data):
    data.fontSize=data.width/40
    data.font=tkFont.Font(family="Calibri",size=data.fontSize)
    data.cursorX=data.width*1/15
    data.cursorY=data.height*2/16
    data.switchButtonXS=data.width*10/12
    data.switchButtonXE=data.width*49/50
    data.switchButtonYS=data.height*1/25
    data.switchButtonYE=data.height*1/10
    data.editorXS=data.width*1/20
    data.editorXE=data.width*19/20
    data.editorYS=data.height*2/17
    data.editorYE=data.height*1/2  
    data.manualXS=data.width*1/5
    data.manualXE=data.width*2/5
    data.manualYS=data.height*1/4
    data.manualYE=data.height*1/3#mutable to due scaling

def drawTranslationEditorBox(canvas,data):
    canvas.create_rectangle(data.editorXS,data.editorYS,data.editorXE,\
                            data.editorYE,fill="light gray")
    if(data.cursorBlink):#edit
        canvas.create_line(data.cursorX+data.cursorXOffset,data.cursorY+data.cursorYOffset,\
        data.cursorX+data.cursorXOffset,data.cursorY+data.fontSize+data.cursorYOffset,fill="black",width=2)#TODO edit

def drawTranslationBox(canvas,data): #draws the box where either translated braille or alphanum goes

    canvas.create_rectangle(data.editorXS,data.editorYS+data.height*3/7,data.editorXE,data.editorYE+data.height*3/7,fill="light gray")

def drawTranslatedText(canvas,data):

    canvas.create_text(data.editorXS,data.editorYS+data.height*3/7, text=data.str,\
                        anchor=NW,font="Calibri %d"%(data.width/25))
                        #for alphanum to braille will #Braille to alpha num shows result textstr

def drawTranslationBraille(canvas,data):###################TODO GET THISWORKING PROPERLY

    editorBoxWidth=data.editorXE-data.editorXS

    for i in range(len(data.str)):
        if(data.str[i]==" "):#no need to draw braille
            continue
        else:
            drawBraille(canvas,findBrailleStr(data,data.str[i]),data.editorXS+editorBoxWidth*(i+1)/(len(data.str)+2),data.editorYS+data.height*3/7,\
                data.editorXS+editorBoxWidth*(i+2)/((len(data.str)+2)),data.editorYE+data.height*3/7)

def getTranslatedOffsets(data):#TODO fix
    
    if(data.str.find("\n")!=-1):
        print('hi')
        tempStr=data.str[::-1]
        tempStr=tempStr[:tempStr.find("n\\")]
        tempStr=tempStr[::-1]
        data.cursorXOffset=data.font.measure(tempStr)
    else:
        data.cursorXOffset=data.font.measure(data.str)
    data.cursorYOffset=data.str.count("\n")*data.fontSize

################################################

def TranslateKeyPressed(event,data):
    if(data.transMode=="AlphanumToBraille"):
        basicKeyAnalysis(data,event.keysym)
        if(char=="Return"):
            data.str+="\n"
        getTranslatedOffsets(data)
    elif(data.transMode.find("BrailleToAlphaNum")):
        if(data.transMode.find("Manual")):
            if(event.keysym=="Return"):
                if(data.tempBrailleStr in data.constBrailleDict):
                    data.str+=data.constBrailleDict[data.tempBrailleStr]
                data.tempBrailleStr="FFFFFF"
        if(event.keysym=="BackSpace" and len(data.str)>=1) :
            data.str=data.str[:-1]

def TranslateMousePressed(event,data):
    if(checkBounds(data.switchButtonXS,data.switchButtonYS,data.switchButtonXE,data.switchButtonYE,event.x,event.y)):
        if(data.transMode=="AlphanumToBraille"):
            data.str=""
            data.transMode="BrailleToAlphanum"

        else:
            data.str=''
            data.transMode="AlphanumToBraille"

    elif(data.transMode.find("BrailleToAlphanum")!=-1):

        if(data.transMode.find("Manual")!=-1):
            checkManualBrailleInput(data,data.width*2/7,data.height*1/40,data.width*5/7,data.height*4/7,event.x,event.y)

        elif(data.transMode.find("Webcam")!=-1):#needs editing
            if(checkBounds(data.manualXS,data.manualYS,data.manualXE,data.manualYE,event.x,event.y)):
                data.str+=getText()
            elif(checkBounds(data.manualXS+data.width*2/5,data.manualYS,data.manualXE+data.width*2/5,data.manualYE,event.x,event.y)):
                if(len(data.str)>=1):
                    data.str+=" " 
                data.str+=getText()
            pass

        else:

            if(checkBounds(data.manualXS,data.manualYS,data.manualXE,data.manualYE,event.x,event.y)):
                data.transMode="BrailleToAlphanumManual"#choose your option

            elif(checkBounds(data.manualXS+data.width*2/5,data.manualYS,data.manualXE+data.width*2/5,data.manualYE,event.x,event.y)):
                
                data.transMode="BrailleToAlphanumWebcam"
              #  go to that option

def TranslateTimerFired(data):
    if(data.cursorBlink):
        data.cursorBlink=False
    else:
        data.cursorBlink=True#only needed to simulate cursor blink

def TranslateRedrawAll(canvas,data):

    TranslateMutable(data)#scalability
    drawTranslationBox(canvas,data)

    if(data.transMode=="AlphanumToBraille"):
        drawTranslationEditorBox(canvas,data)
        drawText(canvas,data.cursorX,data.cursorY+5,"w",data.fontSize,data.str)
        drawTranslationBraille(canvas,data)

    elif(data.transMode.find("BrailleToAlphanum")!=-1):

        if(data.transMode.find("Manual")!=-1):
            drawManualBrailleUI(canvas,data,data.width*2/7,data.height*1/40,data.width*5/7,data.height*4/7)

        elif(data.transMode.find("Webcam")!=-1):
            drawButton(canvas,data.manualXS,data.manualYS,data.manualXE,data.manualYE,"Continue Word")#shows option for manual input
            drawButton(canvas,data.manualXS+data.width*2/5,data.manualYS,data.manualXE+data.width*2/5,data.manualYE,"New Word")#shows option for webcam

        else:
            drawButton(canvas,data.manualXS,data.manualYS,data.manualXE,data.manualYE,"Manual")#shows option for manual input
            drawButton(canvas,data.manualXS+data.width*2/5,data.manualYS,data.manualXE+data.width*2/5,data.manualYE,"Webcam")#shows option for webcam

        drawTranslatedText(canvas,data)

    drawButton(canvas,data.switchButtonXS,data.switchButtonYS,data.switchButtonXE,data.switchButtonYE,"Switch")

    
   ####This should give a rough interface for the translation section



##################################################
#Practice
##################################################

def PracticeInit(data):
    data.timerRead=5
    data.timerTrans=10
    data.score=0
    data.colourLeft="white"
    data.colourRight="white"
    data.pracMode="Practice"
    data.readBrailleEasy='A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,'
    data.readBrailleMed="HI,HE,IS,OR,TO,OF,IN,IT,GO,UP,SO,ON,DO,AT,AS,BY,MY,IF,US,OH,SHE,THE,FOR,NOR,BUT,AND,"
    data.readBrailleHard="HELLO,WORLD,WORD,NOT,BRAILLE,LOUIS,CMU,PYTHON,STRING,LIST,QUIZ,OPEN,CLOSE,"#make up more later
    
def PracticeMutable(data):
    pass

def drawPracticeChoice(canvas,data):# the menu to choose which practice mode
    canvas.create_rectangle(0,0,data.width/2,data.height,fill=data.colourLeft)
    canvas.create_rectangle(data.width/2,0,data.width,data.height,fill=data.colourRight)

def drawPracticeChoiceText(canvas,data): #^but the text
    canvas.create_text(data.width/4,data.height/2, text="Read Braille",font="Calibri %d"%(data.width/20))
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
    if(data.score<10):#easy
        word=getWord(data.readBrailleEasy)
    elif(data.score<20):#med
        word=getWord(data.readBrailleMed)
    else:   #hard
        word=getWord(data.readBrailleHard)
    return word

def drawPracticeBrailleWord(canvas,data,word):
    for i in range(len(word)):
        drawBraille(canvas,findBrailleStr(data,word[i]),\
            data.width*(i+1)/(len(word)+2),data.height*1/4,data.width*(i+2)/((len(word)+2)),data.height*2/4)
   
def checkIfCorrect(data):#implement error system
    if(data.word==data.str):
        data.str=''
        data.score+=1
        data.check=True

########################################################

def PracticeMoveMouse(event,data):
    if(data.pracMode=="Practice"):
        if(event.x<data.width/2):
            data.colourLeft="light green"
            data.colourRight="white"
        elif(event.x>data.width/2):
            data.colourLeft="white"
            data.colourRight="light green"

def PracticeMousePressed(event,data):
    if(data.pracMode=="Practice"):
        if(checkBounds(0,0,data.width/2,data.height,event.x,event.y)):
            data.pracMode="PracticeRead"
        elif(checkBounds(data.width/2,0,data.width,data.height,event.x,event.y)):
            data.pracMode="PracticeTranslate"

    elif(data.pracMode.find("PracticeTranslate")!=-1):
        if(data.pracMode.find("Manual")!=-1):
            checkManualBrailleInput(data,data.width*3/9,data.height*3/5,data.width*6/9,data.height*6/7,event.x,event.y)
            
        elif(data.pracMode.find("Webcam")!=-1):#needs editing
            if(checkBounds(data.width*1/5,data.height*2/3,data.width*2/5,data.height*3/4,event.x,event.y)):
                data.str+=getText()
            elif(checkBounds(canvas,data.width*3/5,data.height*2/3,data.width*4/5,data.height*3/4,event.x,event.y)):
                data.str+=" "
                data.str+=getText()
            pass
        else:
            if(checkBounds(data.width*1/5,data.height*2/3,data.width*2/5,data.height*3/4,event.x,event.y)):
                data.pracMode="PracticeTranslateManual"#choose your option
            elif(checkBounds(data.width*3/5,data.height*2/3,data.width*4/5,data.height*3/4,event.x,event.y)):
                data.pracMode="PracticeTranslateWebcam"

           # elif(checkBounds(data.manualXS+data.width*2/5,data.manualYS,data.manualXE+data.width*2/5,data.manualYE,event.x,event.y)):
                    #data.transMode="PracticeTranslateWebcam"

def PracticeKeyPressed(event,data):
    if(data.pracMode.find("Read")!=-1):
        basicKeyAnalysis(data,event.keysym)
        if(event.keysym=="Return"):
            checkIfCorrect(data)

    elif(data.pracMode.find("Translate")!=-1):
        if(event.keysym=="Return"):
                if(data.tempBrailleStr in data.constBrailleDict):
                    data.str+=data.constBrailleDict[data.tempBrailleStr]
                data.tempBrailleStr="FFFFFF"
        if(event.keysym=="BackSpace" and len(data.str)>=1) :
            data.str=data.str[:-1]

def PracticeTimerFired(data):
    if(data.pracMode.find("Read")!=-1):
        if(data.timerRead==0):
            data.pracMode="Practice"
            data.timerRead=5
            data.score=0
            data.mode="Stats"
        else:
            
            data.timerRead-=1
        pass
    elif(data.pracMode.find("Translate")!=-1):
        if(data.timerTrans==0):
            data.pracMode="Practice"
            data.timerTrans=10
            data.score=0
            data.mode="Stats"
        else:
            data.timerTrans-=1
    pass


def PracticeRedrawAll(canvas,data):
    if(data.check==True):
            data.word=PracticeChooseWord(data)
            print(data.word)
            data.check=False

    if(data.pracMode.find("Read")!=-1):
        
        drawPracticeBrailleWord(canvas,data,data.word)
        #checkIfCorrect(canvas,word,data)
        drawText(canvas,data.width/2,data.height*3/4,None,data.width/20,data.str)
        drawText(canvas,0,data.height,"sw",data.width/20,data.score)
        drawText(canvas,data.width,data.height,"se",data.width/20,data.timerRead)

    elif(data.pracMode.find("Translate")!=-1):
       
        drawText(canvas,data.width/2,data.height/4,None,data.width/20,data.word)
        checkIfCorrect(data)

        if(data.pracMode.find("Manual")!=-1):
            drawManualBrailleUI(canvas,data,data.width*3/9,data.height*3/5,data.width*6/9,data.height*6/7)#need to edit
            pass

        elif(data.pracMode.find("Webcam")!=-1):
            drawButton(canvas,data.width*1/5,data.height*2/3,data.width*2/5,data.height*3/4,"ContinueWord")#need 
            drawButton(canvas,data.width*3/5,data.height*2/3,data.width*4/5,data.height*3/4,"NewWord")
        else:
            drawButton(canvas,data.width*1/5,data.height*2/3,data.width*2/5,data.height*3/4,"Manual")#need 
            drawButton(canvas,data.width*3/5,data.height*2/3,data.width*4/5,data.height*3/4,"Webcam")
        drawText(canvas,10,10,"nw",data.width/20,data.score)
        drawText(canvas,data.width,0,"ne",data.width/20,data.timerRead)
    else:
        drawPracticeChoice(canvas,data)
        drawPracticeChoiceText(canvas,data)
    pass


#####################################################
#Stats
#####################################################
def StatsInit(data):
    pass
def StatsMousePressed(event,data):
    pass
def StatsKeyPressed(event,data):
    pass
def StatsTimerFired(data):
    pass
def StatsRedrawAll(canvas,data):
    pass
























################################################
#Run function
################################################

def run(width=300, height=300):

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
    data.timerDelay = 500 # milliseconds
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack(fill=BOTH,expand=YES)

    
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
    # create the root and the canvas
    
run()