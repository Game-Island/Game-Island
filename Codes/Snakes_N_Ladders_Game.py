import pygame
from random import randint
import time
import pyrebase
from datetime import datetime
import os
import pandas as pd




clock=pygame.time.Clock()

#Initialize
pygame.init()
w=1366
h=768

icon=pygame.image.load("lns.png")
# GD=pygame.display.set_mode((w,h),pygame.FULLSCREEN)
GD=pygame.display.set_mode((w,h))
pygame.display.set_caption("Ladders N Snakes")
pygame.display.set_icon(icon)
pygame.display.update()

#Graphics:
black=(10,10,10)
white=(250,250,250)
red= (200,0,0)
b_red=(240,0,0)
green=(0,200,0)
b_green=(0,230,0)
blue=(0,0,200)
grey=(50,50,50)
yellow=(150,150,0)
purple=(43,3,132)
b_purple=(60,0,190)

board= pygame.image.load("board_lns.png")
dice1=pygame.image.load("Dice1_lns.png")
dice2=pygame.image.load("Dice2_lns.png")
dice3=pygame.image.load("Dice3_lns.png")
dice4=pygame.image.load("Dice4_lns.png")
dice5=pygame.image.load("Dice5_lns.png")
dice6=pygame.image.load("Dice6_lns.png")

redgoti=pygame.image.load("redgoti_lns.png")
yellowgoti=pygame.image.load("yellowgoti_lns.png")
greengoti=pygame.image.load("greengoti_lns.png")
bluegoti=pygame.image.load("bluegoti_lns.png")
menubg=pygame.image.load("menu__lns.png")
p=pygame.image.load("boardbg__lns.png")
intbg=pygame.image.load("intropic_lns.png")
intbg2=pygame.image.load("intropic2_lns.png")
intbg3=pygame.image.load("intropic3_lns.png")
intbg4=pygame.image.load("intropic4_lns.png")
intbg5=pygame.image.load("intropic5_lns.png")

pygame.mixer.music.load("lns_audio.mp3")
pygame.mixer.music.set_volume(0.2)
snakesound=pygame.mixer.Sound("snake_lns.wav")
win=pygame.mixer.Sound("win_lns.wav")
lose=pygame.mixer.Sound("lose_lns.wav")
ladder=pygame.mixer.Sound("ladder_lns.wav")

#mouse pos
mouse=pygame.mouse.get_pos()
click=pygame.mouse.get_pressed()


now = datetime.now()
dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
#print(dt_string)
df = pd.read_excel("User_Id.xlsx",sheet_name="User_Email_Id")
user_id = df["email_id"][0]
symbols=['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>' , '(', ')', '<',"!","^","&","_","-","+","=","[","]","{","}","'",'"']

for i in user_id:
    if i in symbols:
        user_id = user_id.replace(i,"")
        user_id = user_id.replace("gmailcom","")
# user_id = game_island.email_value()
#print("user_id: ",user_id,"-->",type(user_id))


try:
    configfirebase = {"apiKey": "AIzaSyDLSXHA_9IKUP2f_FLQF5_F_pZX-2E78cE",
"authDomain": "game-island-123.firebaseapp.com",
"databaseURL": "https://game-island-123-default-rtdb.asia-southeast1.firebasedatabase.app",
"projectId": "game-island-123",
"storageBucket": "game-island-123.appspot.com",
"messagingSenderId": "673041816597",
"appId": "1:673041816597:web:1fa678812282337dcd021c",
"measurementId": "G-WS0W53GRCN"
    }
    firebase = pyrebase.initialize_app(configfirebase)
    database = firebase.database()

except:
    SyntaxError


