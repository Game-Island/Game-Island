import pygame
import random
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

path = "D:\Study\Coding\RanPlay\Game_Island\Slither.xlsx"
path = os.getcwd() + "/Slither.xlsx"
is_file = os.path.isfile(path)
if is_file == True:
    pass
else:
    df = pd.DataFrame(columns=["Score"])
    df.to_excel("Slither.xlsx",engine="openpyxl",sheet_name="User_Data",index=False)


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
    database.child(user_id).child("Timings").child(logout_date).child("Slither").child(logout_time).set(user_data_dict_island)

pygame.init()
# sounds
# pygame.mixer.init()
pygame.mixer.music.load("slither_audio.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)


# creating colors
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (47,232,143)
violet = (179,109,255)


# Creating pygame windows
screen_width = 400
screen_height = 500
game_window = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Slither")
icon = pygame.image.load("Slither_nobg.png")
pygame.display.set_icon(icon)



# defining functions
def text_screen(text , color ,x ,y,font_size):
    font = pygame.font.SysFont("comic sans ms" , font_size)
    screen_text = font.render(text,True,color)
    game_window.blit(screen_text,[x,y])

def plot_snake(gameWindow,color,snk_list,snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow,color,[x,y,snake_size,snake_size])

#  Game loop
def gameloop():
    global user_id
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    #print(dt_string)
    # Game specific variables
    exit_game = False
    game_over = False
    snake_size = 10
    snake_x = screen_width/2
    snake_y = screen_height/2
    init_velocity = 10
    clock = pygame.time.Clock()
    fps = 20
    velocity_x = 0
    velocity_y = 0
    food_x = round(random.randint(20,screen_width-snake_size)/10)*10
    food_y = round(random.randint(60,screen_height-snake_size)/10)*10
    food_size = snake_size
    score = 0
    data_count = 0
    snk_list = []
    snk_length = 1

    while not exit_game:
        if game_over == True:
            data_count += 1
            if data_count == 1:
                user_data  = {"Score":(score*10)}
                t = repr(str(user_data))
                import json
                user_data_dict = json.loads(t)

                user_data = [(score*10)]
                df = pd.DataFrame(user_data,columns=[("Score")])
                with pd.ExcelWriter("Slither.xlsx",mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer:
                    df.to_excel(writer, sheet_name="User_Data",header=None,startrow=writer.sheets["User_Data"].max_row,index=False)
                database.child(user_id).child("Slither").child(dt_string).set(user_data_dict)
            game_window.fill("grey")
            text_screen("Game over!",red,100,180,40)
            text_screen(f"Score: {score*10}",blue,120,235,40)
            text_screen("Press ENTER to Play again!",red,15,300,30)
            for event in pygame.event.get():

                if event.type == pygame.QUIT :
                    win_logout()
                    exit_game = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()

        if game_over == False:
            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                pygame.mixer.music.set_volume(1)
                score += 1
                # print("Score:",score)
                food_x = round(random.randint(20,screen_width-snake_size)/10)*10
                food_y = round(random.randint(60,screen_height-snake_size)/10)*10
                snk_length += 2

            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    win_logout()
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y = -init_velocity
                    if event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = init_velocity

            game_window.fill("grey")
            text_screen("Score: " + str(score*10) , blue , 5 , 2 , 40) 
            pygame.draw.rect(game_window,red,[food_x,food_y,food_size,food_size])
            pygame.draw.line(game_window,black,(0,51),(400,51),width=4)
            pygame.draw.line(game_window,black,(0,498),(400,498),width=4)
            pygame.draw.line(game_window,black,(1,0),(1,600),width=4)
            pygame.draw.line(game_window,black,(397,0),(397,600),width=4)
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
            # print(snk_length,"snake length")
            # print(snk_list,"snake list")
            # print(head,"head") 

            if len(snk_list) > snk_length :
                del snk_list[0]

            if snake_x < 0 or snake_x >= screen_width or snake_y < 60 or snake_y >= screen_height:
                game_over = True
            
            if head in snk_list[:-1]:
                game_over = True
            # print(snk_list,"snake list change")
            # print(head,"head")

            # pygame.draw.rect(game_window,grey,[snake_x,snake_y,snake_size,snake_size])
            plot_snake(game_window,black,snk_list,snake_size)
            snake_x += velocity_x
            snake_y += velocity_y

        pygame.display.update()
        clock.tick(fps)
        

    pygame.quit()
    quit()

gameloop()