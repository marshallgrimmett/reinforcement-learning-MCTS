import numpy as np
import math


#########################################################################
# def solution(s):
#     l = len(s)
#     best = 1
#     for i in range(2, l+1):
#         if l % i == 0:
#             flag = True
#             parts = int(l/i)
#             for j in range(i):
#                 if s[0:parts] != s[(j*parts):((j+1)*parts)]:
#                     flag = False
#                     break
#             if flag:
#                 best = i
#     return best

# s = 'abcabcabcabc'
# print(solution(s))


#########################################################################
# def solution(n, b):
#     prevIds = [int(n)]
#     while True:
#         x = ''.join(sorted(n, reverse=True))
#         y = ''.join(sorted(n))
#         xInt = int(x, b)
#         yInt = int(y, b)
#         nInt = xInt - yInt
#         n = np.base_repr(nInt, base=b)
#         if int(n) in prevIds:
#             break
#         prevIds.append(int(n))
#     return len(prevIds[prevIds.index(int(n)):])

# print(solution('1211', 10))


#########################################################################
# def solution(h, q):
#     converters = []
#     for i in q:
#         left = 1
#         root = (2**h) - 1
#         if (i >= root) or (i < 1):
#             converters.append(-1)
#         else:
#             while True:
#                 if i < ((left // 2) + (root // 2)):
#                     root = ((left // 2) + (root // 2))
#                 elif i == ((left // 2) + (root // 2)):
#                     converters.append(root)
#                     break
#                 elif i < (root - 1):
#                     left = ((left // 2) + (root // 2))
#                     root = root - 1
#                 elif i == (root - 1):
#                     converters.append(root)
#                     break
#     return converters

# print(solution(5, [19, 14, 28]))


#########################################################################
# def solution(n):
#     stairs = np.zeros(((n + 1), (n + 1)), np.int)
#     stairs[3, 2] = 1
#     for i in range(4, (n + 1)):
#         iMinStair = minStair(i)
#         for j in range(iMinStair, i):
#             if j == (i - j):
#                 stairs[i, j] += np.sum(stairs[(i - j), :])
#             elif j < (i - j):
#                 jMinStair = minStair(j)
#                 stairs[i, j] += np.sum(stairs[(i - j), jMinStair:j])
#             else:
#                 stairs[i, j] += np.sum(stairs[(i - j), :]) + 1
#     return np.sum(stairs[n])

# def minStair(stair):
#     return int(math.ceil((-1 + math.sqrt(1 + (8*stair))) / 2))

# print(solution(5))


#########################################################################
# def solution(x, y):
#     gen = 0
#     x = int(x)
#     y = int(y)
#     while True:
#         if x == 1 and y == 1:
#             return str(gen)
#         if x < 1 or y < 1:
#             return str(gen-1)
#             # return 'impossible'
#         if x > y:
#             newX = x % y
#             gen += (x - newX) // y
#             x = newX
#         elif x < y:
#             newY = y % x
#             gen += (y - newY) // x
#             y = newY

# print(solution('4', '7'))
# print(solution('2', '1'))
# print(solution('100000000000000000000000000000000000000000000000000', '1'))


#########################################################################
def solution(l):
    combos = {}
    count = 0
    for i in enumerate(l):
        for j in enumerate(l[(i[0] + 1):]):
            if ((j[1] % i[1]) == 0):
                key = j[0] + i[0] + 1
                if key in combos:
                    combos[key] += 1
                else:
                    combos[key] = 1
                if i[0] in combos:
                    count += combos[i[0]]
    return count

print(solution([1, 1, 1]))
print(solution([1, 2, 3, 4, 5, 6]))
