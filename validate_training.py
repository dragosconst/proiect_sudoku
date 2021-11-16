import os
TRAINING_PATH_CLASSIC = "antrenare/clasic/"
BONUS = "_bonus"
GT = "_gt"
EXT = ".txt"

def check_results(answers):
    # read results
    results = [[["" for i in range(len(answers[0][1]))] for j in range(len(answers[0]))] for k in range(len(answers))]
    for i in range(1, 21):
        this_result = [["" for i in range(len(answers[0][1]))] for j in range(len(answers[0]))]
        with open(TRAINING_PATH_CLASSIC + ("0" if i < 10 else "") + str(i) + GT + EXT, "r") as f:
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
        print(ans, res)
        if ans == res:
            print("Test passed!")
        else:
            print("Test failed, i=%s", i)