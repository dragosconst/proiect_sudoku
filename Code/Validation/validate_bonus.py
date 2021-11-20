import os
from Code.IO.load_images import CLASSIC, JIGSAW, CLASSIC_IMGS, JIGSAW_IMGS
TRAINING_PATH_CLASSIC = "././antrenare/clasic/"
TRAINING_PATH_JIGSAW = "././antrenare/jigsaw/"
BONUS = "_bonus"
GT = "_gt"
EXT = ".txt"

def check_bonus(answers, flag=CLASSIC):
    # read results
    results = [[["" for i in range(len(answers[0][1]))] for j in range(len(answers[0]))] for k in range(len(answers))]
    for i in range(1, (CLASSIC_IMGS if flag == CLASSIC else JIGSAW_IMGS)):
        this_result = [["" for i in range(len(answers[0][1]))] for j in range(len(answers[0]))]
        with open((TRAINING_PATH_CLASSIC if flag==CLASSIC else TRAINING_PATH_JIGSAW) + ("0" if i < 10 else "") + str(i) + BONUS + GT + EXT, "r") as f:
            lines = f.readlines()
            for k, line in enumerate(lines):
                for j, char in enumerate(line):
                    if char == "\n":
                        continue
                    this_result[k][j] = char

            results[i - 1] = this_result.copy()

    # check them against my answers
    for i, ans in enumerate(answers):
        res = results[i]
        if ans == res:
            print("Bonus passed!")
        else:
            print(f"Bonus failed, i={i}")