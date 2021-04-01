# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/27 00:23
@Author  : Lucius
@FileName: subseq.py
@Software: PyCharm
"""

import math
from random import randint
import sys
import time


def bisect_left(a, x, lo=0, hi=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def get_longest_substr(whole_arr):
    least_last = [math.inf for _ in range(len(whole_arr) + 1)]
    longest_record = [[] for _ in range(len(whole_arr))]
    for num in whole_arr:
        loc = bisect_left(least_last, num)
        least_last[loc] = num
        longest_record[loc].clear()
        longest_record[loc] += longest_record[loc - 1][:] if loc > 0 else []
        longest_record[loc].append(num)
    for index, number in enumerate(least_last):
        if least_last[index + 1] == math.inf:  # the last number
            return longest_record[index]


def cprint(color, text, **kwargs):
    if color[0] == '*':
        pre_code = '1;'
        color = color[1:]
    else:
        pre_code = ''
    code = {
        'a': '30',
        'r': '31',
        'g': '32',
        'y': '33',
        'b': '34',
        'p': '35',
        'c': '36',
        'w': '37'
    }
    print("\x1b[%s%sm%s\x1b[0m" % (pre_code, code[color], text), **kwargs)
    sys.stdout.flush()


def user_command():
    def instruction():
        cprint("y",
               '    test -- type in your own array divided by blank space and find the longest monotonically increasing subsequence of it')
        cprint("b",
               '    rand -- generate a random array and find the longest monotonically increasing subsequence of it')
        cprint("c", '    time -- compute the time cost of this method')
        cprint("p", '    quit -- goodbye')

    cprint("g", 'Please type in the following command to begin your test:')
    instruction()

    while True:
        command = input('\nselect your command: ')

        if command.lower() == 'test':
            cprint("y", 'Please type in your array divided by blank space.')
            str_in = input('Your array: ')
            array = list(map(int, str_in.strip().split()))
            result = get_longest_substr(array)
            cprint("y", 'Here is the result:\n{}'.format(result))
        elif command.lower() == 'rand':
            cprint("b", 'Please type in the length of the random array:')
            length = int(input())
            while True:
                try:
                    cprint("b", 'Please type in the range of the random array: min max')
                    min_, max_ = input().split()
                    min_ = int(min_)
                    max_ = int(max_)
                    if min_ >= max_:
                        raise KeyError
                    break
                except ValueError:
                    cprint("r", 'require 2 numbers')
                except KeyError:
                    cprint("r", 'min must less than max')
            array = [randint(min_, max_) for _ in range(length)]
            result = get_longest_substr(array)
            cprint("b", 'Here is the result:\n{}'.format(result))
        elif command.lower() == 'time':
            cprint("c", 'Please type in your test samples. No input means the default samples will be used.')
            str_in = input('Your array: ')
            array = list(map(int, str_in.strip().split()))
            if not array:
                array = [10, 100, 1000, 10000, 100000, 1000000]
            for n in array:
                begin = time.time()
                array = [randint(0, 10 * n) for _ in range(n)]
                result = get_longest_substr(array)
                end = time.time()
                cprint("c", 'Size: {} Time-cost:{}'.format(n, end - begin))
        elif command.lower() == 'quit':
            break
        else:
            cprint("r", 'Unacceptable command. Please type the right command according to the instruction.')
            instruction()
            continue


if __name__ == '__main__':
    user_command()
