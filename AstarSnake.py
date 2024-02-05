import pygame
from pygame.locals import *
import time
import random 
from queue import PriorityQueue

SIZE = 30
BG_COLOR = (0,175,0)
GAMESPEED = .05

class Border:
    def __init__(self,parentscreen):
        self.borderLR=pygame.image.load("./Resources\\borderLR.png")
        self.borderTB=pygame.image.load("./Resources\\borderTB.png")
        self.parentscreen=parentscreen
        
    def draw(self):
        self.parentscreen.blit(self.borderLR,(0,0))
        self.parentscreen.blit(self.borderLR,(600,0))
        self.parentscreen.blit(self.borderTB,(0,0))
        self.parentscreen.blit(self.borderTB,(0,600))
        # pygame.display.flip()
        
class Apple:
    def __init__(self,parentscreen,snake):
        self.snake=snake
        self.appleblock=pygame.image.load("./Resources\\appleicon.png")
        self.parentscreen=parentscreen
        self.x=random.randint(3,5)*SIZE
        self.y=random.randint(3,5)*SIZE

    def draw(self):
        self.parentscreen.blit(self.appleblock,(self.x,self.y))
        # pygame.display.flip()

    def move(self):
        self.snakexy = []
        for i in range(self.snake.length):
            self.snakexy.append((self.snake.x[i],self.snake.y[i]))

        self.x = random.randrange(1,18)*SIZE
        self.y = random.randrange(1,18)*SIZE

        self.applexy = (self.x, self.y)
        
        for i in range(len(self.snakexy)):
            if (self.applexy == self.snakexy[i]):
                self.move()
        
        print("Apple Moved")

    # def move(self):
    #     self.Tempx=random.randint(0,17)*SIZE
    #     self.Tempy=random.randint(0,17)*SIZE
        
    #     for i in range(self.snake.length):
    #         if(self.snake.x[i]==self.Tempx and self.snake.y[i]==self.Tempy):
    #             print("snake x ",self.snake.x[i]," and snake y ",self.snake.y[i])
    #             self.move()
                                  
    #     self.x=self.Tempx
    #     self.y=self.Tempx
    #     print("Apple Moved")

class Snake:
    def __init__(self,parentscreen,length):
        self.length=length
        self.parentscreen=parentscreen
        self.snakeblock=pygame.image.load("./Resources\\snakehead.png")
        self.x=[SIZE]*length
        self.y=[SIZE]*length
        self.direction='down'
        
    def increase(self):
        print("Snake Length Incresed")
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)   

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]
            
        if self.direction=='up':
            self.y[0]-=SIZE
        if self.direction=='down':
            self.y[0]+=SIZE
        if self.direction=='left':
            self.x[0]-=SIZE
        if self.direction=='right':
            self.x[0]+=SIZE
        self.draw()
        
    def draw(self):
        self.parentscreen.fill((0,175,0))    
        for i in range(self.length):
            self.parentscreen.blit(self.snakeblock,(self.x[i],self.y[i]))
        # pygame.display.flip()

    def upmove(self):
        self.direction='up'

    def downmove(self):
        self.direction='down'   

    def leftmove(self):
        self.direction='left'

    def rightmove(self):
        self.direction='right'

class manhattan:
    def __init__(self,parentscreen,snake,apple):
        self.parentscreen=parentscreen  
        self.snake=snake
        self.apple=apple

    def run(self):
        
        # dist = (self.snake.x-self.apple.x) + (self.snake.y-self.apple.y)
        # distance = |x2 - x1| + |y2 - y1|
        
        self.up = abs(self.snake.x[0] - self.apple.x) + abs((self.snake.y[0]-SIZE) - self.apple.y)
        self.down = abs(self.snake.x[0] - self.apple.x) + abs((self.snake.y[0]+SIZE) - self.apple.y)
        self.left = abs((self.snake.x[0]-SIZE) - self.apple.x) + abs(self.snake.y[0] - self.apple.y)
        self.right = abs((self.snake.x[0]+SIZE) - self.apple.x) + abs(self.snake.y[0] - self.apple.y)        
        
        if self.snake.direction == 'up':
            self.direct = min(self.up,self.left,self.right)    
        if self.snake.direction == 'down':
            self.direct = min(self.down,self.left,self.right)
        if self.snake.direction == 'left':
            self.direct = min(self.left,self.up,self.down)
        if self.snake.direction == 'right':
            self.direct = min(self.right,self.up,self.down)
        
        if self.direct == self.up:
            self.snake.upmove()
        if self.direct == self.down:
            self.snake.downmove()
        if self.direct == self.left:
            self.snake.leftmove()
        if self.direct == self.right:
            self.snake.rightmove()

class AStar:
    """
     A star algorithm implementation
     f(n) = g(n) + h(n)
     """

    def __init__(self):
        self.paths = [
            "UP",
            "DOWN",
            "RIGHT",
            "LEFT"
        ]
        self.invalid = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }

        self.moves = 0

    # def collides(self, headPosition, snake):
    #     """ Check for body collision on the next step """
    #     return any([body.position == headPosition for body in snake.body[: -1]])

    def getDistances(self, goal, snakeheadx, snakeheady, snake):
        """ Finding distance for each path """
        distances = PriorityQueue()
        self.moves += 1

        for path in self.paths:
            x = None
            y = None
            goal_x = goal.x
            goal_y = goal.y

            if path is "UP":
                snake.x = snakeheadx
                snake.y = snakeheady - 1

            elif path is "DOWN":
                x = snakeheadx
                y = snakeheady + 1

            elif path is "RIGHT":
                x = snakeheadx + 1
                y = snakeheady

            elif path is "LEFT":
                x = snakeheadx - 1
                y = snakeheady

            # if self.collides((x, y), snake):
            #     continue

            gn = self.moves
            # hn = abs(x - goal_x) + abs(y - goal_y)
            hn = abs(self.snake.x[0] - self.apple.x) + abs((self.snake.y[0]) - self.apple.y)
            fn = gn + hn

            # add to queue
            distances.put((fn, path))

        return distances

    def getKey(self, food, snake):
        """ Returns the next step """
        if snake.x[0] == food.x and snake.y[0] == food.y:
            self.moves = 0
            return snake.direction

        distances = self.getDistances(food, snake.x[0],snake.y[0], snake)

        if distances.qsize() == 0:
            return snake.direction

        return distances.get()[1]

