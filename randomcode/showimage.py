#! /usr/bin/env python3

import cv2, sys
img = cv2.imread(sys.argv[-1])

cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()