import cv2.cv2 as cv
import numpy as np

THRESH_COLOR = 33
GRAY = 0
BGR = 1
# simple function to check whether a loaded image is grayscale or not
def is_gray(img):
    if(len(img.shape) < 3):
        return True
    if img.shape[2] == 1:
        return True
    b, g, r = img[:, : ,0], img[:, :, 1], img[:, :, 2]
    if np.max(cv.absdiff(b, g)) <= THRESH_COLOR and np.max(cv.absdiff(g, r)) <= THRESH_COLOR:
        return True
    return False

def sort_colors(imgs):
    imgs_gray = []
    imgs_bgr = []
    imgs_pos = [] # a list of (type, pos) tuples, where type is which list it's part of (bgr or gray)
                  # and pos is the position in that list

    i_b = 0
    i_g = 0
    for img in imgs:
        if is_gray(img):
            imgs_gray.append(img)
            imgs_pos.append((GRAY, i_g))
            i_g += 1
        else:
            imgs_bgr.append(img)
            imgs_pos.append((BGR, i_b))
            i_b += 1


    return imgs_gray, imgs_bgr, imgs_pos