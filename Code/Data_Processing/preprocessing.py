import numpy as np
import cv2.cv2 as cv
from Code.IO.load_images import CLASSIC, JIGSAW


def show_image(title,image):
    cv.imshow(title,image)
    cv.waitKey(0)
    cv.destroyAllWindows()

# almost perfect values, I think --> could mean overfitting
def preprocess_image(image, flag=CLASSIC):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image_m_blur = cv.medianBlur(image, 3)
    image_g_blur = cv.GaussianBlur(image_m_blur, (0, 0), 7)
    image_sharpened = cv.addWeighted(image_m_blur, 1.35, image_g_blur, -0.85, 0)
    _, thresh = cv.threshold(image_sharpened, 5, 255, cv.THRESH_BINARY)

    kernel = np.ones((5, 5), np.uint8)
    thresh = cv.erode(thresh, kernel)

    # show_image("median blurred", image_m_blur)
    # show_image("gaussian blurred", image_g_blur)
    # show_image("sharpened", image_sharpened)
    # show_image("threshold of blur", thresh)

    edges = cv.Canny(thresh, 150, 400)
    contours, con = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_area = 0

    for i in range(len(contours)):
        if (len(contours[i]) > 3):
            possible_top_left = None
            possible_bottom_right = None
            for point in contours[i].squeeze():
                if possible_top_left is None or point[0] + point[1] < possible_top_left[0] + possible_top_left[1]:
                    possible_top_left = point

                if possible_bottom_right is None or point[0] + point[1] > possible_bottom_right[0] + \
                        possible_bottom_right[1]:
                    possible_bottom_right = point

            diff = np.diff(contours[i].squeeze(), axis=1)
            possible_top_right = contours[i].squeeze()[np.argmin(diff)]
            possible_bottom_left = contours[i].squeeze()[np.argmax(diff)]
            if cv.contourArea(np.array([[possible_top_left], [possible_top_right], [possible_bottom_right],
                                        [possible_bottom_left]])) > max_area:
                max_area = cv.contourArea(np.array(
                    [[possible_top_left], [possible_top_right], [possible_bottom_right], [possible_bottom_left]]))
                top_left = possible_top_left
                bottom_right = possible_bottom_right
                top_right = possible_top_right
                bottom_left = possible_bottom_left

    image_copy = cv.cvtColor(image.copy(), cv.COLOR_GRAY2BGR)
    cv.circle(image_copy, tuple(top_left), 4, (0, 0, 255), -1)
    cv.circle(image_copy, tuple(top_right), 4, (0, 255, 0), -1)
    cv.circle(image_copy, tuple(bottom_left), 4, (255, 0, 0), -1)
    cv.circle(image_copy, tuple(bottom_right), 4, (0, 255, 255), -1)
    # if flag == JIGSAW:
    #     show_image("detected corners", image_copy)

    return top_left, top_right, bottom_left, bottom_right