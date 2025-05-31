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
from customtkinter import *
import tkinter.ttk as tkk
import tkinter.font as font

base_dir = os.path.dirname(os.path.abspath(__file__))

haarcascade_path = os.path.join(base_dir, 'haarcascade_frontalface_default.xml')
trainimagelabel_path = os.path.join(base_dir, 'TrainingImageLabel', 'Trainner.yml')
trainimage_path = os.path.join(base_dir, 'TrainingImagee')
studentdetail_path = os.path.join(base_dir, 'StudentDetails', 'studentdetails.csv')
attendance_path = os.path.join(base_dir, 'Attendance')
# for choose subject and fill attendance
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20
        print(now)
        print(future)
        if sub == "":
            t = "Please enter the class name!!!"
            text_to_speech(t)
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found,please train model"
                    Notifica.configure(
                        text=e,
                        bg="black",
                        fg="yellow",
                        width=33,
                        font=("Helvetica", 23,'bold'),
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)
                facecasCade = cv2.CascadeClassifier(haarcascade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        if conf < 70:
                            print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            # En='1604501160'+str(Id)
                            attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                            )
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                            )
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ["Enrollment"], keep="first"
                    )
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                print(aa)
                # attendance["date"] = date
                # attendance["Attendance"] = "P"
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                # fileName = "Attendance/" + Subject + ".csv"
                path = os.path.join(attendance_path, Subject)
                fileName = (
                    f"{path}/"
                    + Subject
                    + "_"
                    + date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                print(attendance)
                attendance.to_csv(fileName, index=False)

                m = "Attendance Filled Successfully of " + Subject
                Notifica.configure(
                    text=m,
                    bg="#282424",
                    fg="white",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("Helvetica", 23,'bold'),
                )
                text_to_speech(m)

                Notifica.place(x=800, y=100)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter

                root = CTk()
                root.title("Attendance of " + Subject)
                root.configure(background="black")
                cs = os.path.join(path, fileName)
                print(cs)
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:

                            label = tkinter.Label(
                                root,
                                width=10,
                                height=1,
                                fg="yellow",
                                font=("Helvetica", 23,'bold'),
                                bg="black",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)
            except:
                f = "No Face found for attendance"
                text_to_speech(f)
                cv2.destroyAllWindows()

    ###windo is frame for subject chooser
    subject = CTk()
    # windo.iconbitmap("AMS.ico")
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    # subject_logo = Image.open("UI_Image/0004.png")
    # subject_logo = subject_logo.resize((50, 47), resample=PIL.Image.Resampling.LANCZOS)
    # subject_logo1 = ImageTk.PhotoImage(subject_logo)
    titl = tk.Label(
        subject, bg="#42aaf5", relief=RIDGE, bd=10, font=("arial", 35)
    )
    titl.pack(fill=X)
    # l1 = tk.Label(subject, image=subject_logo1, bg="black",)
    # l1.place(x=100, y=10)
    titl = tk.Label(
        subject,
        text="Enter Class Name",
        bg="#42aaf5",
        fg="White",
        font=("Helvetica", 30,'bold'),
    )
    titl.place(x=200, y=10)
    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="yellow",
        fg="black",
        width=33,
        height=2,
        font=("Helvetica", 23,'bold'),
    )

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the class name!!!"
            text_to_speech(t)
        else:
            os.startfile(
                f"Attendance\{sub}"
            )

    attf = CTkButton(
        subject,
        fg_color="#42aaf5",
        height = 40,
        width= 90,
        font=("Helvetica", 19,'bold'),
        hover_color="#27638f",
        corner_radius= 50,
        command=Attf,
        text="Check Sheets",
    )
    attf.place(x=320, y=180)

    sub = tk.Label(
        subject,
        bg="#242424",
        fg="yellow",
        font=("Helvetica", 24,'bold'),
        text="Name :",

    )
    sub.place(x=180, y=125)

    def exit_btn():

        subject.destroy()
        subject.update()

    tre = CTkButton(
        master=subject,
        text="EXIT",
        command=exit_btn,
        fg_color="#42aaf5",
        height = 40,
        width= 100,
        font=("Helvetica", 18,'bold'),
        hover_color="#e04141",
        corner_radius= 90,
)   
    tre.place(x=260, y=250)

    tx = CTkEntry(
        subject,
        width=200,
        height=40,
        fg_color="Black",
        text_color= 'White',
        corner_radius = 90,
        font=("Helvetica", 22, "bold"),
    )
    tx.place(x=270, y=100)

    fill_a = CTkButton(
        subject,
        fg_color="#42aaf5",
        height = 40,
        width= 90,
        font=("Helvetica", 19,'bold'),
        hover_color="#27638f",
        corner_radius= 50,
        text="Fill Attendance",
        command=FillAttendance,
    )
    fill_a.place(x=120, y=180)
    subject.mainloop()
