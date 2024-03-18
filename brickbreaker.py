import tkinter as tk

class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def getCoords(self):
        return self.canvas.coords(self.item)
    
    def move(self, x, y):
        self.canvas.move(self.item, x, y)
    
    def deleteObject(self):
        self.canvas.delete(self.item)

class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 20
        self.speed = 5
        self.direction = [-1, -1]
        item = canvas.create_oval(x,y,x + self.radius, y + self.radius, fill="ivory", outline="black")
        super(Ball, self).__init__(canvas, item)


    def move(self):
        coords = self.getCoords()
        if coords[0] <= 0 or coords[2] >= 1200:
            self.direction[0] *= -1
        if coords[1] >= 800 or coords[1] <= 0:
            self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.canvas.move(self.item, x, y)
    
    def collide(self, objects, gameObjects):
        ballCoords = self.getCoords()
        x = (ballCoords[0] + ballCoords[2]) * 0.5
        if len(objects) == 1:
            object = objects[0]
            coords = object.getCoords()
            if x > coords[2]:
                self.direction[0] = -1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1
                self.speed *= 1.1
               # if x < (coords[2] + coords[0]) * 0.5 and isinstance(object, Paddle):
    #                self.direction[0] = -1
     #           elif x > (coords[2] + coords[0]) * 0.5 and isinstance(object, Paddle):
      #              self.direction[0] = 1
            if (isinstance(object, Brick)):
                object.deleteObject()
        elif len(objects) > 1:
            for y in objects:
                coords = y.getCoords()
                if x > coords[2]:
                    self.direction[0] = 1
                elif x < coords[0]:
                    self.direction[0] = -1
                else:
                    self.direction[1] *= -1
                if (isinstance(y, Brick)):
                    y.deleteObject()



class Paddle(GameObject):
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

class Brick(GameObject):
    def __init__(self, canvas, x, y):
        self.x = x
        self.y = y
        self.life = 1
        item = canvas.create_rectangle(x, y, x + 150, y + 20, fill="red", outline="black")
        super(Brick, self).__init__(canvas, item)

    


class Game(tk.Frame):
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
        self.objects = []
        self.objects.append(self.paddle)
        self.setupGame()
        self.canvas.focus_set()
        self.canvas.bind('<KeyPress>', self.keyPress)
        self.canvas.bind('<KeyRelease>', self.keyRelease)


    def addBall(self):
        if self.ball is not None:
           self.ball.deleteObject()
        wtf = Ball(self.canvas, 200, 200)
        return wtf
    
    def addPaddle(self):
        if self.paddle is not None:
            self.paddle.deleteObject()
        ret = Paddle(self.canvas, 150, 20)
        return ret
    
    def addBrick(self,x,y):
        brick = Brick(self.canvas, x, y)
        return brick

    def setupGame(self):
        y = 0
        self.ball = self.addBall()
        for i in range(3):
            x = 0
            for j in range(8):
                self.objects.append(self.addBrick(x,y))
                x += 150
            y += 20
        self.text = self.canvas.create_text(300,300, text="press space", fill="black")
        self.canvas.focus_set()
        self.canvas.bind("<space>",lambda event: self.startGame())

    def startGame(self):
        self.canvas.unbind('<space')
        self.canvas.delete(self.text)
        self.gameLoop()
        
    def gameLoop(self):
        i = 1
        while (i == 1):
            coords = self.ball.getCoords()
            self.checkCollisions()
            self.after(1,self.paddle.move(self.paddle.offset))
            self.update()
        #self.paddle.move(self.paddle.offset, 0)
        #self.after(100,self.move)
            if coords[3] >= 800: 
                self.ball.speed = 0
                i = 0
                self.after(1, self.setupGame())
            else:
                self.ball.move()
               # self.after(1,self.gameLoop())
    

    def keyPress(self, event):
        coords = self.paddle.getCoords()
        key = event.char
        if coords[0] > 20:
            if key == 'a':
                self.paddle.offset = -10
        if coords[2] < 1180:
            if key == 'd':
                self.paddle.offset = 10

    def keyRelease(self, event):
        self.paddle.offset = 0
    
    def checkCollisions(self):
        ballCoords = self.ball.getCoords()
        list = self.canvas.find_overlapping(*ballCoords)
        objects = []
        for x in list:
            for y in self.objects:
                if x == y.item:
                    objects.append(y)
        print(objects)
        self.ball.collide(objects, self.objects)



all = tk.Tk()
all.title = "brick breaker"
game = Game(all)
game.mainloop()