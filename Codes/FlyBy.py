import pygame
from sys import exit
from random import randint
import time
from pygame import mixer
import pyrebase
import pandas as pd
import os
from datetime import datetime

    

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

# path = "D:\Study\Coding\RanPlay\Game_Island\FlyBy.xlsx"
path = os.getcwd() + "/FlyBy.xlsx"
print(path)
is_file = os.path.isfile(path)
if is_file == True:
    pass
else:
    df = pd.DataFrame(columns=["Score"])
    df.to_excel("FlyBy.xlsx",engine="openpyxl",sheet_name="User_Data",index=False)

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
    database.child(user_id).child("Timings").child(logout_date).child("FlyBy").child(logout_time).set(user_data_dict_island)

def display_score():
    game_time = int(pygame.time.get_ticks()/300) - start_time
    score_surf = font.render(f'Score  {game_time}',False,(180,180,180),50)
    score_rect=score_surf.get_rect(center=(355,40))
    screen.blit(score_surf,score_rect)
    return game_time

def obstacle_movement(obstacle_list):
    #global a
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            #a = pygame.time.get_ticks()/10000
            obstacle_rect.x -= 5
            if obstacle_rect.y == 265:
                screen.blit(met_surf,obstacle_rect)
            else:
                screen.blit(met_surf,obstacle_rect)

        return obstacle_list
    else:
        return[]

data_count = 0

def collisions(player,obstacle):
    global score
    global data_count
    global dt_string
    if obstacle:
        for obstacle_rect in obstacle:
            if player.colliderect(obstacle_rect) or player.y>=400:
                alien_rect.top=0
                user_data  = {"Score":(score)}
                t = repr(str(user_data))
                import json
                user_data_dict = json.loads(t)
                user_data = [(score)]
                df = pd.DataFrame(user_data,columns=[("Score")])
                with pd.ExcelWriter("FlyBy.xlsx",mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer:
                    df.to_excel(writer, sheet_name="User_Data",header=None,startrow=writer.sheets["User_Data"].max_row,index=False)
                database.child(user_id).child("FlyBy").child(dt_string).set(user_data_dict)
                    #if player.colliderect(obstacle_rect):
                    #a=0
                return False  
    return True 


pygame.init()
mixer.init()
screen=pygame.display.set_mode((730,400))
pygame.display.set_caption('FlyBy')
clock = pygame.time.Clock()
font=pygame.font.Font('ARCADECLASSIC.ttf',40)
game_active=False
start_time= 0
score = 0
#a=pygame.time.get_ticks()/10000
#a = int(pygame.time.get_ticks()/10000) 

obstacle_rect_list=[]

#Background

sky_surf = pygame.image.load('night_sky.jpg').convert_alpha()
ground_surf = pygame.image.load('ground_1.jpg').convert_alpha()
ground_rect=ground_surf.get_rect(topleft=(0,400))
end_surf= pygame.image.load('End_screen.png').convert_alpha()
end_rect=end_surf.get_rect(topleft=(0,0))
main_page=pygame.image.load('Arcade_Gamer.png').convert_alpha()
main_surf=main_page.get_rect(topleft=(0,0))

#icon
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#music
mixer.music.load('audio_1.mp3')
mixer.music.set_volume(0.1)
mixer.music.play()
#Objects

#snail_surf=pygame.image.load('turtle_small.png').convert_alpha()

ufo_surf=pygame.image.load('ufo.png').convert_alpha()
alien_rect=ufo_surf.get_rect(midbottom=(50,290))
alien_rect_1=ufo_surf.get_rect(center=(365,200))
met_surf = pygame.image.load('met_1.png').convert_alpha()
ufo_man=pygame.image.load('final_alien.png').convert_alpha()
ufo_rect=ufo_man.get_rect(center=(365,170))




#Texts

title=font.render('FlyBy',False,(180,180,180),80)
title_rect =title.get_rect(center=(365,50))
# message_box = font.render('Press  Enter  key  to  play  the  game',True,(180,180,180))
# message_box_rect = message_box.get_rect(center=(365,330))
message_box_1 = font.render('Press  Enter  key  to  play  again',True,(180,180,180))
message_box_rect_1 = message_box_1.get_rect(center=(365,360))

alien_gravity = -10

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1200)


if alien_rect.colliderect(ground_rect):
    alien_rect.y=150
    
    
    game_active=False

music=[]

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            win_logout()
            pygame.quit()
            exit()
        
        
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_m:
                mixer.music.pause()
                
                

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_n:
                mixer.music.unpause()
        
        if game_active:
            
            # if int(pygame.time.get_ticks()/500) <=10:
            #     if alien_rect.y>=200:
            #         alien_rect.y = 200


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    alien_gravity=0
                    #if int(pygame.time.get_ticks()/500)>3:
                    alien_gravity = -13
            
            if alien_rect.top<=0:
                alien_rect.top=0
        
                    
                        
                    
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(met_surf.get_rect(midbottom=(randint(900,1100),320)))
                else:
                    obstacle_rect_list.append(met_surf.get_rect(midbottom=(randint(900,1100),90)))

            
        if not game_active:    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    now = datetime.now()
                    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                    #print(dt_string)
                    alien_rect.y=150
                    alien_gravity=-10
                    
                    
                    game_active = True
                    start_time= int(pygame.time.get_ticks()/300)
                    
                    
                    


    if game_active:
        
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(ground_rect))
        screen.blit(ufo_surf,(alien_rect))
        score=display_score()
        # if score==0:
        #     pygame.time.delay(750)

        alien_gravity +=1
        alien_rect.y += alien_gravity -2
        #if alien_rect.bottom >= 290:
            #alien_rect.bottom = 290
        
        obstacle_rect_list= obstacle_movement(obstacle_rect_list)

        game_active=collisions(alien_rect,obstacle_rect_list)

        
            
            

    else:
        if score!=0:
            screen.blit(end_surf,end_rect)
            screen.blit(ufo_man,ufo_rect)
            # screen.blit(title,title_rect)
            score_message = font.render(f'Score  {score}',False,(180,180,180))
            score_message_rect=score_message.get_rect(center=(365,310))
            
            # screen.blit(message_box_1,message_box_rect_1)
            screen.blit(score_message,score_message_rect)
            
        else:
            screen.blit(main_page,main_surf)
            
            alien_rect.y=200
            
            
        obstacle_rect_list.clear()

            
    pygame.display.update()
    clock.tick(60)