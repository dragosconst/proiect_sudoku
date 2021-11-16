import cv2.cv2 as cv
import numpy as np
import os
import errno
from load_images import CLASSIC, JIGSAW


FILEPATH = "evaluare/fisiere_solutie/Tantaru_Dragos-Constantin_344/"
CLASSIC_PATH = "classic/"
JIGSAW_PATH = "jigsaw/"

def write_ans(answers, flag=CLASSIC):
    try:
        os.makedirs(os.path.dirname(FILEPATH))
        os.makedirs(os.path.dirname(FILEPATH + CLASSIC_PATH))
        os.makedirs(os.path.dirname(FILEPATH + JIGSAW_PATH))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

    index = 1
    for ans in answers:
        with open(FILEPATH + CLASSIC_PATH + str(index) + "_" + "predictie.txt", "w") as f:
            for line in ans:
                for char in line:
                    f.write(char)
                f.write('\n')
                f.flush()
        f.close()
        index += 1
