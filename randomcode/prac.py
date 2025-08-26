import cv2
import numpy as np

# img = cv2.imread("assets/DTU_LOGO.png", cv2.IMREAD_UNCHANGED)
# for i in range(100):
# 	for j in range(img.shape[1]):
# 		img[i][j] = [
# 			random.randint(0, 255),
# 			random.randint(0, 255),
# 			random.randint(0, 255),
# 			img[i][j][3]
# 		]

# cv2.imshow('LOGO', img)
# print(img.shape)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('frame', result)
    if cv2.waitKey(1) == ord('q'):
        break