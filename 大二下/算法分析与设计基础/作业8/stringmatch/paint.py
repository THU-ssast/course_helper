# -*- coding: utf-8 -*-
"""
@Time    : 2020/4/14 21:09
@Author  : Lucius
@FileName: paint.py
@Software: PyCharm
"""

import matplotlib
import matplotlib.pyplot as plt

'''
data_dict 为数据的字典，格式为：{data1:[y1, y2, ..., yn], data2:[y1, y2, ..., yn], ...}
x_list 为横轴坐标点，与数据必须对应
name 为标题
y_name 为纵轴名称
x_name 为横轴名称
y_max 为y轴坐标上限
x_max 为x轴坐标上限
'''


def paint(data_dict: dict, x_list: list, name, y_name, x_name, y_max, x_max):  # data为字典

    # paint
    # set style
    plt.rc('font', family="Times New Roman")
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42

    # plt.xlim(xmax=x_list[-1]*1.2, xmin=0)
    plt.ylim(ymax=y_max, ymin=0)

    fontsize = 25

    plt.grid(linestyle='-.', linewidth=1)
    ax = plt.gca()
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)

    for key in data_dict.keys():
        plt.plot(x_list, data_dict[key], label=key)
    plt.xlabel(x_name, fontsize=30)
    plt.ylabel(y_name, fontsize=30)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.legend(fontsize=10, loc="upper left")
    plt.title(name, fontsize=30)
    save = 'curves_{}.pdf'.format(name)
    plt.tight_layout()
    plt.savefig(save, format='pdf', dpi=300, pad_inches=0)
    plt.close()
    print('save image to {}'.format(save))

