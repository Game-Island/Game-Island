from tkinter import *
import random
import os
import pyrebase
from datetime import datetime
import sys
import customtkinter
import threading
import pandas as pd
import time
from PIL import Image, ImageTk, ImageSequence

now_ikey = datetime.now()
dt_string_ikey = now_ikey.strftime("%d-%m-%Y %H:%M:%S")
#print(dt_string_ikey)
df_ikey = pd.read_excel("User_Id.xlsx",sheet_name="User_Email_Id")
user_id_ikey = df_ikey["email_id"][0]
symbols_ikey=['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>' , '(', ')', '<',"!","^","&","_","-","+","=","[","]","{","}","'",'"']

for i in user_id_ikey:
    if i in symbols_ikey:
        user_id_ikey = user_id_ikey.replace(i,"")
        user_id_ikey = user_id_ikey.replace("gmailcom","")
# user_id_ikey = game_island.email_value()
#print("user_id_ikey: ",user_id_ikey,"-->",type(user_id_ikey))


try:
    configfirebase_ikey = {"apiKey": "AIzaSyDLSXHA_9IKUP2f_FLQF5_F_pZX-2E78cE",
"authDomain": "game-island-123.firebaseapp.com",
"databaseURL": "https://game-island-123-default-rtdb.asia-southeast1.firebasedatabase.app",
"projectId": "game-island-123",
"storageBucket": "game-island-123.appspot.com",
"messagingSenderId": "673041816597",
"appId": "1:673041816597:web:1fa678812282337dcd021c",
"measurementId": "G-WS0W53GRCN"
    }
    firebase_ikey = pyrebase.initialize_app(configfirebase_ikey)
    database_ikey = firebase_ikey.database()

except:
    SyntaxError

# path_ikey = "D:\Study\Coding\RanPlay\Game_Island\IKeyFlex.xlsx"
path_ikey = os.getcwd() + "/IKeyFlex.xlsx"
print(path_ikey)
is_file_ikey = os.path.isfile(path_ikey)
if is_file_ikey == True:
    #print("true")
    pass
else:
    df_ikey = pd.DataFrame(columns=["Difficulty Level","Wrong Keys","Score"])
    df_ikey.to_excel("IKeyFlex.xlsx",engine="openpyxl",sheet_name="User_Data",index=False)


temp_ikey = True
label_selected_ikey = []
set_wrong_ikey = set()
time_gap_ikey = 1
timer_thread_ikey = 0
match_thread_ikey = 0
wrong_keys_ikey = []

def win_logout():
    path_timer = os.getcwd() + "/Timer.xlsx"
    os.remove(path_timer)
    global user_id_ikey
    now_logout = datetime.now()
    logout_time = now_logout.strftime("%d-%m-%Y %H:%M:%S")
    logout_ = logout_time.split()
    logout_time = logout_[1]
    logout_date = logout_[0]
    user_data_island  = {"Status":'End'}
    t_island = repr(str(user_data_island))
    import json
    user_data_dict_island = json.loads(t_island)
    database_ikey.child(user_id_ikey).child("Timings").child(logout_date).child("IKeyFlex").child(logout_time).set(user_data_dict_island)
    root_ikey.destroy()

def back_ikey():
    frame_rules_ikey.forget()
    frame_opening_ikey.pack(fill = "both",expand = 1)

def rules_ikey():
    frame_opening_ikey.forget()
    frame_rules_ikey.pack(fill = "both",expand = 1)

def diff_ikey(event):
    global time_gap_ikey
    if int(slider_ikey.get()) == 1:
        time_gap_ikey = 1
        slider_ikey.configure(button_color = "#30A572",button_hover_color = "#146944",progress_color = "#30A572")
        difficult_ikey.set(1)
    elif int(slider_ikey.get()) == 2:
        time_gap_ikey = 0.75
        slider_ikey.configure(button_color = "#FCF926",button_hover_color = "#BAB81C",progress_color = "#FCF926")
        difficult_ikey.set(2) 
    elif int(slider_ikey.get()) == 3:
        time_gap_ikey = 0.5
        slider_ikey.configure(button_color = "#FF340C",button_hover_color = "#BF2709",progress_color = "#FF340C")
        difficult_ikey.set(3)

