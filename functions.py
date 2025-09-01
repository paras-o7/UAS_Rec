import cv2
import numpy as np

__COLOR_RANGE = {
    "severe": (
        np.array([130, 150, 230], np.uint8),
        np.array([210, 210, 255], np.uint8),
    ),
    "moderate": (
        np.array([70, 180, 220], np.uint8),
        np.array([100, 230, 255], np.uint8),
    ),
    "safe": (
        np.array([100, 232, 180], np.uint8),
        np.array([130, 255, 200], np.uint8)
    ),
    "camp_pink": (
        np.array([255, 140, 220], np.uint8),
        np.array([255, 200, 255], np.uint8),
    ),
    "camp_blue": (
        np.array([255, 150, 100], np.uint8),
        np.array([255, 240, 200], np.uint8),
    ),
    "camp_gray": (
        np.array([205, 205, 210], np.uint8),
        np.array([230, 230, 230], np.uint8),
    ),
}


def ground_overlay(img: np.ndarray) -> None:
    lower_green = np.array([10, 100, 10], np.uint8)
    upper_green = np.array([70, 200, 60], np.uint8)
    mask = cv2.inRange(img, lower_green, upper_green)
    result = cv2.bitwise_and(img, img, mask=mask)
    result[np.all(result != [0, 0, 0], axis=-1)] = [0, 255, 255]

    img[result != 0] = result[result != 0]


def get_humans_and_camps(
    img: np.ndarray,
    camps: dict[str, tuple[int, int]],
    casualties: list[tuple[tuple[int, int], int, int]],
) -> None:
    MASK_SEVERE = cv2.inRange(
        img, __COLOR_RANGE["severe"][0], __COLOR_RANGE["severe"][1]
    )
    MASK_MODERATE = cv2.inRange(
        img, __COLOR_RANGE["moderate"][0], __COLOR_RANGE["moderate"][1]
    )
    MASK_SAFE = cv2.inRange(
        img, __COLOR_RANGE["safe"][0], __COLOR_RANGE["safe"][1]
    )
    MASK_CAMP_PINK = cv2.inRange(
        img, __COLOR_RANGE["camp_pink"][0], __COLOR_RANGE["camp_pink"][1]
    )
    MASK_CAMP_GRAY = cv2.inRange(
        img, __COLOR_RANGE["camp_gray"][0], __COLOR_RANGE["camp_gray"][1]
    )
    MASK_CAMP_BLUE = cv2.inRange(
        img, __COLOR_RANGE["camp_blue"][0], __COLOR_RANGE["camp_blue"][1]
    )

    # Improve image for better contour detection
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    clean = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)


    grayed = cv2.cvtColor(clean, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(grayed, 127, 255, cv2.THRESH_BINARY)
    contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

    for i in range(len(contours)):
        # Approximate the polygons
        epsilon = 0.04 * cv2.arcLength(contours[i], True)
        cnt = cv2.approxPolyDP(contours[i], epsilon, True)

        M = cv2.moments(cnt)

        if cnt.shape[0] <= 2:
            continue

        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

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
            assert (
                clr != ""
            ), f"Failed to identify an unknown contour as a camp, COM: ({cx, cy}), maybe check camp mask ranges?"
            camps[clr] = (cx, cy)

        # if the contour is not a circle (casualty)
        else:
            severity = 0
            age_grp = 0

            if MASK_SAFE[cy, cx]:
                severity = 1
            elif MASK_MODERATE[cy, cx]:
                severity = 2
            elif MASK_SEVERE[cy, cx]:
                severity = 3

            assert (
                severity != 0
            ), f"Failed to get severity info on a casualty, COM: ({cx}, {cy}), maybe check the severity mask ranges?"

            match cnt.shape[0]:
                case 4:
                    age_grp = 1
                case 3:
                    age_grp = 2
                case 10:
                    age_grp = 3

            assert age_grp != 0, "Failed to identify the shape of a contour"

            casualties.append(((cx, cy), age_grp, severity))


# Gets priority of all casualties relative to a camp
def get_priority_for_all_points(
    campCoords: dict[str, tuple[int, int]],
    casualties: list[tuple[tuple[int, int], int, int]],
) -> list[list[float]]:
    priorities: list[list[float]] = []
    for camp in campCoords:
        x, y = campCoords[camp]
        p: list[float] = []
        for victim in casualties:
            vx, vy = victim[0]
            dst = float(((vx - x) ** 2 + (vy - y) ** 2) ** 0.5)
            priority = (victim[1] * victim[2]) / dst**0.5
            p.append(priority)

        priorities.append(p)

    return priorities
