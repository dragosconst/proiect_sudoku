from Code.IO.get_number_templates import load_templates_classic
from Code.Data_Processing.get_squares import AVG_SQUARE
from Code.Data_Processing.processing_squares import process_square
import cv2.cv2 as cv
import numpy as np

def check_square(square, ans, templates):
    sx, sy = AVG_SQUARE

    bonus = [["" for i in range(len(ans[0]))] for j in range(len(ans))]
    for i in range(len(ans)):
        for j in range(len(ans[0])):
            if ans[i][j] == "x":
                x, y = sx * j, sy * i
                patch = square[y:(y+sy), x:(x+sx)]
                max_val = None
                template = -1
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
    temp = load_templates_classic()

    bonuses = []
    for i in range(len(squares)):
        square = process_square(squares[i])
        ans = answers[i]

        bonus = check_square(square, ans, temp)
        bonuses.append(bonus)

    return bonuses
