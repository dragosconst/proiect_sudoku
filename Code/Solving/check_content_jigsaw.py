import cv2.cv2 as cv
import numpy as np
import math
from Code.Data_Processing.get_squares import RESIZED_SQ, AVG_SQUARE
from Code.Data_Processing.processing_squares import  *

LEFT_BORDER  = 2 ** 0
RIGHT_BORDER = 2 ** 1
UP_BORDER    = 2 ** 2
BOT_BORDER   = 2 ** 3


def check_square_j_gray(square):
    square_only_lines = process_square_j_gray(square)
    square = process_square(square)
    cv.imshow("square", square_only_lines)
    cv.waitKey(0)
    cv.destroyAllWindows()
    ans = [["" for i in range(9)] for j in range(9)]
    blocks = np.zeros((9, 9), np.uint8) # a matrix containing all the blocking walls

    dx, dy = RESIZED_SQ
    stepx, stepy = AVG_SQUARE
    i, j = 0, 0

    regions = dict()
    regions_patches = np.zeros((9, 9), np.uint8)  # region of every patch
    last_region = 1

    for yi in range(0, dy, stepy):
        if yi + stepy >= dy: # skip bottom part of image
            continue
        j = 0
        for xi in range(0, dx, stepx):
            if xi + stepx >= dx: # last bit of the square is uninteresting
                continue
            current_patch = square[yi:yi+stepy, xi:xi+stepx]
            # center_patch = square[(yi+stepy//3):(yi+stepy*7//8), (xi+stepx//6):(xi+stepx*5//6)]
            center_patch = square[(yi+stepy//4):(yi+stepy*3//4), (xi+stepx//4):(xi+stepx*3//4)]
            mean_center_patch = np.mean(center_patch.squeeze())
            borders = look_for_borders(square_only_lines[yi:yi+stepy, xi:xi+stepx])
            mark_borders(blocks, i, j, borders)

            last_region = check_patch_borders(i, j, blocks, regions, regions_patches, last_region)
            # print(mean_center_patch)
            if mean_center_patch < 255:
                # check if it's not centered
                # we'll start translating towards all four corners
                # print(mean_center_patch)
                # print("IO think it's full")
                ans[i][j] = "x"
            else:
                # print(mean_center_patch)
                # print("IO think it's empty")
                ans[i][j] = "o"
            j += 1
        i += 1

    reassign_regions(regions, regions_patches)
    merge_answer_and_regions(ans, regions_patches)
    return ans

def check_all_squares_j_gray(squares):
    answers = []
    for square in squares:
        answers.append(check_square_j_gray(square))
    return answers

def look_for_borders(patch):
    # the patch is already processed from the check square function, we can directly look for contours
    patch_resized = cv.resize(patch, (0, 0), fx=5, fy=5)
    # should erode, maybe?
    edges = cv.Canny(patch_resized, 150, 400)
    edges_color = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
    lines = cv.HoughLines(edges, 1, np.pi / 180, 100, None, 0, 0)
    lb, rb, ub, bb = False, False, False, False
    if lines is not None:
        for i in range(0, len(lines)):
            # lines are only going to be detected on borders, we have to look only at rho and theta to get an idea
            # of which border it is
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            # stuff for showing the lines, for debugging
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))

            if np.isclose(0, theta):
                # left or right border
                if rho < patch_resized.shape[0] / 5: # left border
                    lb = True
                    cv.line(edges_color, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)
                elif rho >= patch_resized.shape[0] * 4 / 5:
                    rb = True
                    cv.line(edges_color, pt1, pt2, (0, 255, 0), 3, cv.LINE_AA)
            else: # i won't check for it, but logically theta should be close to np.pi / 2
                # up or down border
                if rho < patch_resized.shape[1] / 5:
                    ub = True
                    cv.line(edges_color, pt1, pt2, (255, 0, 0), 3, cv.LINE_AA)
                elif rho >= patch_resized.shape[1] * 4 / 5:
                    bb = True
                    cv.line(edges_color, pt1, pt2, (0, 255, 255), 3, cv.LINE_AA)
    # cv.imshow("original peci", patch_resized)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    # cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", edges_color)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return lb, rb, ub, bb

# function to mark borders in the blocks matrix
def mark_borders(blocks, i, j, borders):
    (lb, rb, ub , bb) = borders
    if lb:
        blocks[i][j] |= LEFT_BORDER
        if j > 0:
            blocks[i][j - 1] |= RIGHT_BORDER
    if rb:
        blocks[i][j] |= RIGHT_BORDER
        if j < len(blocks[0]) - 1:
            blocks[i][j + 1] |= LEFT_BORDER
    if ub:
        blocks[i][j] |= UP_BORDER
        if i > 0:
            blocks[i - 1][j] |= BOT_BORDER
    if bb:
        blocks[i][j] |= BOT_BORDER
        if i < len(blocks) - 1:
            blocks[i + 1][j] |= UP_BORDER

