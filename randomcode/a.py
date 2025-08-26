import cv2

img = cv2.imread("assets/1.png", cv2.IMREAD_COLOR)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()