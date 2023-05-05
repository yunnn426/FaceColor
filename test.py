import os

file_path = "../Desktop/ex_warm"
file_names = os.listdir(file_path)
file_names


i=1
for name in file_names:
    src = os.path.join(file_path, name)
    dst = "warm" + str(i) + '.jpg'
    dst = os.path.join(file_path, dst)
    os.rename(src, dst)
    i += 1

#그래프
# import matplotlib.pyplot as plt
# import numpy as np

# def plot_lab(b):
#     x = np.arange(1, 11)
#     y = np.array(b)

#     threshold = 18
#     plt.plot(x, y, 'bo', label='cool')

#     below_threshold = y < threshold
#     above_threshold = np.logical_not(below_threshold)
#     plt.plot(x[above_threshold], y[above_threshold], 'ro', label='warm')

#     plt.legend(loc='upper right')
#     plt.xlabel('images')
#     plt.ylabel('b')
#     plt.title('Value of B(LAB) by image')
#     plt.show()
