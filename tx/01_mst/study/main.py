import turtle
import time


def pointSetCi(x, y):
    turtle.goto(x, y)
    turtle.stamp()

turtle.screensize(200, 200)
turtle.penup()
turtle.right(90)

# 基本参数
N = 12
W = 50
H = 100

# 字典，格式[行数（y坐标）:[x坐标集合]]
poxy = dict()
for i in range(N):
    # print(H*i, '\t', -i*W)
    poxy[H*i] = [-i*W]

# print(poxy.values())

for y in poxy.keys():
    n = int(y/H+1)
    # print(f'\n第{n}行')
    for x in range(n):
        poxy[y].append(poxy[y][0]+2*x*W)
        # print(poxy[y][0]+2*x, end='\t')

for y in poxy.keys():
    for x in poxy[y]:
        pointSetCi(x, y)

input()
