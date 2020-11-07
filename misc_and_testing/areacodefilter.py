import re
import random

handl = open("areacodes.txt")
rawFileTxt = handl.read()

regex = re.findall("\d\d\d", rawFileTxt)
# print(regex)
# print(len(regex))

handl.close()

def genPhonNum():
    emStr = ""
    indxr = random.randrange(0, 341, 1)
    emStr += regex[indxr]
    emStr += str(random.randrange(1, 9, 1))
    for i in range(6):
        emStr += str(random.randrange(0, 9, 1))
    return emStr

for i in range(10):
    print(genPhonNum())

    print(random.randint(1000, 10000))