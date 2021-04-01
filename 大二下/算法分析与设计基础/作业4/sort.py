# Copyright: Copyright (c) 2020
# Created on 2020-3-20
# Author: Lucius
# Version 1.0
# Title: Sorting algorithm

import random
import copy
import time
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import math


def insert_sort(arr):
    for i in range(1, len(arr)):
        x = arr[i]
        t = 0
        for j in range(i - 1, -1, -1):
            if x < arr[j]:
                arr[j + 1] = arr[j]
            else:
                t = j + 1
                break
        arr[t] = x

    return arr


def shell_sort(arr):
    def shell_insert(arr, d):
        for i in range(d, len(arr)):
            x = arr[i]
            t = (i - d) % d
            for j in range(i - d, -1, -d):
                if x < arr[j]:
                    arr[j + d] = arr[j]
                else:
                    t = j + d
                    break
            arr[t] = x

    length = len(arr)

    while length >= 1:
        shell_insert(arr, length)
        length = int(length / 2)

    return arr


def quick_sort(arr, p, r):
    def partition(arr, p, r):
        x = arr[r]
        i = p - 1
        for j in range(p, r):
            if arr[j] <= x:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[r] = arr[r], arr[i + 1]
        return i + 1

    def random_partition(arr, p, r):
        i = random.randint(p, r)
        arr[r], arr[i] = arr[i], arr[r]
        return partition(arr, p, r)

    if p < r:
        q = random_partition(arr, p, r)
        quick_sort(arr, p, q - 1)
        quick_sort(arr, q + 1, r)


def merge_sort(arr, p, r):
    if p == r:
        return
    pivot = int((p + r) / 2)
    merge_sort(arr, p, pivot)
    merge_sort(arr, pivot + 1, r)
    tmp = []
    i = p
    j = pivot + 1
    while i <= pivot and j <= r:
        if arr[i] <= arr[j]:
            tmp.append(arr[i])
            i += 1
        else:
            tmp.append(arr[j])
            j += 1
    while i <= pivot:
        tmp.append(arr[i])
        i += 1
    while j <= r:
        tmp.append(arr[j])
        j += 1
    for t, number in enumerate(tmp):
        arr[p + t] = number


def radix_sort(arr, r):
    def key_of_number(number, begin, end):  # from right to left
        return (number >> begin) & (2 ** (end - begin) - 1)

    def count_sort(des, src, begin, end):
        k = 2 ** (end - begin)
        c = [0 for i in range(k)]
        for j in range(len(src)):
            c[key_of_number(src[j], begin, end)] += 1
        for i in range(1, k):
            c[i] = c[i] + c[i - 1]
        for j in range(len(src) - 1, -1, -1):
            des[c[key_of_number(src[j], begin, end)] - 1] = src[j]
            c[key_of_number(src[j], begin, end)] -= 1

    for begin in range(0, 32, r):
        end = begin + r
        des = [0 for i in range(len(arr))]
        count_sort(des, arr, begin, end)
        arr = des
    return arr


def test_sort(n, ignore=0):
    arr_test = [random.randint(0, 2 ** 32 - 1) for i in range(n)]
    time_record = []

    if ignore <= 0:
        a1 = copy.deepcopy(arr_test)
        t = time.time()
        insert_sort(a1)
        time_record.append(time.time() - t)

    if ignore <= 1:
        a2 = copy.deepcopy(arr_test)
        t = time.time()
        shell_sort(a2)
        time_record.append(time.time() - t)
    if ignore <= 0:
        assert a1 == a2

    a3 = copy.deepcopy(arr_test)
    t = time.time()
    quick_sort(a3, 0, len(arr_test) - 1)
    time_record.append(time.time() - t)
    if ignore <= 1:
        assert a2 == a3

    a4 = copy.deepcopy(arr_test)
    t = time.time()
    merge_sort(a4, 0, len(arr_test) - 1)
    time_record.append(time.time() - t)
    assert a3 == a4

    a5 = copy.deepcopy(arr_test)
    t = time.time()
    a5 = radix_sort(a5, int(math.log2(n)))
    time_record.append(time.time() - t)
    assert a4 == a5

    return time_record


def paint(data, name):  # data为多元组的列表即可，每个多元组第一个元素代表n
    x = []
    y_all = []
    for i in range(len(data[0]) - 1):  # number of curves
        y_all.append([])

    y_max = 0
    for i in range(len(data)):
        x.append(data[i][0])
        for t in range(len(data[0]) - 1):
            y_all[t].append(data[i][t + 1])
            y_max = max(y_max, data[i][t + 1])

    # paint
    # set style
    plt.rc('font', family="Times New Roman")
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    fontsize = 25

    plt.xlim(xmax=x[-1] * 1.1, xmin=x[0])
    plt.ylim(ymax=y_max * 1.1, ymin=0)

    fontsize = 25

    plt.grid(linestyle='-.', linewidth=1)
    ax = plt.gca()
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)

    labels = ['2', '4', '8', '16', 'quick sort']
    # labels = ['quick sort', 'merge sort', 'radix sort']
    # labels = ['quick sort', 'merge sort', 'radix sort']
    for i, label in enumerate(labels):
        plt.plot(x, y_all[i], label=label)
    plt.xlabel('lg(n)', fontsize=30)
    plt.ylabel('relative time', fontsize=30)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.legend(fontsize=20, loc="upper left")
    plt.title(name, fontsize=30)
    save = 'curves_{}.pdf'.format(name)
    plt.tight_layout()
    plt.savefig(save, format='pdf', dpi=300, pad_inches=0)
    print('save image to {}'.format(save))


def generate_csv(record):
    len_attr = len(record[0]) - 1
    dict = {}
    dict['n'] = [r[0] for r in record]
    for attr in range(len_attr):
        dict[str(attr)] = ['{:.4f}'.format(r[attr + 1]) for r in record]
    df = pd.DataFrame(dict)
    df.to_csv("result.csv")


if __name__ == '__main__':
    # record = []
    # for i in range(2,7):
    #     n = int(10**i)
    #     record.append([i] + test_sort(n, 2))
    #     print(record[-1])
    # # n = 2*10**8
    # # record.append([8.3] + test_sort(n, 2))
    # # print(record[-1])
    # paint(record, 'Time Complexity Comparison')
    # generate_csv(record)

    record = []
    for i in range(2, 7):
        n = int(10 ** i)
        arr_test = [random.randint(0, 2 ** 32 - 1) for i in range(n)]
        time_r = []
        for r in [2, 4, 8, 16]:
            t = time.time()
            radix_sort(arr_test, r)
            time_r.append(time.time() - t)
        t = time.time()
        quick_sort(arr_test, 0, len(arr_test) - 1)
        time_r.append(time.time() - t)
        record.append([i] + time_r)
        print(record[-1])

    paint(record, 'Time Complexity Comparison')
    generate_csv(record)
