import numpy as np
import cv2.cv2 as cv

CLASSIC_PATH = "antrenare/clasic/"
JIGSAW_PATH = "antrenare/jigsaw/"
IMG_EXTENSION = ".jpg"
CLASSIC = 0
JIGSAW = 1

"""
uses a flag variable to decide what images it needs to load, by default it loads the classic images
"""
def load_imgs(flag = CLASSIC):
    imgs = []
    for i in range(1, 21):
        i_char = str(i) if i >= 10 else "0" + str(i)
        img = cv.imread((CLASSIC_PATH if flag == CLASSIC else JIGSAW_PATH) + i_char + IMG_EXTENSION)
        img = cv.resize(img, (0, 0), fx=0.2, fy=0.2) # why??
        imgs.append(img)
    return imgs

