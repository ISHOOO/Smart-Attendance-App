
import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time

base_dir = os.path.dirname(os.path.abspath(__file__))

# take Image of user
def TakeImage(l1, l2, l3, l4, l5, l6, l8, haarcascade_path, trainimage_path, message, err_screen, text_to_speech):
    if (l1 == "") and (l2=="") and (l3=="") and (l4=="") and (l5=="") and (l6=="") and (l8==""):
        t='Please Enter your full information.'
        text_to_speech(t)
    elif l1=='':
        t='Please Enter the your Enrollment Number.'
        text_to_speech(t)
    elif l2 == "":
        t='Please Enter the your Name.'
        text_to_speech(t)
    elif l3 == "":
        t='Please Enter the your Class.'
        text_to_speech(t)
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier(haarcascade_path)
            Enrollment = l1
            Name = l2
            Class = l3
            Dob = l4
            Fn = l5
            cor = l6
            ph = l8

            sampleNum = 0
            directory = Enrollment + "_" + Name
            path = os.path.join(trainimage_path, directory)
            os.mkdir(path)
            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    cv2.imwrite(
                        f"{path}\ "
                        + Name
                        + "_"
                        + Enrollment
                        + "_"
                        + str(sampleNum)
                        + ".jpg",
                        gray[y : y + h, x : x + w],
                    )
                    cv2.imshow("Frame", img)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif sampleNum > 50:
                    break
            cam.release()
            cv2.destroyAllWindows()
            row = [Enrollment, Name]
            row2 = [Enrollment, Name, Class,Dob,Fn,cor,ph]
        
            with open(os.path.join(base_dir, 'StudentDetails', 'studentdetails.csv'), 'a+', newline='') as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row)
                csvFile.close()
            with open(os.path.join(base_dir, 'Attendance', Class, 'studentdetails.csv'), 'a+', newline='') as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row2)
                csvFile.close()
            res = "Images Saved for ER No: " + Enrollment + ", Name: " + Name
            message.configure(text=res)
            text_to_speech(res)
        except FileExistsError as F:
            F = "Student Data already exists"
            text_to_speech(F)
