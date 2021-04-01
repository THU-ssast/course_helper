# -*- coding: utf-8 -*-
"""
@Time    : 2020/5/7 17:59
@Author  : Lucius
@FileName: bf.py
@Software: PyCharm
"""


def brute_force(text: str, pattern: str):
    match = []

    len_t = len(text)
    len_p = len(pattern)
    for i in range(len_t - len_p + 1):
        find = True
        for j in range(len_p):
            if not text[i + j] == pattern[j]:
                find = False
                break
        if find:
            match.append((i + 1, i + len_p))

    return match


