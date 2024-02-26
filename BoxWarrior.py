import pygame
import random
import time 

class Player(pygame.sprite.Sprite):   #defining player class
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(midbottom = (x,y))
        self.rect.x = x
        self.rect.y = y
        self.isjump = False
        self.jump_velocity = 0
        self.collidestate = 0
        self.facing = True
        self.score = 0
        self.health = 10

    def move_left(self):   #character movement
        self.rect.x -= 5
        if self.rect.x < 0:
            self.rect.x = 0
        if self.facing == True:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing = False

    def move_right(self):
        self.rect.x += 5
        if self.rect.x >= 663:
            self.rect.x = 663

        if self.facing == False:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing = True

    def jump(self):
        if self.isjump == False:
            self.isjump = True
            self.jump_velocity = -11

    def update(self):
        if self.isjump == True:
            if self.jump_velocity < 8.5:
                self.jump_velocity += 0.5
            self.rect.y += self.jump_velocity

            
    def gravity(self,whichplatform):     #player falling after walking off platform
        if self.rect.colliderect(whichplatform.rect) == False and self.isjump == False:
            self.jump_velocity += 0.5
            self.rect.y += self.jump_velocity

    def damage(self,enemy):
            self.health -= 1
            
    def attack(self,enemylist,direction):   #creates attack sprite which collides with enemy
        sword = Attacks(self.rect.x, self.rect.y, 'graphics/attack.png',direction)
        if self.facing == False:
            sword.image = pygame.transform.flip(sword.image, True, False)
        attackgroup = pygame.sprite.Group()
        attackgroup.add(sword)
        attackgroup.draw(screen)

        for i in range(len(enemylist)):  #checks for enemy collisions with attack sprite
           if sword.rect.colliderect(enemylist[i].rect):
               enemylist[i].dead = True
               enemylist[i].kill()
               del enemylist[i]
               enemylist[i] = Enemy(random.randint(0,670), random.randint(0,400), 'graphics/enemy.png')
               enemygroup.add(enemylist[i])
               self.score += 1
                           
