import cv2.cv2 as cv
import numpy as np
from get_squares import RESIZED_SQ, AVG_SQUARE

# apply a couple filters to the square, to get a more useful image to work with
def process_square(square):
    square = cv.cvtColor(square, cv.COLOR_BGR2GRAY)
    square_m_blur = cv.medianBlur(square, 3)
    square_g_blur = cv.GaussianBlur(square_m_blur, (0, 0), 7)
    square_sharpened = cv.addWeighted(square_m_blur, 1.35, square_g_blur, -0.85, 0)
    _, thresh = cv.threshold(square_sharpened, 5, 255, cv.THRESH_BINARY)
    return thresh



def check_square(square):
    square = process_square(square)
    cv.imshow("patch", square)
    cv.waitKey(0)
    cv.destroyAllWindows()
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
                # check if it's not centered
                # we'll start translating towards all four corners
                # print(mean_center_patch)
                # print("I think it's full")
                ans[i][j] = "x"
            else:
                # print(mean_center_patch)
                # print("I think it's empty")
                ans[i][j] = "o"

            if i == 7 and j == 6:
                cv.imshow("patch", current_patch)
                cv.waitKey(0)
                cv.destroyAllWindows()
            j += 1
        i += 1
    return ans

def check_all_squares(squares):
    answers = []
    for square in squares:
        answers.append(check_square(square))
    return answers
