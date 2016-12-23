from Tkinter import *
from frontend import*
from backendDraft1 import*
import random 
####################################
# customize these functions
####################################
#3 boards 6 by 6 3 letter words, 8 by 8  4-5 letter words, 10 by 10 6-7 letter words
def GameInit(data):
    data.GameMode="GameTitle"
    data.numOfPlayers=1
    data.boardSize="Easy"
    data.difficultyString=["Easy","Med","Hard"]
    GameTitleInit(data)
    #Game1PlayerInit(data)
    data.gameOver=False
    #data.playerTurn=1
    data.constBrailleDict={"TFFFFF":"A","TFTFFF":"B","TTFFFF":"C","TTFTFF":"D","TFFTFF":"E","TTTFFF":"F",\
                           "TTTTFF":"G","TFTTFF":"H","FTTFFF":"I","FTTTFF":"J","TFFFTF":"K", "TFTFTF":"L",\
                           "TTFFTF":"M","TTTTTT":"N","TFFTTF":"O","TTTFTF":"P","TTTTTF":"Q", "TFTTTF":"R",\
                           "FTTFTF":"S","FTTTTF":"T","TFFFTT":"U","TFTFTT":"V","FTTTFT":"W","TTFFTT":"X",\
                           "TTFTTT":"Y","TFFTTT":"Z","FFFFFF":" "}
    data.tempBrailleStr="FFFFFF"
    # load data.xyz as appropriate
    pass

def make2dList(rows,cols):
    board=[]
    for row in range(rows): board += [[0]*cols]
    return board


################################################
def GameMousePressed(event, data):
    if(data.GameMode=="GameTitle"): GameTitleMousePressed(event,data)
    elif(data.GameMode=="Game1Player"): Game1PlayerMousePressed(event,data)
    elif(data.GameMode=="Game2Player"): Game2PlayerMousePressed(event,data)
    # use event.x and event.y
    pass

def GameKeyPressed(event, data):
    if(data.GameMode=="GameTitle"): GameTitleKeyPressed(event,data)
    elif(data.GameMode=="Game1Player"): Game1PlayerKeyPressed(event,data)
    elif(data.GameMode=="Game2Player"): Game2PlayerKeyPressed(event,data)
    pass

def GameTimerFired(data):
    if(data.GameMode=="GameTitle"): GameTitleTimerFired(data)
    elif(data.GameMode=="Game1Player"): Game1PlayerTimerFired(data)
    elif(data.GameMode=="Game2Player"): Game2PlayerTimerFired(data)
    pass

def GameRedrawAll(canvas, data):
    if(data.gameOver==True):data.mode="Stats"
    if(data.GameMode=="GameTitle"): GameTitleRedrawAll(canvas,data)
    elif(data.GameMode=="Game1Player"): Game1PlayerRedrawAll(canvas,data)
    elif(data.GameMode=="Game2Player"): Game2PlayerRedrawAll(canvas,data)    # draw in canvas
    pass


#############################################
#Game Title
#############################################
#box to determine num of players
#box to determine easy med hard

def GameTitleInit(data):
    data.titleX=data.width/2
    data.titleY=data.height*1/10
    data.titleStr="Braille BattleShip!"
    data.playerBox=[(data.width/5,data.height/4,data.width*2/5,data.height/3),\
    ((data.width*3/5,data.height/4,data.width*4/5,data.height/3))]

    data.difficultyBox=[(data.width/7,data.height*2/3,data.width*2/7,data.height*3/4),\
            (data.width*3/7,data.height*2/3,data.width*4/7,data.height*3/4),\
            (data.width*5/7,data.height*2/3,data.width*6/7,data.height*3/4)]

    
    
def drawInstructions(canvas,data):
    Instructions='''
The goal of this game is to determine the word spelt out 
by the braille characters on the grid. A hint pertaining 
to the word's topic will be given  in  braille. You will 
only be able to reveal  a  limited  number  of tiles and 
attempts on the determining  the word is  also   limited. 
                                    Good luck!
                '''
    canvas.create_text(data.width/2,data.height/3,text=Instructions,font="calibri %d"%(data.height/33))
def GameTitleMousePressed(event,data):
    #for i in range(len(data.playerBox)):
     #   if(checkBounds(data.playerBox[i],event.x,event.y)):
      #      data.numOfPlayers=i+1
    for i in range(len(data.difficultyBox)):
        if(checkBounds(data.difficultyBox[i],event.x,event.y)):
            data.boardSize=data.difficultyString[i]
        
    print(data.numOfPlayers,data.boardSize)
    pass

