import numpy as np
import math
import matplotlib.pyplot as plt

xp, yp = 100, 0
xb, yb = 70, 40
xw, yw = 0, 60

# plt.scatter(xp, -yp, c='b')
# plt.scatter(xb, -yb, c='r')
# plt.scatter(xw, -yw, c='g')
# plt.xlim([0, 100])
# plt.ylim([-100, 0])
# plt.show(block=False)
# plt.pause(1)
# plt.close()

theta_b = math.atan2(xp-xb, yb-yp)
print(theta_b)