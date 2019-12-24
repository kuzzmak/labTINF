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

def xor(row, patternRow, genMat, destinationIndex):

    v1 = genMat[row]
    v2 = genMat[patternRow]

    v3 = [0] * v1.__len__()

    for i in range(v3.__len__()):
        v3[i] = v1[i] ^ v2[i]

    genMat[destinationIndex] = v3

def isGenMatStandardized(genMat):

    flag = True

    for i in range(k):

        if genMat[i][i] == 0:
            print("generirajuca matrica nije standardizirana")
            flag = False
            break

        for j in range(k):
            if j == i:
                continue
            if genMat[i][j] == 1:
                print("generirajuca matrica nije standardizirana")
                flag = False
                break
    if flag:
        print("generirajuca matrica je standardizirana")

def swapRows(genMat, r1, r2):

    temp = genMat[r1]
    genMat[r1] = genMat[r2]
    genMat[r2] = temp

def swapColumns(genMat, c1, c2):

    numOfRows = genMat.__len__()

    for row in range(numOfRows):
        temp = genMat[row][c1]
        genMat[row][c1] = genMat[row][c2]
        genMat[row][c2] = temp

def getColumn(genMat, index):

    numOfRows = genMat.__len__()

    result = [0] * numOfRows

    for row in range(numOfRows):
        result[row] = genMat[row][index]

    return result

def containsColumn(genMat, index):

    numOfRows = genMat.__len__()
    numOfColumns = genMat[0].__len__()

    # trazeni stupac koji ima na poziciji index jedinicu
    target = [0] * numOfRows
    target[index] = 1

    for column in range(numOfColumns):

        temp = getColumn(genMat, column)

        if temp == target:
            return column

    return -1

def findPattern(genMat, currentColumn):

    numOfRows = genMat.__len__()

    pattern = [0] * (currentColumn + 1)
    pattern[currentColumn] = 1

    for row in range(numOfRows):
        ok = True
        for i in range(pattern.__len__()):
            if genMat[row][i] != pattern[i]:
                ok = False
                break
        if ok:
            return row
    return -1




# print("please input your matrix\n1,2,3 -> row 1\n1,0,1 -> row 2\n.\n.\n.\n")
# # abeceda koda
# alphabet = [1, 0]
# # generirajuca matrica
# genMat = [[0, 0, 1, 1, 1], [1, 1, 0, 1, 1]]
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
#
# # print(code)
# print(genMat)
# swapRows(genMat, 0, 1)
# print(genMat)

genMat1 = [[0, 0, 1, 1, 1],
          [1, 1, 0, 1, 1]]

genMat2 = [[1, 0, 1, 1, 0],
           [1, 1, 0, 1, 0],
           [0, 1, 0, 0, 1]]

genMat3 = [[1, 0, 0, 1, 1, 1, 0],
           [0, 1, 0, 1, 1, 0, 1],
           [0, 0, 0, 1, 0, 1, 1],
           [0, 0, 1, 1, 1, 0, 0]]

def normalize(genMat):

    numOfRows = genMat.__len__()
    numOfColumns = genMat[0].__len__()

    for column in range(numOfRows):

        for row in range(numOfRows):

            # ako smo na dijagonali gdje bi elementi trebali biti 1
            if row == column:

                if genMat[row][column] != 1:

                    # probamo pronaci postoji li gotov stupac koji ima jedinicu
                    # na pravom mjestu a na ostalim mjestima nule
                    index = containsColumn(genMat, column)
                    if index != -1:
                        swapColumns(genMat, index, column)
                        break

                    index = findPattern(genMat, column)
                    if index != -1:
                        patternRow = index
                        xor(row, patternRow, genMat, row)
                        continue

            else: # sve ostalo kad nismo na dijagonali

                if genMat[row][column] == 0:
                    continue
                else:

                    index = containsColumn(genMat, column)
                    if index != -1:
                        swapColumns(genMat, index, column)
                        break

                    index = findPattern(genMat, column)
                    if index != -1:
                        patternRow = index
                        xor(row, patternRow, genMat, row)
                        continue


normalize(genMat3)
print(genMat3)