def check_patch_borders(i, j, blocks, regions, regions_patches, last_region):
    """
    Due to the manner in which we traverse the sudoku square, from top-left to bottom-right,
    it shoulde be impossible that when we are at a give point, we haven't already detected all possible
    borders to the adjacent regions calculated until this step. The only case when this could arrise is
    by a problem with accurately determining where the borders are, but that's out of the scope of the
    region-merging algorithm.
    """
    if i == 0 and j == 0:
        regions[last_region] = 1
        last_region += 1
        regions_patches[i][j] = 1
    else:
        cr_region = None
        if not (blocks[i][j] & LEFT_BORDER):
            # if there is no left border, try merging with left region
            if j > 0:
                cr_region = regions_patches[i][j - 1]
        if not (blocks[i][j] & UP_BORDER):
            # try merging with region above
            if i > 0:
                pos_region = regions_patches[i - 1][j]
                if cr_region is None:
                    cr_region = pos_region
                elif cr_region < pos_region:  # merge regions
                    # possibly not necessary, but merge all regions that had the respective root
                    for region, root in regions.items():
                        if root == regions[pos_region]:
                            regions[region] = regions[cr_region]
                    regions[pos_region] = regions[cr_region]
                else:
                    for region, root in regions.items():
                        if root == regions[cr_region]:
                            regions[region] = regions[pos_region]
                    regions[cr_region] = regions[pos_region]
        if cr_region is None:
            # add a new region if it can't reach any new region
            regions[last_region] = last_region
            cr_region = last_region
            last_region += 1
        regions_patches[i][j] = cr_region
    return last_region

def reassign_regions(regions, regions_patches):
    unique_regions = dict()
    unique_so_far = 0
    for i, line in enumerate(regions_patches):
        for j, _ in enumerate(line):
            if regions[regions_patches[i][j]] not in unique_regions:
                unique_so_far += 1
                unique_regions[regions[regions_patches[i][j]]] = unique_so_far
            regions_patches[i][j] = unique_regions[regions[regions_patches[i][j]]]

def merge_answer_and_regions(answer, regions_patches):
    for i, line in enumerate(regions_patches):
        new_line = ""
        for j, patch in enumerate(regions_patches):
            new_line += str(regions_patches[i][j])
            new_line += str(answer[i][j])
        answer[i] = []
        answer[i][:] = new_line

def check_square_j_bgr(square):
    square_only_lines = process_square_j_bgr(square)
    # cv.imshow("bossultan", square_only_lines)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    square = process_square(square)
    ans = [["" for i in range(9)] for j in range(9)]
    blocks = np.zeros((9, 9), np.uint8) # a matrix containing all the blocking walls

    # with the following encoding = ...0000 means no blocks, ...0001 means lb, ...0010 means rb, ...0100 means ub, ...1000 means db and any combinations have their obvious meanings
    dx, dy = RESIZED_SQ
    stepx, stepy = AVG_SQUARE
    i, j = 0, 0

    # i will keep the regions in a hash table and use the following algorithm for merging adjacent regions:
    # 1. regions[i] stores the "true" value of the region i, i.e. the smallest region it, or one of its neighbours
    # is adjacent to
    # 2. if two regions have to be merged, the smaller value will be used, and we will iterate through the regions\
    # and change all occurences of the other value
    regions = dict()
    regions_patches = np.zeros((9, 9), np.uint8)  # region of every patch
    last_region = 1
    for yi in range(0, dy, stepy):
        if yi + stepy >= dy: # skip bottom part of image
            continue
        j = 0
        for xi in range(0, dx, stepx):
            if xi + stepx >= dx: # last bit of the square is uninteresting
                continue
            current_patch = square[yi:yi+stepy, xi:xi+stepx]
            center_patch = square[(yi+stepy//4):(yi+stepy*3//4), (xi+stepx//4):(xi+stepx*3//4)]
            mean_center_patch = np.mean(center_patch.squeeze())
            borders = look_for_borders(square_only_lines[yi:yi+stepy, xi:xi+stepx])
            mark_borders(blocks, i, j, borders)
            # cv.imshow("peci", cv.resize(current_patch, (0, 0), fx=5, fy=5))
            # cv.waitKey(0)
            # cv.destroyAllWindows()
            # print(mean_center_patch)
            last_region = check_patch_borders(i, j, blocks, regions, regions_patches, last_region)

            if mean_center_patch < 255:
                # check if it's not centered
                # we'll start translating towards all four corners
                # print(mean_center_patch)
                # print("IO think it's full")
                ans[i][j] = "x"
            else:
                # print(mean_center_patch)
                # print("IO think it's empty")
                ans[i][j] = "o"
            j += 1
        i += 1

    # rewrite the regions_patches matrix, so it contains the regions ordered by the order given in the task
    reassign_regions(regions, regions_patches)
    merge_answer_and_regions(ans, regions_patches)
    return ans

def check_all_squares_j_bgr(squares):
    answers = []
    for square in squares:
        answers.append(check_square_j_bgr(square))
    return answers

def merge_answers(ans_g, ans_bgr, positions):
    answers = []
    for (which, where) in positions:
        if which == 0:
            answers.append(ans_g[where])
        else:
            answers.append(ans_bgr[where])
    return answers
