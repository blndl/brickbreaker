import tkinter as tk
from tkinter import ttk

class GameObject(object):  #class inherited by all game objects
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def getCoords(self):
        return self.canvas.coords(self.item)
    
    def move(self, x, y):
        self.canvas.move(self.item, x, y)
    
    def deleteObject(self):
        self.canvas.delete(self.item)

class Ball(GameObject): #class managing ball, is a game object
    def __init__(self, canvas, x, y):
        self.radius = 15 #ball siwe
        self.speed = 5 #ball speed
        self.direction = [1, 1]
        item = canvas.create_oval(x,y,x + self.radius, y + self.radius, fill="ivory", outline="black")
        super(Ball, self).__init__(canvas, item)


    def move(self):
        coords = self.getCoords()
        if coords[0] <= 0 or coords[2] >= 1200:
            self.direction[0] *= -1
        if coords[1] >= 800 or coords[1] <= 0: #bounces off canvas limits
            self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.canvas.move(self.item, x, y)
    
    def collide(self, objects): #handles collisions and brick deletion
        ballCoords = self.getCoords()
        x = (ballCoords[0] + ballCoords[2]) * 0.5
        if len(objects) == 1:
            object = objects[0]
            coords = object.getCoords()
            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1
            if (isinstance(object, Brick)):
                object.deleteObject()
                self.speed += 0.25
        elif len(objects) > 1:
            for y in objects:
                if (isinstance(y, Brick)):
                    y.deleteObject()
            self.direction[1] *= -1
            self.speed += 0.25



class Paddle(GameObject): #class managing paddle game object
    def __init__(self, canvas, width, height):
        self.width = width
        self.height = height
        self.offset = 0
        item = canvas.create_rectangle(600, 780, 600 + self.width, 780 + self.height, fill="black", outline="blue")
        super(Paddle,self).__init__(canvas, item)
    
    def move(self, speed):
        coords = self.getCoords()
        width = self.canvas.winfo_width()
        if coords[0] + speed >= 0 and coords[2] + speed <= width:
            super(Paddle, self).move(speed, 0)

class Brick(GameObject): #class managing brick game object
    def __init__(self, canvas, x, y):
        self.x = x
        self.y = y
        self.life = 1
        item = canvas.create_rectangle(x, y, x + 150, y + 50, fill="red", outline="black",tags = "brick")
        super(Brick, self).__init__(canvas, item)

    