def GameTitleKeyPressed(event,data):
    if(event.keysym=="Return"):
        data.GameMode="Game%dPlayer"%(data.numOfPlayers)
        Game1PlayerInit(data)
    print(data.GameMode)
    pass

def GameTitleTimerFired(data):

    pass

def GameTitleRedrawAll(canvas,data):
    canvas.create_text(data.titleX,data.titleY,text=data.titleStr,font="Calibri %d" %(data.height/10)) #title
    #for i in range(len(data.playerBox)):
     #   if(data.numOfPlayers==i+1):
      #      drawButton(canvas,data.playerBox[i],"Player %d"%(i+1),"light grey")
       # else:
        #    drawButton(canvas,data.playerBox[i],"Player %d"%(i+1),None)
    drawInstructions(canvas,data)
    for i in range(len(data.difficultyBox)):
        if(data.boardSize==data.difficultyString[i]):
            drawButton(canvas,data.difficultyBox[i],data.difficultyString[i],"light grey")
        else:
            drawButton(canvas,data.difficultyBox[i],data.difficultyString[i],None)    
    pass


################################################
#1PlayerMode
################################################
def Game1PlayerInit(data):
    if(data.boardSize=="Easy"):
        size=6
    elif(data.boardSize=="Med"):
        size=8
    else:
        size=10
    data.boardWord=make2dList(size,size) #stores the backend of the board/0 is nothing/1 is unfilled circle 2 is filled circle
    data.boardShow=make2dList(size,size) #stores whether the cell has been clicked or not
    data.margin=data.width/11
    data.place=False
    data.guessStr=''
    data.Game1PlayerInput=''
    data.wordBankEasy={"PET":("CAT","DOG"),"PERSON":("DAD","MOM"),"TRAVEL":("CAR",),"COLOR":("RED","TAN")}
    data.wordBankMed={"NAMES":("ALEX","EMMA","JACK","WILL"),"COLOR":("BLUE","CYAN","GREY","NAVY"),"PERSON":("KING",)}
    data.wordBankHard={"NAMES":("ARTHUR","JESSICA","JUSTIN","HILLARY"),"COLOR":("ORANGE","VIOLET","PURPLE","MAROON"),"JOB":("FARMER","LAWYER")}
    data.word="DOG"
    data.hint="PET"

def Game1PlayerInitMutable(data):
    data.Game1PlayerManualBox=(data.width/5,data.height*7/8,data.width*2/5,data.height)
    data.Game1PlayerWebcamBox=(data.width*3/5,data.height*7/8,data.width*4/5,data.height)
    data.Game1PlayerInputBox=(data.width/3,data.height*7/8,data.width*2/3,data.height)
    data.Game1PlayerManualBrailleBox=(data.width/3,data.height*7/8,data.width*2/3,data.height)
    


def drawBoard(canvas,data):
    for row in range(len(data.boardShow)):
        for col in range(len(data.boardShow[0])):
            if(data.boardShow[row][col]==0):
                drawCell(canvas,data,row,len(data.boardShow),col,len(data.boardShow[0]),"grey")
            elif(data.boardShow[row][col]==1):
                drawCell(canvas,data,row,len(data.boardShow),col,len(data.boardShow[0]),"white")
                drawInCell(canvas,data,row,len(data.boardShow),col,len(data.boardShow[0]))
    pass

def convStrToList(str):
    temp=[]
    final=[]
    for char in str:
        temp.append(char)
        if(len(temp)==2):
            final.append(temp)
            temp=[]
    return final

def rotateList(L): 

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
        print(brailleList)    
        randRow=random.randint(0,len(data.boardWord)-1)
        randCol=random.randint(0,len(data.boardWord[0])-1)

        while(isLegal(randRow,randCol,brailleList,data.boardWord)==False):
            numOfRotations=random.randint(0,3)
            for i in range(numOfRotations):
                brailleList=rotateList(brailleList)
            print(brailleList)    
            randRow=random.randint(0,len(data.boardWord)-1)
            randCol=random.randint(0,len(data.boardWord[0])-1)
        placeLetter(randRow,randCol,brailleList,data.boardWord)
        print(randRow,randCol)
    return data.boardWord


def placeLetter(row,col,L,board):
    for i in range(row,row+len(L)):
        for j in range(col,col+len(L[0])):
            if(L[i-row][j-col]=="T"):
                board[i][j]=2
            else:
                board[i][j]=1

def isLegal(row,col,L,board):
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
        canvas.create_oval(XS,YS,XE,YE)
    elif(data.boardWord[row][col]==2):
        canvas.create_oval(XS,YS,XE,YE,fill="black")

