from Code.IO.load_images import load_imgs, JIGSAW
from Code.Data_Processing.get_squares import *
from Code.Solving.check_content_classic import check_all_squares
from Code.Solving.bonus_classic import check_templates
from Code.IO.write_results import write_ans, write_bonus
from Code.Validation.validate_training import check_results
from Code.IO.get_number_templates import get_templates
from Code.Data_Processing.processing_squares import process_square
from Code.Validation.validate_bonus import check_bonus
from Code.Data_Processing.sort_jigsaw import sort_colors
from Code.Solving.check_content_jigsaw import check_all_squares_j_gray, check_all_squares_j_bgr, merge_answers

__all__ = [cv, np]

def main():
    # solve for task one + bonus
    imgs_classic = load_imgs()
    sudoku_squares = crop_squares(imgs_classic)
    sudoku_squares = resize_squares(sudoku_squares)
    answers = check_all_squares(sudoku_squares)
    bonuses = check_templates(sudoku_squares, answers)
    check_results(answers)
    check_bonus(bonuses)
    write_ans(answers)
    write_bonus(bonuses)

    # solve for task two + bonus
    imgs_jigsaw = load_imgs(JIGSAW)
    jig_gray, jig_bgr, positions = sort_colors(imgs_jigsaw) # sort in the gray and bgr set
    sudoku_sq_gray, sudoku_sq_bgr = crop_squares(jig_gray, JIGSAW), crop_squares(jig_bgr, JIGSAW)
    sudoku_sq_gray, sudoku_sq_bgr = resize_squares(sudoku_sq_gray), resize_squares(sudoku_sq_bgr)
    answers_sq_gray, answers_sq_bgr = check_all_squares_j_gray(sudoku_sq_gray), check_all_squares_j_bgr(sudoku_sq_bgr)
    answers_j = merge_answers(answers_sq_gray, answers_sq_bgr, positions)
    check_results(answers, JIGSAW)
    write_ans(answers, JIGSAW)

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

if __name__ == "__main__":
    main()
