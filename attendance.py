import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import PIL.Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3
from customtkinter import *
import customtkinter

from tkinter import ttk
import calendar
from datetime import datetime
from collections import defaultdict
import re
import csv
import glob
import os

# project module
import viewS_info
import show_attendance
import takeImage
import trainImage
import automaticAttedance

#GLOBAL VAR FOR POSITONING 
global my_x
my_x = 300
myGframe = None


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


base_dir = os.path.dirname(os.path.abspath(__file__))

haarcascade_path = os.path.join(base_dir, 'haarcascade_frontalface_default.xml')
trainimagelabel_path = os.path.join(base_dir, 'TrainingImageLabel', 'Trainner.yml')
trainimage_path = os.path.join(base_dir, 'TrainingImagee')
studentdetail_path = os.path.join(base_dir, 'StudentDetails', 'studentdetails.csv')
attendance_path = os.path.join(base_dir, 'Attendance')


app = CTk()
app.title("Attendence Management Systsem through Face Recognition")
app.geometry("1350x750")
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
app.configure(background="black")


def get_num_days(month, year):
    return calendar.monthrange(year, month)[1]

class AttendanceGridCanvas:
    def __init__(self, parent, month, year, subject):
        self.parent = parent
        self.month = month
        self.year = year
        self.subject = subject
        self.num_days = get_num_days(month, year)
        self.students = self.load_students(f"{os.path.join(base_dir, 'Attendance', self.subject, 'studentdetails.csv')}")
        self.attendance_data = self.load_attendance()
        self.create_grid()
 
    def load_students(self, file_path):
        students = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            row_number = 0
            for row in reader:
                students.append({"enrollment": row["Enrollment"], "name": row["Name"]})
        return students

    def load_attendance(self):
        cwd = os.getcwd()
        files = glob.glob(os.path.join(os.path.join(base_dir, 'Attendance', self.subject), '*.csv'))
        attendance_data = defaultdict(dict)

        for file_path in files:
            with open(file_path, 'r') as data:
                reader = csv.DictReader(data)
                date_match = re.search(r'\d{4}-\d{2}-\d{2}', file_path)

                if date_match:
                    date_str = date_match.group()
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()

                    if date.month == self.month and date.year == self.year:
                        for row in reader:
                            enrollment = row["Enrollment"]
                            name = row["Name"][2:-2]  # Remove the square brackets from the name
                            attendance_data[date.day - 1][enrollment] = "P"

        return attendance_data
    
    
    def create_grid(self):
       
        global myGframe  #FRAME DECLARATION 
        myGframe = CTkFrame(self.parent,height=800)
        myGframe.place(x=1, y=1)
        self.frame = tk.Frame(myGframe,height=800) #GRID KO FRAME K ANDAR DALA YAHA
        myGframe.pack(anchor=tk.NW,expand = TRUE,fill=tk.Y)
        self.frame.pack(anchor=tk.NW,expand = TRUE,fill=tk.Y)
 
        

         # Create a label for the month
        month_label = ttk.Label(self.frame, text=calendar.month_name[self.month] + " " + str(self.year), font=("Arial", 14, "bold"))
        month_label.grid(row=0, column=0, columnspan=32, pady=10)  # Increase the columnspan to accommodate up to 31 days

   
        # Create column headers
        column_headers = ["Student"]
        max_day = self.num_days
        for day in range(1, max_day + 1):
            column_headers.append(str(day))

        for col, header in enumerate(column_headers):
            header_label = ttk.Label(self.frame, text=header, font=("Arial", 12, "bold"))
            header_label.grid(row=1, column=col, padx=5, pady=5)

        # Create rows for each student
        for row, student in enumerate(self.students, start=2):
            name_label = ttk.Label(self.frame, text=student["name"], font=("Arial", 12))
            name_label.grid(row=row, column=0, padx=5, pady=5, sticky="w",)
            
        
            for col, day in enumerate(range(1, max_day + 1), start=1):
                date = datetime(self.year, self.month, day).date()
                attendance_value = self.attendance_data[day - 1].get(student["enrollment"], "")

                if attendance_value == "P":
                    value = "P"
                else:
                    value = ""

                attendance_label = ttk.Label(self.frame, text=attendance_value, font=("Arial", 12))
                attendance_label.grid(row=row, column=col, padx=5, pady=5)
                

