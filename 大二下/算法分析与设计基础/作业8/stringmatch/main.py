# -*- coding: utf-8 -*-
"""
@Time    : 2020/5/8 13:41
@Author  : Lucius
@FileName: main.py
@Software: PyCharm
"""

from methods.bf import brute_force
from methods.bm import boyer_moore
from methods.kmp import kmp

import random
import time
from paint import paint
import os


def string_match_test():  # generate random string and insert the pattern into it to test
    def random_string(num):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        salt = ''
        for i in range(num):
            salt += random.choice(alphabet)
        return salt

    for len_target in [10, 100, 1000]:
        target_pattern = random_string(len_target)
        print()
        print(len_target)
        time_record = {'brute_force': [], 'kmp': [], 'boyer_moore': []}
        len_record = []
        for len_text in [100, 1000, 10000, 100000, 1000000]:
            # p = len_text
            # len_text = int(10 ** 5 * len_text)
            ori_text = random_string(int(len_text))
            str_list = list(ori_text)
            for i in range(10):
                insert_pos = random.randint(0, int(len_text))
                str_list.insert(insert_pos, target_pattern)
            text = ''.join(str_list)

            t0 = time.time()
            m1 = brute_force(text, target_pattern)
            t1 = time.time()
            m2 = kmp(text, target_pattern)
            t2 = time.time()
            m3 = boyer_moore(text, target_pattern)
            t3 = time.time()
            assert m1 == m2 == m3

            len_record.append(str(len_text))
            # print(len_text)
            time_record['brute_force'].append(t1 - t0)
            # print(t1 - t0)
            time_record['kmp'].append(t2 - t1)
            # print(t2 - t1)
            time_record['boyer_moore'].append(t3 - t2)
            # print(t3 - t2)

        # paint(time_record, len_record, 'length of pattern {}'.format(len_target), 'time', 'length of text' + '(10^5)',
        #       3.5, None)


def application():
    file_path = input('请输入文件名称（同一目录下）:')

    while True:
        if not os.path.isfile(file_path):
            print(file_path, " does not exist")
        else:
            text = open(file_path).read()
            print(file_path, '读取成功！')
            break

    while True:
        pattern = input('请输入查找的字符串:')
        t0 = time.time()
        m1 = brute_force(text, pattern)
        t1 = time.time()
        print('Brute Force 结果：', m1)
        print('Brute Force 耗时：', t1 - t0)
        m2 = kmp(text, pattern)
        t2 = time.time()
        print('KMP 结果        ：', m2)
        print('KMP 耗时        ：', t2 - t1)
        m3 = boyer_moore(text, pattern)
        t3 = time.time()
        print('Boyer Moore 结果：', m3)
        print('Boyer Moore 耗时：', t3 - t2)


if __name__ == '__main__':
    application()
