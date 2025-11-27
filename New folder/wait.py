import face_recognition
import numpy as np
import cv2
import pymongo
from bson import ObjectId
from flask import Flask, render_template, Response

client = pymongo.MongoClient("mongodb+srv://superuser:superuser123@cluster0.s3aalbl.mongodb.net/images?retryWrites=true&w=majority&appName=Cluster0")
db = client["images"]
collection = db["images"]

app = Flask(__name__)

def fetch_img(image_ids):
    images = []
    labels = []
    for image_id in image_ids:
        image_document = collection.find_one({"_id": ObjectId(image_id)})  # Use bson.ObjectId

        if image_document:
            # Get the binary image data from the document
            image_data = image_document.get("image_data")
            label = image_document.get('label')

            if image_data is not None:
                # Convert binary image data to NumPy array
                nparr = np.frombuffer(image_data, np.uint8)
                # Decode NumPy array to OpenCV image
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                images.append(img)
                labels.append(label)
            else:
                print("Image data is None.")
        else:
            print("Image not found")
    return images, labels

def get_all_image_ids():
    ids = []
    for doc in collection.find():
        ids.append(str(doc["_id"]))
    return ids

def encoding(images):
    finalEncode = []
    for i in images:
        encodings = face_recognition.face_encodings(i)
        finalEncode.append(encodings[0])
    return finalEncode

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    image_ids = get_all_image_ids()
    images, labels = fetch_img(image_ids)
    encode = encoding(images)

    cap = cv2.VideoCapture(0)

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
            matchIndex = np.argmin(faceDis)  # Find the index of the closest match
            y1, x2, y2, x1 = faceLoc
            y1, x2, x1, y2 = y1 * 4, x2 * 4, x1 * 4, y2 * 4
            if matchIndex < len(labels):  # Check if matchIndex is within the bounds of labels
                if faceDis[matchIndex] < 0.52:
                    name = labels[matchIndex].capitalize()
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                else:
                    name = 'Unknown'
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
