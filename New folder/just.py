import face_recognition
import numpy as np
import cv2
import pymongo
from bson import ObjectId
import tkinter as tk
def get_screen_resolution():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width, height
screen_width, screen_height = get_screen_resolution()
# MongoDB setup
client = pymongo.MongoClient(
    "mongodb+srv://superuser:superuser123@cluster0.s3aalbl.mongodb.net/images?retryWrites=true&w=majority&appName=Cluster0")
db = client["images"]
collection = db["images"]

# Function to fetch images from MongoDB
def fetch_img(image_ids):
    images = []
    labels = []
    for image_id in image_ids:
        image_document = collection.find_one({"_id": ObjectId(image_id)})

        if image_document:
            image_data = image_document.get("image_data")
            label = image_document.get('label')

            if image_data is not None:
                nparr = np.frombuffer(image_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                images.append(img)
                labels.append(label)
            else:
                print("Image data is None.")
        else:
            print("Image not found")
    return images, labels

# Function to get face locations in images
def face_locations(images):
    faceLoc = []
    for i in images:
        faceLoc.append(face_recognition.face_locations(i))
    return faceLoc

# Function to encode faces in images
def encoding(images):
    finalEncode = []
    for i in images:
        encodings = face_recognition.face_encodings(i)
        finalEncode.append(encodings[0])
    return finalEncode

# Get all image IDs from MongoDB
def get_all_image_ids():
    ids = []
    for doc in collection.find():
        ids.append(str(doc["_id"]))
    return ids

image_ids = get_all_image_ids()
images, labels = fetch_img(image_ids)
encode = encoding(images)

# Compare each pair of face encodings
cap = cv2.VideoCapture(1)
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
        faceDis = face_recognition.face_distance(encode, encodeFace)

        matchIndex = np.argmin(faceDis)
        y1, x2, y2, x1 = faceLoc
        y1, x2, x1, y2 = y1 * 4, x2 * 4, x1 * 4, y2 * 4

        # Overlay output on a background image
        background = cv2.imread("Untitled design.png")  # Load background image
        center_x = ((background.shape[1] - frame.shape[1]) // 2) +11
        center_y = ((background.shape[0] - frame.shape[0]) // 2) - 27

        print(center_x , center_y)



        # Ensure the frame fits within the background image
        if center_x >= 0 and center_y >= 0:
            # Overlay the frame onto the background image at the calculated center position
            frame = cv2.resize(frame, (screen_width, screen_height))
            background[center_y:center_y + frame.shape[0] , center_x:center_x + frame.shape[1] ] = frame

            # Ensure the frame fits within the background image
        # if y2 <= background.shape[0] and x2 <= background.shape[1]:
        #     # Overlay the frame onto the background image at the specified position (top-left corner)
        #     background[0:frame.shape[0], 0:frame.shape[1]] = frame

            # Display the combined image
            cv2.imshow("window", background)
        else:
            print("Face position exceeds background dimensions.")

        key = cv2.waitKey(1)
        if key == 27:  # Check if 'Esc' key is pressed
            break

cap.release()
cv2.destroyAllWindows()