class Game(tk.Frame): #main class
    def __init__(self, master):
        super().__init__(master)
        self.width = 1200
        self.height = 800
        self.canvas = tk.Canvas(self, bg='#4fc3f7', width=self.width, height=self.height)
        self.canvas.pack()
        self.pack()
        self.paddle = None
        self.ball = None
        self.paddle = self.addPaddle()
        self.objects = [] #list of game objects
        self.objects.append(self.paddle)
        self.menu()     #calls menu
        self.canvas.focus_set()
        self.canvas.bind('<KeyPress>', self.keyPress)#paddle movement key bindings
        self.canvas.bind('<KeyRelease>', self.keyRelease)


    def addBall(self):
        if self.ball is not None:
           self.ball.deleteObject()
        wtf = Ball(self.canvas, 350, 400)
        return wtf
    
    def addPaddle(self):
        if self.paddle is not None:
            self.paddle.deleteObject()
        ret = Paddle(self.canvas, 150, 20)
        return ret
    
    def addBrick(self,x,y):
        brick = Brick(self.canvas, x, y)
        return brick
    
    def menu(self):
        self.playtext = self.canvas.create_text(300, 200, activefill='red', fill='black', font=('sylfaen', 60), text="Press enter to play")
        self.quittext = self.canvas.create_text(800, 200, activefill='red', fill='black', font=('sylfaen', 60), text="Press escape to quit")
        self.canvas.bind('<Return>', lambda a: self.setupGame()) #prepares game
        self.canvas.bind('<Escape>', lambda a: all.destroy())

    def pauseMenu(self):
        ballSpeed = self.ball.speed #keep current ball speed before pausing
        self.canvas.unbind("<KeyPress>")
        self.ball.speed = 0
        self.pauseText = self.canvas.create_text(600,300,fill="black", font=("sylfaen", 30), text="press j to quit")
        self.unpauseText = self.canvas.create_text(300,300,fill="black",font=("sylfaen", 30), text="press space to unpause")
        self.canvas.bind('<space>', lambda a: self.unpause(ballSpeed))
        self.canvas.bind('j', lambda a: all.destroy())

    def unpause(self, speed):
        self.ball.speed = speed
        self.canvas.unbind('<space>')
        self.canvas.unbind('<Escape>')
        self.canvas.delete(self.unpauseText)
        self.canvas.delete(self.pauseText)
        self.canvas.bind("<KeyPress>",self.keyPress)

    def setupGame(self):
        self.canvas.unbind("j")
        self.canvas.delete(self.playtext)
        self.canvas.delete(self.quittext)
        self.canvas.unbind('<Escape>')
        self.canvas.unbind('<Return>')
        y = 0
        self.ball = self.addBall()
        for i in range(3): #create bricks
            x = 0
            for j in range(8):
                self.objects.append(self.addBrick(x,y))
                x += 150
            y += 50
        self.text = self.canvas.create_text(300,300, text="press space to start \n use a and d to move and p to pause", fill="black")
        self.canvas.focus_set()
        self.canvas.bind("<space>",lambda event: self.startGame())

    def startGame(self):
        self.canvas.unbind('<space')
        self.canvas.delete(self.text)
        self.gameLoop() #start game loop

    def victory(self):
        self.playtext = self.canvas.create_text(450,350, font=('sylfaen',50), fill="red", text="You win !\nPress space to replay or j to quit")
        self.ball.speed = 0
        self.canvas.bind("<space>", lambda a:self.setupGame())
        self.canvas.bind("j", lambda a:all.destroy())
    
    def loss(self):
        self.playtext = self.canvas.create_text(450,350, font=('sylfaen',50), fill="red", text="You lose !\nPress space to replay or j to quit")
        self.ball.speed = 0
        self.canvas.bind("<space>", lambda a:self.setupGame())
        self.canvas.bind("j", lambda a:all.destroy())

    def gameLoop(self):
        i = 1
        while (i == 1): #gameloop
            brickLen = len(self.canvas.find_withtag('brick')) #number of bricks on screen
            coords = self.ball.getCoords()
            self.checkCollisions()
            self.after(1,self.paddle.move(self.paddle.offset))#always moving paddle at 0 speed, set it to actual speed on keypress
            self.update()
            if coords[3] >= 800: 
                self.ball.speed = 0
                i = 0
                self.loss()
            elif brickLen == 0:
                self.ball.speed = 0
                i = 0
                self.victory()
            else:
                self.ball.move()
               # self.after(1,self.gameLoop())  #recursive gameloop RIP ;_;
    

    def keyPress(self, event): #move paddle on keypress
        coords = self.paddle.getCoords()
        key = event.char
        if key == "p":
            self.pauseMenu()
        if coords[0] > 20:
            if key == 'a':
                self.paddle.offset = -15
        if coords[2] < 1180:
            if key == 'd':
                self.paddle.offset = 15

    def keyRelease(self, event): #paddle speed back to 0 on key release
        self.paddle.offset = 0
    
    def checkCollisions(self): #look for collisions
        ballCoords = self.ball.getCoords()
        list = self.canvas.find_overlapping(*ballCoords)
        objects = [] #list of colliding objects 
        for x in list:
            for y in self.objects:
                if x == y.item:
                    objects.append(y)
        self.ball.collide(objects)



all = tk.Tk()
all.title = "brick breaker"
game = Game(all)
game.mainloop()