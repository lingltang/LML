import numpy as np

# 图像抽取数据
# arrx = [i for i in range(1, 10+1)]
# arry = [j for j in range(1, 20+1)]
# arr1 = []
# arr2 = []
# arr3 = []
# for i in arrx:
#     for j in arry:
#         arr1.append([i+1000, j+1000])
#         arr2.append([i+2000, j+2000])
#         arr3.append([i+3000, j+3000])
# arr4 = [arr1, arr2, arr3]
# print(np.shape(arr4))
# print(np.stack(arr4, axis=2).shape)

# 测试stack
# arr1 = np.ones([10, 20, 5, 6, 7])
# print(arr1.shape)
# print(np.stack(arr1, axis=4).shape)
# print(np.expand_dims)

# 测试concatenate
# arr1 = np.ones([2, 1, 2], dtype=int)
# arr2 = np.ones([2, 1, 2])
# arr3 = np.ones([1, 2])
# arr4 = np.concatenate((arr1, arr2), axis=1)
# print(arr4.shape)

# 测试max
# arr1 = np.array([[[1, 9, 7, 3],
#                   [8, 4, 5, 1],
#                   [7, 4, 2, 1]],
#                  [[23, 21, 23, 26],
#                   [27, 23, 21, 28],
#                   [29, 29, 27, 21]]])
# print(arr1.shape)
# print(arr1.max(axis=0))
# print(arr1.max(axis=1))
# print(arr1.max(axis=2))

arr2 = np.array([[1, 9],
                 [8, 4],
                 [2, 7]])
print(arr2.shape)
print(arr2.max(axis=0))
print(arr2.max(axis=1))