def win_logout():
    path_timer = os.getcwd() + "/Timer.xlsx"
    os.remove(path_timer)
    global user_id
    now_logout = datetime.now()
    logout_time = now_logout.strftime("%d-%m-%Y %H:%M:%S")
    logout_ = logout_time.split()
    logout_time = logout_[1]
    logout_date = logout_[0]
    user_data_island  = {"Status":'End'}
    t_island = repr(str(user_data_island))
    import json
    user_data_dict_island = json.loads(t_island)
    database.child(user_id).child("Timings").child(logout_date).child("LNS").child(logout_time).set(user_data_dict_island)




#Message displaying for buttons
def message_display(text,x,y,fs):
    largeText = pygame.font.Font('freesansbold.ttf',fs)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x,y)
    GD.blit(TextSurf, TextRect)

   

def text_objects(text, font):
    textSurface = font.render(text, True,white)
    return textSurface, textSurface.get_rect()

#Message displaying for field
def message_display1(text,x,y,fs,c):
    largeText = pygame.font.Font('freesansbold.ttf',fs)
    TextSurf, TextRect = text_objects1(text, largeText)
    TextRect.center = (x,y)
    GD.blit(TextSurf, TextRect)
    

def text_objects1(text, font,c):
    textSurface = font.render(text, True,c)
    return textSurface, textSurface.get_rect()

#Goti movement function
def goti(a):
    l1=[[406,606],[456,606],[506,606],[556,606],[606,606],[656,606],[706,606],[756,606],[806,606],[856,606],[906,606],[906,560],[856,560],[806,560],[756,560],[706,560],[656,560],[606,560],[556,560],[506,560],[456,560],[456,506],[506,506],[556,506],[606,506],[656,506],[706,506],[756,506],[806,506],[856,506],[906,506],[906,460],[856,460],[806,460],[756,460],[706,460],[656,460],[606,460],[556,460],[506,460],[456,460],[456,406],[506,406],[556,406],[606,406],[656,406],[706,406],[756,406],[806,406],[856,406],[906,406],[906,360],[856,360],[806,360],[756,360],[706,360],[656,360],[606,360],[556,360],[506,360],[456,360],[456,306],[506,306],[556,306],[606,306],[656,306],[706,306],[756,306],[806,306],[856,306],[906,306],[906,260],[856,260],[806,260],[756,260],[706,260],[656,260],[606,260],[556,260],[506,260],[456,260],[456,206],[506,206],[556,206],[606,206],[656,206],[706,206],[756,206],[806,206],[856,206],[906,206],[906,160],[856,160],[806,160],[756,160],[706,160],[656,160],[606,160],[556,160],[506,160],[456,160]]
    l2=l1[a]
    x=l2[0]-25
    y=l2[1]-25
    return x,y
     

def text_objects1(text, font):
    textSurface = font.render(text, True,black)
    return textSurface, textSurface.get_rect()

#Ladder check
def ladders(x):
    if x==2: return 37
    elif x==9:return 33
    elif x==45:return 77
    elif x==71:return 92
    else:return x

#Snake Check
def snakes(x): 
    if x==19:return 4
    elif x==63:return 21
    elif x==36:return 7
    elif x==98:return 21
    elif x==72:return 34
    elif x==93:return 75
    else:return x

def dice(a):
    if a==1:
        a=dice1
    elif a==2:
        a=dice2
    elif a==3:
        a=dice3
    elif a==4:
        a=dice4
    elif a==5:
        a=dice5
    elif a==6:
        a=dice6

    time=pygame.time.get_ticks()
    while pygame.time.get_ticks()-time<1000:
        GD.blit(a,(300,500))
        pygame.display.update()    

#for mute and unmute    
def button2(text,xmouse,ymouse,x,y,w,h,i,a,fs):
    #mouse pos
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+w>xmouse>x and y+h>ymouse>y:
        pygame.draw.rect(GD,a,[x-2.5,y-2.5,w+5,h+5])
        if pygame.mouse.get_pressed()==(1,0,0):
            return True
        
    else:
        pygame.draw.rect(GD,i,[x,y,w,h])
    message_display(text,(x+w+x)/2,(y+h+y)/2,fs)    
    
    