# to destroy screen
def del_sc1():
    sc1.destroy()

# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="black")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="black",
        font=("times", 20, " bold "),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="black",
        width=9,
        height=1,
        activebackground="Red",
        font=("times", 20, " bold "),
    ).place(x=110, y=50)


def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

brd = tk.Label(app,
        fg="White",
        bg="#42aaf5",
        width=27,
        relief=RIDGE,
        bd=10,
        font=("arial", 35)
        )
brd.place(x=1000, y=1)

titl = tk.Label(
    app, text="Attendance Management", bg="#42aaf5", fg="white", font=("Helvetica", 30,'bold'),
)
titl.place(x=1160, y=12)

ri = Image.open("UI_Image/register.png")
new_size = (200, 200)  
ri = ri.resize(new_size, Image.Resampling.LANCZOS)
r = ImageTk.PhotoImage(ri)
label1 = Label(app, image=r)
label1.image = r 
label1 = tk.Label(border = 0, text = 'Submit', fg = 'black', image= r,bg = '#282424') 
label1.place(x=1100, y=130)

ai = Image.open("UI_Image/attendance.png")
new_size = (200, 200)   
ai = ai.resize(new_size, Image.Resampling.LANCZOS)
a = ImageTk.PhotoImage(ai)
label2 = Label(app, image=a)
label2.image = a
label2 = tk.Label(border = 0, text = 'Submit', fg = 'black', image= a,bg = '#282424') 
label2.place(x=1470, y=130)

vi = Image.open("UI_Image/verifyy.png")
new_size = (200, 200)   
vi = vi.resize(new_size, Image.Resampling.LANCZOS)
v = ImageTk.PhotoImage(vi)
label3 = Label(app, image=v)
label3.image = v
label3 = tk.Label(border = 0, text = 'Submit', fg = 'black', image= v,bg = '#282424') 
label3.place(x=1100, y=460)


li = Image.open("UI_Image/info.png")
new_size = (200, 200)   
li = li.resize(new_size, Image.Resampling.LANCZOS)
l = ImageTk.PhotoImage(li)
label4 = Label(app, image=l)
label4.image = l
label4 = tk.Label(border = 0, text = 'Submit', fg = 'black', image= l,bg = '#282424') 
label4.place(x=1470, y=460)



#################################################

