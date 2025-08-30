#! /usr/bin/env python3
import cv2
import numpy as np
from functions import ground_overlay, get_humans_and_camps, get_priority_for_all_points

if __name__ == "__main__":
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

    img: np.ndarray = cv2.imread("assets/3.png", cv2.IMREAD_COLOR)
    assert img is not None, "Failed to read image"

    # MAIN STORAGE OF THE DATA FROM THE IMAGE
    CASUALTIES: list[tuple[tuple[int, int], int, int]] = []
    CAMPS: dict[str, tuple[int, int]] = {"pink": (0, 0), "blue": (0, 0), "gray": (0, 0)}
    FINAL_CAMP_ASSIGNMENT: dict[str, list[tuple[tuple[int, int], int, int, float]]] = {
        "pink": [],
        "blue": [],
        "gray": [],
    }
    get_humans_and_camps(img, CAMPS, CASUALTIES)
    ground_overlay(img)

    PINK_POINTS, BLUE_POINTS, GRAY_POINTS = get_priority_for_all_points(
        CAMPS, CASUALTIES
    )
    for i in range(len(CASUALTIES)):
        if i % 3 == 0: # PINK
            maxidx = PINK_POINTS.index(max(PINK_POINTS))
        elif i % 3 == 1: # BLUE
            maxidx = BLUE_POINTS.index(max(BLUE_POINTS))
        else:
            maxidx = GRAY_POINTS.index(max(GRAY_POINTS))
        _ = (
            PINK_POINTS[maxidx] if len(FINAL_CAMP_ASSIGNMENT["pink"]) != 3 else 0,
            BLUE_POINTS[maxidx] if len(FINAL_CAMP_ASSIGNMENT["blue"]) != 4 else 0,
            GRAY_POINTS[maxidx] if len(FINAL_CAMP_ASSIGNMENT["gray"]) != 2 else 0
        )
        clr, points = "", 0.0
        match _.index(max(_)):
            case 0:
                clr = "pink"
                points = PINK_POINTS[maxidx]
            case 1:
                clr = "blue"
                points = BLUE_POINTS[maxidx]
            case 2:
                clr = "gray"
                points = GRAY_POINTS[maxidx]

        FINAL_CAMP_ASSIGNMENT[clr].append((
            CASUALTIES[maxidx][0],
            CASUALTIES[maxidx][1],
            CASUALTIES[maxidx][2],
            points
        ))
        PINK_POINTS.pop(maxidx)
        BLUE_POINTS.pop(maxidx)
        GRAY_POINTS.pop(maxidx)
        CASUALTIES.pop(maxidx)
    
    for i in FINAL_CAMP_ASSIGNMENT:
        for j in FINAL_CAMP_ASSIGNMENT[i]:
            cv2.line(img, CAMPS[i], j[0], (0, 0, 255), 3)


    a = [[], [], []]
    for i in FINAL_CAMP_ASSIGNMENT["blue"]:
        a[0].append([i[1], i[2]])
    for i in FINAL_CAMP_ASSIGNMENT["pink"]:
        a[1].append([i[1], i[2]])
    for i in FINAL_CAMP_ASSIGNMENT["gray"]:
        a[2].append([i[1], i[2]])
    print(a)

    cv2.imshow("RESULT", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()