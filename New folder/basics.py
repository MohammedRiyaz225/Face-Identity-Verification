import face_recognition
import numpy as np
import cv2
import pymongo
from bson import ObjectId
client = pymongo.MongoClient(
    "mongodb+srv://superuser:superuser123@cluster0.s3aalbl.mongodb.net/images?retryWrites=true&w=majority&appName=Cluster0")
db = client["images"]
collection = db["images"]


def get_all_image_ids():
    ids = []
    for doc in collection.find():
        ids.append(str(doc["_id"]))

    return ids

image_id = get_all_image_ids()
print(image_id)


def fetch_img():
    for i in range(len(image_id)):
        image_document = collection.find_one({"_id": ObjectId(image_id[i])})  # Use bson.ObjectId

        if image_document:
            # Get the binary image data and content type from the document
            image_data = image_document.get("data")

            # Convert binary image data to NumPy array
            nparr = np.frombuffer(image_data, np.uint8)
            images_main = []
            # Decode NumPy array to OpenCV image
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return img

            # Display or process the OpenCV image as needed
            # cv2.imshow('Image', img)  # Display the image
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            # images_main.append(img)

        else:
            print("Image not found")

    # return images_main



# Step - 1: loading the images
imgElon = face_recognition.load_image_file('imageAttendance\Kapil.jpg')
imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)


imgTest = fetch_img()
imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)

# imgBill = face_recognition.load_image_file('imageBasic\Bill Gates.jpeg')
# imgBill = cv2.cvtColor(imgBill,cv2.COLOR_BGR2RGB)
# resizing image
scale_percent = 60 # percent of original size
width = int(imgElon.shape[1] * scale_percent / 100)
height = int(imgElon.shape[0] * scale_percent / 100)
dim = (width, height)
imgElon = cv2.resize(imgElon,dim,interpolation=cv2.INTER_AREA)

# step - 2: Finding the face in the image

# finding the face location in the image
faceLoc = face_recognition.face_locations(imgElon)[0]
# finding the face encoding in the image
faceEncode = face_recognition.face_encodings(imgElon)[0]
print(type(faceEncode))
# detected and drawn a rectangle on the face
cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(0,255,0),2)

# finding the face location in the image
faceLocTest = face_recognition.face_locations(imgTest)[0]
# finding the face encoding in the image
faceEncodeTest = face_recognition.face_encodings(imgTest)[0]
# detected and drawn a rectangle on the face
cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(0,255,0),2)

# finding the face location in the image
# faceLocBill = face_recognition.face_locations(imgBill)[0]
# # finding the face encoding in the image
# faceEncodeBill = face_recognition.face_encodings(imgBill)[0]
# detected and drawn a rectangle on the face

# cv2.rectangle(imgBill,(faceLocBill[3],faceLocBill[0]),(faceLocBill[1],faceLocBill[2]),(0,255,0),2)

# comparing the faces

results = face_recognition.compare_faces([faceEncode],faceEncodeTest)
distance_face= face_recognition.face_distance([faceEncode],faceEncodeTest)
# print(distance_face)

# text on the image
cv2.putText(imgTest,f"{results} {round(distance_face[0],2)}",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)

cv2.imshow('Elon Musk',imgElon)
# cv2.imshow('Bill Gates',imgBill)
cv2.imshow('Elon MuskTest',imgTest)
cv2.waitKey(0)