class Enemy(pygame.sprite.Sprite): #defines enemy class
    def __init__(self,x,y,image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(midtop = (x,y))
        self.rect.x = x
        self.rect.y = y
        self.health = 1
        self.velocity_y = random.uniform(-2.0,2.0)
        self.velocity_x = random.uniform(-3.0,3.0)
        self.collidestate = 1
        self.dead = False

    def movement(self):

        if 125 > warrior.rect.y - self.rect.y > -125 and 125 > warrior.rect.x - self.rect.x > -125:   #enemy seeking player

            if warrior.rect.y < self.rect.y:
                self.velocity_y -= 2
            elif warrior.rect.y > self.rect.y:
                self.velocity_y += 2

            if warrior.rect.x < self.rect.x:
                self.velocity_x -= 2
            elif warrior.rect.x > self.rect.x:
                self.velocity_x += 2

        if self.velocity_x > 3:     #limits enemy velocity
            self.velocity_x = 3
        if self.velocity_y > 2:
            self.velocity_y = 2
        if self.velocity_x < -3:
            self.velocity_x = -3
        if self.velocity_y < -2:
            self.velocity_y = -2
        if self.velocity_y == 0:
            self.velocity_y += 1
        if self.velocity_x == 0:
            self.velocity_x += 1
        
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        if self.rect.x < 0:   #boundaries for enemies
            self.rect.x = 0
            self.velocity_x = 3
        if self.rect.x >= 680:
            self.rect.x = 680
            self.velocity_x = -3
        if self.rect.y <= 0:
            self.rect.y = 0
            self.velocity_y = 2
            
        
    def gravity(self,whichplatform):
        nothing = 0

class Platform(pygame.sprite.Sprite):  #defines platform class
    def __init__(self,x,y,image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(midtop = (x,y))
        
        self.rect.x = x
        self.rect.y = y

class Attacks(pygame.sprite.Sprite):     #defines attack class
    def __init__(self,x,y,image,direction):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center = (x,y))

        self.rect.x = x - direction        #changes position of attack sprite depending on player direction
        self.rect.y = y - 5 
         
def collisions(whichplatform,sprite):  
    if sprite.rect.colliderect(whichplatform.rect):
        if whichplatform.rect.y == 464:
            sprite.rect.bottom = whichplatform.rect.top
            sprite.isjump = False
            sprite.jump_velocity = 0

        if sprite.rect.bottom > whichplatform.rect.top and sprite.rect.bottom - whichplatform.rect.top < 10 and whichplatform.rect.y != 464:  #only allows collisions within certain range of a player
            sprite.rect.bottom = whichplatform.rect.top
            sprite.isjump = False
            sprite.jump_velocity = 0
        if sprite.rect.top < whichplatform.rect.bottom and whichplatform.rect.bottom - sprite.rect.top < 10 and whichplatform.rect.y != 464:
            sprite.rect.top = whichplatform.rect.bottom 
            sprite.jump_velocity = 0

        if sprite.collidestate == 1:     #checks type of sprite
            sprite.velocity_y = random.uniform(-3.0,3.0)

def collisionselect(sprite): #checks which platform has the collision
    if sprite.rect.colliderect(platformlist[0].rect):
        collisions(platformlist[0],sprite)
        sprite.gravity(platformlist[0])
    elif sprite.rect.colliderect(platformlist[1].rect):
        collisions(platformlist[1],sprite)
        sprite.gravity(platformlist[1])
    elif sprite.rect.colliderect(platformlist[2].rect):
        collisions(platformlist[2],sprite)
        sprite.gravity(platformlist[2])
    elif sprite.rect.colliderect(platformlist[3].rect):
        collisions(platformlist[3],sprite)
        sprite.gravity(platformlist[3])
    elif sprite.rect.colliderect(platformlist[4].rect):
        collisions(platformlist[4],sprite)
        sprite.gravity(platformlist[4])
    elif sprite.rect.colliderect(platformlist[5].rect):
        collisions(platformlist[5],sprite)
        sprite.gravity(platformlist[5])
    elif sprite.rect.colliderect(platformlist[6].rect):
        collisions(platformlist[6],sprite)
        sprite.gravity(platformlist[6])
    elif sprite.rect.colliderect(platformlist[7].rect):
        collisions(platformlist[7],sprite)
        sprite.gravity(platformlist[7])
    collisions(floor1,sprite)
    sprite.gravity(floor1)

pygame.init()

screen = pygame.display.set_mode((696,594))
pygame.display.set_caption('Box Warrior')
clock = pygame.time.Clock()


menu = pygame.image.load('graphics/menu.png')     #loading images to variables
helppage = pygame.image.load('graphics/help.png')

startscreen = pygame.image.load('graphics/startscreen.png')
screen.blit(startscreen,(0,0))
pygame.display.update()
    
font = pygame.font.SysFont(None, 35)

file = "highscore.txt"

with open(file,"r") as myfile:    #reading highscore file
    highscores = myfile.readlines()
    highscore = highscores[1]
    highscore_integer = int(highscores[0])

display_highscore = font.render('Current Fastest Time: ' + highscore, True, (30,30,30))

background = pygame.image.load('graphics/background.png')

warrior = Player(50, 300, 'graphics/soldier1.png') #create player sprite
playergroup = pygame.sprite.Group()
playergroup.add(warrior)
 
enemygroup = pygame.sprite.Group()
enemylist = {}

HELP = False
pregame = True
start = True

while pregame == True:                    #loop for menu and controls screens
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if HELP == False and start == False:
                screen.blit(menu,(0,0))
                screen.blit(display_highscore, (160, 510))
                pygame.display.update()
                    
        if event.type == pygame.KEYDOWN:
                start = False
            
                if event.key == pygame.K_1:
                    enemycount = 4
                    warrior.health = 15
                    pregame = False
                if event.key == pygame.K_2:
                    enemycount = 6
                    warrior.health = 10
                    pregame = False
                if event.key == pygame.K_3:
                    enemycount = 8
                    warrior.health = 5
                    pregame = False
                if event.key == pygame.K_h:
                    screen.blit(helppage,(0,0))
                    pygame.display.update()
                    HELP = True
                
                if event.key == pygame.K_ESCAPE:
                    HELP = False
                                
time.sleep(1)

for i in range(enemycount):    #creates instances of enemy class
    enemylist[i] = Enemy(random.randint(0,670), random.randint(0,400), 'graphics/enemy.png')
    enemygroup.add(enemylist[i])

platformgroup = pygame.sprite.Group()
platformlist = {}

coordslist = [50,370,50,130,175,250,300,370,300,130,425,250,550,130,550,370]  #holds platform coordinates

for x in range(8):
    platformlist[x] = Platform(coordslist[2*x],coordslist[2*x+1],'graphics/platform.png')    #creates instances of platform class
    platformgroup.add(platformlist[x])
    
floor1 = Platform(0, 464,'graphics/floor1.png')
platformgroup.add(floor1)

immunity = True
clockcount = 0
clockcount2 = 0
clockcount3 = 0
seconds = 0
minutes = 0
canattack = True
direction_value = 5


while warrior.health > 0 and warrior.score < 20:   #game loop
    
    screen.blit(background,(0,0))
    img = font.render('Health: ' + str(warrior.health), True, (30,30,30)) #variables for creating text
    img2 = font.render('Score: ' + str(warrior.score), True, (30,30,30))

    platformgroup.draw(screen)
        
    playergroup.update()
    playergroup.draw(screen)

    enemygroup.update()
    enemygroup.draw(screen)

    clockcount2 += 1
    clockcount3 += 1
    clockcount += 1

    if clockcount == 75:
        immunity = False
        clockcount = 0

    if clockcount2 == 20:
        canattack = True

    if clockcount3 == 50:    #timer
        seconds += 1
        clockcount3 = 0

    if seconds == 60:
        minutes += 1
        seconds = 0

    if seconds < 10:
        string_seconds = "0" + str(seconds)
    else:
        string_seconds = str(seconds)

    if minutes < 10:
        string_minutes = "0" + str(minutes)
    else:
        string_minutes = str(minutes)

    img3 = font.render('Time: ' + ' ' + string_minutes + ':' + string_seconds, True, (30,30,30))

    for i in range(len(enemylist)):   #checks for enemy collisions
        enemylist[i].movement()
        collisionselect(enemylist[i])
        if immunity == False and enemylist[i].dead == False:
            if warrior.rect.colliderect(enemylist[i].rect):
                warrior.damage(enemylist[i])
                immunity = True
        
    collisionselect(warrior)
        
    for event in pygame.event.get():      #checks if X is pressed
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                warrior.jump()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:    #user inputs
        warrior.move_left()
        direction_value = 35
    if keys[pygame.K_RIGHT]:
        warrior.move_right()
        direction_value = -5
    if keys[pygame.K_x] and canattack == True:
        warrior.attack(enemylist,direction_value)
        canattack = False
        clockcount2 = 0

    screen.blit(img, (20, 20))  #pastes text
    screen.blit(img2, (275, 20))
    screen.blit(img3, (525, 20))

    pygame.display.update()
    clock.tick(50)    #framerate
        
if warrior.health < 1:  #loss
    gameover = pygame.image.load('graphics/gameover.png')
    screen.blit(gameover,(-62,-100))

else:
    youwin = pygame.image.load('graphics/youwin.png') #win
    screen.blit(youwin,(-62,-100))
    img3 = font.render('Completion Time: ' + ' ' + string_minutes + ':' + string_seconds, True, (255,255,255))
    newhighscore = font.render('NEW FASTEST TIME!', True, (255,255,255))
    screen.blit(img3, (200, 525))

    newscore = int(string_minutes + string_seconds) #write to highscore text file
    if newscore < highscore_integer:  
        with open(file, "w") as myfile:
            myfile.write(str(newscore) + "\n")
            myfile.write(string_minutes + ':' + string_seconds)
            screen.blit(newhighscore, (210, 490))

pygame.display.update()
time.sleep(5)
pygame.quit()    
