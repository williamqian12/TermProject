from tkinter import *

####################################
# customize these functions
####################################
#3 boards 6 by 6 3 letter words, 8 by 8  4-5 letter words, 10 by 10 6-7 letter words
def GameInit(data):

    data.board=make2dBoard
    # load data.xyz as appropriate
    pass
def make2dBoard(dimension):
    board=[]
    for dim in range(dimension): board += [[0]*dimension]
    return dimension

def drawBoard(canvas,data):
    pass

def setShips

################################################
def GameMousePressed(event, data):
    # use event.x and event.y
    pass

def GameKeyPressed(event, data):
    # use event.char and event.keysym
    pass

def GameTimerFired(data):
    pass

def GameRedrawAll(canvas, data):
    # draw in canvas
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
    init(data)
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

run(400, 200)