time_limit_ikey = 0

def timer_ikey():
    global wrong_keys_ikey
    global score_ikey
    global time_limit_ikey
    global user_id_ikey
    global dt_string_ikey
    global set_wrong_ikey
    global timeleft_ikey
    global temp_ikey
    start_ikey = time.time()
    time_limit_ikey = 20
    while temp_ikey == True:
        
        elapsed_ikey = time.time() - start_ikey
        timeleft_ikey.set(time_limit_ikey - int(elapsed_ikey))
        frame_game_ikey.update()

        if elapsed_ikey > time_limit_ikey:
            temp_ikey = False
            wrong_keys_ikey = list(set_wrong_ikey)
            wrong_keys_ikey.sort()
            wrong_keys_ikey = [(int(slider_ikey.get()),tuple(wrong_keys_ikey),score_ikey.get())]
            user_data_ikey  = {"Difficulty Level":int(slider_ikey.get()),"Wrong Keys":wrong_keys_ikey[0][1],"Score":score_ikey.get()}

            t_ikey = repr(str(user_data_ikey))
            import json
            user_data_dict_ikey = json.loads(t_ikey)

            df_ikey = pd.DataFrame(wrong_keys_ikey,columns=["Difficulty Level","Wrong Keys","Score"])
            with pd.ExcelWriter("IKeyFlex.xlsx",mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer:
                df_ikey.to_excel(writer, sheet_name="User_Data",header=None,startrow=writer.sheets["User_Data"].max_row,index=False)
            frame_game_ikey.forget()
            progress_bar_ikey.stop()
            try:
                database_ikey.child(user_id_ikey).child("IKeyFlex").child(dt_string_ikey).set(user_data_dict_ikey)
            except:SyntaxError
            score_frame_ikey.place(relx=0.39,rely = 0.27)
            # frame_game_ikey.update()
            break
            
def match_ikey():
    # print("match function starts")
    buttp_1.focus()
    global time_gap_ikey
    global temp_ikey
    global li_ikey
    global label_selected_ikey
    while temp_ikey == True:
        label_selected_ikey = li_ikey[random.randint(0,26)]
        label_selected_ikey.configure(fg_color = "red")
        frame_game_ikey.update()
        time.sleep(time_gap_ikey)
        label_selected_ikey.configure(fg_color = "#FF3B8B")
        frame_game_ikey.update()


def foc_1(): #Focus
    buttp_1.focus()

def foc(): #Start
    global timer_thread_ikey
    global match_thread_ikey
    frame_game_ikey.pack(fill = "both",expand = 1)
    frame_opening_ikey.forget()
    root_ikey.update()
    time.sleep(1)
    progress_bar_ikey.start()
    timer_thread_ikey = threading.Thread(target=timer_ikey)
    timer_thread_ikey.start()
    match_thread_ikey = threading.Thread(target=match_ikey)
    match_thread_ikey.start()


def end(event):
    global label_selected_ikey
    global set_wrong_ikey
    try:
        if 65 <= ord(event.char) <= 90 or 97 <= ord(event.char) <= 122 or ord(event.char) == 44:
            if ord(event.char) == ord(label_selected_ikey.cget("text")) or ord(event.char.upper()) == ord(label_selected_ikey.cget("text")) :
                score_ikey.set(score_ikey.get() + 10)
                label_selected_ikey.configure(fg_color = "#FF3B8B")
            else:
                label_selected_ikey.configure(fg_color = "#FF3B8B")
                set_wrong_ikey.add(label_selected_ikey.cget("text"))
        else:
            set_wrong_ikey.add(label_selected_ikey.cget("text"))
            label_selected_ikey.configure(fg_color = "#FF3B8B")
            #print("wrong")
    except:
        SyntaxError

def play_again_ikey():
    global temp_ikey
    temp_ikey = True
    # global time_limit_ikey
    # time_limit_ikey = 20
    difficult_ikey.set(1)
    slider_ikey.set(0)
    score_ikey.set(0)
    progress_bar_ikey.set(0)
    frame_opening_ikey.update()
    frame_game_ikey.update()
    score_frame_ikey.place_forget()
    frame_opening_ikey.pack(fill = "both",expand = 1)



    


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root_ikey = customtkinter.CTk()
root_ikey.title("IKeyFlex")
root_ikey.geometry("900x500+405+200")
root_ikey.resizable(False,False)
root_ikey.wm_iconbitmap("eye_icon.ico")
root_ikey.maxsize(900,500)
root_ikey.wm_attributes('-alpha', 0.9)
root_ikey.protocol("WM_DELETE_WINDOW",win_logout)

# opening frame starts
frame_opening_ikey = customtkinter.CTkFrame(master=root_ikey,fg_color="transparent")

key_image_ikey = customtkinter.CTkImage(dark_image=Image.open("eye_key.png"),size=(500,500))
label_image_main_ikey = customtkinter.CTkLabel(master=frame_opening_ikey ,image= key_image_ikey,text="")
label_image_main_ikey.place(relx = 0,rely = 0.05)

label_heading_ikey = customtkinter.CTkLabel(master=frame_opening_ikey,text="IKeyFlex",text_color="yellow",font=("comic sans ms",40),width=50,height=50,corner_radius=7)
label_heading_ikey.pack(pady = 7)

b_start_ikey = customtkinter.CTkButton(master=frame_opening_ikey,text="Play",font=("comic sans ms",35),width=150,height=40,command = foc)
b_start_ikey.place(relx=0.69,rely = 0.25)

b_rules_ikey = customtkinter.CTkButton(master=frame_opening_ikey,text="Rules",font=("comic sans ms",35),width=150,height=40,command = rules_ikey)
b_rules_ikey.place(relx=0.69,rely = 0.45)

progessbar_top = customtkinter.CTkProgressBar(master= frame_opening_ikey,width=900,mode="indeterminate",indeterminate_speed=0.8)
progessbar_top.place(x=0,y=0)
progessbar_top.start()

progessbar_bottom = customtkinter.CTkProgressBar(master= frame_opening_ikey,width=900,mode="indeterminate",indeterminate_speed=0.8)
progessbar_bottom.place(x=0,y=491)
progessbar_bottom.start()

progessbar_right = customtkinter.CTkProgressBar(master= frame_opening_ikey,height=500,orientation="vertical",mode="indeterminate",indeterminate_speed=0.8)
progessbar_right.place(x=891,y=0)
progessbar_right.start()

progessbar_left = customtkinter.CTkProgressBar(master= frame_opening_ikey,height=500,orientation="vertical",mode="indeterminate",indeterminate_speed=0.8)
progessbar_left.place(x=0,y=0)
progessbar_left.start()

difficulty_label_ikey = customtkinter.CTkLabel(master=frame_opening_ikey,text="Difficulty level:",font=("comic sans ms",27),width=50,height=50,corner_radius=7)
difficulty_label_ikey.place(relx = 0.655,rely = 0.6)


slider_ikey = customtkinter.CTkSlider(master=frame_opening_ikey,from_=1, to=3,number_of_steps=2,command=diff_ikey)
slider_ikey.set(0)
slider_ikey.place(relx = 0.665,rely = 0.83)

difficult_ikey = IntVar()
difficult_ikey.set(1)

difficulty_entry_ikey = customtkinter.CTkEntry(master=frame_opening_ikey,textvariable=difficult_ikey,font=("comic sans ms",27),width=50,height=50,justify = "center")
difficulty_entry_ikey.place(relx = 0.748,rely = 0.71)

frame_opening_ikey.pack(fill = "both",expand = 1)
# opening frame ends

# rules frames starts
frame_rules_ikey = customtkinter.CTkFrame(master=root_ikey,fg_color="transparent")

keyboard_finger_image = customtkinter.CTkImage(dark_image= Image.open("keyboard.png"),size=(300,200))
keyboard_finger = customtkinter.CTkLabel(master=frame_rules_ikey,text="",image=keyboard_finger_image)
# keyboard_finger.pack()

rule_window_ikey = customtkinter.CTkFrame(master=frame_rules_ikey)

label_rule_heading_ikey = customtkinter.CTkLabel(master=frame_rules_ikey,text="IKeyFlex",text_color="yellow",font=("comic sans ms",40),width=50,height=50,corner_radius=7)
label_rule_heading_ikey.pack()

label_rule_1_ikey = customtkinter.CTkLabel(master=rule_window_ikey,text = "1. Select the difficulty level according to you.",font=("cambria",32))

label_rule_2_ikey = customtkinter.CTkLabel(master=rule_window_ikey,text = "2. For each game you will have 20 seconds.",font=("cambria",32))

label_rule_3_ikey = customtkinter.CTkLabel(master=rule_window_ikey,text = "3. Press the Play button to start the game.",font=("cambria",32))

label_rule_4_ikey = customtkinter.CTkLabel(master=rule_window_ikey,text = "4. Press the key which is highlighted on the virtual keyboard.",font=("cambria",32))

label_rule_5_ikey = customtkinter.CTkLabel(master=rule_window_ikey,text = "5. For every right keypress score will increase by 10.",font=("cambria",32))

label_rule_5_ikey.pack(side = "bottom",anchor = "w",pady = 5)
label_rule_4_ikey.pack(side = "bottom",anchor = "w",pady = 5)
label_rule_3_ikey.pack(side = "bottom",anchor = "w",pady = 5)
label_rule_2_ikey.pack(side = "bottom",anchor = "w",pady = 5)
label_rule_1_ikey.pack(side = "bottom",anchor = "w",pady = 5)

rule_window_ikey.pack(anchor = "center",pady = 50,ipady = 5,ipadx = 10)

b_back_ikey = customtkinter.CTkButton(master=frame_rules_ikey,command=back_ikey,text="Back",font=("comic sans ms",35),width=100,height = 40)
b_back_ikey.place(rely = 0.8,relx = 0.45)
# rules frames ends

# Game frame starts
frame_game_ikey = customtkinter.CTkFrame(master=root_ikey,fg_color="transparent")

frame_keyboard_1 = customtkinter.CTkFrame(master=frame_game_ikey,fg_color="transparent")
frame_keyboard_2 = customtkinter.CTkFrame(master=frame_game_ikey,fg_color="transparent")
frame_keyboard_3 = customtkinter.CTkFrame(master=frame_game_ikey,fg_color="transparent")
frame_keyboard_4 = customtkinter.CTkFrame(master=frame_game_ikey,fg_color="transparent")

invisible_1_ikey = customtkinter.CTkLabel(master=frame_keyboard_1,text="  ")
invisible_1_ikey.pack(padx=70,pady=3,side = "left",fill = "y")

q = customtkinter.CTkLabel(master=frame_keyboard_1,text="Q",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7,justify = "center")
q.pack(padx=5,pady = 4,side = "left",anchor = "nw")

w = customtkinter.CTkLabel(master=frame_keyboard_1,text="W",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
w.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

e = customtkinter.CTkLabel(master=frame_keyboard_1,text="E",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
e.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

r = customtkinter.CTkLabel(master=frame_keyboard_1,text="R",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
r.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

t = customtkinter.CTkLabel(master=frame_keyboard_1,text="T",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
t.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

y = customtkinter.CTkLabel(master=frame_keyboard_1,text="Y",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
y.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

u = customtkinter.CTkLabel(master=frame_keyboard_1,text="U",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
u.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

i = customtkinter.CTkLabel(master=frame_keyboard_1,text="I",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
i.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

o = customtkinter.CTkLabel(master=frame_keyboard_1,text="O",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
o.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

p = customtkinter.CTkLabel(master=frame_keyboard_1,text="P",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
p.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

invisible_2_ikey = customtkinter.CTkLabel(master=frame_keyboard_2,text="  ")
invisible_2_ikey.pack(padx=90,pady=3,side = "left",fill = "y")

a = customtkinter.CTkLabel(master=frame_keyboard_2,text="A",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
a.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

s = customtkinter.CTkLabel(master=frame_keyboard_2,text="S",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
s.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

d = customtkinter.CTkLabel(master=frame_keyboard_2,text="D",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
d.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

f = customtkinter.CTkLabel(master=frame_keyboard_2,text="F",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
f.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

g = customtkinter.CTkLabel(master=frame_keyboard_2,text="G",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
g.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

h = customtkinter.CTkLabel(master=frame_keyboard_2,text="H",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
h.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

j = customtkinter.CTkLabel(master=frame_keyboard_2,text="J",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
j.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

k = customtkinter.CTkLabel(master=frame_keyboard_2,text="K",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
k.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

l = customtkinter.CTkLabel(master=frame_keyboard_2,text="L",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
l.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

invisible_3_ikey = customtkinter.CTkLabel(master=frame_keyboard_3,text="  ")
invisible_3_ikey.pack(padx=105,pady=3,side = "left",fill = "y")

z = customtkinter.CTkLabel(master=frame_keyboard_3,text="Z",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
z.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

x = customtkinter.CTkLabel(master=frame_keyboard_3,text="X",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
x.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

c = customtkinter.CTkLabel(master=frame_keyboard_3,text="C",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
c.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

v = customtkinter.CTkLabel(master=frame_keyboard_3,text="V",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
v.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

b = customtkinter.CTkLabel(master=frame_keyboard_3,text="B",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
b.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

n = customtkinter.CTkLabel(master=frame_keyboard_3,text="N",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
n.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

m = customtkinter.CTkLabel(master=frame_keyboard_3,text="M",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
m.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

comma = customtkinter.CTkLabel(master=frame_keyboard_3,text="<,",font=("cambria",40),fg_color="#FF3B8B",width=50,height=50,corner_radius=7)
comma.pack(padx = 5,pady = 4,side = "left",anchor = "nw")

score_ikey = IntVar()
score_ikey.set(0)
score_label_invisible_ikey = customtkinter.CTkLabel(master=frame_keyboard_4,text="  ")
score_label_invisible_ikey.pack(side = "left")

score_label_ikey = customtkinter.CTkLabel(master=frame_keyboard_4,text="Score:",font=("cambria",40),fg_color="transparent",width=50,height=50,corner_radius=7)
score_label_ikey.pack(side = "left",pady = 5,anchor = "n")

score_label_value_ikey = customtkinter.CTkLabel(master=frame_keyboard_4,textvariable=score_ikey,font=("cambria",40),fg_color="transparent",width=50,height=50,corner_radius=7)
score_label_value_ikey.pack(side = "left",pady = 5,anchor = "n")

timeleft_ikey = IntVar()
timeleft_ikey.set(20)

time_label_value = customtkinter.CTkLabel(master=frame_keyboard_4,textvariable = timeleft_ikey,font=("cambria",40),fg_color="transparent",width=50,height=50,corner_radius=7)
time_label_value.pack(side = "right",pady = 5,padx = 5)

time_label = customtkinter.CTkLabel(master=frame_keyboard_4,text="Time left:",font=("cambria",40),fg_color="transparent",width=50,height=50,corner_radius=7)
time_label.pack(side = "right",pady = 5)

li_ikey = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,comma]

frame_keyboard_4.pack(fill = "x",side="top")
frame_keyboard_3.place(y=425)
frame_keyboard_2.place(y=370)
frame_keyboard_1.place(y=315)

progress_bar_ikey = customtkinter.CTkProgressBar(master= frame_game_ikey,progress_color="light blue",width=600,height=10,determinate_speed=0.0514)
progress_bar_ikey.set(0)
progress_bar_ikey.place(rely = 0.45,relx = 0.16)

progessbar_top_1 = customtkinter.CTkProgressBar(master= frame_game_ikey,width=900,mode="indeterminate",indeterminate_speed=0.8)
progessbar_top_1.place(x=0,y=0)
progessbar_top_1.start()

progessbar_bottom_1 = customtkinter.CTkProgressBar(master= frame_game_ikey,width=900,mode="indeterminate",indeterminate_speed=0.8)
progessbar_bottom_1.place(x=0,y=491)
progessbar_bottom_1.start()

progessbar_right_1 = customtkinter.CTkProgressBar(master= frame_game_ikey,height=500,orientation="vertical",mode="indeterminate",indeterminate_speed=0.8)
progessbar_right_1.place(x=891,y=0)
progessbar_right_1.start()

progessbar_left_1 = customtkinter.CTkProgressBar(master= frame_game_ikey,height=500,orientation="vertical",mode="indeterminate",indeterminate_speed=0.8)
progessbar_left_1.place(x=0,y=0)
progessbar_left_1.start()

buttp_1 = customtkinter.CTkButton(master=frame_game_ikey,text=" ",hover_color="#242424",fg_color="#242424",width=0,height=0)
buttp_1.bind("a",end)
buttp_1.bind("b",end)
buttp_1.bind("c",end)
buttp_1.bind("d",end)
buttp_1.bind("e",end)
buttp_1.bind("f",end)
buttp_1.bind("g",end)
buttp_1.bind("h",end)
buttp_1.bind("i",end)
buttp_1.bind("j",end)
buttp_1.bind("k",end)
buttp_1.bind("l",end)
buttp_1.bind("m",end)
buttp_1.bind("n",end)
buttp_1.bind("o",end)
buttp_1.bind("p",end)
buttp_1.bind("q",end)
buttp_1.bind("r",end)
buttp_1.bind("s",end)
buttp_1.bind("t",end)
buttp_1.bind("u",end)
buttp_1.bind("v",end)
buttp_1.bind("w",end)
buttp_1.bind("x",end)
buttp_1.bind("y",end)
buttp_1.bind("z",end)
buttp_1.bind("A",end)
buttp_1.bind("B",end)
buttp_1.bind("C",end)
buttp_1.bind("D",end)
buttp_1.bind("E",end)
buttp_1.bind("F",end)
buttp_1.bind("G",end)
buttp_1.bind("H",end)
buttp_1.bind("I",end)
buttp_1.bind("J",end)
buttp_1.bind("K",end)
buttp_1.bind("L",end)
buttp_1.bind("M",end)
buttp_1.bind("N",end)
buttp_1.bind("O",end)
buttp_1.bind("P",end)
buttp_1.bind("Q",end)
buttp_1.bind("R",end)
buttp_1.bind("S",end)
buttp_1.bind("T",end)
buttp_1.bind("U",end)
buttp_1.bind("V",end)
buttp_1.bind("W",end)
buttp_1.bind("X",end)
buttp_1.bind("Y",end)
buttp_1.bind("Z",end)

buttp_1.pack()
# buttp_1.place(x = ,y = 0.99)

# frame_game_ikey.pack(fill = "both",expand = 1)
# Game frame ends

# score frame starts
score_frame_ikey = customtkinter.CTkFrame(master=root_ikey)

# score.set(20)
score_label_end_ikey = customtkinter.CTkLabel(master=score_frame_ikey,text="Score: ",font=("Cambria",35,"bold"))
score_label_end_ikey.place(relx = 0.14,rely=0.1)

score_label_value__end_ikey = customtkinter.CTkLabel(master=score_frame_ikey,text="",textvariable=score_ikey,font=("Cambria",35,"bold"))
score_label_value__end_ikey.place(relx = 0.68,rely=0.1)

b_play_again_ikey = customtkinter.CTkButton(master=score_frame_ikey,command=play_again_ikey,text="Play Again!",font=("comic sans ms",20,"bold"),height=40)
b_play_again_ikey.place(relx = 0.15,rely=0.4)

b_exit = customtkinter.CTkButton(master=score_frame_ikey,text="Exit",font=("comic sans ms",20,"bold"),hover_color="dark red",fg_color="red",height=40,command=win_logout)
b_exit.place(relx = 0.15,rely=0.7)


# score_frame_ikey.place(relx=0.39,rely = 0.27)
# score frame ends
root_ikey.mainloop()
