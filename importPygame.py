#Imports pygame, allowing gaming creation
import pygame
pygame.init()

#Game window dimensions
sHeight = 472
sWidth = 500

clock = pygame.time.Clock()

#Sets score to 0
score = 0

win = pygame.display.set_mode((sWidth,sHeight))

#This code chunk loads all pictures of player, allows animation
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

#This creates a class "player".
class player(object):
    #The code below is the first "init method"
    def __init__(self,x,y,width,height):
        #The code below are variables for the "player" class
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

    #The draw funtion found in the init method "draws" the player  
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

    #The code below is the "hit" funtion.
    def hit(self):
        self.x = 60 
        self.y = 410
        self.walkCount = 0
        #The code below sets the game font.
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
        
#Enemy Class (NPC)
class enemy(object):
    #The code below calls from, "resources", the images 
    i = 0
    numberOfImages = 11
    walkLeft = []
    walkRight = []
    directoryName = 'enemy'
    

    while(i < numberOfImages):
        i += 1
        walkLeftElement = "resources/" + directoryName + "/L" + str(i) + ".png"
        walkRightElement = "resources/" + directoryName + "/R" + str(i) + ".png"
        walkLeft.append(pygame.image.load(walkLeftElement))
        walkRight.append(pygame.image.load(walkRightElement))
        
    #This is the init method for the class "enemy."    
    def __init__(self,x,y,width,height,end):
         #These are the attributes for "enemy"
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
         self.respawn = False
    #This is the draw method for "enemy." This "draws" the enemy.         
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
            #This code draws the hitbox for the "enemy" class.
            pygame.draw.rect(win,(255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win,(0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    #This code creates the moving animation for the NPC. Making it move without any key presses. 
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

    #"enemy" class hit funtion.
    def hit(self):
        if self.health >0:
            self.health -= 1
        else:
            #This code forces the "enemy" image to dissapear, and Deletes the hitbox. 
            self.visible = False
            self.hitbox = (self.x + 0, self.y + 0, 0,0)
            self.respawn = True

#This is the "secondEnemy" class. (NPC)
class secondEnemy(object):
    #Init method for "secondEnemy."
    def __init__(self,x,y,width,height,end,numberOfImages,directoryName):
        #"secondEnemy" attributes.
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
        self.respawn = False
        i = 0
        self.numberOfImages = 9
        self.walkLeft = []
        self.walkRight = []
        directoryName = 'secondEnemy'
        while(i < numberOfImages):
            #This code calls the "secondEnemy" images. Allowing animation.
            i = i + 1
            walkLeftElement = "resources/" + directoryName + "/L" + str(i) + "S.png"
            walkRightElement = "resources/" + directoryName + "/R" + str(i) + "S.png"
            walkLeft.append(pygame.image.load(walkLeftElement))
            walkRight.append(pygame.image.load(walkRightElement))

    #This code draws "secondEnemy."
    def draw(self,win):
        self.move()
        if self.walkCount + 1 >= self.numberOfImages * 3:
            self.walkCount = 0
            
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
            self.walkCount += 1
            
        else:
            win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
            self.walkCount += 1

            #This code draws the hitbox for the "secondEnemy" class.
            pygame.draw.rect(win,(255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win,(0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    #This code creates the moving animation for the NPC. Making it move without any key presses.
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

    #"enemy" class hit funtion.
    def hit(self):
        if self.health >0:
            self.health -= 1
        else:
            #This code forces the "enemy" image to dissapear, and Deletes the hitbox.
            self.visible = False
            self.hitbox = (self.x + 0, self.y + 0, 0,0)
            self.respawn = True

#This code is the class for the player's "projectiles."
class projectile(object):
    #init method for "projectile."
    def __init__(self,x,y,radius,color,facing):
        #Projectile attribute.
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = facing
        self.color = color
        self.vel = 8*facing

    #Draws "projectile."
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)

#This code draws all proposed images with a "draw" funtion, inside the game window.
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
#This sets the size and spawn location of "player."
man = player(300, 410, 64, 64)
#This sets the size and spawn location of "enemy."
goblin = secondEnemy(100,410,64,64,450,9,"secondEnemy")
#I have no idea what this does.
shootLoop = 0
run = True
bullets = []
while run:
    clock.tick(27)

    #This code sets a funtion to when the "player" hits the "enemy", the score is decreased by 5.
    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            man.hit()
            score -= 5

    #Your guess is as good as mine.
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    #This exits the loop.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #exit the loop

    #This code makes it so when enough bullets hits the "enemy", it will remove the "enemy" images and hitbox. It also adds 1 point to the score whenever a bullet hits.
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
        
    #This code defines "keys."
    keys = pygame.key.get_pressed()

    #This code is a funtion that states, when the space bar is pressed, it will shoot a bullet.
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1

        #This code sets the size of the bullet, and how many bullets are allowed on screen.
        if len(bullets)<5:
            bullets.append(projectile(round(man.x+man.width//2),
                            round(man.y+man.height//2),6,(0,0,0),facing))

        shootLoop = 1
    #This code sets the left arrow key to move "player" left when pressed.
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    #This code sets the right key to move the "player" right when pressed.
    elif keys[pygame.K_RIGHT] and man.x < (sWidth - man.width):  
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
        #This code sets the up arrow key to make the "player" jump when pressed.
        if keys[pygame.K_UP]:
            man.isJump = True
            #man.left = False
            #man.right = False
            man.walkCount = 0
    else:
        #I think this code keeps him down otherwise.
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







