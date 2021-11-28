import os
import errno
from Code.IO.load_images import CLASSIC

FILEPATH = "././evaluare/fisiere_solutie/Tantaru_Dragos-Constantin_344/"
CLASSIC_PATH = "clasic/"
JIGSAW_PATH = "jigsaw/"
BONUS_TEXT = "_bonus_"

def write_ans(answers, flag=CLASSIC):
    try:
        os.makedirs(os.path.dirname(FILEPATH + CLASSIC_PATH))
        os.makedirs(os.path.dirname(FILEPATH + JIGSAW_PATH))
        os.makedirs(os.path.dirname(FILEPATH))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

    for index, ans in enumerate(answers):
        with open(FILEPATH + (CLASSIC_PATH if flag == CLASSIC else JIGSAW_PATH) + str(index + 1) + "_" + "predicted.txt", "w+") as f:
            for index, line in enumerate(ans):
                for char in line:
                    f.write(char)
                if index != len(ans) - 1:
                    f.write('\n')
                f.flush()

def write_bonus(bonuses, flag=CLASSIC):
    for index, bonus in enumerate(bonuses):
        with open(FILEPATH + (CLASSIC_PATH if flag == CLASSIC else JIGSAW_PATH) + str(index + 1) + BONUS_TEXT + "predicted.txt", "w+") as f:
            for index, line in enumerate(bonus):
                for char in line:
                    f.write(char)
                if index != len(bonus) - 1:
                    f.write('\n')
                f.flush()
