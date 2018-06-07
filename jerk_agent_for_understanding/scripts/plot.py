import matplotlib.pyplot as plt
import numpy as np
import os
dir_path = os.getcwd()

r, l, t = np.loadtxt(dir_path+'/results/jerk-agentv6/monitor.csv', delimiter=',', unpack=True, skiprows=1)
fig = plt.figure(num=None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='k')

ax  = fig.add_subplot(111)
ax.plot(t, r, c='b', label='Reward',linewidth=0.5)
ax.plot(t, l, c='r', label='Episode Length',linewidth=0.5)
plt.xlabel('Wall Time')
# plt.ylabel('y')
plt.title('Reward & Episode Length')
plt.legend()
plt.show()
