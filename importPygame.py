import pygame
pygame.init()


sHeight = 472
sWidth = 500

clock = pygame.time.Clock()
score = 0

win = pygame.display.set_mode((sWidth,sHeight))

walkRight = [pygame.image.load('resources/character/R1.png'),
        pygame.image.load('resources/character/R2.png'),
        pygame.image.load('resources/character/R3.png'),
        pygame.image.load('resources/character/R4.png'),
        pygame.image.load('resources/character/R5.png'),
        pygame.image.load('resources/character/R6.png'),
        pygame.image.load('resources/character/R7.png'),
        pygame.image.load('resources/character/R8.png'),
        pygame.image.load('resources/character/R9.png')]
walkLeft = [pygame.image.load('resources/character/L1.png'),
        pygame.image.load('resources/character/L2.png'),
        pygame.image.load('resources/character/L3.png'),
        pygame.image.load('resources/character/L4.png'),
        pygame.image.load('resources/character/L5.png'),
        pygame.image.load('resources/character/L6.png'),
        pygame.image.load('resources/character/L7.png'),
        pygame.image.load('resources/character/L8.png'),
        pygame.image.load('resources/character/L9.png')]
bg = pygame.image.load('resources/bg.jpg')
char = pygame.image.load('resources/character/standing.png')

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
 
    def draw(self,win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3],(self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0],(self.x,self.y))
            else:
                win.blit(walkLeft[0],(self.x,self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        
#Enemy Class
class enemy(object):
    walkRight = [pygame.image.load('resources/enemy/R1E.png'),
        pygame.image.load('resources/enemy/R2E.png'),
        pygame.image.load('resources/enemy/R3E.png'),
        pygame.image.load('resources/enemy/R4E.png'),
        pygame.image.load('resources/enemy/R5E.png'),
        pygame.image.load('resources/enemy/R6E.png'),
        pygame.image.load('resources/enemy/R7E.png'),
        pygame.image.load('resources/enemy/R8E.png'),
        pygame.image.load('resources/enemy/R9E.png'),
        pygame.image.load('resources/enemy/R10E.png'),
        pygame.image.load('resources/enemy/R11E.png')]
    walkLeft = [pygame.image.load('resources/enemy/L1E.png'),
        pygame.image.load('resources/enemy/L2E.png'),
        pygame.image.load('resources/enemy/L3E.png'),
        pygame.image.load('resources/enemy/L4E.png'),
        pygame.image.load('resources/enemy/L5E.png'),
        pygame.image.load('resources/enemy/L6E.png'),
        pygame.image.load('resources/enemy/L7E.png'),
        pygame.image.load('resources/enemy/L8E.png'),
        pygame.image.load('resources/enemy/L9E.png'),
        pygame.image.load('resources/enemy/L10E.png'),
        pygame.image.load('resources/enemy/L11E.png')]
    def __init__(self,x,y,width,height,end):
         self.x = x
         self.y = y
         self.width = width
         self.height = height
         self.end = end
         self.path = [self.x,self.end]
         self.walkCount = 0
         self.vel = 3
         self.hitbox = (self.x + 17, self.y + 2, 31,57)
         self.health = 10
         self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
            
            else:
                win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1

            pygame.draw.rect(win,(255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win,(0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self):
        if self.vel  > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel ^ -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel ^ -1
                self.walkCount = 0

    def hit(self):
        if self.health >0:
            self.health -= 1
        else:
            self.visible = False

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = facing
        self.color = color
        self.vel = 8*facing
    
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)
        
def redrawGameWindow():
    win.blit(bg,(0,0))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    text = font.render("Score: " + str(score), 1, (0,0,0))
    # Arguments are: text, anti-aliasing, color
    win.blit(text, (390, 10))

    pygame.display.update()
 

#Main Loop
font = pygame.font.SysFont("comicsans", 30, True)
man = player(300, 410, 64, 64)
goblin = enemy(100,410,64,64,450)
shootLoop = 0
run = True
bullets = []
while run:
    clock.tick(27)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #exit the loop

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
                
        if bullet.x < 500 and bullet.x >0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
        

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets)<5:
            bullets.append(projectile(round(man.x+man.width//2),
                            round(man.y+man.height//2),6,(0,0,0),facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < (sWidth - man.width):  #You had (man.width - man.vel) instead of (sWidth - man.width)
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False

    else:
        #man.left = False
        #man.right = False
        man.walkCount = 0
        man.standing = True
        
    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            #man.left = False
            #man.right = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1

        else:
            man.isJump = False
            man.jumpCount = 10

            
    redrawGameWindow()
   
pygame.quit()
