# -*- coding: utf-8 -*-
"""
@Time    : 2020/5/7 18:11
@Author  : Lucius
@FileName: kmp.py
@Software: PyCharm
"""


def prefix_function(pattern: str):
    len_p = len(pattern)
    pi = [-1 for _ in range(len_p + 1)]

    pi[1] = 0
    for k in range(1, len_p):
        if pattern[-1 + pi[k] + 1] == pattern[-1 + k + 1]:
            pi[k + 1] = pi[k] + 1
        else:
            pi[k + 1] = 0

    return pi


def kmp(text: str, pattern: str):
    match = []

    len_t = len(text)
    len_p = len(pattern)
    pi = prefix_function(pattern)
    q = 0
    for i in range(1, len_t + 1):
        while q > 0 and pattern[q + 1 - 1] != text[i - 1]:
            q = pi[q]
        if pattern[q + 1 - 1] == text[i - 1]:
            q += 1
        if q == len_p:
            match.append((i - len_p + 1, i))
            q = pi[q]

    return match
