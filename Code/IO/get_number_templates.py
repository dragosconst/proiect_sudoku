from Code.Data_Processing.get_squares import  AVG_SQUARE
import cv2.cv2 as cv
import numpy as np
import os
import errno

TEMP_FP = "././antrenare/clasic/templates/"
TEMP_J_BGR = "././antrenare/jigsaw/templates/bgr/"
TEMP_J_GRAY = "././antrenare/jigsaw/templates/gray/"
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


    for index, i in enumerate((one, two, three, four, five, six, seven, eight, nine)):
        cv.imwrite(TEMP_FP + str(index + 1) + EXT, i)


def get_j_bgr_templates(square_one):
    one   = square_one[3*AVG_SQUARE[0]:4*AVG_SQUARE[0], 5*AVG_SQUARE[1]:6*AVG_SQUARE[1]]
    two   = square_one[AVG_SQUARE[0]:2*AVG_SQUARE[0], 8*AVG_SQUARE[1]:9*AVG_SQUARE[1]]
    three = square_one[2*AVG_SQUARE[0]:3*AVG_SQUARE[0], AVG_SQUARE[1]:2*AVG_SQUARE[1]]
    four  = square_one[0*AVG_SQUARE[0]:AVG_SQUARE[0], 8*AVG_SQUARE[1]:9*AVG_SQUARE[1]]
    five  = square_one[AVG_SQUARE[0]:2*AVG_SQUARE[0], 6*AVG_SQUARE[1]:7*AVG_SQUARE[1]]
    six   = square_one[0:AVG_SQUARE[0], 3*AVG_SQUARE[1]:4*AVG_SQUARE[1]]
    seven = square_one[0*AVG_SQUARE[0]:1*AVG_SQUARE[0], 5*AVG_SQUARE[1]:6*AVG_SQUARE[1]]
    eight = square_one[3*AVG_SQUARE[0]:4*AVG_SQUARE[0], 2*AVG_SQUARE[1]:3*AVG_SQUARE[1]]
    nine  = square_one[1*AVG_SQUARE[0]:2*AVG_SQUARE[0], 2*AVG_SQUARE[1]:3*AVG_SQUARE[1]]

    try:
        os.makedirs(os.path.dirname(TEMP_J_BGR))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

    for index, i in enumerate((one, two, three, four, five, six, seven, eight, nine)):
        cv.imwrite(TEMP_J_BGR + str(index + 1) + EXT, i)


def get_j_gray_templates(square_one):
    one   = square_one[0*AVG_SQUARE[0]:1*AVG_SQUARE[0], 6*AVG_SQUARE[1]:7*AVG_SQUARE[1]]
    two   = square_one[AVG_SQUARE[0]:2*AVG_SQUARE[0], 0*AVG_SQUARE[1]:1*AVG_SQUARE[1]]
    three = square_one[3*AVG_SQUARE[0]:4*AVG_SQUARE[0], 7*AVG_SQUARE[1]:8*AVG_SQUARE[1]]
    four  = square_one[7*AVG_SQUARE[0]:8*AVG_SQUARE[0], 4*AVG_SQUARE[1]:5*AVG_SQUARE[1]]
    five  = square_one[AVG_SQUARE[0]:2*AVG_SQUARE[0], 4*AVG_SQUARE[1]:5*AVG_SQUARE[1]]
    six   = square_one[0:AVG_SQUARE[0], 3*AVG_SQUARE[1]:4*AVG_SQUARE[1]]
    seven = square_one[1*AVG_SQUARE[0]:2*AVG_SQUARE[0], 5*AVG_SQUARE[1]:6*AVG_SQUARE[1]]
    eight = square_one[4*AVG_SQUARE[0]:5*AVG_SQUARE[0], 7*AVG_SQUARE[1]:8*AVG_SQUARE[1]]
    nine  = square_one[3*AVG_SQUARE[0]:4*AVG_SQUARE[0], 3*AVG_SQUARE[1]:4*AVG_SQUARE[1]]

    try:
        os.makedirs(os.path.dirname(TEMP_J_GRAY))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

    for index, i in enumerate((one, two, three, four, five, six, seven, eight, nine)):
        cv.imwrite(TEMP_J_GRAY + str(index + 1) + EXT, i)

def load_templates_classic():
    temps = []
    for i in range(1, 10):
        temps.append(cv.cvtColor(cv.imread(TEMP_FP + str(i) + EXT), cv.COLOR_BGR2GRAY))
    return np.array(temps)

def load_templates_bgr():
    temps = []
    for i in range(1, 10):
        temps.append(cv.cvtColor(cv.imread(TEMP_J_BGR + str(i) + EXT), cv.COLOR_BGR2GRAY))
    return np.array(temps)

def load_templates_gray():
    temps = []
    for i in range(1, 10):
        temps.append(cv.cvtColor(cv.imread(TEMP_J_GRAY + str(i) + EXT), cv.COLOR_BGR2GRAY))
    return np.array(temps)
