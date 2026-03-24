import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import pymongo
from bson import ObjectId
#
#
# client = pymongo.MongoClient(
#     "mongodb+srv://superuser:superuser123@cluster0.s3aalbl.mongodb.net/images?retryWrites=true&w=majority&appName=Cluster0")
# db = client["images"]
# collection = db["images"]
#
#
# def get_all_image_ids():
#     ids = []
#     for doc in collection.find():
#         ids.append(str(doc["_id"]))
#
#     return ids
#
#
# image_id = get_all_image_ids()
#
#
# def fetch_img():
#     for i in range(len(image_id)):
#         image_document = collection.find_one({"_id": ObjectId(image_id[i])})  # Use bson.ObjectId
#
#         if image_document:
#             # Get the binary image data and content type from the document
#             image_data = image_document.get("data")
#
#             # Convert binary image data to NumPy array
#             nparr = np.frombuffer(image_data, np.uint8)
#             images_main = []
#             # Decode NumPy array to OpenCV image
#             img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#
#             # Display or process the OpenCV image as needed
#             # cv2.imshow('Image', img)  # Display the image
#             # cv2.waitKey(0)
#             # cv2.destroyAllWindows()
#             images_main.append(img)
#
#         else:
#             print("Image not found")
#
#     return images_main
# Function to resize an image
def resize_img(image):
    scale_percent = 30  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# Function to find face encodings
def findEncodings(images):
    final_Encodings = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgEncodings = face_recognition.face_encodings(img)[0]
        final_Encodings.append(imgEncodings)
    return final_Encodings

# Function to mark attendance
def markAttendance(name):
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

# Path to the folder containing images
path = 'imageAttendance'
images_main = []
classNames = []
myList = os.listdir(path)

# Reading images and extracting class names
for cl in myList:
    img_Current = cv2.imread(f'{path}/{cl}')
    images_main.append(img_Current)
    classNames.append(os.path.splitext(cl)[0])

print(classNames)

# Get known faces encodings

# images_main = fetch_img()
knownFaces = findEncodings(images_main)

print(type(knownFaces))
print(len(knownFaces))
print(knownFaces[0])


print('Encoding completed')

# Load background image
# imgBackground = cv2.imread('background.png')  # Replace 'background.jpg' with your background image path

# Video capture from webcam
cap = cv2.VideoCapture(1)

# Loop through video frames
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    currentFaceLoc = face_recognition.face_locations(imgS)
    imgEncodingsCurrent = face_recognition.face_encodings(imgS, currentFaceLoc)

    for encodeFace, faceLoc in zip(imgEncodingsCurrent, currentFaceLoc):
        faceDis = face_recognition.face_distance(knownFaces, encodeFace)
        print(len(faceDis))
        print(faceDis[0])

        matchIndex = np.argmin(faceDis)  # Find the index of the closest match
        y1, x2, y2, x1 = faceLoc
        y1, x2, x1, y2 = y1 * 4, x2 * 4, x1 * 4, y2 * 4
        if faceDis[matchIndex] < 0.52:  # Check if the closest match is below a certain threshold
            name = classNames[matchIndex].capitalize()
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            # markAttendance(name)
        else:
            name = 'Unknown'
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)

        cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)


    # Display the combined image
    cv2.imshow("window", frame)
    key = cv2.waitKey(10)
    #
    if key == 27:  # Check if 'Esc' key is pressed
        break

cap.release()
cv2.destroyAllWindows()

