import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

def func(p, x):
    k, b = p
    return k * x + b

# Residual function
def res(p, x, y):
    return func(p, x) - y

def lsc(x, y):
    p0 = [1, 20]
    Para = leastsq(res, p0, args=(x, y)) # 把res函数中除了p0以外的参数打包到args中
    k, b = Para[0]
    print("k= ", k, "b= ", b)
    print("cost: " + str(Para[1]))
    print("求解的拟合直线为: ")
    print("y= " + str(round(k, 2)) + "x^2 + " + str(round(b, 2)))
    return k, b

# max index
def site(y):
    ymax = max(y[:])
    yIndex = np.where(y == ymax)
    print(ymax)
    return yIndex

def bilinear(x, y):
    # a = site(y)[0][0]
    i = lsc(x, y)
    # j = lsc(x[a:], y[a:])
    # origin plot
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color="green", label="Data", linewidth=2)
    # fitting plot
    fx = np.linspace(0, x, 100)
    fy = i[0] * fx ** 2+ i[1]
    # fc = np.linspace(x[a], max(x), 100)
    # fz = j[0] * fx ** 2 + j[1]
    plt.plot(fx, fy, color="darkblue", label="fitting line", linewidth=2)
    # plt.plot(fc, fz, color="blue", label="fitting line", linewidth=2)
    plt.plot(loc="lower right")
    plt.show()

