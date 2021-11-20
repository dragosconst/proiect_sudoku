from Code.IO.get_number_templates import load_templates_classic, load_templates_gray, load_templates_bgr
from Code.Data_Processing.get_squares import AVG_SQUARE
from Code.Data_Processing.processing_squares import process_square
import cv2.cv2 as cv
import numpy as np

def check_square(square, ans, temp_classic, temp_j_bgr, temp_j_gray):
    sx, sy = AVG_SQUARE

    bonus = [["" for i in range(len(ans[0]))] for j in range(len(ans))]
    for i, line in enumerate(ans):
        for j, _ in enumerate(line):
            if ans[i][j] == "x":
                x, y = sx * j, sy * i
                patch = square[y:(y+sy), x:(x+sx)]
                max_val = None
                template = -1
                for templates in (temp_classic, temp_j_bgr, temp_j_gray):
                    index = 1
                    for t in templates:
                        min_t, max_t, min_l_t, max_l_t = cv.minMaxLoc(cv.matchTemplate(patch, t, cv.TM_CCOEFF_NORMED))
                        if max_val is None or max_t > max_val:
                            max_val = max_t
                            template = index
                        index += 1
                bonus[i][j] = str(template)
            else:
                bonus[i][j] = "o"

    return bonus


def check_templates(squares, answers):
    temp_classic = load_templates_classic()
    temp_j_bgr = load_templates_bgr()
    temp_j_gray = load_templates_gray()

    bonuses = []
    for i, _ in enumerate(squares):
        square = process_square(squares[i])
        ans = answers[i]

        bonus = check_square(square, ans, temp_classic, temp_j_bgr, temp_j_gray)
        bonuses.append(bonus)

    return bonuses
