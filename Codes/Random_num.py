import tkinter
import pandas as pd
import os
from datetime import datetime
from openpyxl import load_workbook
import customtkinter
from pygame import mixer
import random 
from PIL import Image, ImageTk, ImageSequence
import threading
import pyrebase
# from game_island import email_value
# import game_island
mixer.init()
mixer.music.load('gtn_audio.mp3')
# mixer.music.set_volume(5)

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
user_id = "User_Id_7"
#print("user_id: ",user_id,"-->",type(user_id))
df = pd.read_excel("User_Id.xlsx",sheet_name="User_Email_Id")
user_id = df["email_id"][0]
symbols=['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>' , '(', ')', '<',"!","^","&","_","-","+","=","[","]","{","}","'",'"']

for i in user_id:
    if i in symbols:
        user_id = user_id.replace(i,"")
        user_id = user_id.replace("gmailcom","")
# user_id = game_island.email_value()
#print("user_id: ",user_id,"-->",type(user_id))

try : 
    configfirebase = {
"apiKey": "AIzaSyDLSXHA_9IKUP2f_FLQF5_F_pZX-2E78cE",
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
except Exception as e:
    print(e)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

# path = "D:\Study\Coding\RanPlay\Game_Island\Random_num.xlsx"
path = os.getcwd() + "/Random_num.xlsx"
is_file = os.path.isfile(path)
if is_file == True:
    pass
else:
    df = pd.DataFrame(columns=["No. of attempts","Time taken","Difficulty Level"])
    df.to_excel("Random_num.xlsx",engine="openpyxl",sheet_name="User_Data",index=False)

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
    database.child(user_id).child("Timings").child(logout_date).child("Guess the number").child(logout_time).set(user_data_dict_island)
    root.destroy()

def num_player():
    import time
    page_1.forget()
    time.sleep(0.09)
    page_2.pack(fill = "both",expand=1)
    
def num_of_player(player_1):
    global player
    global second
    global speed
    player.set(int(slider.get()))
    if slider.get() == 1:
        second.set(40)
        speed.set(0.0259)
        progressbar.configure(determinate_speed=float(speed.get()))
        page_2.update()
        page_3.update()
    elif slider.get() == 2:
        second.set(30)
        speed.set(0.0346)
        progressbar.configure(determinate_speed=float(speed.get()))
        page_2.update()
        page_3.update()
    elif slider.get() == 3:
        second.set(20)
        speed.set(0.0518)
        progressbar.configure(determinate_speed=float(speed.get()))
        page_2.update()
        page_3.update()
    elif slider.get() == 4:
        second.set(15)
        speed.set(0.0695)
        progressbar.configure(determinate_speed=float(speed.get()))
        page_2.update()
        page_3.update()

def game():
    global temp
    global num
    import time
    temp = True
    #print(num)
    # print(float(speed.get()))
    page_2.forget()
    time.sleep(0.09)
    page_3.pack(fill = "both",expand=1)
    progressbar.start()
    timer_thread = threading.Thread(target=new_window)
    timer_thread.start()
    mixer.music.play()
    mixer.music.set_volume(5)
    page_3.update()
    # stop_func()
    
def play_again(event):
    global dt_string
    global num
    global now
    global attempt
    # mixer.music.unpause()
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    attempt.set(0)
    progressbar.set(0)
    num = random.randint(1,100)
    page_5.forget()
    page_2.pack(fill = "both",expand = 1)
    entry_3.delete(0,len(entry_3.get()))
    b_guess.configure(hover_color="#146944",fg_color="#30A572")
    speed.set(0.0259)
    progressbar.configure(determinate_speed=float(speed.get()))
    message.set("Start Guessing!")
    page_3.update()
    slider.set(1)
    player.set(1)
    second.set(40)
    page_2.update()
    
num = random.randint(1,100)
time_taken = 0
temp = True 

def new_window():
# speed = 0.03
    import time
    global time_taken
    global second
    global temp
    global timer
    
    start = time.time()
    # a = 1
    timer.set(1)
    time_limit = int(second.get())
    page_3.update()
    label_new.pack()
    while temp == True:
        # print("time_limit",time_limit)
        elapsed = time.time() - start
        time_taken = round(elapsed,2)
        # a += 1
        timer.set(timer.get() + 1)
        if elapsed > time_limit:
            progressbar.stop()
            page_4.pack(pady=65)
            page_3.forget()
            # mixer.music.pause()
            mixer.music.set_volume(0)
            break
        
def page_3_again(event):
    global timer
    global num
    global attempt
    # mixer.music.unpause()
    num = random.randint(1,100)
    attempt.set(0) 
    page_4.forget()
    progressbar.set(0)
    entry_3.delete(0,len(entry_3.get()))
    b_guess.configure(hover_color="#146944",fg_color="#30A572")
    speed.set(0.0259)
    progressbar.configure(determinate_speed=float(speed.get()))
    message.set("Start Guessing!")
    page_3.update()
    slider.set(1)
    player.set(1)
    second.set(40)
    page_2.update()
    page_2.pack(fill = "both",expand=1)

def guess(event):
    import time
    global time_taken
    global user_id
    global message
    global player
    global database
    global temp
    global dt_string
    global attempt
    global player_number
    global num
    attempt.set(attempt.get() + 1)
    try:
        if int(entry_3.get()) == num:
            temp = False
            message.set("Congratulations! You got it.")
            page_page.configure(text_color = "green")
            b_guess.configure(hover_color="#146944",fg_color="#30A572")
            entry_3.delete(0,2)
            page_3.update()

            user_data = [(attempt.get(),time_taken,slider.get())]
            user_data_1 = {"No. of attempts":attempt.get(),"Time taken":time_taken,"Difficulty Level":int(slider.get())}
            import json
            t=repr(str(user_data_1))
            user_data_dict = json.loads(t)
            # print(user_data_dict,type(user_data_dict))

            progressbar.stop()
            time.sleep(1)
            page_5.pack(fill = "both",expand=1)
            message.set("Start Guessing!")
            page_page.configure(text_color = "white")
            # mixer.music.pause()
            mixer.music.set_volume(0)
            page_3.forget()    

            df = pd.DataFrame(user_data,columns=["No. of attempts","Time taken","Difficulty Level"])
            with pd.ExcelWriter("Random_num.xlsx",mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer:
                df.to_excel(writer, sheet_name="User_Data",header=None,startrow=writer.sheets["User_Data"].max_row,index=False)
            #print("data entered in excel")

            #print("user_id: ",user_id,"-->",type(user_id))
            database.child(user_id).child("Guess the number").child(dt_string).set(user_data_dict)
            #print("data entered in firebase")
            dita = database.child(user_id).child("Guess the number").child(dt_string).get().val()
            dita = dita.replace("'",'"')
            #print(dita,type(dita))
            dita_dict = json.loads(dita)
            #print(dita_dict,type(dita_dict))

        else:
            if int(entry_3.get()) > num:
                if int(entry_3.get()) > 100 or int(entry_3.get()) < 1:
                    message.set("Please enter a number between 1 to 100")
                    entry_3.delete(0,len(entry_3.get()))
                    page_3.update()
                
                else:
                    message.set(f"Try a smaller number than {int(entry_3.get())}!")
                    b_guess.configure(hover_color="dark red",fg_color="red")
                    entry_3.delete(0,len(entry_3.get()))
                    page_3.update()

            elif int(entry_3.get()) < num:
                if int(entry_3.get()) > 100 or int(entry_3.get()) < 1:
                    message.set("Please enter a number between 1 to 100")
                    entry_3.delete(0,len(entry_3.get()))
                    page_3.update()
    
                else:
                    message.set(f"Try a bigger number than {int(entry_3.get())}!")
                    b_guess.configure(hover_color="dark red",fg_color="red")
                    entry_3.delete(0,len(entry_3.get()))
                    page_3.update()

    except Exception as e:
        print(e)
        message.set("Please enter a number between 1 to 100")
        entry_3.delete(0,len(entry_3.get()))
        page_3.update()
    
def rules():
    page_6.pack(fill = "both",expand=1)
    page_1.forget()

def back(event):
    page_6.forget()
    page_1.pack(fill = "both",expand = 1)


root = customtkinter.CTk()
root.title("Guess the number")
root.wm_iconbitmap("GTN_ico.ico")
root.geometry(f"433x333")
root.resizable(False,False)
root.eval('tk::PlaceWindow . center')
root.maxsize(433,400)
root.protocol("WM_DELETE_WINDOW",win_logout)
timer = tkinter.IntVar()
attempt = tkinter.IntVar()
attempt.set(0)
speed = tkinter.StringVar()
speed.set(0.0259)

page_1 = customtkinter.CTkFrame(master=root)

label_1 = customtkinter.CTkLabel(master=page_1,text="Guess The Number",corner_radius = 8,font=customtkinter.CTkFont(family="Cambria",size = 40, weight="bold"),fg_color="transparent")
label_1.pack()
label_1.place(anchor = tkinter.CENTER, rely = 0.2, relx = 0.5)

b_play = customtkinter.CTkButton(master=page_1,text="Play",font=customtkinter.CTkFont(family="Cambria",size=20),height=40,command=num_player)
b_play.pack()
b_play.place(anchor = tkinter.CENTER,rely = 0.45, relx = 0.5)

b_rules = customtkinter.CTkButton(master=page_1,text="Rules",font=customtkinter.CTkFont(family="Cambria",size=20),height=40,command=rules)
b_rules.pack()
b_rules.place(anchor = tkinter.CENTER,rely = 0.7, relx = 0.5)

page_1.pack(fill = "both",expand=1)
# First frame (homepage) ends

# Second frame (number of players) starts
page_2 = customtkinter.CTkFrame(master=root)

label_2 = customtkinter.CTkLabel(master=page_2,text="Difficulty Level",font= customtkinter.CTkFont(family="Cambria",size=30,weight="bold"))
label_2.pack()
label_2.place(anchor = tkinter.CENTER, rely = 0.1, relx = 0.5)

second = tkinter.StringVar()
second.set(40)

label_7 = customtkinter.CTkLabel(master=page_2,textvariable = second,font= customtkinter.CTkFont(family="Cambria",size=25,weight="bold"))
label_7.pack()
label_7.place(anchor = tkinter.CENTER, rely = 0.8, relx = 0.57)

label_8 = customtkinter.CTkLabel(master=page_2,text="You will have ",font= customtkinter.CTkFont(family="Cambria",size=25,weight="bold"))
label_8.pack()
label_8.place(anchor = tkinter.CENTER, rely = 0.8, relx = 0.35)

label_9 = customtkinter.CTkLabel(master=page_2,text=" seconds",font= customtkinter.CTkFont(family="Cambria",size=25,weight="bold"))
label_9.pack()
label_9.place(anchor = tkinter.CENTER, rely = 0.8, relx = 0.72)

slider = customtkinter.CTkSlider(master=page_2,from_=1, to=4,number_of_steps=3,command=num_of_player)
slider.pack()
slider.set(1)
slider.place(anchor = tkinter.CENTER,rely=0.25,relx = 0.5)

player = tkinter.StringVar()
player.set(1)


entry_1 = customtkinter.CTkEntry(master=page_2,placeholder_text="0",textvariable=player,font=customtkinter.CTkFont(family="Cambria",size = 20,weight="bold"),height=40,justify = "center",state="disabled")
entry_1.pack()
entry_1.place(anchor = tkinter.CENTER,rely=0.4,relx = 0.5)

b_start = customtkinter.CTkButton(master=page_2,text="Start",font=customtkinter.CTkFont(family="Cambria",size=20),height=40,command=game)
b_start.pack()
b_start.place(anchor = tkinter.CENTER,rely = 0.6, relx = 0.5)
# Second frame (number of players) ends

# Third frame (game) starts
page_3 = customtkinter.CTkFrame(master=root)

label_new = customtkinter.CTkEntry(page_3,textvariable= timer,height=0,text_color="#2B2B2B",fg_color="transparent",border_width=0,bg_color="transparent",state="disabled")

label_3 = customtkinter.CTkLabel(master=page_3,text="Guess The Number:",font= customtkinter.CTkFont(family="Cambria",size=30,weight="bold"))
label_3.pack()
label_3.place(anchor = tkinter.CENTER, rely = 0.1, relx = 0.5)

entry_3 = customtkinter.CTkEntry(master=page_3,placeholder_text="0",font=customtkinter.CTkFont(family="Cambria",size = 20,weight="bold"),height=40,justify = "center")
entry_3.pack()
entry_3.place(anchor = tkinter.CENTER,rely=0.40,relx = 0.5)

b_guess = customtkinter.CTkButton(master=page_3,text="Guess",font=customtkinter.CTkFont(family="Cambria",size=20),height=40)
b_guess.pack()
b_guess.bind("<Button-1>",guess)
b_guess.place(anchor = tkinter.CENTER,rely = 0.65, relx = 0.5)



message = tkinter.StringVar()
message.set("Start Guessing!")

player_number = tkinter.IntVar()
player_number.set(1)

label_5 = customtkinter.CTkLabel(master=page_3,text="(Between 1 to 100)",font= customtkinter.CTkFont(family="Cambria",size=20,weight="bold"))
label_5.pack()
label_5.place(anchor = tkinter.CENTER, rely = 0.2, relx = 0.5)

progressbar = customtkinter.CTkProgressBar(master=page_3,progress_color="light blue",determinate_speed=float(speed.get()),mode = "determinate")
progressbar.set(0,1)
progressbar.pack()
progressbar.place(anchor = tkinter.CENTER,rely = 0.78, relx = 0.5)


page_page = customtkinter.CTkEntry(master=page_3,textvariable=message,corner_radius=8,font=customtkinter.CTkFont(family="Cambria",size=20),fg_color="transparent",state="disabled",width=433,height=50,justify="center")
page_page.pack()
page_page.place(anchor=tkinter.CENTER,rely = 0.9,relx = 0.5)

# Third frame (game) ends

# Fourth frame(fail message) starts
page_4 = customtkinter.CTkFrame(master=root)

label_6 = customtkinter.CTkLabel(master=page_4,text="Oops! Times Up",font= customtkinter.CTkFont(family="Cambria",size=20,weight="bold"))
label_6.pack()
label_6.place(anchor = tkinter.CENTER, rely = 0.2, relx = 0.5)

b_try = customtkinter.CTkButton(master=page_4,text="Try again!",font=customtkinter.CTkFont(family="Cambria",size=20),height=40)
b_try.pack()
b_try.bind("<Button-1>",page_3_again)
b_try.place(anchor = tkinter.CENTER,rely = 0.5, relx = 0.5)

b_try_again_exit = customtkinter.CTkButton(master=page_4,text="Exit",hover_color="dark red",fg_color="red",font=customtkinter.CTkFont(family="Cambria",size=20),height=40,command=win_logout)
b_try_again_exit.pack()
# b_try_again_exit.bind("<Button-1>",win_logout)
b_try_again_exit.place(anchor = tkinter.CENTER,rely = 0.8, relx = 0.5)

# Fourth frame(fail message) starts

# Fifth frame(attempt message) starts
page_5 = customtkinter.CTkFrame(master=root)

label_11 = customtkinter.CTkLabel(master=page_5,text="No. of attempts - ",font= customtkinter.CTkFont(family="Cambria",size=30,weight="bold"))
label_11.pack()
label_11.place(anchor = tkinter.CENTER, rely = 0.2, relx = 0.47)

entry_10 = customtkinter.CTkEntry(master=page_5,textvariable=attempt,font= customtkinter.CTkFont(family="Cambria",size=30,weight="bold"),border_width=0,fg_color="transparent")
entry_10.pack()
entry_10.place(anchor = tkinter.CENTER, rely = 0.2, relx = 0.88)

b_play_again = customtkinter.CTkButton(master=page_5,text="Play again!",font=customtkinter.CTkFont(family="Cambria",size=20),height=40)
b_play_again.pack()
b_play_again.bind("<Button-1>",play_again)
b_play_again.place(anchor = tkinter.CENTER,rely = 0.45, relx = 0.5)

b_play_again_exit = customtkinter.CTkButton(master=page_5,text="Exit",hover_color="dark red",fg_color="red",font=customtkinter.CTkFont(family="Cambria",size=20),height=40,command=win_logout)
b_play_again_exit.pack()
# b_play_again_exit.bind("<Button-1>",win_logout)
b_play_again_exit.place(anchor = tkinter.CENTER,rely = 0.7, relx = 0.5)

# Fifth frame(attempt message) ends

# Sixth frame(Rules) starts
page_6 = customtkinter.CTkFrame(master=root)

label_rule1 = customtkinter.CTkLabel(master=page_6,text="1) Press the Play Button.",font= customtkinter.CTkFont(family="Cambria",size=20,weight="bold"))
label_rule1.pack()
label_rule1.place(rely = 0.02)

label_rule2 = customtkinter.CTkLabel(master=page_6,text="2) Set the difficulty level according to you.",font= customtkinter.CTkFont(family="Cambria",size=20,weight="bold"))
label_rule2.pack()
label_rule2.place(rely = 0.1)

label_rule3 = customtkinter.CTkLabel(master=page_6,text="3) For each difficulty level there will be a \n  particular time to guess the number :- \n --> For diff level 1 - 40 secs \n --> For diff level 2 - 30 secs \n--> For diff level 3 - 20 secs\n--> For diff level 4 - 15 secs",font=customtkinter.CTkFont(family="Cambria",size=20,weight="bold"))
label_rule3.pack()
label_rule3.place(rely = 0.2)

label_rule4 = customtkinter.CTkLabel(master=page_6,text="4) If you guess the number between 1 to 100   \n    in the given time then you will win the game.",font=customtkinter.CTkFont(family="Cambria",size=20,weight="bold"))
label_rule4.pack()
label_rule4.place(rely = 0.65,relx = 0)

b_back = customtkinter.CTkButton(master=page_6,text="Back",font=customtkinter.CTkFont(family="Cambria",size=20),height=40)
b_back.pack()
b_back.bind("<Button-1>",back)
b_back.place(anchor = tkinter.CENTER,rely = 0.9, relx = 0.5)
# Sixth frame(Rules) ends

# my_image_ = customtkinter.CTkImage(dark_image=Image.open("ranplay.png"),size=(30, 27))
# label_image_ = customtkinter.CTkLabel(master=root,text="",image=my_image_)
# label_image_.pack()
# label_image_.place(rely=0.91)

root.mainloop()