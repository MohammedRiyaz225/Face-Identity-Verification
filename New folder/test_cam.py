import cv2
print('Testing Camera 0')
cap = cv2.VideoCapture(0)
print('isOpened:', cap.isOpened())
if cap.isOpened():
    ret, frame = cap.read()
    print('Read success:', ret)
cap.release()
print('\nTesting Camera 1')
cap = cv2.VideoCapture(1)
print('isOpened:', cap.isOpened())
if cap.isOpened():
    ret, frame = cap.read()
    print('Read success:', ret)
cap.release()
