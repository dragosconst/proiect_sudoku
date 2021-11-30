import numpy as np
import cv2.cv2 as cv
import os

CLASSIC_PATH = "././evaluare/fake_test/clasic/"
JIGSAW_PATH = "././evaluare/fake_test/jigsaw/"
IMG_EXTENSION = ".jpg"
CLASSIC = 0
JIGSAW = 1

CLASSIC_IMGS = 1
JIGSAW_IMGS = 1

"""
uses a flag variable to decide what images it needs to load, by default it loads the classic images
"""
def load_imgs(flag = CLASSIC):
    imgs = []
    list_dir = os.listdir(CLASSIC_PATH if flag == CLASSIC else JIGSAW_PATH)
    if flag == CLASSIC:
        CLASSIC_IMGS = len(list_dir)
    else:
        JIGSAW_IMGS = len(list_dir)
    for i in range(1, CLASSIC_IMGS + 1 if flag == CLASSIC else JIGSAW_IMGS + 1):
        i_char = str(i) if i >= 10 else "0" + str(i)
        img = cv.imread((CLASSIC_PATH if flag == CLASSIC else JIGSAW_PATH) + i_char + IMG_EXTENSION)
        img = cv.resize(img, (0, 0), fx=0.2, fy=0.2)
        imgs.append(img)
    return imgs