def TakeImageUI():
    ImageUI = CTkToplevel()
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("640x700")
    ImageUI.after(500, ImageUI.grab_set())
    ImageUI.configure(background="#242424")
    ImageUI.resizable(0, 0)
    titl = tk.Label(ImageUI, bg="#42aaf5", relief=RIDGE, bd=10, font=("arial", 35))
    titl.pack(fill=X)
    # image and title
    titl = tk.Label(
        ImageUI, text="Register College Student", bg="#42aaf5", fg="White",font=("Helvetica", 30,'bold'),
    )
    titl.place(x=190, y=12)

    # heading
    a = tk.Label(
        ImageUI,
        text="Enter Student Details",
        bg="#242424",
        fg="White",
        bd=10,
        font=("Helvetica", 24,'bold'),
    )
    a.place(x=225, y=90)

    # ER no
    lbl1 = tk.Label(
        ImageUI,
        text="Enrollment No :",
        bg="#242424",
        fg="yellow",
        font=("Helvetica", 22,'bold'),
    )
    lbl1.place(x=120, y=180)
  
    txt1 = CTkEntry(
        ImageUI,
        width=200,
        fg_color="Black",
        text_color= 'White',
        corner_radius = 90,
        font=("Helvetica", 22, "bold"),
        validate="key",
    )
    txt1.place(x=350,  y=145)

    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # name
    lbl2 = tk.Label(
        ImageUI,
        bg="#242424",
        fg="yellow",
        font=("Helvetica", 22,'bold'),
        text="Name :",
    )
    lbl2.place(x=120, y=235)
   
    txt2 = CTkEntry(
        ImageUI,
        width=200,
        fg_color="Black",
        text_color= 'White',
        corner_radius = 90,
        font=("Helvetica", 22, "bold"),
    )
    txt2.place(x=350, y=190)

    lbl3 = tk.Label(
        ImageUI,
        bg="#242424",
        fg="yellow",
        font=("Helvetica", 22,'bold'),
        text="Class :",
    )
    lbl3.place(x=120, y=290)

    txt3 = CTkEntry(
        ImageUI,
        width=200,
        fg_color="Black",
        text_color= 'White',
        corner_radius = 90,
        font=("Helvetica", 22, "bold"),
    )
    txt3.place(x=350, y=235)

    lbl4 = tk.Label(
    ImageUI,
    bg="#242424",
    fg="yellow",
    font=("Helvetica", 22,'bold'),
    text="DOB :",
    )
    lbl4.place(x=120, y=345)

    txt4 = CTkEntry(
        ImageUI,
        width=200,
        fg_color="Black",
        text_color= 'White',
        corner_radius = 90,
        font=("Helvetica", 22, "bold"),
    )
    txt4.place(x=350, y=280)

    lbl5 = tk.Label(
        ImageUI,
        bg="#242424",
        fg="yellow",
        font=("Helvetica", 22,'bold'),
        text="Father's Name :",
    )
    lbl5.place(x=120, y=400)

    txt5 = CTkEntry(
        ImageUI,
        width=200,
        fg_color="Black",
        text_color= 'White',
        corner_radius = 90,
        font=("Helvetica", 22, "bold"),
    )
    txt5.place(x=350, y=325)

    lbl6 = tk.Label(
        ImageUI,
        bg="#242424",
        fg="yellow",
        font=("Helvetica", 22,'bold'),
        text="Course :",
    )
    lbl6.place(x=120, y=455)
 
    txt6 = CTkEntry(
        ImageUI,
        width=200,
        fg_color="Black",
        text_color= 'White',
        corner_radius = 90,
        font=("Helvetica", 22, "bold"),
    )
    txt6.place(x=350, y=370)

    lbl8 = tk.Label(
        ImageUI,
        bg="#242424",
        fg="yellow",
        font=("Helvetica", 22,'bold'),
        text="Phone :",
    )
    lbl8.place(x=120, y=510)

    txt8 = CTkEntry(
        ImageUI,
        width=200,
        fg_color="Black",
        text_color= 'White',
        corner_radius = 90,
        font=("Helvetica", 22, "bold"),
    )
    txt8.place(x=350, y=415)

    lbl7 = tk.Label(
        ImageUI,
        bg="#242424",
        fg="yellow",
        font=("Helvetica", 22,'bold'),
        text="",
    )
    lbl7.place(x=120, y=565)

    txt7 = CTkEntry(
        ImageUI,
        width=0,
        height=0,
        fg_color="Black",
        text_color= 'White',
        corner_radius = 60,
        font=("Helvetica", 22, "bold"),
    )
    txt7.place(x=700, y=460)

    message = tk.Label(
        ImageUI,
        bg="#242424",
        fg="red",
        font=("Helvetica", 22,'bold'),
    )
    message.place(x=90, y=600)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        l3 = txt3.get()
        l4 = txt4.get()
        l5 = txt5.get()
        l6 = txt6.get()
        l8 = txt8.get()
        takeImage.TakeImage(
            l1,
            l2,
            l3,
            l4,
            l5,
            l6,
            l8,
            haarcascade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")
        txt3.delete(0, "end")
        txt4.delete(0, "end")
        txt5.delete(0, "end")
        txt6.delete(0, "end")
        txt8.delete(0, "end")
        

    # take Image button
    # image
    takeImg = CTkButton(
        ImageUI,
        fg_color="#42aaf5",
        height = 40,
        width= 90,
        font=("Helvetica", 19,'bold'),
        hover_color="#27638f",
        corner_radius= 90,
        text="Take Image",
        command=take_image,
    )
    takeImg.place(x=150, y=550)

    def train_image():
        trainImage.TrainImage(
            haarcascade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )


    def exit_btn():

        ImageUI.destroy()
        ImageUI.update()

    tre = CTkButton(
        ImageUI,
        text="EXIT",
        command=exit_btn,
        fg_color="#42aaf5",
        height = 40,
        width= 100,
        font=("Helvetica", 18,'bold'),
        hover_color="#e04141",
        corner_radius= 90,
)
    tre.place(x=270, y=620)

    # train Image function call
    trainImg = CTkButton(
        ImageUI,
        fg_color="#42aaf5",
        height = 40,
        width= 90,
        font=("Helvetica", 19,'bold'),
        hover_color="#27638f",
        corner_radius= 90,
        text="Train Image",
        command=train_image,
    )
    trainImg.place(x=350, y=550)

r = CTkButton(master=app,
    fg_color="#42aaf5",
    height = 32,
    width= 90,
    font=("Helvetica", 19,'bold'),
    hover_color="#27638f",
    corner_radius= 50,
    text="Register a new student",
    command=TakeImageUI
)
r.place(x=835, y=280)

def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)

