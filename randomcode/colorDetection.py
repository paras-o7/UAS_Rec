import cv2 as cv
import numpy as np
 
cap = cv.VideoCapture(0)
 
while True:
 
    # Take each frame
    isRead, frame = cap.read()
    assert isRead, "Failed to capture video"
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
 
    # define range of blue color in HSV
    lower_blue = np.array([100,30,25])
    upper_blue = np.array([140,255,255])
 
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)
 
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)
 
    cv.imshow('res',res)
    k = cv.waitKey(5)
    if k == 27:
        break
 
cv.destroyAllWindows()