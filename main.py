from Code.IO.load_images import load_imgs
from Code.Data_Processing.get_squares import *
from Code.Solving.check_content_classic import check_all_squares
from Code.IO.write_results import write_ans
from Code.Validation.validate_training import check_results

__all__ = [cv, np]

imgs = load_imgs()
sudoku_squares = crop_squares(imgs, len(imgs))
sudoku_squares = resize_squares(sudoku_squares)
answers = check_all_squares(sudoku_squares)
check_results(answers)
write_ans(answers)



# def get_results(img,lines_horizontal,lines_vertical):
#     for i in range(len(lines_horizontal) - 1):
#         for j in range(len(lines_vertical) - 1):
#             y_min = lines_vertical[j][0][0]
#             y_max = lines_vertical[j + 1][1][0]
#             x_min = lines_horizontal[i][0][1]
#             x_max = lines_horizontal[i + 1][1][1]
#             patch = img_crop[x_min:x_max, y_min:y_max].copy()
#             cv.imshow("patch", patch)
#             cv.waitKey(0)
#             cv.destroyAllWindows()

# get_results(img,lines_horizontal,lines_vertical)