r = CTkButton(master=app,
    text="Take Attendance",
    command=automatic_attedance,
    fg_color="#42aaf5",
    height = 32,
    width= 100,
    font=("Helvetica", 18,'bold'),
    hover_color="#27638f",
    corner_radius= 50,
)
r.place(x=1166, y=280)


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)


r = CTkButton(master=app,
    text="View Attendance",
    command=view_attendance,
    fg_color="#42aaf5",
    height = 32,
    width= 100,
    font=("Helvetica", 18,'bold'),
    hover_color="#27638f",
    corner_radius= 50,
)
r.place(x=875, y=540)

def view_info():
    viewS_info.subjectchoose(text_to_speech)

r = CTkButton(master=app,
    text="View Student Info",
    command=view_info,
    fg_color="#42aaf5",
    height = 32,
    width= 100,
    font=("Helvetica", 18,'bold'),
    hover_color="#27638f",
    corner_radius= 50,
)
r.place(x=1165, y=540)

r = CTkButton(master=app,
    text="EXIT",
    command=quit,
    fg_color="#cf352e",
    height = 60,
    width= 120,
    font=("Helvetica", 22,'bold'),
    hover_color="#922822",
    corner_radius= 30,
)
r.place(x=1195, y=635)

current_month = datetime.now().month
current_year = datetime.now().year
AttendanceGridCanvas(app, current_month, current_year, "MA")

def submit_button_clicked():
    global myGframe

    if myGframe is not None:
        myGframe.destroy()
        myGframe = None
    
    text = text_box.get()
    current_month = datetime.now().month
    current_year = datetime.now().year
    AttendanceGridCanvas(app, current_month, current_year, text)



grid_text = tk.Label(
    app,
    bg="#242424",
    fg="white",
    font=("Helvetica", 21,'bold'),
    text="Class: ",
)
grid_text.place(x=1115, y=781)

text_box = CTkEntry(app,
    width=65,
    height=30,
    fg_color="Black",
    text_color= 'White',
    corner_radius = 90,
    font=("Helvetica", 20, "bold"),
)

text_box.place(x=970, y=625)

submit_button = CTkButton(app, 
    command=submit_button_clicked,                    
    text="Attendnce Grid",
    fg_color="#42aaf5",
    height = 30,
    width= 100,
    font=("Helvetica", 18,'bold'),
    hover_color="#27638f",
    corner_radius= 15,
)
submit_button.place(x=886, y=664)

app.resizable(False, False)
app.mainloop()
