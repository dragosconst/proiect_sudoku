import cv2.cv2 as cv
import numpy as np

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

    edges = cv.Canny(cv.bitwise_not(thresh), square.shape[0], square.shape[1])

    return thresh