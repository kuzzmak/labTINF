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

import numpy as np


def rref(B, tol=1e-8, debug=False):
    A = B.copy()
    rows, cols = A.shape
    r = 0
    pivots_pos = []
    row_exchanges = np.arange(rows)
    for c in range(cols):
        if debug: print
        "Now at row", r, "and col", c, "with matrix:";
        print
        A

        ## Find the pivot row:
        pivot = np.argmax(np.abs(A[r:rows, c])) + r
        m = np.abs(A[pivot, c])
        if debug: print
        "Found pivot", m, "in row", pivot
        if m <= tol:
            ## Skip column c, making sure the approximately zero terms are
            ## actually zero.
            A[r:rows, c] = np.zeros(rows - r)
            if debug: print
            "All elements at and below (", r, ",", c, ") are zero.. moving on.."
        else:
            ## keep track of bound variables
            pivots_pos.append((r, c))

            if pivot != r:
                ## Swap current row and pivot row
                A[[pivot, r], c:cols] = A[[r, pivot], c:cols]
                row_exchanges[[pivot, r]] = row_exchanges[[r, pivot]]

                if debug: print
                "Swap row", r, "with row", pivot, "Now:";
                print
                A

            ## Normalize pivot row
            A[r, c:cols] = A[r, c:cols] / A[r, c];

            ## Eliminate the current column
            v = A[r, c:cols]
            ## Above (before row r):
            if r > 0:
                ridx_above = np.arange(r)
                A[ridx_above, c:cols] = A[ridx_above, c:cols] - np.outer(v, A[ridx_above, c]).T
                if debug: print
                "Elimination above performed:";
                print
                A
            ## Below (after row r):
            if r < rows - 1:
                ridx_below = np.arange(r + 1, rows)
                A[ridx_below, c:cols] = A[ridx_below, c:cols] - np.outer(v, A[ridx_below, c]).T
                if debug: print
                "Elimination below performed:";
                print
                A
            r += 1
        ## Check if done
        if r == rows:
            break;
    return (A, pivots_pos, row_exchanges)

genMat = [[0, 0, 1, 1, 1], [1, 1, 0, 1, 1]]
genMat2 = [[1,0,1,1,0], [1,1,0,1,0], [0,1,0,0,1]]

print(rref(np.array(genMat)))