#Buttons for playing:
def button1(text,xmouse,ymouse,x,y,w,h,i,a,fs):
    #mouse pos
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+w>xmouse>x and y+h>ymouse>y:
        pygame.draw.rect(GD,a,[x-2.5,y-2.5,w+5,h+5])
        if pygame.mouse.get_pressed()==(1,0,0):
            return True
        
    else:
        pygame.draw.rect(GD,i,[x,y,w,h])
    message_display(text,(x+w+x)/2,(y+h+y)/2,fs)
    

#Turn
def turn(score,l,s):
    
    a=randint(1,6)#player dice roll
    if a==6:
        six=True
    else:
        six=False
    p=dice(a)
    score+=a
    if score<=100:
        lad=ladders(score) #checking for ladders for player
        if lad!=score:
            l=True
            pygame.mixer.Sound.play(ladder)
            time=pygame.time.get_ticks()
            score=lad 
        snk=snakes(score)
        if snk!=score: #checking for snakes for player
            s=True
            pygame.mixer.Sound.play(snakesound)
            score=snk
           
    else: #checks if player score is not grater than 100
        score-=a
        time=pygame.time.get_ticks()
        while pygame.time.get_ticks()-time<1500:
            message_display1("Can't move!",650,50,35,black)
            pygame.display.update()
    return score,l,s,six
    

#Quitting:
def Quit():
    win_logout()
    pygame.quit()
    quit()

#Buttons:
def button(text,xmouse,ymouse,x,y,w,h,i,a,fs,b):
    if x+w>xmouse>x and y+h>ymouse>y:
        pygame.draw.rect(GD,a,[x-2.5,y-2.5,w+5,h+5])
        if pygame.mouse.get_pressed()==(1,0,0):
            if b==1:
                options()
            elif b==5:
                return 5
            elif b==0:
                Quit()
                # pygame.quit()
                quit()
            elif b=="s" or b==2 or b==3 or b==4:
                return b
            elif b==7:
                options()
            else :return True
                
            
            
            
                
            
    else:
        pygame.draw.rect(GD,i,[x,y,w,h])
    message_display(text,(x+w+x)/2,(y+h+y)/2,fs)


#def pause():
    #j=True
    #while j:
        #mouse pos
        #mouse=pygame.mouse.get_pos()
        #click=pygame.mouse.get_pressed()
        #GD.blit(pause_bg,(0,0))
        #mouse=pygame.mouse.get_pos()
        #click=pygame.mouse.get_pressed()
        #if button("Resume",mouse[0],mouse[1],(w/2)-150,350,300,50,green,b_green,30,10):
            #j=False
        #if button("Main Menu",mouse[0],mouse[1],(w/2)-150,500,300,50,red,b_red,30,10):
            #main()
        #pygame.display.update()
    
def intro():
    time=pygame.time.get_ticks()
    while pygame.time.get_ticks()-time<2500:
        GD.blit(intbg,(0,0))
        pygame.display.update()
    while True:
        time=pygame.time.get_ticks()
        while pygame.time.get_ticks()-time<500:    
            GD.blit(intbg2,(0,0))
            pygame.display.update()
        time=pygame.time.get_ticks()
        while pygame.time.get_ticks()-time<500:
            GD.blit(intbg3,(0,0))
            pygame.display.update()
        time=pygame.time.get_ticks()
        while pygame.time.get_ticks()-time<500:
            GD.blit(intbg4,(0,0))
            pygame.display.update()
        time=pygame.time.get_ticks()
        while pygame.time.get_ticks()-time<500:
            GD.blit(intbg5,(0,0))
            pygame.display.update()
            
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                return
        pygame.display.update()


        
    


    
