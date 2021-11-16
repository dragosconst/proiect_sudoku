import cv2.cv2 as cv
import numpy as np
from load_images import load_imgs
from preprocessing import *
from get_squares import *
from check_content_classic import check_all_squares, check_square
from write_results import write_ans
from validate_training import check_results

__all__ = [cv, np]

imgs = load_imgs()
sudoku_squares = crop_squares(imgs, len(imgs))
sudoku_squares = resize_squares(sudoku_squares)
check_square(sudoku_squares[11])

lines_vertical=[]
ind = 0
for i in range(10,500,55):
    l=[]
    if i % 10 == 0:
        ind += 1
    l.append((i,0))
    l.append((i,499))
    lines_vertical.append(l)
    ind += 55

ind = 0
lines_horizontal=[]
for i in range(0,500,55):
    l=[]
    if i % 10 == 0:
        ind += 1
    l.append((0,i))
    l.append((499,i))
    lines_horizontal.append(l)
    ind += 55

for line in  lines_vertical :
    cv.line(sudoku_squares[11], line[0], line[1], (0, 255, 0), 5)
for line in  lines_horizontal :
    cv.line(sudoku_squares[11], line[0], line[1], (0, 0, 255), 5)
cv.imshow("img", sudoku_squares[11])
cv.waitKey(0)
cv.destroyAllWindows()

answers = check_all_squares(sudoku_squares)
check_results(answers)
write_ans(answers)

img = imgs[0]
img_crop = cv.imread("antrenare/cropped/01.jpg")
img_crop = cv.resize(img_crop, (500, 500))

lines_vertical=[]
for i in range(0,500,55):
    l=[]
    l.append((i,0))
    l.append((i,499))
    lines_vertical.append(l)

lines_horizontal=[]
for i in range(0,500,55):
    l=[]
    l.append((0,i))
    l.append((499,i))
    lines_horizontal.append(l)

for line in  lines_vertical :
    cv.line(img_crop, line[0], line[1], (0, 255, 0), 5)
for line in  lines_horizontal :
    cv.line(img_crop, line[0], line[1], (0, 0, 255), 5)
cv.imshow("img", img_crop)
cv.waitKey(0)
cv.destroyAllWindows()


def get_results(img,lines_horizontal,lines_vertical):
    for i in range(len(lines_horizontal) - 1):
        for j in range(len(lines_vertical) - 1):
            y_min = lines_vertical[j][0][0]
            y_max = lines_vertical[j + 1][1][0]
            x_min = lines_horizontal[i][0][1]
            x_max = lines_horizontal[i + 1][1][1]
            patch = img_crop[x_min:x_max, y_min:y_max].copy()
            cv.imshow("patch", patch)
            cv.waitKey(0)
            cv.destroyAllWindows()

get_results(img,lines_horizontal,lines_vertical)


