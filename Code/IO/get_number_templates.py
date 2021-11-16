from Code.Data_Processing.get_squares import  AVG_SQUARE
import cv2.cv2 as cv
import numpy as np
import os
import errno

TEMP_FP = "././antrenare/clasic/templates/"
EXT = ".jpg"

# this function should be called ONLY on square one, and ONLY after it is processed using the respective function
# from the get_squares file, and ONLY !!! once, calling it multiple times would be a waste of time
def get_templates(square_one):
    one   = square_one[3*AVG_SQUARE[0]:4*AVG_SQUARE[0], 5*AVG_SQUARE[1]:6*AVG_SQUARE[1]]
    two   = square_one[AVG_SQUARE[0]:2*AVG_SQUARE[0], 3*AVG_SQUARE[1]:4*AVG_SQUARE[1]]
    three = square_one[4*AVG_SQUARE[0]:5*AVG_SQUARE[0], 6*AVG_SQUARE[1]:7*AVG_SQUARE[1]]
    four  = square_one[AVG_SQUARE[0]:2*AVG_SQUARE[0], 2*AVG_SQUARE[1]:3*AVG_SQUARE[1]]
    five  = square_one[AVG_SQUARE[0]:2*AVG_SQUARE[0], AVG_SQUARE[1]:2*AVG_SQUARE[1]]
    six   = square_one[0:AVG_SQUARE[0], AVG_SQUARE[1]:2*AVG_SQUARE[1]]
    seven = square_one[2*AVG_SQUARE[0]:3*AVG_SQUARE[0], 0:AVG_SQUARE[1]]
    eight = square_one[0:AVG_SQUARE[0], 2*AVG_SQUARE[1]:3*AVG_SQUARE[1]]
    nine  = square_one[3*AVG_SQUARE[0]:4*AVG_SQUARE[0], 4*AVG_SQUARE[1]:5*AVG_SQUARE[1]]

    try:
        os.makedirs(os.path.dirname(TEMP_FP))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

    index = 1
    for i in (one, two, three, four, five, six, seven, eight, nine):
        cv.imwrite(TEMP_FP + str(index) + EXT, i)
        index += 1


def load_templates_classic():
    temps = []
    for i in range(1, 10):
        temps.append(cv.cvtColor(cv.imread(TEMP_FP + str(i) + EXT), cv.COLOR_BGR2GRAY))
    return np.array(temps)