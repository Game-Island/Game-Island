import tkinter
import customtkinter
import ast
import hashlib
import time
from PIL import Image,ImageTk
import os
import threading
import smtplib
from email.mime.text import MIMEText as text
from datetime import datetime
import pandas as pd
from cryptography.fernet import Fernet
from openpyxl import load_workbook
from tkVideoPlayer import TkinterVideo
from pygame import mixer
import pyrebase

mixer.init()
mixer.music.load("game___island_audio.mp3")
mixer.music.set_volume(0)
mixer.music.play(-1)

otp = 0
otp_forgot = 0
receiver_forgot = ''
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
#print(dt_string)

login_time = 0
logout_time = 0

path = os.getcwd() + "/User_Id.xlsx"
#print(path)
is_file = os.path.isfile(path)
if is_file == True:
    #print("passed path")
    pass
else:
    email = [("empty")]
    df = pd.DataFrame(email,columns=["email_id"])
    df.to_excel("User_Id.xlsx",engine="openpyxl",sheet_name="User_Email_Id",index=False)

os.system(f"attrib +h {path}")

try : 
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
except Exception as e:
    print(e)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

user_id = 0

def temp():
    pass

def get_otp():
    global otp
    global email
    global user_id
    match = False

    if len(entry_name.get()) != 0 and len(entry_email.get()) != 0:
        if entry_email.get().endswith("@gmail.com") == False:
            already_email.configure(text="Invalid email")
            already_image_label.place(rely=0.54,relx=0.11)
            already_email.place(relx=0.15,rely=0.54)
        else:
            star_email.place_forget()
            star_name.place_forget()
            info_match = entry_email.get()
            symbols=['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>' , '(', ')', '<',"!","^","&","_","-","+","=","[","]","{","}","'",'"']
            for i in info_match:
                if i in symbols:
                    info_match = info_match.replace(i,"")
                    info_match = info_match.replace("gmailcom","")
            checking_none = database.get().val()
            if checking_none == None:
                pass
            else:
                for i in database.get().val():
                    if i == info_match:
                        match = True
            if match == True:
                ##print("Email_id already exists")
                already_email.configure(text="This account already exists")
                already_image_label.place(rely=0.54,relx=0.11)
                already_email.place(relx=0.15,rely=0.54)

            elif match == False:
                already_image_label.place_forget()
                already_email.place_forget()
                try:
                    import random
                    server=smtplib.SMTP('smtp.gmail.com',587)
                    server.starttls()
                    password='pcmpwosgwntorsuw'
                    server.login('gameisland.info@gmail.com',password)
                    otp=''.join([str(random.randint(0,9)) for i in range(4)])
                    name = entry_name.get()
                    msg='Hello, '+name+'. Your Verification Code is '+str(otp)
                    m = text(msg)
                    m['Subject'] = 'Gmail Verification-Game Island'
                    # msg['Subject'] = 'OTP Verification'
                    sender='gameisland.info@gmail.com'  
                    receiver_email=str(entry_email.get())
                    receiver=receiver_email 
                    server.sendmail(sender,receiver,m.as_string())
                    server.quit()
                    b_otp.configure(command=temp)

                    email_get = entry_email.get()
                    email = [(email_get)]
                    ##print(email,type(entry_email.get()))
                    df = pd.DataFrame(email,columns=["email_id"])
                    with pd.ExcelWriter("User_Id.xlsx",mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer:
                        df.to_excel(writer,sheet_name="User_Email_Id",header=None,startrow=1,index=False)
                    df = pd.read_excel("User_Id.xlsx",sheet_name="User_Email_Id")
                    user_id = df["email_id"][0]
                    symbols=['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>' , '(', ')', '<',"!","^","&","_","-","+","=","[","]","{","}","'",'"']
                    for i in user_id:
                        if i in symbols:
                            user_id = user_id.replace(i,"")
                            user_id = user_id.replace("gmailcom","")
                except Exception as e:
                    star_email.place(rely = 0.41,relx = 0.91)
                    already_image_label.place_forget()
                    already_email.place_forget()
                    ##print(e)
                    ##print("Invalid email-id or internet connection missing")

    if len(entry_name.get()) == 0 and len(entry_email.get()) == 0:
        star_name.place(rely = 0.24,relx = 0.91)
        star_email.place(rely = 0.41,relx = 0.91)
        login_back.update()
    if len(entry_email.get()) == 0 :
        star_email.place(rely = 0.41,relx = 0.91)
        if len(entry_name.get()) != 0:
            star_name.place_forget()
        login_back.update()
        
    elif len(entry_name.get()) == 0 :
        star_name.place(rely = 0.24,relx = 0.91)
        if len(entry_email.get()) != 0:
            star_email.place_forget()
        login_back.update()

def ok():
    page_3.forget()
    verification_frame.forget()
    password_frame.pack(fill = "both",expand = 1)

def app():
    global dt_string
    global join_time
    global join_date
    global timer_value
    li = []
    if len(entry_password.get()) == 0:
        pass
    if len(entry_password.get()) > 8:
        ##print("entered if > 8")
        uppercase=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        uppercase_bool = False
        lowercase=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        lowercase_bool = False
        digits=["1","2","3","4","5","6","7","8","9","0"]
        digits_bool = False
        if entry_password.get() == entry_password_confirm.get():
            ##print("entered ==")
            for a in entry_password.get():
                if a in uppercase:
                    uppercase_bool = True
                elif a in lowercase:
                    lowercase_bool = True
                elif a in digits:
                    digits_bool = True
            li = [uppercase_bool,lowercase_bool,digits_bool]
            ##print(li)
            if li.count(True) == 3:
                message = str(entry_password.get())
                encMessage = hashlib.sha256(message.encode('UTF-8')).hexdigest()
                df = pd.read_excel("User_Id.xlsx",sheet_name="User_Email_Id")
                user_id = df["email_id"][0]
                symbols=['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>' , '(', ')', '<',"!","^","&","_","-","+","=","[","]","{","}","'",'"']
                for i in user_id:
                    if i in symbols:
                        user_id = user_id.replace(i,"")
                        user_id = user_id.replace("gmailcom","")
                dash_profile_name.configure(text = user_id)
                user_data_1 = {"User_Email_Id":entry_email.get(),"Password":encMessage}
                import json
                t=repr(str(user_data_1))
                user_data_dict = json.loads(t)
                database.child(user_id).child("User_Id_Info").child(dt_string).set(user_data_dict)
                j = dt_string.split()
                join_date = j[0]
                join_time = j[1]
                joined_date_label.configure(text=f'Joined at:\n{join_date}\n{join_time}')
                submenu_dash.place_forget()
                app_drawer.pack(fill = "both",expand = 1)
                user_info = database.child(user_id).get()
                for a in user_info:
                    # #print("key:",a.key(),"value",a.val())
                    for b,c in a.val().items():
                        if a.key() == "User_Id_Info" :
                            user_password = c
                            j = b.split()
                            join_date = j[0]
                            join_time = j[1]
                            joined_date_label.configure(text=f'Joined at:\n{join_date}\n{join_time}')
                            submenu_dash.forget()
                            
                timer_value = 3600
                island.protocol("WM_DELETE_WINDOW",win_logout)
                timer_app = threading.Thread(target=timer)
                timer_app.start()
                password_frame.forget()
            elif li.count(True) < 3:
                entry_password.configure(fg_color="#FF7676",border_color="red")
                label_pass_match.configure(text="Password criteria doesn't match")
                label_pass_match.place(relx = 0.1,rely = 0.615)
                    
        else:
            entry_password_confirm.delete(0,len(entry_password_confirm.get()))
            entry_password_confirm.configure(fg_color="#FF7676",border_color="red")
            entry_password_confirm.delete(0,len(entry_password_confirm.get()))
            label_pass_match.configure(text="Password doesn't match")
            label_pass_match.place(relx=0.1,rely=0.615)
    elif 0 < len(entry_password.get()) < 8 :
        entry_password.configure(fg_color="#FF7676",border_color="red")
        label_pass_match.configure(text="Password criteria doesn't match")
        label_pass_match.place(relx=0.1,rely=0.615)

def try_again():
    b_otp.configure(command = get_otp)
    page_4.forget()
    verification_frame.forget()
    sign.pack(fill ="both",expand = 1)

gtn_popen = 0
ikeyflex_popen = 0
shafty_popen = 0
flyby_popen = 0
lns_popen = 0
slither_popen = 0
graph_popen = 0

def guess_the_number():
    global gtn_temp
    global gtn_popen
    global user_id
    global count_minimize
    count_minimize = 1
    gtn_temp = True
    # island.state(newstate="iconic")
    from subprocess import Popen
    mixer.music.set_volume(0)
    gtn_popen=Popen('python Random_num.py')
    now_login = datetime.now()
    login_time = now_login.strftime("%d-%m-%Y %H:%M:%S")
    login_ = login_time.split()
    login_time = login_[1]
    login_date = login_[0]
    user_data_island  = {"Status":'Start'}
    t_island = repr(str(user_data_island))
    import json
    user_data_dict_island = json.loads(t_island)
    email = [("empty")]
    df = pd.DataFrame(email,columns=["Timer"])
    df.to_excel("Timer.xlsx",engine="openpyxl",sheet_name="Timer",index=False)
    path_timer_hide = os.getcwd() + "/Timer.xlsx"
    os.system(f"attrib +h {path_timer_hide}")
    database.child(user_id).child("Timings").child(login_date).child("Guess the number").child(login_time).set(user_data_dict_island)

def IKeyFlex():
    global ikeyflex_temp
    global user_id
    global ikeyflex_popen
    global count_minimize
    count_minimize = 1
    ikeyflex_temp = True
    # island.state(newstate="iconic")
    from subprocess import Popen
    mixer.music.set_volume(0)
    ikeyflex_popen=Popen('python keyflex.py')
    now_login = datetime.now()
    login_time = now_login.strftime("%d-%m-%Y %H:%M:%S")
    login_ = login_time.split()
    login_time = login_[1]
    login_date = login_[0]
    user_data_island  = {"Status":'Start'}
    t_island = repr(str(user_data_island))
    import json
    user_data_dict_island = json.loads(t_island)
    email = [("empty")]
    df = pd.DataFrame(email,columns=["Timer"])
    df.to_excel("Timer.xlsx",engine="openpyxl",sheet_name="Timer",index=False)
    path_timer_hide = os.getcwd() + "/Timer.xlsx"
    os.system(f"attrib +h {path_timer_hide}")
    database.child(user_id).child("Timings").child(login_date).child("IKeyFlex").child(login_time).set(user_data_dict_island)

def FlyBy():
    global flyby_temp
    global flyby_popen
    global user_id
    global count_minimize
    count_minimize = 1
    flyby_temp = True
    # island.state(newstate="iconic")
    from subprocess import Popen
    mixer.music.set_volume(0)
    flyby_popen=Popen('python FlyBy.py')
    now_login = datetime.now()
    login_time = now_login.strftime("%d-%m-%Y %H:%M:%S")
    login_ = login_time.split()
    login_time = login_[1]
    login_date = login_[0]
    user_data_island  = {"Status":'Start'}
    t_island = repr(str(user_data_island))
    import json
    user_data_dict_island = json.loads(t_island)
    email = [("empty")]
    df = pd.DataFrame(email,columns=["Timer"])
    df.to_excel("Timer.xlsx",engine="openpyxl",sheet_name="Timer",index=False)
    path_timer_hide = os.getcwd() + "/Timer.xlsx"
    os.system(f"attrib +h {path_timer_hide}")
    database.child(user_id).child("Timings").child(login_date).child("FlyBy").child(login_time).set(user_data_dict_island)
        

def LNS():
    global lns_popen
    global lns_temp
    global user_id
    global count_minimize
    count_minimize = 1
    lns_temp = True
    # island.state(newstate="iconic")
    from subprocess import Popen
    mixer.music.set_volume(0)
    lns_popen=Popen('python Snakes_N_Ladders_Game.py')
    now_login = datetime.now()
    login_time = now_login.strftime("%d-%m-%Y %H:%M:%S")
    login_ = login_time.split()
    login_time = login_[1]
    login_date = login_[0]
    user_data_island  = {"Status":'Start'}
    t_island = repr(str(user_data_island))
    import json
    user_data_dict_island = json.loads(t_island)
    email = [("empty")]
    df = pd.DataFrame(email,columns=["Timer"])
    df.to_excel("Timer.xlsx",engine="openpyxl",sheet_name="Timer",index=False)
    path_timer_hide = os.getcwd() + "/Timer.xlsx"
    os.system(f"attrib +h {path_timer_hide}")
    database.child(user_id).child("Timings").child(login_date).child("LNS").child(login_time).set(user_data_dict_island)

def Slither():
    global slither_temp
    global slither_popen
    global user_id
    global count_minimize
    count_minimize = 1
    slither_temp = True
    # island.state(newstate="iconic")
    from subprocess import Popen
    mixer.music.set_volume(0)
    slither_popen=Popen('python slither.py')
    now_login = datetime.now()
    login_time = now_login.strftime("%d-%m-%Y %H:%M:%S")
    login_ = login_time.split()
    login_time = login_[1]
    login_date = login_[0]
    user_data_island  = {"Status":'Start'}
    t_island = repr(str(user_data_island))
    import json
    user_data_dict_island = json.loads(t_island)
    email = [("empty")]
    df = pd.DataFrame(email,columns=["Timer"])
    df.to_excel("Timer.xlsx",engine="openpyxl",sheet_name="Timer",index=False)
    path_timer_hide = os.getcwd() + "/Timer.xlsx"
    os.system(f"attrib +h {path_timer_hide}")
    database.child(user_id).child("Timings").child(login_date).child("Slither").child(login_time).set(user_data_dict_island)

def Shafty():
    global shafty_temp
    global shafty_popen
    global user_id
    global count_minimize
    count_minimize = 1
    shafty_temp = True
    # island.state(newstate="iconic")
    from subprocess import Popen
    mixer.music.set_volume(0)
    shafty_popen=Popen('python Shafty.py')
    now_login = datetime.now()
    login_time = now_login.strftime("%d-%m-%Y %H:%M:%S")
    login_ = login_time.split()
    login_time = login_[1]
    login_date = login_[0]
    user_data_island  = {"Status":'Start'}
    t_island = repr(str(user_data_island))
    import json
    user_data_dict_island = json.loads(t_island)
    email = [("empty")]
    df = pd.DataFrame(email,columns=["Timer"])
    df.to_excel("Timer.xlsx",engine="openpyxl",sheet_name="Timer",index=False)
    path_timer_hide = os.getcwd() + "/Timer.xlsx"
    os.system(f"attrib +h {path_timer_hide}")
    database.child(user_id).child("Timings").child(login_date).child("Shafty").child(login_time).set(user_data_dict_island)

def graphs_display():
    global graph_temp
    global graph_popen
    graph_temp = True
    global count_minimize
    count_minimize = 1
    from subprocess import Popen
    # mixer.music.set_volume(0)
    graph_popen=Popen('python checktrend.py')
    email = [("empty")]
    df = pd.DataFrame(email,columns=["Timer"])
    df.to_excel("Timer.xlsx",engine="openpyxl",sheet_name="Timer",index=False)
    path_timer_hide = os.getcwd() + "/Timer.xlsx"
    os.system(f"attrib +h {path_timer_hide}")
    

def gmail():
    global otp
    if otp == entry_otp.get():
        now_login = datetime.now()
        login_time = now_login.strftime("%d-%m-%Y %H:%M:%S")
        login_ = login_time.split()
        login_time = login_[1]
        login_date = login_[0]
        verification_frame.pack(fill="both",expand = 1)
        user_data_island  = {"Status":'Logged In',"Time Left":"59:59"}
        t_island = repr(str(user_data_island))
        import json
        user_data_dict_island = json.loads(t_island)
        database.child(user_id).child("Timings").child(login_date).child("Game_Island").child(login_time).set(user_data_dict_island)
        page_3.pack(pady=200)
        sign.forget()
    elif len(entry_otp.get()) == 0:
        pass
    else:
        verification_frame.pack(fill="both",expand = 1)
        page_4.pack(pady = 200)
        sign.forget()
    
def show_criteria(event):
    criteria_label.place(relx = 0.4,rely=0.13)

def disappear_criteria(event):
    criteria_label.place_forget()

def hypertext(event):
    have_account.configure(font=("Cambria",20,"bold","underline"),text_color="#4F4F4F")

def hypertext_disappear(event):
    have_account.configure(font=("Cambria",20,"bold"),text_color="black")

def hypertext_login(event):
    forgot_password.configure(font=("Cambria",15,"bold","underline"),text_color="#4F4F4F")

def disappear_hypertext_login(event):
    forgot_password.configure(font=("Cambria",15,"bold"),text_color="black")

def up_to_in(event):
    sign.forget()
    login_frame.pack(fill="both",expand=1)

def in_to_up():
    login_frame.forget()
    sign.pack(fill="both",expand=1)

def forgot_to_in():
    forgot_frame.place_forget()
    login_back_2.place(relx = 0.25,rely=0.27,width = 500,height = 350,bordermode = "outside")

def in_to_forgot(event):
    login_back_2.place_forget()
    forgot_email.set(entry_login_email.get())
    forgot_frame.place(relx = 0.25,rely=0.27,width = 500,height = 350,bordermode = "outside")

def forgot_get_otp():
    global receiver_forgot
    global otp_forgot
    import random
    # import smtplib
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    password='pcmpwosgwntorsuw'
    server.login('gameisland.info@gmail.com',password)
    otp_forgot=''.join([str(random.randint(0,9)) for i in range(4)])
    # name = entry_name.get()
    msg='Hello, '+receiver_forgot+'. Your Verification Code is '+str(otp_forgot)
    m = text(msg)
    m['Subject'] = 'Reset Password Request'
    # msg['Subject'] = 'OTP Verification'
    sender='gameisland.info@gmail.com'  
    receiver_email=str(forgot_email.get())
    receiver=receiver_email 
    server.sendmail(sender,receiver,m.as_string())
    server.quit()
    b_getotp_forgot_pass.configure(command=temp)

def newpass_to_app():
    global dt_string
    global receiver_forgot
    global join_time
    global join_date
    global timer_value
    li = []
    if len(entry_password.get()) == 0:
        pass
    if len(entry_password.get()) > 8:
        ##print("entered if > 8")
        uppercase=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        uppercase_bool = False
        lowercase=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        lowercase_bool = False
        digits=["1","2","3","4","5","6","7","8","9","0"]
        digits_bool = False
        if entry_password.get() == entry_password_confirm.get():
            ##print("entered ==")
            for a in entry_password.get():
                if a in uppercase:
                    uppercase_bool = True
                elif a in lowercase:
                    lowercase_bool = True
                elif a in digits:
                    digits_bool = True
            li = [uppercase_bool,lowercase_bool,digits_bool]
            ##print(li)
            if li.count(True) == 3:
                list_time=[]
                now_login = datetime.now()
                login_time = now_login.strftime("%d-%m-%Y %H:%M:%S")
                login_ = login_time.split()
                login_time = login_[1]
                login_date = login_[0]
                message = str(entry_password.get())
                # key = Fernet.generate_key()
                # fernet = Fernet(key)
                encMessage = hashlib.sha256(message.encode('UTF-8')).hexdigest()
                user_id = receiver_forgot
                user_data_1 = {"User_Email_Id":entry_login_email.get(),"Password":encMessage}
                import json
                t=repr(str(user_data_1))
                user_data_dict = json.loads(t)
                user_info = database.child(user_id).get()
                for a in user_info:
                    ##print(a.key(),a.val())
                    for b,c in a.val().items():
                        user_login_date = b
                dt_string = b
                j = b.split()
                join_date = j[0]
                join_time = j[1]
                ##print(b)
                user_info = database.child(receiver_forgot).get()
                for a in user_info:
                    # #print("key:",a.key(),"value",a.val())
                    for b,c in a.val().items():
                        if a.key() == "User_Id_Info" :
                            user_password = c
                            j = b.split()
                            join_date = j[0]
                            join_time = j[1]
                            joined_date_label.configure(text=f'Joined at:\n{join_date}\n{join_time}')
                            submenu_dash.forget()
                            ##print(user_password,"user_password",b)
                            user_info = database.child(user_id).get()
                            for a in user_info:
                                # #print("key:",a.key(),"value",a.val())
                                for b,c in a.val().items():
                                    if a.key() == "Timings":
                                        ze = database.child(user_id).child(a.key()).get()
                                        # #print(z.val())
                                        for x in ze:
                                            # #print(x.val(),"x.val()")
                                            for d,e in x.val().items():
                                                if x.key() == login_date:
                                                    ye = database.child(user_id).child(a.key()).child(login_date).get()
                                                    for h in ye:
                                                        for m,n in h.val().items():
                                                            if h.key() == "Game_Island":
                                                                list_time.append(n)

                                                        # #print(x.key())
                                                        # #print(d,e)
                    # database.child(user_id).child("Timings").child(login_date).child(login_time).set("Logged In")
                    #print(list_time)
                    if len(list_time) > 0:
                        list_time = list_time[::-1]
                        time_limit_str = list_time[0]
                        #print(time_limit_str)
                        time_limit_dict = ast.literal_eval(time_limit_str)
                        time_limit = time_limit_dict['Time Left']
                        time_limit = time_limit.split(":")
                        #print(time_limit)
                        time_limit_minute = int(time_limit[0])
                        time_limit_second = int(time_limit[1])
                        timer_value = (time_limit_minute*60) + time_limit_second
                    else:
                        timer_value = 3600
                dash_profile_name.configure(text = user_id)
                database.child(user_id).child("User_Id_Info").child(dt_string).set(user_data_dict)
                joined_date_label.configure(text=f'Joined at:\n{join_date}\n{join_time}')
                submenu_dash.place_forget()
                timer_app = threading.Thread(target=timer)
                timer_app.start()
                # now_login = datetime.now()
                # login_time = now_login.strftime("%d-%m-%Y %H:%M:%S")
                # login_ = login_time.split()
                # login_time = login_[1]
                # login_date = login_[0]

                # verification_frame.pack(fill="both",expand = 1)
                timer_value_login_minute = timer_value // 60
                ##print(timer_value_login_minute,"timer_value_minute_login")
                timer_value_login_second = timer_value % 60
                if timer_value_login_minute < 10:
                    timer_value_login_minute = '0'+str(timer_value_login_minute)
                if timer_value_login_second < 10:
                    timer_value_login_second = '0'+str(timer_value_login_second)
                timer_value_login_minute = str(timer_value_login_minute)
                timer_value_login_second = str(timer_value_login_second)
                user_data_island  = {"Status":'Logged In',"Time Left":f"{timer_value_login_minute}:{timer_value_login_second}"}
                t_island = repr(str(user_data_island))
                import json
                user_data_dict_island = json.loads(t_island)
                database.child(user_id).child("Timings").child(login_date).child("Game_Island").child(login_time).set(user_data_dict_island)
                password_frame.forget()
                island.protocol("WM_DELETE_WINDOW",win_logout)
                app_drawer.pack(fill = "both",expand = 1)
            elif li.count(True) < 3:
                entry_password.configure(fg_color="#FF7676",border_color="red")
                label_pass_match.configure(text="Password criteria doesn't match")
                label_pass_match.place(relx = 0.1,rely = 0.615)
                    
        else:
            entry_password_confirm.delete(0,len(entry_password_confirm.get()))
            entry_password_confirm.configure(fg_color="#FF7676",border_color="red")
            entry_password_confirm.delete(0,len(entry_password_confirm.get()))
            label_pass_match.configure(text="Password doesn't match")
            label_pass_match.place(relx=0.1,rely=0.615)
    elif 0 < len(entry_password.get()) < 8 :
        entry_password.configure(fg_color="#FF7676",border_color="red")
        label_pass_match.configure(text="Password criteria doesn't match")
        label_pass_match.place(relx=0.1,rely=0.615)
    

def forgot_otp_verify():
    global otp_forgot
    if len(entry_forgot_pass_otp.get()) == 0:
        label_match_otp_forgot.configure(text="Please enter OTP")
        label_match_otp_forgot.place(relx = 0.14,rely=0.62)
        image_match_otp_forgot.place(rely=0.62,relx=0.1)
    if len(entry_forgot_pass_otp.get()) != 0:
        if entry_forgot_pass_otp.get() == otp_forgot:
            b_getotp_forgot_pass.configure(command = forgot_get_otp)
            forgot_frame.place_forget()
            login_frame.forget()
            password_frame.pack(fill="both",expand = 1)
            entry_password.configure(placeholder_text = "Create new password")
            b_done.configure(command = newpass_to_app)
        else:
            b_getotp_forgot_pass.configure(command = forgot_get_otp)
            label_match_otp_forgot.configure(text="Invalid OTP")
            label_match_otp_forgot.place(relx = 0.14,rely=0.62)
            image_match_otp_forgot.place(rely=0.62,relx=0.1)
        

def login():
    global timer_value
    global receiver_forgot
    global join_time
    global join_date
    list_time = []
    if len(entry_password_login.get()) == 0 or len(entry_login_email.get()) == 0:
        pass
    if len(entry_password_login.get()) != 0 and len(entry_login_email.get()) != 0:       
        match = False
        if entry_login_email.get().endswith("@gmail.com") == True:
            email_get = entry_login_email.get()
            email = [(email_get)]
            df = pd.DataFrame(email,columns=["email_id"])
            with pd.ExcelWriter("User_Id.xlsx",mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer:
                df.to_excel(writer,sheet_name="User_Email_Id",header=None,startrow=1,index=False)
            info_match = entry_login_email.get()
            symbols=['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>' , '(', ')', '<',"!","^","&","_","-","+","=","[","]","{","}","'",'"']
            for i in info_match:
                if i in symbols:
                    info_match = info_match.replace(i,"")
                    info_match = info_match.replace("gmailcom","")
            for i in database.get().val():
                if i == info_match:
                    match = True
            if match == True:
                receiver_forgot = info_match
                label_pass_match_login.place_forget()
                image_login.place_forget()
                user_info_login = database.child(info_match).get()
                now_login = datetime.now()
                login_time = now_login.strftime("%d-%m-%Y %H:%M:%S")
                login_ = login_time.split()
                login_time = login_[1]
                login_date = login_[0]
                for a in user_info_login:
                    # #print("key:",a.key(),"value",a.val())
                    for b,c in a.val().items():
                        if a.key() == "User_Id_Info" :
                            user_password = c
                            #print(b,"b_login")
                            j = b.split()
                            join_date = j[0]
                            join_time = j[1]
                            joined_date_label.configure(text=f'Joined at:\n{join_date}\n{join_time}')
                            submenu_dash.forget()
                            ##print(user_password,"user_password",b)
                            user_id = info_match
                            #print(user_id,"inside login")
                            user_info = database.child(user_id).get()
                            for a in user_info:
                                # #print("key:",a.key(),"value",a.val())
                                for b,c in a.val().items():
                                    if a.key() == "Timings":
                                        ze = database.child(user_id).child(a.key()).get()
                                        # #print(z.val())
                                        for x in ze:
                                                # #print(x.val(),"x.val()")
                                            for d,e in x.val().items():
                                                if x.key() == login_date:
                                                    ye = database.child(user_id).child(a.key()).child(login_date).get()
                                                    for h in ye:
                                                        for m,n in h.val().items():
                                                            if h.key() == "Game_Island":
                                                                list_time.append(n)

                    # database.child(user_id).child("Timings").child(login_date).child(login_time).set("Logged In")
                    #print(list_time)
                    if len(list_time) > 0:
                        list_time = list_time[::-1]
                        time_limit_str = list_time[0]
                        #print(time_limit_str)
                        time_limit_dict = ast.literal_eval(time_limit_str)
                        time_limit = time_limit_dict['Time Left']
                        time_limit = time_limit.split(":")
                        #print(time_limit)
                        time_limit_minute = int(time_limit[0])
                        time_limit_second = int(time_limit[1])
                        timer_value = (time_limit_minute*60) + time_limit_second
                    else:
                        timer_value = 3600
                dita = ast.literal_eval(user_password)
                login_pass = str(entry_password_login.get())
                login_pass_decrypt = hashlib.sha256(login_pass.encode('UTF-8')).hexdigest()
                decrypted_password =  dita['Password'] 
                if login_pass_decrypt == decrypted_password:
                    # now_login = datetime.now()
                    # login_time = now_login.strftime("%d-%m-%Y %H:%M:%S")
                    # login_ = login_time.split()
                    # login_time = login_[1]
                    # login_date = login_[0]
                    timer_value_login_minute = timer_value // 60
                    #print(timer_value_login_minute,"timer_value_minute_login")
                    timer_value_login_second = timer_value % 60
                    if timer_value_login_minute < 10:
                        timer_value_login_minute = '0'+str(timer_value_login_minute)
                    if timer_value_login_second < 10:
                        timer_value_login_second = '0'+str(timer_value_login_second)
                    timer_value_login_minute = str(timer_value_login_minute)
                    timer_value_login_second = str(timer_value_login_second)
                    user_data_island  = {"Status":'Logged In',"Time Left":f"{timer_value_login_minute}:{timer_value_login_second}"}
                    t_island = repr(str(user_data_island))
                    import json
                    user_data_dict_island = json.loads(t_island)
                    database.child(user_id).child("Timings").child(login_date).child("Game_Island").child(login_time).set(user_data_dict_island)
                    island.protocol("WM_DELETE_WINDOW",win_logout)
                    remember_login()
                    dash_profile_name.configure(text = receiver_forgot)
                    submenu_dash.place_forget()
                    app_drawer.pack(fill = "both",expand = 1)
                    timer_app = threading.Thread(target=timer)
                    timer_app.start()
                    login_frame.forget()
                else:
                    label_pass_match_login.configure(text="Wrong Password")
                    label_pass_match_login.place(relx = 0.14,rely=0.6)
                    forgot_password.place(relx=0.58,rely=0.6)
                    image_login.place(relx = 0.1,rely=0.6)
            else:
                label_pass_match_login.configure(text="This account does not exist")
                label_pass_match_login.place(relx = 0.14,rely=0.6)
                image_login.place(relx = 0.1,rely=0.6)

        else:
            label_pass_match_login.configure(text = "Invalid email")
            label_pass_match_login.place(relx = 0.14,rely=0.6)
            image_login.place(relx = 0.1,rely=0.6)

def app_to_dash():
    app_canvas.forget()
    dashboard_frame.pack(fill="both",expand=1)

def back_to_dash_games():
    dash_games_frame.place(relx=0.2,rely=0.37)
    time_left_label.place(relx=0.305,rely=0.3)
    time_minute_label.place(relx=0.515,rely=0.3)
    time_colon_label.place(relx=0.585,rely=0.3)
    time_second_label.place(relx=0.62,rely=0.3)
    statistics_label.place_forget()
    no_data.place_forget()
    # statistics_label.configure(text="Statistics")
    # statistics_label.place(relx = 0.21,rely=0.24)
    b_cross.place_forget()
    stats_gtn.place_forget()
    stats_ikeyflex.place_forget()
    stats_flyby.place_forget()
    stats_slither.place_forget()

sub = True
def submenu():
    global sub
    if sub == True:
        submenu_dash.place(relx=0.788,rely=0.12)
        sub = False
    elif sub == False:
        submenu_dash.place_forget()
        sub = True

def gtn_stats():
    stats_date_now = datetime.now()
    stats_date = stats_date_now.strftime("%d-%m-%Y")
    # stats_gtn.place(relx=0.08,rely=0.4)
    b_cross.place(relx = 0.873,rely=0.35)
    time_left_label.place_forget()
    time_minute_label.place_forget()
    time_colon_label.place_forget()
    time_second_label.place_forget()
    dash_games_frame.place_forget()
    statistics_label.configure(text="Guess The Number")
    statistics_label.place(relx = 0.08,rely=0.33)
    username = dash_profile_name.cget("text")
    user_info = database.child(username).get()
    data_list = []
    date_time_list = []
    table = False
    for a in user_info:
        for b,c in a.val().items():
            if a.key() == "Guess the number":
                table = True
                # #print("new",b,c,type(c))
                date_time_list.append(b)
                date_time_list.sort()
                data_tuple = []
                data_tuple.append(b)
                c = ast.literal_eval(c)
                for ele in c.keys():
                    data_tuple.append(c.get(ele))
                data_tuple = tuple(data_tuple)
                data_list.append(data_tuple)
    ##print(data_list,"unsorted")
    date_time_list = date_time_list[::-1]
    
    data_list = data_list[::-1]
    if table == True:
        stats_gtn.place(relx=0.08,rely=0.4)
        count = 0
        for row in range(len(data_list)):
            count += 1
            for col in range(len(data_list[0])):
                entry_table = customtkinter.CTkEntry(master=stats_gtn,fg_color="#5E3D34",justify="center",font=("cambria",25))
                if col == 0:
                    entry_table.configure(width=250)
                entry_table.grid(row = row+1, column = col)
                entry_table.insert('end',data_list[row][col])
                entry_table.configure(state="disabled")
            if count >= 7:
                break
    if table == False:
        no_data.place(relx=0.08,rely=0.4)
        ##print("No Data!")

def ikeyflex_stats():
    # stats_gtn.place(relx=0.08,rely=0.4)
    b_cross.place(relx = 0.873,rely=0.35)
    dash_games_frame.place_forget()
    time_left_label.place_forget()
    time_minute_label.place_forget()
    time_colon_label.place_forget()
    time_second_label.place_forget()
    statistics_label.configure(text="IKeyFlex")
    statistics_label.place(relx = 0.08,rely=0.33)
    username = dash_profile_name.cget("text")
    user_info = database.child(username).get()
    data_list = []
    table = False
    for a in user_info:
        for b,c in a.val().items():
            # #print(a.val())
            if a.key() == "IKeyFlex":
                table = True
                ##print("new",b,c,type(c))
                data_tuple = []
                data_tuple.append(b)
                c = ast.literal_eval(c)
                for ele in c.keys():
                    data_tuple.append(c.get(ele))
                data_tuple = tuple(data_tuple)
                data_list.append(data_tuple)
                ##print(data_list)
    data_list = data_list[::-1]
    if table == True:
        stats_ikeyflex.place(relx=0.08,rely=0.4)
        count = 0
        for row in range(len(data_list)):
            count += 1
            for col in range(len(data_list[0])):
                entry_table = customtkinter.CTkEntry(master=stats_ikeyflex,fg_color="#5E3D34",justify="center",font=("cambria",25))
                if col == 0:
                    entry_table.configure(width=250)
                entry_table.grid(row = row+1, column = col)
                entry_table.insert('end',data_list[row][col])
                entry_table.configure(state="disabled")
            if count >= 7:
                break
    if table == False:
        no_data.place(relx=0.08,rely=0.4)
        ##print("No Data!")

def flyby_stats():
    # stats_gtn.place(relx=0.08,rely=0.4)
    b_cross.place(relx = 0.873,rely=0.35)
    time_left_label.place_forget()
    time_minute_label.place_forget()
    time_colon_label.place_forget()
    time_second_label.place_forget()
    dash_games_frame.place_forget()
    statistics_label.configure(text="FlyBy")
    statistics_label.place(relx = 0.08,rely=0.33)
    username = dash_profile_name.cget("text")
    user_info = database.child(username).get()
    # #print(user_info,type(user_info))
    data_list = []
    table = False
    for a in user_info:
        for b,c in a.val().items():
            # #print(a.val())
            # #print(a.items())
            if a.key() == "FlyBy":
                table = True
                ##print("new",b,c,type(c))
                data_tuple = []
                data_tuple.append(b)
                c = ast.literal_eval(c)
                for ele in c.keys():
                    data_tuple.append(c.get(ele))
                data_tuple = tuple(data_tuple)
                data_list.append(data_tuple)
                #print(data_list)
    data_list = data_list[::-1]
    if table == True:
        statistics_label.place(relx = 0.26,rely=0.33)
        b_cross.place(relx = 0.70,rely=0.35)
        stats_flyby.place(relx=0.26,rely=0.4)
        count = 0
        for row in range(len(data_list)):
            count += 1
            for col in range(len(data_list[0])):
                entry_table = customtkinter.CTkEntry(master=stats_flyby,fg_color="#5E3D34",justify="center",font=("cambria",25))
                if col == 0:
                    entry_table.configure(width=250)
                entry_table.grid(row = row+1, column = col)
                entry_table.insert('end',data_list[row][col])
                entry_table.configure(state="disabled")
            if count >= 7:
                break
    if table == False:
        no_data.place(relx=0.08,rely=0.4)
        ##print("No Data!")


def slither_stats():
    # stats_gtn.place(relx=0.08,rely=0.4)
    b_cross.place(relx = 0.873,rely=0.35)
    time_left_label.place_forget()
    time_minute_label.place_forget()
    time_colon_label.place_forget()
    time_second_label.place_forget()
    dash_games_frame.place_forget()
    statistics_label.configure(text="Slither")
    statistics_label.place(relx = 0.08,rely=0.33)
    username = dash_profile_name.cget("text")
    user_info = database.child(username).get()
    data_list = []
    table = False
    for a in user_info:
        for b,c in a.val().items():
            # #print(a.val())
            if a.key() == "Slither":
                table = True
                ##print("new",b,c,type(c))
                data_tuple = []
                data_tuple.append(b)
                c = ast.literal_eval(c)
                for ele in c.keys():
                    data_tuple.append(c.get(ele))
                data_tuple = tuple(data_tuple)
                data_list.append(data_tuple)
                ##print(data_list)
    data_list = data_list[::-1]
    if table == True:
        statistics_label.place(relx = 0.26,rely=0.33)
        b_cross.place(relx = 0.70,rely=0.35)
        stats_slither.place(relx=0.26,rely=0.4)
        count = 0
        for row in range(len(data_list)):
            count += 1
            for col in range(len(data_list[0])):
                entry_table = customtkinter.CTkEntry(master=stats_slither,fg_color="#5E3D34",justify="center",font=("cambria",25))
                if col == 0:
                    entry_table.configure(width=250)
                entry_table.grid(row = row+1, column = col)
                entry_table.insert('end',data_list[row][col])
                entry_table.configure(state="disabled")
            if count >= 7:
                break
    if table == False:
        no_data.place(relx=0.08,rely=0.4)
        ##print("No Data!")

def remember():
    df = pd.read_excel("User_Id.xlsx",sheet_name="User_Email_Id")
    user_id = df["email_id"][0]
    symbols=['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>' , '(', ')', '<',"!","^","&","_","-","+","=","[","]","{","}","'",'"']
    for i in user_id:
        if i in symbols:
            user_id = user_id.replace(i,"")
            user_id = user_id.replace("gmailcom","")
    if remember_check.get() == 1:
        database.child(user_id).child("Remembered").child(dt_string).set("")
    elif remember_check.get() == 0:
        database.child(user_id).child("Remembered").remove()

def remember_login():
    if len(entry_password_login.get()) == 0 or len(entry_login_email.get()) == 0:
        #print("length zero")
        pass
    if len(entry_password_login.get()) != 0 and len(entry_login_email.get()) != 0:    
        #print("inside length")   
        if entry_login_email.get().endswith("@gmail.com") == True:
            #print("valid email")
            user_id = entry_login_email.get()
            symbols=['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>' , '(', ')', '<',"!","^","&","_","-","+","=","[","]","{","}","'",'"']
            for i in user_id:
                if i in symbols:
                    user_id = user_id.replace(i,"")
                    user_id = user_id.replace("gmailcom","")
            if remember_check_login.get() == 1:
                #print("data entered")
                database.child(user_id).child("Remembered").child(dt_string).set("")
            elif remember_check_login.get() == 0:
                database.child(user_id).child("Remembered").remove()

def remember_forgot():
    df = pd.read_excel("User_Id.xlsx",sheet_name="User_Email_Id")
    user_id = df["email_id"][0]
    symbols=['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>' , '(', ')', '<',"!","^","&","_","-","+","=","[","]","{","}","'",'"']
    for i in user_id:
        if i in symbols:
            user_id = user_id.replace(i,"")
            user_id = user_id.replace("gmailcom","")
    if remember_check_forgot.get() == 1:
        database.child(user_id).child("Remembered").child(dt_string).set("")
    elif remember_check_forgot.get() == 0:
        database.child(user_id).child("Remembered").remove()

def music():
    mixer.music.stop()
    island.destroy()

def win_logout():
    global gtn_temp 
    global ikeyflex_temp 
    global lns_temp 
    global flyby_temp 
    global shafty_temp 
    global slither_temp 
    global graph_temp
    global graph_popen
    global gtn_popen
    global ikeyflex_popen
    global lns_popen
    global flyby_popen
    global shafty_popen
    global slither_popen
    if gtn_temp == True:
        gtn_popen.kill()
    if ikeyflex_temp == True:
        ikeyflex_popen.kill()
    if lns_temp == True:
        lns_popen.kill()
    if flyby_temp == True:
        flyby_popen.kill()
    if shafty_temp == True:
        shafty_popen.kill()
    if slither_temp == True:
        slither_popen.kill()
    if graph_temp == True:
        graph_popen.kill()
    path_timer = os.getcwd() + "/Timer.xlsx"
    is_file = os.path.isfile(path_timer)
    if is_file == True:
        os.remove(path_timer)
    mixer.music.stop()
    island.protocol("WM_DELETE_WINDOW",root_destroy)
    now_logout = datetime.now()
    logout_time = now_logout.strftime("%d-%m-%Y %H:%M:%S")
    logout_ = logout_time.split()
    logout_time = logout_[1]
    logout_date = logout_[0]
    user_data_island  = {"Status":'Logged Out',"Time Left":f"{time_minute_var.get()}:{time_second_var.get()}"}
    t_island = repr(str(user_data_island))
    import json
    user_data_dict_island = json.loads(t_island)
    user_id = dash_profile_name.cget("text")
    database.child(user_id).child("Timings").child(logout_date).child("Game_Island").child(logout_time).set(user_data_dict_island)
    island.destroy()

def root_destroy():
    mixer.stop()
    island.destroy()

def timesup_frame():
    timesup_major.pack(fill="both",expand=1)
    app_drawer.forget()

def timesup_ok():
    timesup_major.forget()
    app_drawer.pack(fill="both",expand=1)


temp_timer = True
gtn_temp = False
ikeyflex_temp = False
lns_temp = False
flyby_temp = False
shafty_temp = False
graph_temp = False
slither_temp = False
timer_value = 0
count_minimize = 0

def timer():
    global count_minimize
    global timer_value
    global time_minute_var
    global time_second_var
    global gtn_temp 
    global ikeyflex_temp 
    global lns_temp 
    global flyby_temp 
    global shafty_temp 
    global slither_temp 
    global graph_temp 
    global gtn_popen
    global graph_popen
    global ikeyflex_popen
    global lns_popen
    global flyby_popen
    global shafty_popen
    global slither_popen
    global user_id
    global temp_timer
    temp_timer = True
    start = time.time()
    time_limit = timer_value
    while temp_timer == True:

        path_timer = os.getcwd() + "/Timer.xlsx"
        # #print(path_timer)
        is_file = os.path.isfile(path_timer)
        if is_file == True:
            island.state(newstate="iconic")
            b_guess.configure(command = temp)
            b_lns.configure(command = temp)
            b_shafty.configure(command = temp)
            b_ikeyflex.configure(command = temp)
            b_slither.configure(command = temp)
            b_flyby.configure(command = temp)
            graph_button.configure(command = temp)
        else:
            if count_minimize == 1:
                island.state(newstate="normal")
            count_minimize = 0
            mixer.music.set_volume(0.2)
            b_guess.configure(command=guess_the_number)
            b_lns.configure(command=LNS)
            b_shafty.configure(command=Shafty)
            b_ikeyflex.configure(command=IKeyFlex)
            b_slither.configure(command=Slither)
            b_flyby.configure(command=FlyBy)
            graph_button.configure(command = graphs_display)

        elapsed_time = time.time()-start
        time_left = time_limit - int(elapsed_time)
        time_left_minute = time_left//60
        time_left_second = time_left%60
        if time_left_minute < 10:
            time_minute_var.set(f"0{time_left_minute}")
        else:
            time_minute_var.set(f"{time_left_minute}")
        if time_left_second < 10:
            time_second_var.set(f"0{time_left_second}")
        else:
            time_second_var.set(f"{time_left_second}")

        if elapsed_time > time_limit:
            if gtn_temp == True:
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
                gtn_popen.kill()

            if ikeyflex_temp == True:
                now_logout = datetime.now()
                logout_time = now_logout.strftime("%d-%m-%Y %H:%M:%S")
                logout_ = logout_time.split()
                logout_time = logout_[1]
                logout_date = logout_[0]
                user_data_island  = {"Status":'End'}
                t_island = repr(str(user_data_island))
                import json
                user_data_dict_island = json.loads(t_island)
                database.child(user_id).child("Timings").child(logout_date).child("IKeyFlex").child(logout_time).set(user_data_dict_island)
                ikeyflex_popen.kill()

            if lns_temp == True:
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
                lns_popen.kill()

            if flyby_temp == True:
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
                flyby_popen.kill()

            if shafty_temp == True:
                now_logout = datetime.now()
                logout_time = now_logout.strftime("%d-%m-%Y %H:%M:%S")
                logout_ = logout_time.split()
                logout_time = logout_[1]
                logout_date = logout_[0]
                user_data_island  = {"Status":'End'}
                t_island = repr(str(user_data_island))
                import json
                user_data_dict_island = json.loads(t_island)
                database.child(user_id).child("Timings").child(logout_date).child("Shafty").child(logout_time).set(user_data_dict_island)
                shafty_popen.kill()

            if slither_temp == True:
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
                slither_popen.kill()

            temp_timer = False
            b_guess.configure(command=timesup_frame)
            b_lns.configure(command=timesup_frame)
            b_shafty.configure(command=timesup_frame)
            b_ikeyflex.configure(command=timesup_frame)
            b_slither.configure(command=timesup_frame)
            b_flyby.configure(command=timesup_frame)
            # timesup.pack(fill = "both",expand = 1)
            # app_drawer.forget()
            break

island = customtkinter.CTk()
island.geometry("800x600+480+150")
island.title("Game Island")
island.configure()
island.iconbitmap("game_island_icon_bg.ico")
island.resizable(False,False)
island.protocol("WM_DELETE_WINDOW",music)

def startPageFuncSign():
    starting_frame.forget()
    sign.pack(fill ="both",expand=1)

# start_screen starts
starting_frame = customtkinter.CTkFrame(master=island,fg_color="transparent")
starting_frame.pack(fill = "both",expand = 1)
raf = threading.Thread(target=startPageFuncSign)
# raf.start()
# starting_frame.forget()


start_image = tkinter.PhotoImage(file="Start_page.png")

my_canvas_start_page = tkinter.Canvas(master=starting_frame,width=800,height=600)
my_canvas_start_page.pack(fill="both",expand=1)
my_canvas_start_page.create_image(0,0,image=start_image,anchor = "nw")
b_letsgo = customtkinter.CTkButton(master=starting_frame,text="Let's Go...",font=("comic sans ms",25,"bold"),width=80,height=50,bg_color="#FFE1AB",fg_color="#867C1A",hover_color="#6B6315",corner_radius=10)
b_letsgo.place(relx=0.41,rely=0.9)
# start_screen ends


# sign up page starts

sign = customtkinter.CTkFrame(master=island,fg_color="transparent")
# sign.pack(fill = "both",expand = 1)


back_image = tkinter.PhotoImage(file="Add a heading.png")

my_canvas = tkinter.Canvas(master=sign,width=800,height=600)
my_canvas.pack(fill="both",expand=1)
my_canvas.create_image(0,0,image=back_image,anchor = "nw")

login_back = customtkinter.CTkFrame(master=sign,fg_color="white",corner_radius=8,bg_color="grey")
login_back.place(relx = 0.25,rely=0.15,width = 500,height = 500,bordermode = "outside")


# login_back.pack(padx=100,pady=200,ipady=200)

label_heading = customtkinter.CTkLabel(master = login_back,text="Welcome to Game Island",font=("Comic sans ms",32),text_color="#965B00")
label_heading.pack(pady = 20)

entry_name = customtkinter.CTkEntry(master=login_back,placeholder_text="Enter your Name",width=320,height=45,fg_color="#FEE9D5",placeholder_text_color="black",font=customtkinter.CTkFont(size=20),text_color="black")
entry_name.place(relx = 0.1,rely = 0.23)
star_name = customtkinter.CTkLabel(master=login_back,text="*",font=("cambria",20),fg_color="transparent",text_color="red")

entry_email = customtkinter.CTkEntry(master=login_back,font=customtkinter.CTkFont(size=20),placeholder_text="Enter your Email",width=320,height=45,fg_color="#FEE9D5",placeholder_text_color="black",text_color="black")
entry_email.place(relx = 0.1,rely = 0.42)
star_email = customtkinter.CTkLabel(master=login_back,text="*",font=("cambria",20),fg_color="transparent",text_color="red")

already_image = customtkinter.CTkImage(dark_image=Image.open("cross-removebg-preview.png"),size=(13,13))
already_image_label = customtkinter.CTkLabel(master=login_back,text="",image=already_image)
# already_image_label.place(rely=0.54,relx=0.11)

already_email = customtkinter.CTkLabel(master=login_back,text="This account already exists",text_color="red",font=("helevicta",12,"bold"))
# already_email.place(relx=0.15,rely=0.54)

entry_otp = customtkinter.CTkEntry(master=login_back,font=customtkinter.CTkFont(size=20),placeholder_text="Enter OTP",width=320,height=45,fg_color="#FEE9D5",placeholder_text_color="black",text_color="black")
entry_otp.place(relx = 0.1,rely = 0.61)

b_otp = customtkinter.CTkButton(master=login_back,text="Get OTP",fg_color="#854B4A",hover_color="#734140",width=150,height=40,font=customtkinter.CTkFont(size=18),command=get_otp)
b_otp.place(rely = 0.79,relx=0.1)

b_submit = customtkinter.CTkButton(master=login_back,text="Submit",fg_color="#854B4A",hover_color="#734140",width=150,height=40,font=customtkinter.CTkFont(size=18),command=gmail)
b_submit.place(rely = 0.79,relx=0.52)

have_account = customtkinter.CTkLabel(master=login_back,text="Already have an account?",text_color="black",font=("Cambria",20,"bold"))
have_account.place(rely=0.91,relx=0.2)
have_account.bind('<Enter>',command=hypertext)
have_account.bind('<Leave>',command=hypertext_disappear)
have_account.bind('<Button-1>',command=up_to_in)

# sign up page ends

# sign in page starts
login_frame = customtkinter.CTkFrame(master=island)
# login_frame.pack(fill = "both",expand = 1)


login_back_image = tkinter.PhotoImage(file="password_page.png")

my_canvas_3 = tkinter.Canvas(master=login_frame,width=800,height=600)
my_canvas_3.pack(fill="both",expand=1)
my_canvas_3.create_image(0,0,image=login_back_image,anchor = "nw")

login_back_2 = customtkinter.CTkFrame(master=login_frame,fg_color="white",corner_radius=8,bg_color="grey")
login_back_2.place(relx = 0.25,rely=0.27,width = 500,height = 350,bordermode = "outside")

label_heading_login = customtkinter.CTkLabel(master = login_back_2,text="Sign in",font=("Cambria",35,"bold"),text_color="#965B00")
label_heading_login.place(relx=0.36,rely=0)

entry_login_email = customtkinter.CTkEntry(master=login_back_2,font=customtkinter.CTkFont(size=20),placeholder_text="Enter your email",width=320,height=45,fg_color="#FEE9D5",placeholder_text_color="black",text_color="black")
entry_login_email.place(relx = 0.1,rely = 0.2)

entry_password_login = customtkinter.CTkEntry(master=login_back_2,show="*",font=customtkinter.CTkFont(size=20),placeholder_text="Enter your password",width=320,height=45,fg_color="#FEE9D5",placeholder_text_color="black",text_color="black")
entry_password_login.place(relx = 0.1,rely = 0.43)

label_pass_match_login = customtkinter.CTkLabel(master=login_back_2,text="Password doesn't match",text_color="red",font=("helevicta",13,"bold"))
# label_pass_match_login.place(relx = 0.14,rely=0.62)

my_image_login = customtkinter.CTkImage(dark_image=Image.open("cross-removebg-preview.png"),size=(13, 13))
image_login = customtkinter.CTkLabel(master=login_back_2,text="",image=my_image_login)
# image_login.place(relx=0.1,rely=0.62)

forgot_password = customtkinter.CTkLabel(master= login_back_2,text="Forgot Password?",font=("Cambria",15,"bold"),text_color="black")
# forgot_password.place(relx=0.58,rely=0.6)
forgot_password.bind('<Enter>',command=hypertext_login)
forgot_password.bind('<Leave>',command=disappear_hypertext_login)
forgot_password.bind('<Button-1>',command=in_to_forgot)

remember_check_login = customtkinter.CTkCheckBox(master=login_back_2,text="Remember me",checkbox_height=20,checkbox_width=20,text_color="black",font=("cambria",17),hover_color="#854B4A")
remember_check_login.place(rely=0.9,relx=0.32)

b_done_login = customtkinter.CTkButton(master=login_back_2,text="Done",fg_color="#854B4A",hover_color="#734140",width=150,height=40,font=customtkinter.CTkFont(size=18),command=login)
b_done_login.place(rely = 0.74,relx=0.52)

b_back_login = customtkinter.CTkButton(master=login_back_2,text="Back",fg_color="#854B4A",hover_color="#734140",width=150,height=40,font=customtkinter.CTkFont(size=18),command=in_to_up)
b_back_login.place(rely = 0.74,relx=0.1)


    # forgot password frame starts
forgot_frame = customtkinter.CTkFrame(master=login_frame,fg_color="white",corner_radius=8,bg_color="grey")
# forgot_frame.place(relx = 0.25,rely=0.27,width = 500,height = 350,bordermode = "outside")

heading_forgot_password = customtkinter.CTkLabel(master = forgot_frame,text="Forgot Password",font=("Cambria",30,"bold"),text_color="#965B00")
heading_forgot_password.place(relx=0.2,rely=0.02)

forgot_email = tkinter.StringVar()
forgot_email.set("")

entry_forgot_pass_email = customtkinter.CTkEntry(master=forgot_frame,textvariable=forgot_email,state="disabled",font=customtkinter.CTkFont(size=20),placeholder_text="Enter your email",width=320,height=45,fg_color="#FEE9D5",placeholder_text_color="black",text_color="black")
entry_forgot_pass_email.place(relx = 0.1,rely = 0.2)

entry_forgot_pass_otp = customtkinter.CTkEntry(master=forgot_frame,show="*",font=customtkinter.CTkFont(size=20),placeholder_text="Enter OTP",width=320,height=45,fg_color="#FEE9D5",placeholder_text_color="black",text_color="black")
entry_forgot_pass_otp.place(relx = 0.1,rely = 0.46)

my_image_forgot = customtkinter.CTkImage(dark_image=Image.open("cross-removebg-preview.png"),size=(13, 13))
image_match_otp_forgot = customtkinter.CTkLabel(master=forgot_frame,text="",image=my_image_forgot)
# image_match_otp_forgot.place(rely=0.62,relx=0.1)
label_match_otp_forgot = customtkinter.CTkLabel(master=forgot_frame,text="OTP doesn't match",text_color="red",font=("Cambria",14,"bold"))
# label_match_otp_forgot.place(relx = 0.11,rely=0.62)

b_done_forgot_pass = customtkinter.CTkButton(master=forgot_frame,text="Done",fg_color="#854B4A",hover_color="#734140",width=150,height=40,font=customtkinter.CTkFont(size=18),command=forgot_otp_verify)
b_done_forgot_pass.place(rely = 0.74,relx=0.52)

b_getotp_forgot_pass = customtkinter.CTkButton(master=forgot_frame,text="Get OTP",fg_color="#854B4A",hover_color="#734140",width=150,height=40,font=customtkinter.CTkFont(size=18),command=forgot_get_otp)
b_getotp_forgot_pass.place(rely = 0.74,relx=0.1)

b_back_image = customtkinter.CTkImage(dark_image=Image.open("back_to_login.png"),size=(25,15))
b_back_forgot_pass = customtkinter.CTkButton(master=forgot_frame,image=b_back_image,width=25,fg_color="transparent",text="",hover_color="#734140",command=forgot_to_in)
b_back_forgot_pass.place(relx = 0.01,rely=0.02)
    # forgot password frame ends

    # create password frame starts
new_pass_frame = customtkinter.CTkFrame(master=login_frame,fg_color="white",corner_radius=8,bg_color="grey")
# new_pass_frame.place(relx = 0.25,rely=0.27,width = 500,height = 350,bordermode = "outside")

heading_new_password = customtkinter.CTkLabel(master = new_pass_frame,text="Create New Password",font=("Cambria",25,"bold"),text_color="#965B00")
heading_new_password.place(relx=0.2,rely=0.02)


new_password = customtkinter.CTkEntry(master=new_pass_frame,show="*",font=customtkinter.CTkFont(size=20),placeholder_text="Create your password",width=320,height=45,fg_color="#FEE9D5",placeholder_text_color="black",text_color="black")
new_password.place(relx = 0.1,rely = 0.15)
new_password.bind('<Enter>',command=show_criteria)
new_password.bind('<Leave>',command=disappear_criteria)

new_password_confirm = customtkinter.CTkEntry(master=new_pass_frame,show="*",font=customtkinter.CTkFont(size=20),placeholder_text="Confirm your password",width=320,height=45,fg_color="#FEE9D5",placeholder_text_color="black",text_color="black")
new_password_confirm.place(relx = 0.1,rely = 0.43)

remember_check_forgot = customtkinter.CTkCheckBox(master=new_pass_frame,text="Remember me",checkbox_height=20,checkbox_width=20,text_color="black",font=("cambria",17),hover_color="#854B4A",command=remember_forgot)
remember_check_forgot.place(rely=0.72,relx=0.1)

    # create password frame ends


# sign in page ends


# verification frames starts
verification_frame = customtkinter.CTkFrame(master=island,fg_color="transparent")

back_image_1 = tkinter.PhotoImage(file="Login_Page.png")

my_canvas_1 = tkinter.Canvas(master=verification_frame,width=800,height=600)
my_canvas_1.pack(fill="both",expand=1)
my_canvas_1.create_image(0,0,image=back_image_1,anchor = "nw")


page_3 = customtkinter.CTkFrame(master=my_canvas_1,width=300,border_width=5,fg_color="#DBDBDB")
my_image2 = customtkinter.CTkImage(dark_image=Image.open("tick-removebg-preview.png"),size=(40, 40))
label_image2 = customtkinter.CTkLabel(master=page_3,text="",image=my_image2)
label_image2.pack()
label_image2.place(rely = 0.09,relx=0.43)
# page_3.pack(pady =200)

label_message2 = customtkinter.CTkLabel(master= page_3,text="Your email has been verified.",font=customtkinter.CTkFont("lucida",size=17,weight="bold"),text_color="black")
label_message2.pack()
label_message2.place(rely=0.4,relx=0.1)

b_ok = customtkinter.CTkButton(master=page_3,hover_color="#146944",fg_color="#30A572",text="Ok",font=customtkinter.CTkFont(family="lucida",size=20,weight="bold"),height=40,corner_radius=15,command=ok)
b_ok.pack()
b_ok.place(anchor=tkinter.CENTER,relx=0.5,rely=0.84)

page_4 = customtkinter.CTkFrame(master=my_canvas_1,width=300,border_width=5,fg_color="#DBDBDB")
my_image3 = customtkinter.CTkImage(dark_image=Image.open("cross-removebg-preview.png"),size=(40, 40))
label_image3 = customtkinter.CTkLabel(master=page_4,text="",image=my_image3)
label_image3.pack()
label_image3.place(rely = 0.09,relx=0.43)

label_message3 = customtkinter.CTkLabel(master= page_4,text="Invalid Otp!",font=customtkinter.CTkFont("lucida",size=20,weight="bold"),text_color="black")
label_message3.pack()
label_message3.place(rely=0.4,relx=0.32)

b_try = customtkinter.CTkButton(master=page_4,hover_color="dark red",fg_color="red",text="Try again!",font=customtkinter.CTkFont(family="lucida",size=20,weight="bold"),height=40,corner_radius=15,command=try_again)
b_try.pack()
b_try.place(anchor=tkinter.CENTER,relx=0.5,rely=0.78)

# verification frames ends

# Password frames starts

password_frame = customtkinter.CTkFrame(master=island)
# password_frame.pack(fill="both",expand=1)

back_image_2 = tkinter.PhotoImage(file="password_page.png")

my_canvas_2 = tkinter.Canvas(master=password_frame,width=800,height=600)
my_canvas_2.pack(fill="both",expand=1)
my_canvas_2.create_image(0,0,image=back_image_2,anchor = "nw")

login_back_1 = customtkinter.CTkFrame(master=password_frame,fg_color="white",corner_radius=8,bg_color="grey")
login_back_1.place(relx = 0.25,rely=0.3,width = 500,height = 300,bordermode = "outside")

entry_password = customtkinter.CTkEntry(master=login_back_1,show="*",font=customtkinter.CTkFont(size=20),placeholder_text="Create your password",width=320,height=45,fg_color="#FEE9D5",placeholder_text_color="black",text_color="black")
entry_password.place(relx = 0.1,rely = 0.15)
entry_password.bind('<Enter>',command=show_criteria)
entry_password.bind('<Leave>',command=disappear_criteria)

entry_password_confirm = customtkinter.CTkEntry(master=login_back_1,show="*",font=customtkinter.CTkFont(size=20),placeholder_text="Confirm your password",width=320,height=45,fg_color="#FEE9D5",placeholder_text_color="black",text_color="black")
entry_password_confirm.place(relx = 0.1,rely = 0.43)

label_pass_match = customtkinter.CTkLabel(master=login_back_1,text="Password doesn't match",text_color="red",font=("helevicta",13,"bold"))

criteria_image = customtkinter.CTkImage(dark_image=Image.open("Password_must_be_8_characters.png"),size=(150,130))
criteria_label = customtkinter.CTkLabel(master=password_frame,text="",image=criteria_image,fg_color="white")


remember_check = customtkinter.CTkCheckBox(master=login_back_1,text="Remember me",checkbox_height=20,checkbox_width=20,text_color="black",font=("cambria",17),hover_color="#854B4A",command=remember)
remember_check.place(rely=0.72,relx=0.1)

b_done = customtkinter.CTkButton(master=login_back_1,text="Done",fg_color="#854B4A",hover_color="#734140",width=150,height=40,font=customtkinter.CTkFont(size=18),command=app)
b_done.place(rely = 0.72,relx=0.525)

# Password frames ends

# App drawer starts
app_drawer = customtkinter.CTkFrame(master=island)
# app_drawer.pack(fill="both",expand=1)

app_canvas = tkinter.Canvas(master=app_drawer,width=800,height=600)
app_canvas.pack(fill="both",expand=1)

app_back = tkinter.PhotoImage(file="app_drawer_back.png")
# app_back = tkinter.PhotoImage(file="app_back_new.png")
app_canvas.create_image(0,0,image=app_back,anchor = "nw")



# app_back = TkinterVideo(master=app_canvas,scaled=True)
# app_back.load("app_drawer_background - Made with Clipchamp.mp4")
# app_back.pack(fill="both",expand=1)
# app_back.play()

app_heading = customtkinter.CTkLabel(master=app_drawer,text="Game Island",text_color="#965B00",corner_radius=10,fg_color="white",font=("comic sans ms",40,"bold"))
app_heading.place(relx = 0.34,rely=0.03)

graph_image = customtkinter.CTkImage(dark_image=Image.open("graph.png"),size = (40,40))
graph_button = customtkinter.CTkButton(master=app_drawer,text="",image=graph_image,fg_color="white",hover_color="grey",width=1,height=30,command=graphs_display)
graph_button.place(relx = 0.7,rely = 0.036)

profile_image = customtkinter.CTkImage(dark_image=Image.open("profile_image.png"),size = (40,40))
profile_button = customtkinter.CTkButton(master=app_drawer,text="",image=profile_image,fg_color="white",hover_color="grey",width=1,height=30,command=app_to_dash)
profile_button.place(relx = 0.8,rely = 0.036)

menu_image = customtkinter.CTkImage(dark_image=Image.open("menu_image.png"),size = (40,40))
menu_button = customtkinter.CTkButton(master=app_drawer,text="",image=menu_image,fg_color="white",hover_color="grey",width=1,height=30,command = submenu)
menu_button.place(relx = 0.9,rely = 0.036)

    # Shafty starts
shafty_image = customtkinter.CTkImage(dark_image=Image.open("Shafty.png"),size=(165,165))
b_shafty = customtkinter.CTkButton(master=app_drawer,text="",image= shafty_image,fg_color="#5E3D34",hover_color="grey",command=Shafty,corner_radius=10)
b_shafty.place(relx=0.085,rely=0.22)
    # Shafty ends

    # IKeyFlex starts
ikeyflex_image = customtkinter.CTkImage(dark_image=Image.open("eye_key.png"),size=(165,165))
b_ikeyflex = customtkinter.CTkButton(master=app_drawer,text="",image= ikeyflex_image,fg_color="#5E3D34",hover_color="grey",command=IKeyFlex,corner_radius=10)
b_ikeyflex.place(relx=0.385,rely=0.22)
    # IKeyFlex ends

    # Guess the number starts
guess_image = customtkinter.CTkImage(dark_image=Image.open("GTN_nobg.png"),size=(165,165))
b_guess = customtkinter.CTkButton(master=app_drawer,text="",image= guess_image,fg_color="#5E3D34",hover_color="grey",command=guess_the_number,corner_radius=10)
b_guess.place(relx=0.685,rely=0.22)
    # Guess the number ends


submenu_dash = customtkinter.CTkFrame(master=app_drawer,fg_color="white",corner_radius=10,width=150,height=120)
# submenu_dash.place(relx=0.788,rely=0.12)

def sound():
    sound_text = soundOnOff.cget("text")
    if sound_text == "Sound OFF":
        soundOnOff.configure(text="Sound ON")
        mixer.music.pause()
    elif sound_text == "Sound ON":
        soundOnOff.configure(text="Sound OFF")
        mixer.music.unpause()

soundOnOff = customtkinter.CTkButton(master=submenu_dash,text="Sound OFF",fg_color="transparent",hover_color="grey",text_color="black",font=("calibri",25,"bold"),command=sound) 
soundOnOff.place(relx=0.034,rely=0.05)

def sign_out():
    global temp_timer
    global gtn_temp 
    global ikeyflex_temp 
    global lns_temp 
    global flyby_temp 
    global shafty_temp 
    global slither_temp 
    global graph_temp
    global graph_popen
    global gtn_popen
    global ikeyflex_popen
    global lns_popen
    global flyby_popen
    global shafty_popen
    global slither_popen
    if gtn_temp == True:
        gtn_popen.kill()
    if ikeyflex_temp == True:
        ikeyflex_popen.kill()
    if lns_temp == True:
        lns_popen.kill()
    if flyby_temp == True:
        flyby_popen.kill()
    if shafty_temp == True:
        shafty_popen.kill()
    if slither_temp == True:
        slither_popen.kill()
    if graph_temp == True:
        graph_popen.kill()
    path_timer = os.getcwd() + "/Timer.xlsx"
    is_file = os.path.isfile(path_timer)
    if is_file == True:
        os.remove(path_timer)
    temp_timer = False
    df = pd.read_excel("User_Id.xlsx",sheet_name="User_Email_Id")
    user_id = df["email_id"][0]
    symbols=['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>' , '(', ')', '<',"!","^","&","_","-","+","=","[","]","{","}","'",'"']
    for i in user_id:
        if i in symbols:
            user_id = user_id.replace(i,"")
            user_id = user_id.replace("gmailcom","")
    database.child(user_id).child("Remembered").remove()
    island.protocol("WM_DELETE_WINDOW",root_destroy)
    now_logout = datetime.now()
    logout_time = now_logout.strftime("%d-%m-%Y %H:%M:%S")
    logout_ = logout_time.split()
    logout_time = logout_[1]
    logout_date = logout_[0]
    user_data_island  = {"Status":'Logged Out',"Time Left":f"{time_minute_var.get()}:{time_second_var.get()}"}
    t_island = repr(str(user_data_island))
    import json
    user_data_dict_island = json.loads(t_island)
    database.child(user_id).child("Timings").child(logout_date).child("Game_Island").child(logout_time).set(user_data_dict_island)
    b_otp.focus_set()
    star_email.place_forget()
    star_name.place_forget()
    already_email.place_forget()
    already_image_label.place_forget()
    entry_email.delete(0,len(entry_email.get()))
    entry_name.delete(0,len(entry_name.get()))
    entry_otp.delete(0,len(entry_otp.get()))
    entry_password.delete(0,len(entry_password.get()))
    entry_password_confirm.delete(0,len(entry_password_confirm.get()))
    entry_login_email.delete(0,len(entry_login_email.get()))
    entry_password_login.delete(0,len(entry_password_login.get()))
    entry_forgot_pass_otp.delete(0,len(entry_forgot_pass_otp.get()))
    new_password.delete(0,len(new_password.get()))
    new_password_confirm.delete(0,len(new_password_confirm.get()))
    app_drawer.forget()
    b_otp.configure(command=get_otp)
    sign.pack(fill="both",expand=1)


sign_out_sub = customtkinter.CTkButton(master=submenu_dash,text="Sign out",fg_color="transparent",hover_color="grey",text_color="black",font=("calibri",25,"bold"),command=sign_out) 
sign_out_sub.place(relx=0.034,rely=0.35)


def feed():
    feedback_frame.pack(fill="both",expand=1)
    app_canvas.forget()

feedback_sub = customtkinter.CTkButton(master=submenu_dash,text="Feedback",fg_color="transparent",hover_color="grey",text_color="black",font=("calibri",25,"bold"),command=feed) 
feedback_sub.place(relx=0.032,rely=0.65)



    # slither starts
slither_image = customtkinter.CTkImage(dark_image=Image.open("Slither_nobg.png"),size=(165,165))
b_slither = customtkinter.CTkButton(master=app_drawer,text="",image= slither_image,fg_color="#5E3D34",hover_color="grey",command=Slither,corner_radius=10)
b_slither.place(relx=0.085,rely=0.62)
    # slither ends

    # flyby starts
flyby_image = customtkinter.CTkImage(dark_image=Image.open("FlyBy.png"),size=(168,168))
b_flyby = customtkinter.CTkButton(master=app_drawer,text="",image= flyby_image,fg_color="#5E3D34",hover_color="grey",command=FlyBy,corner_radius=10)
b_flyby.place(relx=0.385,rely=0.62)
    # flyby ends

    # lns starts
lns_image = customtkinter.CTkImage(dark_image=Image.open("lns.png"),size=(165,165))
b_lns = customtkinter.CTkButton(master=app_drawer,text="",image= lns_image,fg_color="#5E3D34",hover_color="grey",command=LNS,corner_radius=10)
b_lns.place(relx=0.685,rely=0.62)
    # lns ends

# App drawer ends

#dashboard frame starts

dashboard_frame = customtkinter.CTkFrame(master= app_drawer,fg_color="transparent",bg_color="transparent")
# dashboard_frame.pack(fill = "both",expand = 1)

dash_back = tkinter.PhotoImage(file="dash_board_back.png")

dash_canvas = tkinter.Canvas(master=dashboard_frame,width=900,height=600,border=0)
dash_canvas.pack(fill="both",expand=1)
dash_canvas.create_image(0,0,image=dash_back,anchor = "nw")

dash_profile_image = customtkinter.CTkImage(dark_image= Image.open("profile_image.png"),size =(80,80))
dash_profile_label = customtkinter.CTkLabel(master=dashboard_frame,text="",fg_color="#915E50",height=90,corner_radius=8,image=dash_profile_image)
dash_profile_label.place(relx = 0.1,rely=0.02)

dash_profile_name = customtkinter.CTkLabel(master=dashboard_frame,fg_color="white",text_color="#965B00",corner_radius=8,text='gearwar8340',font=('cambria',30,"bold"),height=55)
dash_profile_name.place(relx = 0.225,rely = 0.055)

no_data = customtkinter.CTkFrame(master=dashboard_frame,width=670,height=200,corner_radius=10,bg_color="transparent",fg_color="#915E50")

no_data_label = customtkinter.CTkLabel(master=no_data,text="No Data!",font=("cambria",40,"bold"),fg_color="transparent")
no_data_label.place(relx=0.38,rely=0.35)

join_date = '01-02-2023'
join_time = '01:23:40'
joined_date_label = customtkinter.CTkLabel(master=dashboard_frame,text=f'Joined at:\n{join_date}\n{join_time}',width=35,font=('cambria',23,"bold"),fg_color="#5E5E5E",corner_radius=10)
joined_date_label.place(relx = 0.8,rely = 0.02)


# timesup frame starts 
timesup_major = customtkinter.CTkFrame(master=island)
# timesup_major.pack(fill="both",expand = 1)

timesup_back = tkinter.PhotoImage(file="dash_board_back.png")

timesup_canvas = tkinter.Canvas(master=timesup_major,width=900,height=600,border=0)
timesup_canvas.pack(fill="both",expand=1)
timesup_canvas.create_image(0,0,image=timesup_back,anchor = "nw")

timesup = customtkinter.CTkFrame(master=timesup_major,fg_color="#F6F6F6",width=250,height=200,border_width=3)
timesup.place(relx=0.34,rely=0.33)

timer_image = customtkinter.CTkImage(dark_image=Image.open("sand_clock.png"),size=(85,65))
timer_image_label = customtkinter.CTkLabel(master=timesup,image=timer_image,text="")
timer_image_label.place(relx=0.33,rely=0.05)

timer_label_1 = customtkinter.CTkLabel(master=timesup,text="Time limit exceeded",text_color="black",font=("cambria",20,"bold"))
timer_label_1.place(relx=0.127,rely=0.42)

timer_label_2 = customtkinter.CTkLabel(master=timesup,text="Play tomorrow",text_color="black",font=("cambria",20,"bold"))
timer_label_2.place(relx=0.22,rely=0.55)

b_ok_timesup = customtkinter.CTkButton(master=timesup,text="Ok",width=110,height=35,font=('comic sans ms',20,'bold'),fg_color="#EA1B23",hover_color="dark red",command=timesup_ok)
b_ok_timesup.place(relx=0.28,rely=0.75)
# timesup.pack(fill = "both",expand = 1)

# timesup frame ends 

time_minute_var = tkinter.StringVar()
time_minute_var.set('00')
time_second_var = tkinter.StringVar()
time_second_var.set('00')

#Remember me starts

def startPageFuncRem():
    starting_frame.forget()
    app_drawer.pack(fill ="both",expand=1)
    

df = pd.read_excel("User_Id.xlsx",sheet_name="User_Email_Id")
check_nan = df["email_id"][0]
#print(check_nan,"check")
if check_nan == 'empty':
    b_letsgo.configure(command = startPageFuncSign)
    mixer.music.set_volume(0.2)
    #print("pass")
    pass
else:
    user_id = df["email_id"][0]
    symbols=['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>' , '(', ')', '<',"!","^","&","_","-","+","=","[","]","{","}","'",'"']
    for i in user_id:
        if i in symbols:
            user_id = user_id.replace(i,"")
            user_id = user_id.replace("gmailcom","")
    let = database.child(user_id).get().val()
    let_list = list(let)
    if "Remembered" not in let_list:
        b_letsgo.configure(command = startPageFuncSign)
    else:
        b_letsgo.configure(command = startPageFuncRem)
        
        
    dash_profile_name.configure(text=user_id)
    user_info = database.child(user_id).get()
    list_time = []
    # #print(user_info.val())
    if user_info.val() == None:
        pass
    else:
        for z in user_info:
            for x,y in z.val().items():
                if z.key() == "Remembered":
                    now_login = datetime.now()
                    login_time = now_login.strftime("%d-%m-%Y %H:%M:%S")
                    login_ = login_time.split()
                    login_time = login_[1]
                    login_date = login_[0]
                    #print(login_date)
                    island.protocol("WM_DELETE_WINDOW",win_logout)
                    user_info = database.child(user_id).get()
                    for a in user_info:
                        # #print("key:",a.key(),"value",a.val())
                        for b,c in a.val().items():
                            if a.key() == "Timings":
                                ze = database.child(user_id).child(a.key()).get()
                                # #print(z.val())
                                for x in ze:
                                        # #print(x.val(),"x.val()")
                                    for d,e in x.val().items():
                                        if x.key() == login_date:
                                            ye = database.child(user_id).child(a.key()).child(login_date).get()
                                            for h in ye:
                                                for m,n in h.val().items():
                                                    if h.key() == "Game_Island":
                                                        list_time.append(n)

                    #print(list_time,"remember_me")
                    if len(list_time) > 0:
                        list_time = list_time[::-1]
                        time_limit_str = list_time[0]
                        #print(time_limit_str)
                        time_limit_dict = ast.literal_eval(time_limit_str)
                        time_limit = time_limit_dict['Time Left']
                        time_limit = time_limit.split(":")
                        #print(time_limit)
                        time_limit_minute = int(time_limit[0])
                        time_limit_second = int(time_limit[1])
                        timer_value = (time_limit_minute*60) + time_limit_second
                    else:
                        timer_value = 3600
                    # timesup_major.pack(fill="both",expand=1)
                    timer_value_login_minute = timer_value // 60
                    timer_value_login_second = timer_value % 60
                    if timer_value_login_minute < 10:
                        timer_value_login_minute = '0'+str(timer_value_login_minute)
                    if timer_value_login_second < 10:
                        timer_value_login_second = '0'+str(timer_value_login_second)
                    timer_value_login_minute = str(timer_value_login_minute)
                    timer_value_login_second = str(timer_value_login_second)
                    user_data_island  = {"Status":'Logged In',"Time Left":f"{timer_value_login_minute}:{timer_value_login_second}"}
                    t_island = repr(str(user_data_island))
                    import json
                    user_data_dict_island = json.loads(t_island)
                    database.child(user_id).child("Timings").child(login_date).child("Game_Island").child(login_time).set(user_data_dict_island)
                    # app_drawer.pack(fill="both",expand=1)
                    # raf2 = threading.Thread(target=startPageFuncRem)
                    # raf2.start()
                    timer_app = threading.Thread(target=timer)
                    timer_app.start()
                    sign.forget()
                # mixer.music.set_volume(0.2)
                if z.key() == "User_Id_Info" :
                    j = x.split()
                    join_date = j[0]
                    join_time = j[1]
                    joined_date_label.configure(text=f'Joined at:\n{join_date}\n{join_time}')
#Remember me ends


def dash_to_app():
    dashboard_frame.forget()
    app_canvas.pack(fill="both",expand=1)

b_back_dash_image = customtkinter.CTkImage(dark_image=Image.open("back_to_app.png"))
b_back_dash = customtkinter.CTkButton(master=dashboard_frame,text="",image=b_back_dash_image,hover_color="grey",width=7,fg_color="white",command=dash_to_app)
b_back_dash.place(relx=0.01,rely=0.02)

statistics_label = customtkinter.CTkLabel(master=dashboard_frame,text="Statistics",fg_color="white",text_color="black",corner_radius=8,font=("Cambria",30,"bold"))
# statistics_label.place(relx = 0.21,rely=0.24)

dash_games_frame = customtkinter.CTkFrame(master=dashboard_frame,width=475,height=320,corner_radius=10,fg_color="#915E50",bg_color="transparent")
dash_games_frame.place(relx=0.2,rely=0.37)

# time_minute_var = tkinter.StringVar()
# time_minute_var.set('00')
# time_second_var = tkinter.StringVar()
# time_second_var.set('00')

time_left_label = customtkinter.CTkLabel(master=dashboard_frame,text="Time Left:",text_color="black",corner_radius=10,fg_color="white",font=("cambria",30,"bold"))
time_left_label.place(relx=0.305,rely=0.3)

time_minute_label = customtkinter.CTkLabel(master=dashboard_frame,width=30,textvariable=time_minute_var,text_color="white",corner_radius=10,fg_color="#915E50",font=("cambria",30,"bold"))
time_minute_label.place(relx=0.515,rely=0.3)

time_colon_label = customtkinter.CTkLabel(master=dashboard_frame,text=":",text_color="white",corner_radius=10,fg_color="#5E3D34",font=("cambria",30,"bold"))
time_colon_label.place(relx=0.585,rely=0.3)

time_second_label = customtkinter.CTkLabel(master=dashboard_frame,textvariable=time_second_var,text_color="white",corner_radius=10,fg_color="#915E50",font=("cambria",30,"bold"))
time_second_label.place(relx=0.62,rely=0.3)

stat_dash_game = customtkinter.CTkLabel(master=dash_games_frame,text="Statistics",font=("Cambria",45,"bold"))
stat_dash_game.place(relx=0.31,rely=0.03)

b_cross_image = customtkinter.CTkImage(dark_image=Image.open("cross_stats.png"))
b_cross = customtkinter.CTkButton(master=dashboard_frame,width=10,hover_color="#FF665E",fg_color="#5E3D34",image=b_cross_image,text="",command=back_to_dash_games)
# b_cross.place(relx = 0.8,rely=0.24)

flyby_dash_image = customtkinter.CTkImage(dark_image= Image.open("FlyBy.png"),size=(70,70))
flyby_dash = customtkinter.CTkButton(master=dash_games_frame,hover_color="grey",text="FlyBy    ",width=185,height=85,font=("Comic sans ms",30,"bold"),fg_color="#5E3D34",image=flyby_dash_image,command=flyby_stats)
flyby_dash.place(relx = 0.02,rely=0.25)

ikeyflex_dash_image = customtkinter.CTkImage(dark_image= Image.open("eye_key.png"),size=(70,70))
ikeyflex_dash = customtkinter.CTkButton(master=dash_games_frame,hover_color="grey",text="IKeyFlex",width=185,height=85,font=("Comic sans ms",30,"bold"),fg_color="#5E3D34",image=ikeyflex_dash_image,command=ikeyflex_stats)
ikeyflex_dash.place(relx = 0.51,rely=0.25)

guess_the_number_dash_image = customtkinter.CTkImage(dark_image= Image.open("GTN_nobg.png"),size=(70,70))
guess_the_number_dash = customtkinter.CTkButton(master=dash_games_frame,hover_color="grey",text="GTN     ",width=185,height=85,font=("Comic sans ms",30,"bold"),fg_color="#5E3D34",image=guess_the_number_dash_image,command=gtn_stats)
guess_the_number_dash.place(relx = 0.02,rely=0.6)

slither_dash_image = customtkinter.CTkImage(dark_image= Image.open("Slither_nobg.png"),size=(70,70))
slither_dash = customtkinter.CTkButton(master=dash_games_frame,hover_color="grey",text="Slither  ",width=225,height=85,font=("Comic sans ms",30,"bold"),fg_color="#5E3D34",image=slither_dash_image,command=slither_stats)
slither_dash.place(relx = 0.51,rely=0.6)

    # User stats per game starts
stats_gtn = customtkinter.CTkFrame(master=dashboard_frame,width=475,height=800,corner_radius=10,bg_color="transparent",fg_color="#915E50")
    # stats_gtn.place(relx=0.2,rely=0.3)


playedat_label_gtn = customtkinter.CTkLabel(master=stats_gtn,text="Played at",font=("cambria",21))
playedat_label_gtn.grid(row=0,column=0)

attempts_label_gtn = customtkinter.CTkLabel(master=stats_gtn,text="No. of attempts",font=("cambria",21))
attempts_label_gtn.grid(row=0,column=1)

time_label_gtn = customtkinter.CTkLabel(master=stats_gtn,text="Time taken",font=("cambria",21))
time_label_gtn.grid(row=0,column=2)

difficulty_label_gtn = customtkinter.CTkLabel(master=stats_gtn,text="Difficulty Level",font=("cambria",20))
difficulty_label_gtn.grid(row=0,column=3)


stats_ikeyflex = customtkinter.CTkFrame(master=dashboard_frame,width=475,height=800,corner_radius=10,bg_color="transparent",fg_color="#915E50")

playedat_label_ik = customtkinter.CTkLabel(master=stats_ikeyflex,text="Played at",font=("cambria",21))
playedat_label_ik.grid(row=0,column=0)

difficulty_label_ik = customtkinter.CTkLabel(master=stats_ikeyflex,text="Difficulty Level",font=("cambria",21))
difficulty_label_ik.grid(row=0,column=1)

wrong_key_ik = customtkinter.CTkLabel(master=stats_ikeyflex,text="Wrong Keys",font=("cambria",21))
wrong_key_ik.grid(row=0,column=2)

score_label_ik = customtkinter.CTkLabel(master=stats_ikeyflex,text="Score",font=("cambria",20))
score_label_ik.grid(row=0,column=3)


stats_flyby = customtkinter.CTkFrame(master=dashboard_frame,width=475,height=800,corner_radius=10,bg_color="transparent",fg_color="#915E50")

playedat_label_ik = customtkinter.CTkLabel(master=stats_flyby,text="Played at",font=("cambria",21))
playedat_label_ik.grid(row=0,column=0)

score_label_ik = customtkinter.CTkLabel(master=stats_flyby,text="Score",font=("cambria",20))
score_label_ik.grid(row=0,column=1)


stats_slither = customtkinter.CTkFrame(master=dashboard_frame,width=475,height=800,corner_radius=10,bg_color="transparent",fg_color="#915E50")

playedat_label_ik = customtkinter.CTkLabel(master=stats_slither,text="Played at",font=("cambria",21))
playedat_label_ik.grid(row=0,column=0)

score_label_ik = customtkinter.CTkLabel(master=stats_slither,text="Score",font=("cambria",20))
score_label_ik.grid(row=0,column=1)
    #User stats per game ends

#dashboard frame ends

feedback_frame = customtkinter.CTkFrame(master=app_drawer)

feedback_back_image = tkinter.PhotoImage(file="feedback_back.png")

feedback_canvas = tkinter.Canvas(master=feedback_frame,width=800,height=500)
feedback_canvas.pack(fill="both",expand=1)
feedback_canvas.create_image(0,0,image=feedback_back_image,anchor = "nw")

feedback_label = customtkinter.CTkLabel(master=feedback_frame,text="Feedback",corner_radius=10,fg_color="#EBEBEB",bg_color="transparent",text_color="#965B00",font=("Cambria",30,"bold"))
feedback_label.place(relx=0.20,rely=0.24)

feedback_entry = customtkinter.CTkTextbox(master=feedback_frame,scrollbar_button_hover_color="#734140",corner_radius=10,border_width=3,text_color="black",width=500,height=300,font=("comic sans ms",20,"bold"),fg_color="#C2C2C2",bg_color="transparent")
feedback_entry.place(relx=0.2,rely=0.3)

# feedback_entry = tkinter.Text(master=feedback_frame,width=50,height=30)
# feedback_canvas.create_window(200,100,window=feedback_entry)


def feed_cross():
    feedback_frame.forget()
    submenu_dash.place_forget()
    ##print(feedback_entry.get("1.0","end"))
    feedback_entry.delete("1.0","end")
    app_canvas.pack(fill="both",expand=1)


feedback_cross = customtkinter.CTkButton(master=feedback_frame,width=10,hover_color="#FF665E",fg_color="#5E3D34",image=b_cross_image,text="",command=feed_cross)
feedback_cross.place(relx=0.78,rely=0.25)


def submit_feedback():
    global dt_string
    if feedback_entry.get("1.0","end") == "\n" or feedback_entry.get("1.0","end").isspace() == True:
        #print("pass")
        pass
    else:
        ##print(feedback_entry.get("1.0","end"))
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        database.child("Feedback").child(dt_string).set(feedback_entry.get("1.0","end"))
        feedback_entry.delete("1.0","end")


feedback_submit_button = customtkinter.CTkButton(master=feedback_frame,text="Submit",font=("calibri",20),fg_color="#854B4A",hover_color="#734140",width=40,command=submit_feedback)
feedback_submit_button.place(relx=0.735,rely=0.8)

# feedback_frame.pack(fill="both",expand=1)

mixer.music.set_volume(0.2)
island.mainloop()


