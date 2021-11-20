from Code.Data_Processing.preprocessing import *
from Code.IO.load_images import CLASSIC

THRESHOLD_ROTATE = 10
RESIZED_SQ = (500, 500)
AVG_SQUARE = (RESIZED_SQ[0] // 9, RESIZED_SQ[1] // 9)

def crop_squares(imgs, flag=CLASSIC):
    sudoku_squares = []
    for ind, img in enumerate(imgs):
        # print(ind + 1)
        (tlx, tly), (trx, trry), (blx, bly), (brx, bry) = preprocess_image(img, flag)
        x0 = np.min(np.array([tlx, blx]))
        y0 = np.min(np.array([tly, trry]))
        xn = np.max(np.array([trx, brx]))
        yn = np.max(np.array([bly, bry]))

        # check for rotated image, we are assuming an angle of rotation under 90 degrees (or over 270)
        # for something over 90 degrees, we'd need to rotate by whatever is (angle - 90) and then figure out
        # with pattern matching that the numbers are reversed

        if np.abs(x0 - tlx) >= THRESHOLD_ROTATE or np.abs(x0 - blx) >= THRESHOLD_ROTATE:
            slope = (tly - bly) / (tlx - blx)
            angle = np.degrees(np.arctan(slope))  # find the angle with the origin
            if angle > 0:
                angle = 90 - angle  # everything is inverted, due to (0, 0) being the top, left point, instead of the usual bottom left used in geometry
                rot_angle = 360 - angle  # rotation seems to be implicitly to the left
            else:
                angle = np.abs(angle)  # negative angle means that it's been rotated by 360 - abs(val) already
                angle = 90 - angle  # therefore, we find how much is left to
                rot_angle = angle
            center = ((xn - x0) / 2, (yn - y0) / 2)  # although not the center of the image, it is the center of the square
            rotation_mat = cv.getRotationMatrix2D(center, rot_angle, scale=1.0)
            rot_angle = np.deg2rad(rot_angle)
            img_rot = cv.warpAffine(src=img[y0:yn, x0:xn, :], M=rotation_mat,
                                    # dsize=((xn- x0), (yn - y0)))
                                    dsize=(int((abs(np.sin(rot_angle) * (yn - y0)) +
                                                abs(np.cos(rot_angle) * (xn - x0)))),
                                           int(abs(np.sin(rot_angle) * (xn - x0)) +
                                               abs(np.cos(rot_angle) * (yn - y0)))))


            # recalculate where the points are
            if x0 == tlx:
                old_points = np.array([[(0, tly - y0), (trx - x0, 0), (blx - x0, yn - y0 - 1), (xn - x0 - 1, bry - y0)]])
            else:
                old_points = np.array([[(tlx - x0, 0), (xn - x0 - 1, trry - y0), (0, bly - y0), (brx - x0, yn - y0 - 1)]])
            new_points = cv.transform(old_points,
                                      rotation_mat).squeeze()
            (tlx, tly), (trx, trry), (blx, bly), (brx, bry) = new_points
            x0 = np.max((np.max(np.array([tlx, blx])), 0)) # account for small angles, in which we could have bizzare cases of not exact perfect squares
            y0 = np.max((np.max(np.array([tly, trry])), 0))
            xn = np.max((np.min(np.array([trx, brx])), 0))
            yn = np.max((np.min(np.array([bly, bry])), 0))

            old_perspective = cv.transform(old_points, rotation_mat)
            old_perspective = np.array(old_perspective, np.float32)
            new_perspective = np.array([[(x0, y0), (xn - 1, y0), (x0, yn - 1), (xn - 1, yn - 1)]], np.float32)

            """
            A bizzare event unfolds often after rotations. For some reason, rotated images seem to have a weird
            deviation on their horizontal lines (after rotation), that's usually just small enough to disrupt my
            predictions, using the center patch idea. Warping the perspective so it should be as expected should
            hopefully solve this problem.
            """

            persp_transform = cv.getPerspectiveTransform(old_perspective, new_perspective)
            img_rot = cv.warpPerspective(img_rot.copy(), persp_transform, (img_rot.shape[0], img_rot.shape[1]))
            sudoku_squares += [img_rot[y0:yn, x0:xn, :]]
            continue

        """
        Some photos have perspectives that are just a tiny bit off from being parallel enough, so with this
        perspective trick I make sure I get them close enough to being parallel. Due to the approach of checking
        each 55x55 patch, the closeness to actual parallel lines matters a lot for my program.
        """
        old_perspective = np.array([[(tlx, tly), (trx, trry), (blx, bly), (brx, bry)]])
        old_perspective = np.array(old_perspective, np.float32)
        new_perspective = np.array([[(x0, y0), (xn - 1, y0), (x0, yn - 1), (xn - 1, yn - 1)]], np.float32)
        persp_transform = cv.getPerspectiveTransform(old_perspective, new_perspective)
        img = cv.warpPerspective(img.copy(), persp_transform, (img.shape[0] * 2, img.shape[1] * 2))
        # print(x0, y0, xn, yn, tlx, tly, blx, bly, trx, trry, brx, bry)
        sudoku_squares += [img[y0:yn, x0:xn, :]]
    #
    # for sq in sudoku_squares:
    #     cv.imshow("square", sq)
    #     cv.waitKey(0)
    #     cv.destroyAllWindows()
    return sudoku_squares

def resize_squares(squares, size=RESIZED_SQ):
    for i, square in enumerate(squares):
        squares[i] = cv.resize(squares[i], size)

    # for sq in squares:
    #     cv.imshow("square", sq)
    #     cv.waitKey(0)
    #     cv.destroyAllWindows()
    return squares