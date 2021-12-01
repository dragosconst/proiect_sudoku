import cv2.cv2 as cv
import numpy as np
from Code.IO.load_images import CLASSIC, JIGSAW

def normalize_image(img):
    noise = cv.dilate(img, np.ones((7,7),np.uint8))
    blur = cv.medianBlur(noise, 21)
    res = 255 - cv.absdiff(img, blur)
    no_shdw = cv.normalize(res,None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
    return no_shdw

# apply a couple filters to the square, to get a more useful image to work with
def process_square(square):
    square = cv.cvtColor(square, cv.COLOR_BGR2GRAY)
    square = normalize_image(square)
    square_m_blur = cv.medianBlur(square, 3)
    square_g_blur = cv.GaussianBlur(square_m_blur, (0, 0), 7)
    square_sharpened = cv.addWeighted(square_m_blur, 1.35, square_g_blur, -0.85, 0)
    _, thresh = cv.threshold(square_sharpened, 5, 255, cv.THRESH_BINARY)

    return thresh


# this will only leave the thick lines
def process_square_j_bgr(square):
    square = cv.cvtColor(square, cv.COLOR_BGR2GRAY)
    square = normalize_image(square)
    square_m_blur = cv.medianBlur(square, 7)
    square_g_blur = cv.GaussianBlur(square_m_blur, (0, 0), 7)
    square_sharpened = cv.addWeighted(square_m_blur, 1.35, square_g_blur, -0.85, 0)
    _, thresh = cv.threshold(square_sharpened, 5, 255, cv.THRESH_BINARY)

    kernel = np.ones((3, 3), np.uint8)
    thresh = cv.dilate(thresh, kernel)

    return thresh

def process_square_j_gray(square):
    square = cv.cvtColor(square, cv.COLOR_BGR2GRAY)
    square = normalize_image(square)
    square_m_blur = cv.medianBlur(square, 5)
    square_g_blur = cv.GaussianBlur(square_m_blur, (0, 0), 7)
    square_sharpened = cv.addWeighted(square_m_blur, 1.35, square_g_blur, -0.85, 0)
    _, thresh = cv.threshold(square_sharpened, 5, 255, cv.THRESH_BINARY)

    kernel = np.ones((3, 3), np.uint8)
    thresh = cv.dilate(thresh, kernel)
    thresh = cv.erode(thresh, kernel)

    return thresh

