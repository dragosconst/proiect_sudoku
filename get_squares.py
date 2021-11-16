from preprocessing import *
from load_images import CLASSIC, JIGSAW

THRESHOLD_ROTATE = 10
RESIZED_SQ = (500, 500)
AVG_SQUARE = (RESIZED_SQ[0] // 9, RESIZED_SQ[1] // 9)

def crop_squares(imgs, how_many=20, flag=CLASSIC):
    sudoku_squares = []
    ind = 1
    for img in imgs:
        print(ind)
        ind += 1
        (tlx, tly), (trx, trry), (blx, bly), (brx, bry) = preprocess_image(img)
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

            sudoku_squares += [img_rot[(y0):yn, (x0):xn, :]]
            # print("yamasha")
            print("yamasha")
            print(x0, y0, xn, yn, tlx, tly, blx, bly, trx, trry, brx, bry)
            image_copy = img_rot[(y0):yn, (x0):xn, :].copy()
            cv.circle(image_copy, tuple((tlx - x0, tly - y0)), 4, (0, 0, 255), -1)
            cv.circle(image_copy, tuple((trx - x0, trry - y0)), 4, (0, 255, 0), -1)
            cv.circle(image_copy, tuple((blx - x0, bly - y0)), 4, (255, 0, 0), -1)
            cv.circle(image_copy, tuple((brx - x0, bry - y0)), 4, (0, 255, 255), -1)

            # cv.imshow("yamasha", image_copy)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
            continue

        print(x0, y0, xn, yn, tlx, tly, blx, bly, trx, trry, brx, bry)
        sudoku_squares += [img[y0:yn, x0:xn, :]]
    #
    # for sq in sudoku_squares:
    #     cv.imshow("square", sq)
    #     cv.waitKey(0)
    #     cv.destroyAllWindows()
    return sudoku_squares

def resize_squares(squares, size=RESIZED_SQ):
    for i in range(len(squares)):
        squares[i] = cv.resize(squares[i], size)

    # for sq in squares:
    #     cv.imshow("square", sq)
    #     cv.waitKey(0)
    #     cv.destroyAllWindows()
    return squares