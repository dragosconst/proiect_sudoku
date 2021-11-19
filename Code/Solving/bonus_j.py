from Code.IO.get_number_templates import load_templates_bgr, load_templates_gray
from Code.Data_Processing.get_squares import AVG_SQUARE
from Code.Data_Processing.processing_squares import process_square
import cv2.cv2 as cv
import numpy as np

def check_square_j(square, ans, templates):
    sx, sy = AVG_SQUARE

    bonus = [["" for i in range(len(ans[0]))] for j in range(len(ans))]
    for i in range(len(ans)):
        tj = 0 # use tj to ignore the numbers for the regions
        for j in range(len(ans[0])):
            if ans[i][j] == "x":
                x, y = sx * tj, sy * i
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
                tj += 1
            elif ans[i][j] == "o":
                bonus[i][j] = "o"
                tj += 1
            else: # region numbers
                bonus[i][j] = ans[i][j]

    return bonus


def check_templates_bgr(squares, answers):
    temp = load_templates_bgr()

    bonuses = []
    for i in range(len(squares)):
        square = process_square(squares[i])
        ans = answers[i]

        bonus = check_square_j(square, ans, temp)
        bonuses.append(bonus)

    return bonuses

def check_templates_gray(squares, answers):
    temp = load_templates_gray()

    bonuses = []
    for i in range(len(squares)):
        square = process_square(squares[i])
        ans = answers[i]

        bonus = check_square_j(square, ans, temp)
        bonuses.append(bonus)

    return bonuses