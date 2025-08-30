import cv2

img = cv2.imread("assets/samples/1.png", cv2.IMREAD_GRAYSCALE)
img = cv2.Canny(img, 50, 200)

cv2.imshow("a", img)
cv2.waitKey(0)
cv2.destroyAllWindows()