#Main Menu
def main():
        
    pygame.mixer.music.play(-1)

    
    menu=True
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                Quit()
                # pygame.quit()
                # quit()
            if event.type== pygame.KEYDOWN:
                if event.key== pygame.K_ESCAPE:
                    Quit()
                    # pygame.quit()
                    # quit()

        #mouse pos
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        
        GD.blit(menubg,(0,0))
        button("Play",mouse[0],mouse[1],(w/2-300),(h-150),200,100,green,b_green,60,1)

        button("Quit",mouse[0],mouse[1],(w/2+100),(h-150),200,100,red,b_red,60,0)

        mouse=pygame.mouse.get_pos()
        if button2("Mute Music",mouse[0],mouse[1],1166,0,200,50,purple,b_purple,25):
            pygame.mixer.music.pause()
        if button2("Play Music",mouse[0],mouse[1],1166,75,200,50,purple,b_purple,25):
            pygame.mixer.music.unpause()
        
        pygame.display.update()


#Options Menu:
def options():
    
    flag=True
    while flag==True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                Quit()
                # pygame.quit()
                # quit()
            if event.type== pygame.KEYDOWN:
                if event.key== pygame.K_ESCAPE:
                    Quit()
                    # pygame.quit()
                    # quit()



        #mouse pos
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        b1=b2=b3=b4=b5=-1
        GD.blit(menubg,(0,0))
        #Single player button
        b1=button("Single Player",mouse[0],mouse[1],(w/2-150),250,300,50,green,b_green,30,"s")
        #2 player button
        b2=button("2 Players",mouse[0],mouse[1],(w/2)-150,350,300,50,green,b_green,30,2)
        #3 player
        b3=button("3 Players",mouse[0],mouse[1],(w/2)-150,450,300,50,green,b_green,30,3)
        #4 player
        b4=button("4 Players",mouse[0],mouse[1],(w/2)-150,550,300,50,green,b_green,30,4)
        #Back button
        b5=button("Back",mouse[0],mouse[1],0,650,200,50,red,b_red,30,5)
        if b5==5:
            main()
        if b1=="s":
            play(21)
        if b2==2:
            play(2)
        if b3==3:
            play(3)
        if b4==4:
            play(4)
        
        pygame.display.update()

