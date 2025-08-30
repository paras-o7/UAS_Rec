#! /usr/bin/env python3

import cv2

img = cv2.imread("assets/samples/1.png")

cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()