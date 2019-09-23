# 根据输入的点坐标绘制图像
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline

xs = []
ys = []

while(1):

    s = input('axises:')
    if s == '0':
        break
    x = float(s.split(',')[0])
    y = float(s.split(',')[1])
    xs.append(x)
    ys.append(y)

xs = np.array(xs)
ys = np.array(ys)
x_new = np.linspace(xs.min(),xs.max(),300)
y_smooth = spline(xs,ys,x_new)
plt.plot(x_new, y_smooth)
# plt.axis([0,82,0,40])
plt.show()