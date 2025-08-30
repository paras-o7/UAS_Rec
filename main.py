#! /usr/bin/env python3
import cv2
import numpy as np

IMAGES = [
    "assets/1.png",
    "assets/2.png",
    "assets/3.png",
    "assets/4.png",
    "assets/5.png",
    "assets/6.png",
    "assets/7.png",
    "assets/8.png",
    "assets/9.png",
    "assets/10.png",
]

img = cv2.imread("assets/3.png", cv2.IMREAD_COLOR)
assert img is not None, "Failed to read image"

# RANGE OF COLOURS MARKING SEVERITY OF A VICTIM
COLOR_RANGE = {
    "severe": (
        np.array([130, 150, 230], np.uint8),
        np.array([190, 190, 255], np.uint8),
    ),
    "moderate": (
        np.array([70, 180, 220], np.uint8),
        np.array([100, 230, 255], np.uint8)
    ),
    "safe": (
        np.array([116, 242, 190], np.uint8),
        np.array([130, 255, 200], np.uint8)
    ),
    "camp_pink": (
        np.array([255, 140, 220], np.uint8),
        np.array([255, 200, 255], np.uint8)
    ),
    "camp_blue": (
        np.array([255, 150, 100], np.uint8),
        np.array([255, 240, 200], np.uint8)
    ),
    "camp_gray": (
        np.array([205, 205, 210], np.uint8),
        np.array([230, 230, 230], np.uint8)
    )
}

# MASKS OF THE RESPECTIVE SEVERITY, USED TO IDENTIFY THE SEVERITY OF A 
# DETECTED CONTOUR (victim) IN get_humans()
MASK_SEVERE = cv2.inRange(img, COLOR_RANGE["severe"][0], COLOR_RANGE["severe"][1])
MASK_MODERATE = cv2.inRange(img, COLOR_RANGE["moderate"][0], COLOR_RANGE["moderate"][1])
MASK_SAFE = cv2.inRange(img, COLOR_RANGE["safe"][0], COLOR_RANGE["safe"][1])
MASK_CAMP_PINK = cv2.inRange(img, COLOR_RANGE["camp_pink"][0], COLOR_RANGE["camp_pink"][1])
MASK_CAMP_GRAY = cv2.inRange(img, COLOR_RANGE["camp_gray"][0], COLOR_RANGE["camp_gray"][1])
MASK_CAMP_BLUE = cv2.inRange(img, COLOR_RANGE["camp_blue"][0], COLOR_RANGE["camp_blue"][1])

# MAIN STORAGE OF THE DATA FROM THE IMAGE
CASUALTIES: dict[str, dict[str, list[tuple[int, int]]]] = {
    "adult": {
        "severe": [],
        "moderate": [],
        "safe": []
    },
    "child": {
        "severe": [],
        "moderate": [],
        "safe": []
    },
    "elder": {
        "severe": [],
        "moderate": [],
        "safe": []
    }
}
CAMPS: dict[str, list[int]] = {
    "pink": [],
    "blue": [],
    "gray": []
}

def ground_overlay():
    lower_green = np.array([10, 100, 10], np.uint8)
    upper_green = np.array([70, 200, 60], np.uint8)
    mask = cv2.inRange(img, lower_green, upper_green)
    result = cv2.bitwise_and(img, img, mask=mask)
    result[np.all(result != [0, 0, 0], axis=-1)] = [0, 255, 255]

    img[result != 0] = result[result != 0]

def get_humans_and_camps():
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    clean = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    grayed = cv2.cvtColor(clean, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(grayed, 127, 255, cv2.THRESH_BINARY)
    contours = cv2.findContours(
        thresh,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )[0]
    newcnt = []
    for i in range(len(contours)):
        epsilon = 0.04 * cv2.arcLength(contours[i], True)
        newcnt.append(cv2.approxPolyDP(contours[i], epsilon, True))
    
    ## FOR DEBUG, MARK ALL CONTOUR POINTS
    # for i in newcnt:
    #     clr = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    #     for j in i:
    #         cv2.circle(img, j[0], 4, clr, 1)

    for cnt in newcnt:
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        # cnt.shape[0] = number of points in the contour

        # if the contour is a circle (camp)

        if cnt.shape[0] not in [3, 4, 10]:
            clr = ""
            if MASK_CAMP_PINK[cy, cx]:
                clr = "pink"
            elif MASK_CAMP_GRAY[cy, cx]:
                clr = "gray"
            elif MASK_CAMP_BLUE[cy, cx]:
                clr = "blue"
            CAMPS[clr] = [cx, cy]

        # if the contour is not a circle (casualty)
        else: 
            severity = ""
            if MASK_SAFE[cy, cx]:
                severity = "safe"
            elif MASK_MODERATE[cy, cx]:
                severity = "moderate"
            elif MASK_SEVERE[cy, cx]:
                severity = "severe"

            match cnt.shape[0]:
                case 4:
                    CASUALTIES["adult"][severity].append((cx, cy))
                case 3:
                    CASUALTIES["elder"][severity].append((cx, cy))
                case 10:
                    CASUALTIES["child"][severity].append((cx, cy))

get_humans_and_camps()
# ground_overlay()

print("CASUALTIES: ", CASUALTIES)
print("CAMPS: ", CAMPS)
# cv2.imshow("RESULT", img)

# cv2.waitKey(0)
# cv2.destroyAllWindows()