class Game:
    def __init__(self):
        pygame.init()
        self.surface=pygame.display.set_mode((630,660))
        self.surface.fill(BG_COLOR)
        self.snake=Snake(self.surface,2)
        self.snake.draw()
        self.apple=Apple(self.surface,self.snake)
        self.apple.draw()
        self.border=Border(self.surface)
        self.border.draw()
        self.man=manhattan(self.surface,self.snake,self.apple)
        self.man.run()
        self.astar = AStar()
    
    def play(self):

        self.snake.walk()
        self.apple.draw()
        self.display_score()
        self.border.draw()
        pygame.display.flip()
        self.collision()
        # self.man.run()
        self.path = self.astar.getKey(self.apple,self.snake)
        print(self.path)
        
    def collision(self):

        #snake colliding with apple
        if(self.apple.x==self.snake.x[0] and self.apple.y==self.snake.y[0]):
            print("Apple Eated")
            self.snake.increase()
            self.apple.move()
            # self.checkapple()
        
        #snake colliding with itself
        for i in range(1,self.snake.length):
            if(self.snake.x[0]==self.snake.x[i] and self.snake.y[0]==self.snake.y[i]):
                print("snake collided itself")
                raise "Game Over"
   
        #snake colliding the boundaries:
        #Top Non Visible Wall
        for i in range(0,600,30):
            if(self.snake.x[0]==i and self.snake.y[0]==0):
                print("snake collided with Top Wall")
                raise "Game Over"
        #Bottom Non Visible Wall    
        for i in range(0,600,30):
            if(self.snake.x[0]==i and self.snake.y[0]==600):
                print("snake collided with Bottom Wall")
                raise "Game Over"      
        #Left Non Visible Wall
        for i in range(0,600,30):
            if(self.snake.x[0]==0 and self.snake.y[0]==i):
                print("snake collided with Left Wall")
                raise "Game Over"  
        #Right Non Visible Wall
        for i in range(0,600,30):
            if(self.snake.x[0]==600 and self.snake.y[0]==i):
                print("snake collided with Right Wall")
                raise "Game Over"  
    
    def display_score(self):
        font=pygame.font.SysFont('Verdana',20)
        score=font.render(f"Score:{self.snake.length-2}",True,(247, 227, 0))
        self.surface.blit(score,(500,630))
    
    def display_gameover(self):
        self.surface.fill(BG_COLOR)
        font1=pygame.font.SysFont('Verdana',30)
        font2=pygame.font.SysFont('Verdana',20)
        msg1=font1.render(f"Game Over! Your Score:{self.snake.length-2}",True,(255,255,255))
        self.surface.blit(msg1,(130,250))
        msg2=font2.render(f"Press Enter OR Space for Replay",True,(255,255,255))
        self.surface.blit(msg2,(160,310))
        msg3=font2.render(f"(or)",True,(255,255,255))
        self.surface.blit(msg3,(280,340))
        msg4=font2.render(f"Press Escape for Exit",True,(255,255,255))
        self.surface.blit(msg4,(220,370))
        pygame.display.flip()
    
    def gamereset(self):
        self.snake = Snake(self.surface,2)
        self.apple = Apple(self.surface,self.snake)
        # self.man = manhattan(self.surface,self.snake,self.apple)

    def run(self):
        running=True
        pause=False
        while running:
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        pygame.quit()
                    if event.key==K_RETURN or event.key==K_SPACE:
                        pause=False
                        
                    if (event.key==K_w or event.key==K_UP): 
                        if(self.snake.length==1):
                            self.snake.upmove()
                        elif(self.snake.length>1):
                            self.snake.downmove() if(self.snake.direction=='down') else self.snake.upmove()
                       
                    if (event.key==K_s or event.key==K_DOWN):
                        if(self.snake.length==1):
                            self.snake.downmove()
                        elif(self.snake.length>1):
                            self.snake.upmove() if(self.snake.direction=='up') else self.snake.downmove()
                                
                    if (event.key==K_a or event.key==K_LEFT):
                        if(self.snake.length==1):
                            self.snake.leftmove()
                        elif(self.snake.length>1):
                            self.snake.rightmove() if(self.snake.direction=='right') else self.snake.leftmove()
                            
                    if (event.key==K_d or event.key==K_RIGHT):
                        if(self.snake.length==1):
                                self.snake.rightmove()
                        elif(self.snake.length>1):
                            self.snake.leftmove() if(self.snake.direction=='left') else self.snake.rightmove()
                        
                elif event.type==QUIT :
                    pygame.quit()
                    
            try: 
                if not pause:                   
                    self.play()
            except Exception as e:
                self.display_gameover()    
                pause=True
                self.gamereset()
                
            time.sleep(GAMESPEED)
 
game=Game()
game.run()
