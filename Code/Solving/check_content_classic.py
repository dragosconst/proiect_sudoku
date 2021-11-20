import cv2.cv2 as cv
import numpy as np
from Code.Data_Processing.get_squares import RESIZED_SQ, AVG_SQUARE
from Code.Data_Processing.processing_squares import  *


def check_square(square):
    square = process_square(square)
    ans = [["" for i in range(9)] for j in range(9)]
    dx, dy = RESIZED_SQ
    stepx, stepy = AVG_SQUARE
    i, j = 0, 0

    for yi in range(0, dy, stepy):
        if yi + stepy >= dy: # skip bottom part of image
            continue
        j = 0
        for xi in range(0, dx, stepx):
            if xi + stepx >= dx: # last bit of the square is uninteresting
                continue
            current_patch = square[yi:yi+stepy, xi:xi+stepx]
            center_patch = square[(yi+stepy//4):(yi+stepy*3//4), (xi+stepx//4):(xi+stepx*3//4)]
            mean_center_patch = np.mean(center_patch.squeeze())
            # print(mean_center_patch)
            if mean_center_patch < 255:
                # print(mean_center_patch)
                # print("IO think it's full")
                ans[i][j] = "x"
            else:
                # print(mean_center_patch)
                # print("IO think it's empty")
                ans[i][j] = "o"
            j += 1
        i += 1
    return ans

def check_all_squares(squares):
    answers = []
    for square in squares:
        answers.append(check_square(square))
    return answers
