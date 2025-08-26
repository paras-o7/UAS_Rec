import cv2
import numpy as np

img = cv2.imread("assets/1.png", cv2.IMREAD_COLOR)

lower_green = np.array([10, 100, 10])
upper_green = np.array([70, 200, 60])
mask = cv2.inRange(img, lower_green, upper_green)
result = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("RESULT", result)

cv2.waitKey(0)
cv2.destroyAllWindows()