def play(b):

    
    b6=-1
    time=3000
    if b6==7:
        options()
    GD.blit(p,(0,0))
    GD.blit(board,(w/2-250,h/2-250))
    xcr=xcy=xcg=xcb=406-25
    ycr=ycy=ycg=ycb=606-25
    GD.blit(redgoti,(xcy,ycy))
    if 5>b>1 or b==21:
        GD.blit(yellowgoti,(xcy,ycy))
            
    if 5>b>2 or b==21:
        GD.blit(greengoti,(xcg,ycg))
            
    if 5>b>2:
        GD.blit(bluegoti,(xcb,ycb))
    p1="Player 1"
    p1score=0
    if b==21:
        p2="Computer"
        p2score=0
    if 5>b>1:
        p2="Player 2"
        p2score=0
    if 5>b>2:
        p3="Player 3"
        p3score=0
    if 5>b>3:
        p4="Player 4"
        p4score=0
    t=1
    play=True
    while True:
        l=False
        s=False
        time=3000
        GD.blit(p,(0,0))
        GD.blit(board,(w/2-250,h/2-250))
        mouse=pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            
            if event.type==pygame.QUIT:
                Quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    Quit()

            
        if b==21:
            #(player,score,text,xmouse,ymouse,x,y,w,h,i,a,fs)
            
            if button1("Player 1",mouse[0],mouse[1],100,700,200,50,red,grey,30):
                if t==1:
                    p1score,l,s,six=turn(p1score,l,s)
                    if not six:
                        t+=1
                    xcr,ycr=goti(p1score)
                    if p1score==100:
                        time=pygame.time.get_ticks()
                        while pygame.time.get_ticks()-time<2000:
                            message_display1("Player 1 Wins",650,50,50,black)
                            pygame.mixer.Sound.play(win)
                            pygame.display.update()
                        break
            
            button1("Computer",mouse[0],mouse[1],400,700,200,50,yellow,grey,30)
            if True:
                if t==2:
                    p2score,l,s,six=turn(p2score,l,s)
                    xcy,ycy=goti(p2score)
                    if not six:
                        t+=1
                        if b<3 or b==21:
                            t=1
                    
                    if p2score==100:
                        time=pygame.time.get_ticks()
                        while pygame.time.get_ticks()-time<2000:
                            message_display1("Computer Wins",650,50,50,black)
                            pygame.mixer.Sound.play(lose)
                            pygame.display.update()
                        break
        if 5>b>1:
            if button1("Player 1",mouse[0],mouse[1],100,700,200,50,red,grey,30):
                if t==1:
                    p1score,l,s,six=turn(p1score,l,s)
                    xcr,ycr=goti(p1score)
                    if not six:
                        t+=1
                    if p1score==100:
                        time=pygame.time.get_ticks()
                        while pygame.time.get_ticks()-time<2000:
                            message_display1("Player 1 Wins",650,50,50,black)
                            pygame.mixer.Sound.play(win)
                            pygame.display.update()
                        break
                
            if button1("Player 2",mouse[0],mouse[1],400,700,200,50,yellow,grey,30):
                if t==2:
                    p2score,l,s,six=turn(p2score,l,s)
                    xcy,ycy=goti(p2score)
                    if not six:
                        t+=1
                        if b<3:
                            t=1
                    
                    if p2score==100:
                        time=pygame.time.get_ticks()
                        while pygame.time.get_ticks()-time<2000:
                            message_display1("Player 2 Wins",650,50,50,black)
                            pygame.mixer.Sound.play(win)
                            pygame.display.update()
                        break
                
        if 5>b>2:
            if button1("Player 3",mouse[0],mouse[1],700,700,200,50,green,grey,30):
                if t==3:
                    p3score,l,s,six=turn(p3score,l,s)
                    xcg,ycg=goti(p3score)
                    if not six:
                        t+=1
                        if b<4:
                            t=1
                    
                    if p3score==100:
                        time=pygame.time.get_ticks()
                        while pygame.time.get_ticks()-time<2000:
                            message_display1("Player 3 Wins",650,50,50,black)
                            pygame.mixer.Sound.play(win)
                            pygame.display.update()
                        break
                
        if 5>b>3:   
            if button1("Player 4",mouse[0],mouse[1],1000,700,200,50,blue,grey,30):
                if t==4:
                    p4score,l,s,six=turn(p4score,l,s)
                    xcb,ycb=goti(p4score)
                    if not six:
                        t+=1
                        if b<5:
                            t=1
                    
                    if p4score==100:
                        time=pygame.time.get_ticks()
                        while pygame.time.get_ticks()-time<2000:
                            message_display1("Player 4 Wins",650,50,50,black)
                            pygame.mixer.Sound.play(win)
                            pygame.display.update()
                        break

        
        b6=button("Back",mouse[0],mouse[1],0,0,200,50,red,b_red,30,7)
        GD.blit(redgoti,(xcr,ycr))
        if 5>b>1 or b==21:
            GD.blit(yellowgoti,(xcy+2,ycy))
            
            
        if 5>b>2:
            GD.blit(greengoti,(xcg+4,ycg))
            
             
        if 5>b>3:
            GD.blit(bluegoti,(xcb+6,ycb))
            
        if l:
            time=pygame.time.get_ticks()
            while pygame.time.get_ticks()-time<2000:
                message_display1("There's a Ladder!",650,50,35,black)
                pygame.display.update()
        if s:
            time=pygame.time.get_ticks()
            while pygame.time.get_ticks()-time<2000:
                message_display1("There's a Snake!",650,50,35,black)
                pygame.display.update()

        clock.tick(7)
        pygame.display.update()
        
            
        
intro()    
main()
