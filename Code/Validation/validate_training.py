import os
from Code.IO.load_images import CLASSIC, JIGSAW
TRAINING_PATH_CLASSIC = "././antrenare/clasic/"
TRAINING_PATH_JIGSAW = "././antrenare/jigsaw/"
BONUS = "_bonus"
GT = "_gt"
EXT = ".txt"

def check_results(answers, flag=CLASSIC):
    # read results
    results = [[["" for i in range(len(answers[0][1]))] for j in range(len(answers[0]))] for k in range(len(answers))]
    for i in range(1, (21 if flag==CLASSIC else 41)):
        this_result = [["" for i in range(len(answers[0][1]))] for j in range(len(answers[0]))]
        with open((TRAINING_PATH_CLASSIC if flag == CLASSIC else TRAINING_PATH_JIGSAW) + ("0" if i < 10 else "") + str(i) + GT + EXT, "r") as f:
            lines = f.readlines()
            k, j = 0, 0
            for line in lines:
                j = 0
                for char in line:
                    if char == "\n":
                        continue
                    this_result[k][j] = char
                    j += 1
                k += 1
            results[i - 1] = this_result.copy()

    # check them against my answers
    for i in range(len(answers)):
        ans = answers[i]
        res = results[i]
        if ans == res:
            print("Test passed!")
        else:
            print("Test failed, i=%i", i)