import cv2

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    assert _, "Failed to get video capture"

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # img = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 6)
    img = cv2.Canny(frame, 50, 200)
    cv2.imshow("img", img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
