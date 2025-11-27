import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime

path = 'imageAttendance'
images_main = []
classNames = []
myList = os.listdir(path)

for cl in myList:
    img_Current = cv2.imread(f'{path}/{cl}')
    images_main.append(img_Current)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def resize_img(image):
    scale_percent = 30  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    image = cv2.resize(image,dim,interpolation=cv2.INTER_AREA)

def findEncodings(images):
    final_Encodings = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        imgEncodings = face_recognition.face_encodings(img)[0]
        final_Encodings.append(imgEncodings)
    return final_Encodings

def markAttedance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dt = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dt}')

print(len(images_main))
knownFaces = findEncodings(images_main)

print('Encoding completed')

frame = cv2.VideoCapture(0)
# cv2.imshow('frame',frame)
while True:
    success, img = frame.read()
    img = cv2.flip(img,1)
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    currentFaceLoc = face_recognition.face_locations(imgS)
    imgEncodingsCurrent = face_recognition.face_encodings(imgS, currentFaceLoc)

    # known_face_detected = False  # Flag to track if any known face is detected

    for encodeFace, faceLoc in zip(imgEncodingsCurrent, currentFaceLoc):
        matches = face_recognition.compare_faces(knownFaces, encodeFace)
        print(matches)
        faceDis = face_recognition.face_distance(knownFaces, encodeFace)

        name = 'Face not recognizied'
        # known_face_detected = False
        y1, x2, y2, x1 = faceLoc
        y1, x2, x1, y2 = y1 * 4, x2 * 4, x1 * 4, y2 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        if True in matches:
            matchIndex = matches.index(True)
            name = classNames[matchIndex].capitalize()
            # known_face_detected = True  # Set the flag to True when a known face is detected
            print(name)
            # markAttedance(name)
        cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

        # if not known_face_detected:
        # print("Face not recognized")  # Display "No known faces" when no known face is detected

    cv2.imshow('test',img)
    key = cv2.waitKey(1)

    # Check if 'Esc' key is pressed
    if key == 27:  # ASCII value for 'Esc' key
        break  # Break the loop if 'Esc' is pressed

# Release the VideoCapture object and close all OpenCV windows
frame.release()
cv2.destroyAllWindows()