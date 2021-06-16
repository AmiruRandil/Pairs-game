import pygame
import time
import random
pygame.init()

#win size
display_height = 600
display_width = 1000
#creating arrays
X = [0,150,300,450,0,150,300,450,0,150,300,450]
Y = [0,0,0,0,150,150,150,150,300,300,300,300]
#colors
white = (255,255,255)
red = (255,0,0)
blue = (0,255,255)
dblue = (0,0,255)
lred = (255,102,102)
#load images
background1 = pygame.image.load('background1.png') 
background = pygame.image.load('background.png')
background2 = pygame.image.load('background2.png')
background3 = pygame.image.load('background3.png')
cover = pygame.image.load('cover.png')
image1 = pygame.image.load('inside1.png')
image2 = pygame.image.load('inside2.png')
image3 = pygame.image.load('inside3.png')
#scale images
scover = pygame.transform.scale(cover,(150,150))
simage1 = pygame.transform.scale(image1,(150,150))
simage2 = pygame.transform.scale(image2,(150,150))
simage3 = pygame.transform.scale(image3,(150,150))
sbackground = pygame.transform.scale(background, (1000,600))
sbackground1 = pygame.transform.scale(background1, (1000,600))
sbackground2 = pygame.transform.scale(background2, (1000,600))
sbackground3 = pygame.transform.scale(background3, (1000,600))
#image order
order = [simage1,simage2,simage1,simage3,simage2,simage1,simage3,simage1,simage2,simage3,simage2,simage3]
random.shuffle(order)#shuffle
revealed = [False,False,False,False,False,False,False,False,False,False,False,False]
locked = [False,False,False,False,False,False,False,False,False,False,False,False]
ClickCount = [0,0,0,0,0,0,0,0,0,0,0,0] #how many times an imag was clicked
#game display
win = pygame.display.set_mode((display_width,display_height)) 
#game caption
pygame.display.set_caption("TWELVE CELLS") 


# image click func
def ImageClicked(x,y):
    global X
    global Y
    global revealed
    Clicked = False
    ImageIndex = None
    for count in range(len(X)):
        if X[count]<x and X[count] + 150 >x:
            if Y[count]<y and Y[count] + 150 >y:
                if revealed[count] == True: #check if the image was clicked before
                    ImageIndex = None #if image was clicked before
                else:
                    revealed[count] = True #if not
                    Clicked = True
                    ImageIndex = count
    return Clicked, ImageIndex #return values


#image click check and score
Score  = 0
First = None
def Check(index):
    global Score
    global First
    global ClickCount
    if First == None:
        First = index #first image that was clicked
    else:
        display_update()
        pygame.time.delay(300)
        if order[index] == order[First]: #check if the clicked images are equal
            locked[index] = True #lock if the images match
            locked[First] = True
            Score += 20 #if matched
        else:
            pygame.time.delay(100)
            revealed[index] = False #hide if the images dont match
            revealed[First] = False
            Score -= ClickCount[First]*5 #penalty
            ClickCount[First] += 1 #clicked counter
            ClickCount[index] += 1
        First = None
    return Score


def display_update():
    #bliting image
    global revealed
    global locked
    for count in range(len(X)):
         if revealed[count] == True or locked[count] == True: #if an image is revealed or locked
             win.blit(order[count], (X[count],Y[count])) #inside the cover image
         else:
            win.blit(scover, (X[count], Y[count])) #if not revealed or locked
    #update display
    pygame.display.update()
    

#count dowm
t = 0
def timer():
    global StartTime
    global white
    global t
    TimeFinish = 0.0
    t = 60-(time.time() - StartTime)
    t1 = "Time Left: "+str(round(t,1))
    if t >=0.0:
        Font = pygame.font.SysFont('Times New Roman', 32) #font
        SurfaceTime = Font.render(str(t1), True, white)
        win.blit(SurfaceTime, (750,50)) #bliting and pos of time
    else:
        Font = pygame.font.SysFont('Times New Roman', 32) #font
        SurfaceTime = Font.render(str(TimeFinish), True, white)
        win.blit(SurfaceTime, (750,50)) #bliting and pos of time over
        Retry()


#start menu
def Main_menu(): 
    global white
    global white 
    start = "Click to Start"
    win.blit(sbackground1,(0,0))
    Font = pygame.font.SysFont('Times New Roman', 50) #font
    SurfaceMenu = Font.render(str(start), True, red)
    win.blit(SurfaceMenu, (350,520)) #bliting and pos
    run = True
    pygame.display.update()
    while run == True:
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN: #if pressed
                run = False #stop function

                
