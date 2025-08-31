#! /usr/bin/env python3
import cv2, os
import numpy as np
from pprint import pprint
from functions import ground_overlay, get_humans_and_camps, get_priority_for_all_points

DEBUG = True

if __name__ == "__main__":
    # Path to images to analyse
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

    # Analysed images
    OUTPUT_IMAGES_LIST: list[np.ndarray] = []

    # List of assigned camps to a casualty
    # {
    #     "image1.png": {
    #         "blue": [
    #             (...), ...
    #         ],
    #         "pink": {
    #             ...
    #         }
    #     }
    # }
    CASUALTY_ASSIGNMENT_DEETS: dict[str, dict[str, list[tuple[int, int]]]] = dict()

    # Sum of priority scores
    CAMP_PRIORITY_SCORES_TOTAL: dict[str, dict[str, int]] = dict()
    CAMP_PRIORITY_SCORES_AVG: dict[str, float] = dict()

    for path in IMAGES:
        if DEBUG:
            print(f"[+] DEBUG: READING IMAGE {path}")
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        assert img is not None, f"Failed to read image on path {path}"

        # MAIN STORAGE OF THE DATA FROM THE IMAGE
        # CASUALTIES: [((x, y), age_grp, severity), ...]
        CASUALTIES: list[tuple[tuple[int, int], int, int]] = []

        # CAMPS: {"campcolor": (x, y), ...}
        CAMPS: dict[str, tuple[int, int]] = {"pink": (0, 0), "blue": (0, 0), "gray": (0, 0)}

        # FINAL_CAMP_ASSIGNMENT: {"campcolor": [((x, y), age_grp, severity, campscore), ...]}
        FINAL_CAMP_ASSIGNMENT: dict[str, list[tuple[tuple[int, int], int, int, float]]] = {
            "pink": [],
            "blue": [],
            "gray": [],
        }

        # This function analyses the casualties and camps in the photo
        # and puts the data in CAMPS and CASUALTIES.
        get_humans_and_camps(img, CAMPS, CASUALTIES)
        # Puts a yellow overlay on the ground area
        ground_overlay(img)

        PINK_POINTS, BLUE_POINTS, GRAY_POINTS = get_priority_for_all_points(
            CAMPS, CASUALTIES
        )
        NCASUALTY = len(CASUALTIES)
        for i in range(NCASUALTY):
            if i % 3 == 0:  # PINK
                maxidx = PINK_POINTS.index(max(PINK_POINTS))
            elif i % 3 == 1:  # BLUE
                maxidx = BLUE_POINTS.index(max(BLUE_POINTS))
            else: # GRAY
                maxidx = GRAY_POINTS.index(max(GRAY_POINTS))
            _ = (
                PINK_POINTS[maxidx] if len(FINAL_CAMP_ASSIGNMENT["pink"]) != 3 else 0,
                BLUE_POINTS[maxidx] if len(FINAL_CAMP_ASSIGNMENT["blue"]) != 4 else 0,
                GRAY_POINTS[maxidx] if len(FINAL_CAMP_ASSIGNMENT["gray"]) != 2 else 0,
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
                points,
            ))
            
            cv2.line(img, CAMPS[clr], CASUALTIES[maxidx][0], (0, 0, 255), 3)

            PINK_POINTS.pop(maxidx)
            BLUE_POINTS.pop(maxidx)
            GRAY_POINTS.pop(maxidx)
            CASUALTIES.pop(maxidx)
        
        OUTPUT_IMAGES_LIST.append(img)

        camp_scores: dict[str, list[tuple[int, int]]] = {
            "blue": [],
            "pink": [],
            "gray": []
        }
        camp_sum: dict[str, int] = {
            "blue": 0,
            "pink": 0,
            "gray": 0
        }
        camp_sum_avg = 0.0

        for i in FINAL_CAMP_ASSIGNMENT["blue"]:
            camp_scores["blue"].append((i[1], i[2]))
            camp_sum["blue"] += i[1]*i[2]
        for i in FINAL_CAMP_ASSIGNMENT["pink"]:
            camp_scores["pink"].append((i[1], i[2]))
            camp_sum["pink"] += i[1]*i[2]
        for i in FINAL_CAMP_ASSIGNMENT["gray"]:
            camp_scores["gray"].append((i[1], i[2]))
            camp_sum["gray"] += i[1]*i[2]
        
        camp_sum_avg = sum(camp_sum.values())/NCASUALTY

        image_name = os.path.basename(path)
        CASUALTY_ASSIGNMENT_DEETS[image_name] = camp_scores
        CAMP_PRIORITY_SCORES_TOTAL[image_name] = camp_sum
        CAMP_PRIORITY_SCORES_AVG[image_name] = camp_sum_avg

        cv2.imwrite(f"assets/outputs/{os.path.basename(path)}", img)

    print("CASUALTY CAMP ASSIGNMENT:", "="*15)
    pprint(CASUALTY_ASSIGNMENT_DEETS)

    print("CAMP PRIORITY SCORES (TOTAL) ", "="*15)
    pprint(CAMP_PRIORITY_SCORES_TOTAL)

    print("CAMP PRIORITY SCORES (AVERAGE) ", "="*15)
    pprint(CAMP_PRIORITY_SCORES_AVG)

    
    print("Images in order based on avg priority scores", "="*15)
    pprint([k for k, v in sorted(CAMP_PRIORITY_SCORES_AVG.items(), key=lambda item: item[1])])

    print("The output images have been dumped in the folder: assets/outputs")