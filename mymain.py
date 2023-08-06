import random #generating random nums
import sys   #exiting game
import pygame
from pygame.locals import * #basic

#variables declaration
FPS = 32 # frames per second
Screen_width=289
Screen_height=511
Screen = pygame.display.set_mode((Screen_width,Screen_height))
ground_y = Screen_height*0.8
Game_sprites = {}
Game_sounds = {}
Player = 'C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\bird.png'
Background='C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\background.png'
Pipe='C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\pipe.png'

def welcomeScreen():
    
    Playerx=int(Screen_width/5)
    Playery=int(Screen_height-Game_sprites['player'].get_height())/2
    Messagex= -40
    Messagey=0
    basex=0
    while True:
        for event in pygame.event.get():
            #if user clicks on X button 
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
               pygame.quit()
               sys.exit()

            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                Screen.blit(Game_sprites['background'], (0,0))
                Screen.blit(Game_sprites['player'], (Playerx,Playery))
                Screen.blit(Game_sprites['message'], (Messagex,Messagey))
                Screen.blit(Game_sprites['base'], (basex,ground_y))
                pygame.display.update()
                FPSclock.tick(FPS)
                
def mainGame():
        score=0
        Playerx=int(Screen_width/5)
        Playery= int(Screen_width/2) 
        basex = 0  

        #creating 2 pipes randomly
        newPipe1=getRandomPipe()
        newPipe2=getRandomPipe()

        upperPipes = [
            {'x': Screen_width+200,'y':newPipe1[0]['y']},
            {'x': Screen_width+200+Screen_width/2,'y':newPipe1[0]['y'] }
        ]
        lowerPipes = [
            {'x': Screen_width+200,'y':newPipe2[1]['y']},
            {'x': Screen_width+200+Screen_width/2,'y':newPipe2[1]['y'] }
        ]
        pipevelx = -4
        Playervel1= -9
        PlayerMaxVel= 10
        PlayerminVel= -8
        PlayerAccY = 1

        Playerlapaccv= -8  #acceleration 
        Playerflapped = False # true only when bird is flapping

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key ==K_SPACE or event.key==K_UP):
                    if Playery>0:
                        Playervel1 = Playerlapaccv
                        Playerflapped=True 
                        Game_sounds['wing'].play()   
            crashtest = isCollide(Playerx,Playery,upperPipes,lowerPipes)
            if crashtest:
                return
            
            #checking score
            playerMidPos = Playerx + Game_sprites['player'].get_width()/2
            for pipe in upperPipes:
               pipeMidPos = pipe['x'] + Game_sprites['pipe'][0].get_width()/2
        
               if pipeMidPos<= playerMidPos < pipeMidPos +4:
                 score +=1
                 print(f"Your score is {score}") 
                 Game_sounds['point'].play()
            if Playervel1 < PlayerMaxVel and not Playerflapped:
                Playervel1+=PlayerAccY

            if Playerflapped:
                Playerflapped=False
            playerHeight = Game_sprites['player'].get_height()
            Playery=Playery + min(Playervel1,ground_y - Playery - playerHeight)

            for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
                upperPipe['x']+= pipevelx
                lowerPipe['x']+= pipevelx
            #adding new pipe
            if 0<upperPipes[0]['x']<5:
                newpipe = getRandomPipe()
                upperPipes.append(newpipe[0])  
                lowerPipes.append(newpipe[1])  

             #if pipe is out of screen remove it
            if upperPipes[0]['x'] <  -Game_sprites['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)  

            #blittig our sprites
            Screen.blit(Game_sprites['background'],(0,0))
            for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
               Screen.blit(Game_sprites['pipe'][0],(upperPipe['x'],upperPipe['y']))
               Screen.blit(Game_sprites['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
            Screen.blit(Game_sprites['base'],(basex,ground_y))
            Screen.blit(Game_sprites['player'],(Playerx,Playery))
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width+= Game_sprites['numbers'][digit].get_width()
            Xoffset = (Screen_width-width)/2   

            for digit in myDigits:
                Screen.blit(Game_sprites['numbers'][digit],(Xoffset,Screen_height*0.12))
                Xoffset += Game_sprites['numbers'][digit].get_width() 
            pygame.display.update()
            FPSclock.tick(FPS)    
def isCollide(Playerx,Playery,upperPipes,lowerPipes) :
    if Playery>ground_y - 25 or Playery<0:
        Game_sounds['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = Game_sprites['pipe'][0].get_height()
        if(Playery < pipeHeight + pipe['y'] and abs(Playerx-pipe['x'])<Game_sprites['pipe'][0].get_width()):
            Game_sounds['hit'].play()
            return True
    for pipe in lowerPipes:
        if(Playery+Game_sprites['player'].get_height()>pipe['y']) and abs(Playerx-pipe['x'])<Game_sprites['pipe'][0].get_width():
            Game_sounds['hit'].play()
            return True
    return False      


    
 
                




def getRandomPipe():
    #generating 2 random pipe 1 straight and 1 rotated 
    pipeHeight= Game_sprites['pipe'][0].get_height()
    offset = Screen_height/3 
    y2=offset + random.randrange(0,int(Screen_height - Game_sprites['base'].get_height() - 1.2 * offset) )  
    
    pipex  = Screen_width + 10
    y1 = pipeHeight - y2 + offset
    pipe=[
        {'x':pipex,'y': -y1},
        {'x':pipex,'y':y2}
    ]
    return pipe


                                      

if __name__ == "__main__":
    #the main funcion ,game  will start from here
    pygame.init() #initialize pygame modules
    FPSclock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Praneetha 1844')
    Game_sprites['numbers']= (
       pygame.image.load('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\0.png').convert_alpha(),
       pygame.image.load('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\1.png').convert_alpha(),
       pygame.image.load('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\2.png').convert_alpha(),
       pygame.image.load('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\3.png').convert_alpha(),
       pygame.image.load('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\4.png').convert_alpha(),
       pygame.image.load('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\5.png').convert_alpha(),
       pygame.image.load('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\6.png').convert_alpha(),
       pygame.image.load('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\7.png').convert_alpha(),
       pygame.image.load('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\8.png').convert_alpha(),
       pygame.image.load('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\9.png').convert_alpha()
       
    )

    Game_sprites['message']= pygame.image.load('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\message.png').convert_alpha()
    Game_sprites['base']= pygame.image.load('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\sprites\\base.png').convert_alpha()
    Game_sprites['pipe']= (
        pygame.transform.rotate(pygame.image.load(Pipe).convert_alpha(),180),
        pygame.image.load(Pipe).convert_alpha()

    )

    #sounds
    Game_sounds['die']= pygame.mixer.Sound('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\audio\\die.wav')
    Game_sounds['hit']= pygame.mixer.Sound('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\audio\\hit.wav')
    Game_sounds['point']= pygame.mixer.Sound('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\audio\\point.wav')
    Game_sounds['swoosh']= pygame.mixer.Sound('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\audio\\swoosh.wav')
    Game_sounds['wing']= pygame.mixer.Sound('C:\\Users\\sures\\OneDrive\\Desktop\\flappy\\gallery\\audio\\wing.wav')

    Game_sprites['background']= pygame.image.load(Background).convert()
    Game_sprites['player']=pygame.image.load(Player).convert_alpha()

    while True:
        welcomeScreen() #show screen until button is clicked
        mainGame() 
    