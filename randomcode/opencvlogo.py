import cv2
import numpy as np

img = np.zeros((512, 800, 3), np.uint8)

cv2.ellipse(img, (158, 166), (50, 50), 0, 120, 420, (0, 0, 255), 40)
cv2.ellipse(img, (230, 298), (50, 50), 0, -60, 240, (255, 0, 0), 40)
cv2.ellipse(img, (86, 298), (50, 50), 0, 0, 300, (0, 255, 0), 40)
cv2.putText(img, "OpenCV", (300, 274), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 4, cv2.LINE_AA)

cv2.imshow("OpenCV Logo", img)
cv2.waitKey(0)
cv2.destroyAllWindows()