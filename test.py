import cv2
import numpy as np
import face_recognition

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ret, frame = cap.read()
cap.release()

imgS = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

print("Shape:", imgS.shape)
print("Dtype:", imgS.dtype)
print("Flags:", imgS.flags)

try:
    print("Detecting faces...")
    locs = face_recognition.face_locations(imgS)
    print("Success! Found:", len(locs))
except Exception as e:
    print("Error:", type(e).__name__, "-", str(e))
