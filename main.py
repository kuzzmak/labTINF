import numpy as np
import math


def add(v1, v2):
    result = []

    for i in range(v1.__len__()):
        if v1[i] == v2[i]:
            result.append(0)
        else:
            result.append(1)

    return result


def multiply(const, v):
    result = []

    for i in range(v.__len__()):
        result.append(const * v[i])
    return result






















#
# code = []
#
# # inputString = input()
# #
# # while inputString != "":
# #     temp = [int(i) for i in inputString.split(",")]
# #     genMat.append(temp)
# #     inputString = input()
#
# # vektorski prostor
# n = genMat[0].__len__()
# # dimenzija koda
# k = genMat.__len__()
#
# code.append(add(multiply(alphabet[0], genMat[0]), multiply(alphabet[0], genMat[1])))
# code.append(add(multiply(alphabet[0], genMat[0]), multiply(alphabet[1], genMat[1])))
# code.append(add(multiply(alphabet[1], genMat[0]), multiply(alphabet[0], genMat[1])))
# code.append(add(multiply(alphabet[1], genMat[0]), multiply(alphabet[1], genMat[1])))
#
# # ako je kod linearan onda sadrzi kodnu rijec 0
# # if code.__contains__([0] * n):
# #     print("linearan")
#
# isGenMatStandardized(genMat)


genMat1 = [[0, 0, 1, 1, 1],
          [1, 1, 0, 1, 1]]

genMat2 = [[1, 0, 1, 1, 0],
           [1, 1, 0, 1, 0],
           [0, 1, 0, 0, 1]]

genMat3 = [[1, 0, 0, 1, 1, 1, 0],
           [0, 1, 0, 1, 1, 0, 1],
           [0, 0, 0, 1, 0, 1, 1],
           [0, 0, 1, 1, 1, 0, 0]]



normalize(genMat2)

codeWords = generateCodeWords(genMat2.__len__())

for c in codeWords:
    print(multiplyMod2(genMat2, c))








