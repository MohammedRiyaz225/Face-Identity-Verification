import os
import face_recognition
import numpy as np
import cv2
import pymongo
from bson import ObjectId
from flask import Flask, render_template, Response

mongo_uri = os.getenv(
    "MONGO_URI",
    "mongodb+srv://superuser:superuser123@cluster0.s3aalbl.mongodb.net/images?retryWrites=true&w=majority&appName=Cluster0",
)
client = pymongo.MongoClient(mongo_uri)
db = client["images"]
collection = db["images"]

app = Flask(__name__, template_folder="templates")

def fetch_img(image_ids):
    images = []
    labels = []
    for image_id in image_ids:
        image_document = collection.find_one({"_id": ObjectId(image_id)})
        if not image_document:
            continue

        image_data = image_document.get("data") or image_document.get("image_data")
        label = image_document.get("label") or "unknown"
        if not image_data:
            continue

        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            continue
        # Convert to standard RGB to prevent "Unsupported image type" errors from face_recognition
        if len(img.shape) == 3 and img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        images.append(img_rgb)
        labels.append(label)
    return images, labels

def get_all_image_ids():
    return [str(doc["_id"]) for doc in collection.find({}, {"_id": 1})]

def encoding(images):
    final_encode = []
    for i in images:
        encodings = face_recognition.face_encodings(i)
        if encodings:
            final_encode.append(encodings[0])
    return final_encode

@app.route("/")
def index():
    return render_template("index.html")

def gen_frames():
    image_ids = get_all_image_ids()
    images, labels = fetch_img(image_ids)
    encodings_db = encoding(images)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Camera failed to open!")
        # Create a black image with an error message
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(img, "Camera Blocked/Unavailable", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        ret, buffer = cv2.imencode('.jpg', img)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)

        # Convert directly to RGB without resizing, as cv2.resize creates incompatible memory strides for dlib
        imgS = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        currentFaceLoc = face_recognition.face_locations(imgS)
        imgEncodingsCurrent = face_recognition.face_encodings(imgS, currentFaceLoc)

        for encodeFace, faceLoc in zip(imgEncodingsCurrent, currentFaceLoc):
            if not encodings_db:
                name = "No known faces"
                y1, x2, y2, x1 = faceLoc
                p = 30 # padding
                y1, x2, y2, x1 = max(0, y1 - p), min(frame.shape[1], x2 + p), min(frame.shape[0], y2 + p), max(0, x1 - p)
                
                font = cv2.FONT_HERSHEY_COMPLEX
                (tw, th), _ = cv2.getTextSize(name, font, 0.8, 2)
                bw = max(x2 - x1, tw + 12)
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 165, 255), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x1 + bw, y2), (0, 165, 255), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), font, 0.8, (255, 255, 255), 2)
                continue

            faceDis = face_recognition.face_distance(encodings_db, encodeFace)
            matchIndex = int(np.argmin(faceDis))

            y1, x2, y2, x1 = faceLoc
            p = 30 # padding
            y1, x2, y2, x1 = max(0, y1 - p), min(frame.shape[1], x2 + p), min(frame.shape[0], y2 + p), max(0, x1 - p)

            if matchIndex < len(labels) and faceDis[matchIndex] < 0.52:
                name = str(labels[matchIndex]).capitalize()
                color = (0, 255, 0)
            else:
                name = "Unknown"
                color = (0, 0, 255)

            font = cv2.FONT_HERSHEY_COMPLEX
            (tw, th), _ = cv2.getTextSize(name, font, 0.9, 2)
            bw = max(x2 - x1, tw + 12)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x1 + bw, y2), color, cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), font, 0.9, (255, 255, 255), 2)

        ret, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )
    cap.release()

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(debug=True)
