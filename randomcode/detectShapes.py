import cv2, random
import numpy as np

image = cv2.imread("assets/samples/1.png", cv2.IMREAD_COLOR)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
clean = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
grayed = cv2.cvtColor(clean, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(grayed, 127, 255, cv2.THRESH_BINARY)

# thresh = cv2.filter2D(thresh, -1, np.ones((2,2), np.float32)/25)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
newcnt = []
for i in range(len(contours)):
    epsilon = 0.04 * cv2.arcLength(contours[i], True)
    newcnt.append(cv2.approxPolyDP(contours[i], epsilon, True))

for i in newcnt:
    M = cv2.moments(i)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    print(f"============= ({cx}, {cy})")
    clr = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    for j in i:
        print(j[0])
        cv2.circle(image, j[0], 2, clr, 1)
# cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

print(len(contours))
cv2.imshow("test", image)
cv2.waitKey(0)
cv2.destroyAllWindows()