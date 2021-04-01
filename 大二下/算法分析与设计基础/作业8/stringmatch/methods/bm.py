# -*- coding: utf-8 -*-
"""
@Time    : 2020/5/8 11:17
@Author  : Lucius
@FileName: bm.py
@Software: PyCharm
"""


def boyer_moore(text: str, pattern: str):
    match = []

    len_t = len(text)
    len_p = len(pattern)
    bmbc = compute_bmbc(pattern)
    bmgs = compute_bmgs(pattern)
    s = 0
    while s < len_t - len_p:
        i = len_p
        while pattern[i - 1] == text[s + i - 1]:
            if i == 1:
                match.append((s + 1, s + len_p))
                break
            else:
                i -= 1
        s = s + max(bmgs[i], bmbc.get(text[s + i - 1], len_p) - len_p + i)

    return match


def compute_bmbc(pattern: str):
    len_p = len(pattern)
    bmbc = {}
    # expect the chat in pattern, all other char will be 'len_p'
    for i in range(1, len_p):
        bmbc[pattern[i-1]] = len_p - i

    return bmbc


def compute_bmgs(pattern: str):
    def overlapping_suffix_function(pattern: str):
        len_p = len(pattern)
        osuff = [-1 for _ in range(len_p + 1)]
        for i in range(1, len_p + 1):
            lapping = 0
            for j in range(i):
                if pattern[i - j - 1] == pattern[len_p - j - 1]:
                    lapping += 1
                else:
                    break
            osuff[i] = lapping

        return osuff

    len_p = len(pattern)
    osuff = overlapping_suffix_function(pattern)
    bmgs = [len_p for _ in range(len_p + 1)]
    bmgs[0] = -1
    j = 1
    for i in range(len_p - 1, 0, -1):
        if osuff[i] == i:
            while j <= len_p - i:
                if bmgs[j] == len_p:
                    bmgs[j] = len_p - i
                j += 1
    for i in range(1, len_p):
        bmgs[len_p - osuff[i]] = len_p - i

    return bmgs


