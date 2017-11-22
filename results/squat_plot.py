'''
plots content of squat_file
'''

import matplotlib.patches as mpatches
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

LINE_LIM = 111
file_name = '../squat_file'

with open(file_name) as f:
    content = f.readlines()

content = [x.strip() for x in content] 


content = content[:111]
content

import json

colors = { 'sup': 'b',
           'heellift': 'r',
           'pron': 'k', 
           'heeldom': 'm',
           'normal': 'g' }

AREA_SCALE = 7

X, Y, S, C =  [], [], [], [] #x, y, area, colors
x = 0
for line in content:
    plot_obj = {}
    line = line.split(', ')
    pos_info = line[0].split(': ')
    pos = pos_info[0]
    if pos == 'STABLE':
        y = 1 if int(pos_info[1]) > 0 else 0
    elif pos == 'DESCENT':
        y = 1 - float(pos_info[1])
    else:
        y = float(pos_info[1])   
    if len(line) > 2:
        error_str = line[1] + ', ' + line[2]
    else:
        error_str = line[1]
    errors = json.loads(error_str)
    if len(errors) == 0:
        area = np.pi * (AREA_SCALE * 0.5)**2
        S.append(area)
        C.append(colors['normal'])
        Y.append(y)
        X.append(x)
    else:
        for k in errors:
            color = colors[k]
            C.append(color)
            area = np.pi * (AREA_SCALE * errors[k])**2
            S.append(area)
            Y.append(y)
            X.append(x)
    x += 25


sup = mpatches.Patch(color='b', label='Supination')
heellift = mpatches.Patch(color='r', label='Heel-Lift')
pron = mpatches.Patch(color='k', label='Pronation')
heeldom = mpatches.Patch(color='m', label='Heel-Dominance')
normal = mpatches.Patch(color='g', label='Normal')

plt.figure(figsize=(10,5))
plt.title('Errors Throughout Squat Movement')
plt.xlabel('Time in Milliseconds')
plt.ylabel('Squat Depth as Fraction of Calibrated Max/Min Height')
plt.scatter(X, Y, c=C, s=S, alpha=0.5)
plt.legend(handles = [sup, heellift, pron, heeldom, normal])
plt.show()
