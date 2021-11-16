import os
import errno
from Code.IO.load_images import CLASSIC

FILEPATH = "././evaluare/fisiere_solutie/Tantaru_Dragos-Constantin_344/"
CLASSIC_PATH = "classic/"
JIGSAW_PATH = "jigsaw/"
BONUS_TEXT = "_bonus_"

def write_ans(answers, flag=CLASSIC):
    try:
        os.makedirs(os.path.dirname(FILEPATH))
        os.makedirs(os.path.dirname(FILEPATH + CLASSIC_PATH))
        os.makedirs(os.path.dirname(FILEPATH + JIGSAW_PATH))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

    index = 1
    for ans in answers:
        with open(FILEPATH + CLASSIC_PATH + str(index) + "_" + "predictie.txt", "w") as f:
            for line in ans:
                for char in line:
                    f.write(char)
                f.write('\n')
                f.flush()
        f.close()
        index += 1

def write_bonus(bonuses):
    index = 1
    for bonus in bonuses:
        with open(FILEPATH + CLASSIC_PATH + str(index) + BONUS_TEXT + "predictie.txt", "w") as f:
            for line in bonus:
                for char in line:
                    f.write(char)
                f.write('\n')
                f.flush()
        f.close()
        index += 1