def drawCell(canvas,data,row,rows,col,cols,color):#create each cell
    (XS,YS,XE,YE)=getCell(data,row,rows,col,cols)
    canvas.create_rectangle(XS,YS,XE,YE,fill="black")
    canvas.create_rectangle(XS+1,YS+1,XE-1,YE-1,fill=color)
    pass

def getCell(data,row,rows,col,cols):
    rowHeight =  ((data.width)*2/3) / rows
    columnWidth = ((data.width)*2/3) / cols
    XS = data.width/6 + col * columnWidth
    XE = data.width/6 + (col+1) * columnWidth
    YS = data.margin + row * rowHeight
    YE =data.margin + (row+1) * rowHeight
    return (XS,YS,XE,YE)


def chooseWord(data):
    if(data.boardSize=="Easy"):
        dataBank=data.wordBankEasy
    elif(data.boardSize=="Hard"):
        dataBank=data.wordBankMed
    else:
        dataBank=data.wordBankHard
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

def drawBrailleWord(canvas,data,string,coords):
    (XS,YS,XE,YE)=coords
    numChar=len(string)
    for i in range(len(string)):
        XSC=i*(XE-XS)/(numChar)+XS
        XEC=(i+1)*(XE-XS)/(numChar)+XS
        brailleStr=findBrailleStr(data,string[i])
        drawBraille(canvas,brailleStr,(XSC,YS,XEC,YE))


def drawTries(canvas,data):
    canvas.create_text(0,data.height,text=str(data.tries),anchor="sw",font="calibri %d"%(data.height/20))

##############################################
def Game1PlayerMousePressed(event,data):
    for row in range(len(data.boardWord)):
        for col in range(len(data.boardWord[0])):
            coords=getCell(data,row,len(data.boardWord),col,len(data.boardWord[0]))
            if(checkBounds(coords,event.x,event.y)):
                if(data.boardShow[row][col]==0):
                    data.tries-=1
                data.boardShow[row][col]=1
                #print(data.boardWord[row][col])

    if(data.Game1PlayerInput=="Manual"):
        checkManualBrailleInput(data,data.Game1PlayerManualBrailleBox,event.x,event.y)
    elif(data.Game1PlayerInput=="Webcam"):
        if(checkBounds(data.Game1PlayerInputBox,event.x,event.y)):
            data.guessStr+=getText()
    else:
        if(checkBounds(data.Game1PlayerManualBox,event.x,event.y)):
            data.Game1PlayerInput="Manual"#choose your option

        elif(checkBounds(data.Game1PlayerWebcamBox,event.x,event.y)):
                
            data.Game1PlayerInput="Webcam"
    pass

def Game1PlayerKeyPressed(event,data):
    if(data.Game1PlayerInput=="Manual"):
        if(event.keysym=="Return"):
            if(data.tempBrailleStr=="FFFFFF"):
                if(data.guessStr==data.word):
                    data.gameOver=True
                else:
                    data.tries-=1
            else:
                if(data.tempBrailleStr in data.constBrailleDict):
                    data.guessStr+=data.constBrailleDict[data.tempBrailleStr]
            data.tempBrailleStr="FFFFFF"
        
    elif(data.Game1PlayerInput=="Webcam" and event.keysym=="Return"):
        if(data.guessStr==data.word):
                data.gameOver=True
        else:
            data.tries-=1
    pass

def Game1PlayerTimerFired(data):
    pass

def Game1PlayerRedrawAll(canvas,data):
    Game1PlayerInitMutable(data)
    if(data.place==False):#data thats initialized only once
        data.word=chooseWord(data)
        print(data.word,data.hint)
        placeWord(data.word,data)
        data.tries=int(len(data.word*6)*1.4)
        print(data.boardWord)
        data.place=True
        
    elif(data.tries==0):
        data.gameOver=True
    else:
        drawBoard(canvas,data)
        drawBrailleWord(canvas,data,data.hint,(data.width*1/5,data.height/100,data.width*4/5,data.height/11))
        drawBrailleWord(canvas,data,data.guessStr,(data.width*1/5,data.height*75/100,data.width*4/5,data.height*85/100))
        drawTries(canvas,data)
        if(data.Game1PlayerInput=="Manual"):
            drawManualBrailleUI(canvas,data,data.Game1PlayerManualBrailleBox)
        elif(data.Game1PlayerInput=="Webcam"):
            drawButton(canvas,data.Game1PlayerInputBox,"Input",None)
        else:
            drawButton(canvas,data.Game1PlayerManualBox,"Manual",None)
            drawButton(canvas,data.Game1PlayerWebcamBox,"Webcam",None)
    pass 













####################################
# use the run function as-is
####################################


def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        GameRedrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        GameMousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        GameKeyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        GameTimerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    GameInit(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 400)