#next level menu
def Menu():
    global white
    global white
    global revealed
    global locked
    global ClickCount
    global Score
    global StartTime
    global level
    win.blit(sbackground3,(0,0))
    NextMessage = "Level Complete"
    con = "Press (Y) to Continue to Next Level" #continue to next level
    qui = "Press (E) to Exit" #quit
    S1 = "Score: " +str(Score)
    Font = pygame.font.SysFont('Times New Roman', 50) #Score font
    CFont = pygame.font.SysFont('Times New Roman', 30) #key font
    NFont = pygame.font.SysFont('Times New Roman', 90) #Message font
    SurfaceNext = NFont.render(str(NextMessage), True, red)
    SurfaceSubMenuCon = CFont.render(str(con), True, blue)
    SurfaceSubMenuQui = CFont.render(str(qui), True, blue)
    SurfaceScore = Font.render(str(S1), True, lred)
    win.blit(SurfaceNext, (400,100)) #bliting and pos
    win.blit(SurfaceScore, (550,300)) #bliting and pos
    win.blit(SurfaceSubMenuCon, (50,500)) #bliting and pos
    win.blit(SurfaceSubMenuQui, (750,500)) #bliting and pos
    if locked == [True,True,True,True,True,True,True,True,True,True,True,True]: #if all the pairs are matched
        BonusScore() #Bonus Score and Final Score
    pygame.display.update()
    run = True
    while run == True:
        for e in pygame.event.get(): #get event
            if e.type == pygame.KEYDOWN: #if key pressed
                if e.key == pygame.K_y: #next level if "Y" pressed
                    revealed = [False,False,False,False,False,False,False,False,False,False,False,False] #reset values
                    random.shuffle(order) #shuffle
                    locked = [False,False,False,False,False,False,False,False,False,False,False,False] #reset
                    ClickCount = [0,0,0,0,0,0,0,0,0,0,0,0] #reset
                    run = False
                if e.key == pygame.K_e: #exit if "N" pressed
                    Quit_Game()
    if Level == 2:
        win.blit(sbackground,(0,0))
        revealed = [True,True,True,True,True,True,True,True,True,True,True,True] #reveal all
        display_update()
        time.sleep(8) #sleep timer of 8 secs
        revealed = [False,False,False,False,False,False,False,False,False,False,False,False]
        display_update()
    StartTime = time.time() #reset timer


#retry level
def Retry():
    global white
    global black
    global revealed
    global locked
    global ClickCount
    global Score
    global StartTime
    global level
    win.blit(sbackground2,(0,0))
    pygame.display.update()
    S = "Your Score is: " +str(Score)
    remessage1 = "OOPS!!"
    remessage2 = "Time Out"
    retry = "Press (P) to Play Again"
    qui = "Press (E) to Exit"
    OFont = pygame.font.SysFont('Times New Roman', 100) #font
    Font = pygame.font.SysFont('Times New Roman', 45) #font
    RQFont = pygame.font.SysFont('Times New Roman', 30) #font
    SurfaceScore = Font.render(str(S), True, lred)
    SurfaceMess1 = OFont.render(str(remessage1), True, red)
    SurfaceMess2 = Font.render(str(remessage2), True, red)
    SurfaceRetry = RQFont.render(str(retry), True, dblue)
    SurfaceQuit = RQFont.render(str(qui), True, dblue)
    win.blit(SurfaceMess1, (550,50)) #bliting and pos
    win.blit(SurfaceMess2, (610,150)) #bliting and pos
    win.blit(SurfaceScore, (565,350)) #bliting and pos
    win.blit(SurfaceRetry, (50,520)) #bliting and pos
    win.blit(SurfaceQuit, (750,520)) #bliting and pos
    pygame.display.update()
    run = True
    while run == True:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p: #next level
                   revealed = [False,False,False,False,False,False,False,False,False,False,False,False]#reset values
                   random.shuffle(order)#shuffle
                   locked = [False,False,False,False,False,False,False,False,False,False,False,False]#reset
                   ClickCount = [0,0,0,0,0,0,0,0,0,0,0,0]#reset
                   Score = 0
                   run = False 
                if e.key == pygame.K_e: #exit
                    Quit_Game()
                display_update()
    StartTime = time.time() #reset timer
    if Level == 2:
        win.blit(sbackground,(0,0))
        revealed = [True,True,True,True,True,True,True,True,True,True,True,True] #reveal all
        display_update()
        time.sleep(8) #sleep timer of 8 secs
        revealed = [False,False,False,False,False,False,False,False,False,False,False,False]
        display_update()
    StartTime = time.time() #reset timer


#display score
def Display_score():
    global Score
    global white
    S = "Score : "+str(Score)
    Font = pygame.font.SysFont('Times New Roman', 32) #font
    SurfaceScore = Font.render(str(S), True, white)
    win.blit(SurfaceScore, (750,100)) #bliting and pos of score

    
#Final and Bonus Score
def BonusScore():
    global t
    bonus = t #Bonus Score
    FinalScore= Score + bonus #final Score
    B = "Bonus Score: " +str(round(bonus))
    F = "Final Score: " +str(round(FinalScore))
    Font = pygame.font.SysFont('Times New Roman', 50) #font
    FFont = pygame.font.SysFont('Times New Roman', 60) #Font
    SurfaceBonus = Font.render(str(B), True, lred)
    SurfaceFinal = FFont.render(str(F), True, lred)
    win.blit(SurfaceBonus, (550,350))
    win.blit(SurfaceFinal, (550,400)) #bliting and pos
         

#Next level
Level = 1
def Next_level():
    global Level
    if locked == [True,True,True,True,True,True,True,True,True,True,True,True]: #check if all pairs are matched
        Level += 1
        Menu()

        
#Quit the game
def Quit_Game():
    pygame.quit()
    quit()   


Main_menu() #main menu
StartTime = time.time() #assigning the starting time
run = True
while run:
    pygame.time.delay(100) #game delay
    win.blit(sbackground,(0,0))
    timer() #timer
    Display_score() #score
    for event in pygame.event.get(): #keyboard or mouse events
        if event.type == pygame.QUIT: #event for exit button clicked
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN: #event for mouse button clicked
            x,y = pygame.mouse.get_pos() #mouse position
            Clicked, ImageIndex = ImageClicked(x,y)
            if ImageIndex != None: #if the image clicked wasnt clicked before
                Check(ImageIndex) #checking if images are equal
    display_update()
    Next_level() #to go to next level

Quit_Game() #Quit
