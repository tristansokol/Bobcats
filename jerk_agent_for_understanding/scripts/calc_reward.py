import numpy as np
import os
dir_path = os.getcwd()

import sys
firstarg=sys.argv[1]

r, _, _ = np.loadtxt(dir_path+'/results/'+firstarg+'/monitor.csv', delimiter=',', unpack=True, skiprows=1)
l, _ = np.loadtxt(dir_path+'/results/'+firstarg+'/log.csv', delimiter=',', unpack=True, skiprows=1)
print('%f%% done, reward: %f' % (max(l)/10000 ,np.mean(r)))
