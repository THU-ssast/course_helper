# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/27 15:38
@Author  : Lucius
@FileName: seamcarving.py
@Software: PyCharm
"""

import cv2
import numpy as np
from tqdm import tqdm
import math
from PIL import Image
import sys


def get_pixel_damage(img_data, damage_array, row_col):
    row = row_col[0]
    col = row_col[1]
    damage = 0
    for row_bias in [-1, 0, 1]:
        for col_bias in [-1, 0, 1]:
            if row + row_bias in range(0, img_data.shape[0]) \
                    and col + col_bias in range(0, img_data.shape[1]):
                damage_r = abs(
                    int(img_data[row][col][0]) - int(img_data[row + row_bias][col + col_bias][0]))
                damage_g = abs(
                    int(img_data[row][col][1]) - int(img_data[row + row_bias][col + col_bias][1]))
                damage_b = abs(
                    int(img_data[row][col][2]) - int(img_data[row + row_bias][col + col_bias][2]))
                damage += (damage_r + damage_g + damage_b)/(abs(row_bias)+abs(col_bias)+2)
    damage_array[row][col] = damage


def get_img_damage(img_data):
    damage_array = np.empty([img_data.shape[0], img_data.shape[1]])

    print('calculate damage...')
    for row in tqdm(range(damage_array.shape[0])):
        for col in range(damage_array.shape[1]):
            get_pixel_damage(img_data, damage_array, (row, col))

    return damage_array


def get_sum_damage_row(damage_array):
    sum_array = np.empty([damage_array.shape[0], damage_array.shape[1]])

    for col in range(sum_array.shape[1]):
        sum_array[0][col] = damage_array[0][col]

    print('calculate sum of damage by row...')
    for row in tqdm(range(1, sum_array.shape[0])):
        for col in range(sum_array.shape[1]):
            sum_array[row][col] = damage_array[row][col]
            if col == 0:
                sum_array[row][col] += min(sum_array[row - 1][col], sum_array[row - 1][col + 1])
            elif col == sum_array.shape[1] - 1:
                sum_array[row][col] += min(sum_array[row - 1][col - 1], sum_array[row - 1][col])
            else:
                sum_array[row][col] += min(sum_array[row - 1][col - 1], sum_array[row - 1][col],
                                           sum_array[row - 1][col + 1])

    return sum_array


def get_sum_damage_col(damage_array):
    damage_array = damage_array.T

    sum_array = np.empty([damage_array.shape[0], damage_array.shape[1]])

    for col in range(sum_array.shape[1]):
        sum_array[0][col] = damage_array[0][col]

    print('calculate sum of damage by col...')
    for row in tqdm(range(1, sum_array.shape[0])):
        for col in range(sum_array.shape[1]):
            sum_array[row][col] = damage_array[row][col]
            if col == 0:
                sum_array[row][col] += min(sum_array[row - 1][col], sum_array[row - 1][col + 1])
            elif col == sum_array.shape[1] - 1:
                sum_array[row][col] += min(sum_array[row - 1][col - 1], sum_array[row - 1][col])
            else:
                sum_array[row][col] += min(sum_array[row - 1][col - 1], sum_array[row - 1][col],
                                           sum_array[row - 1][col + 1])

    return sum_array.T


class Pixel:
    def __init__(self, r, g, b, row, col, row_sum, col_sum):
        self.row = int(row)
        self.col = int(col)
        self.row_sum = row_sum
        self.col_sum = col_sum
        self.color = [r, g, b]

        self.up = None
        self.down = None
        self.left = None
        self.right = None


def seam_carving_by_row(head):
    def find_up(node):
        if not node.up:
            return None
        up = node.up
        if not up.left:
            if up.row_sum < up.right.row_sum:
                return up
            else:
                return up.right
        elif not up.right:
            if up.row_sum < up.left.row_sum:
                return up
            else:
                return up.left
        else:
            if up.left.row_sum < min(up.row_sum, up.right.row_sum):
                return up.left
            elif up.right.row_sum < min(up.row_sum, up.left.row_sum):
                return up.right
            else:
                return up

    last_row = head.right
    while last_row.down:
        last_row = last_row.down

    to_be_delete = last_row

    min_sum = math.inf
    while last_row:
        if last_row.row_sum < min_sum:
            to_be_delete = last_row
            min_sum = last_row.row_sum
        last_row = last_row.right

    while to_be_delete:
        up_delete = find_up(to_be_delete)
        if to_be_delete.left:
            to_be_delete.left.right = to_be_delete.right
        if to_be_delete.right:
            to_be_delete.right.left = to_be_delete.left
        if up_delete:
            to_be_delete.up.down = up_delete.down
            up_delete.down.up = to_be_delete.up

        to_be_delete = up_delete


def seam_carving_by_col(head):
    def find_left(node):
        if not node.left:
            return None
        left = node.left
        if not left.up:
            if left.col_sum < left.down.col_sum:
                return left
            else:
                return left.down
        elif not left.down:
            if left.col_sum < left.up.col_sum:
                return left
            else:
                return left.up
        else:
            if left.up.col_sum < min(left.col_sum, left.down.col_sum):
                return left.up
            elif left.down.col_sum < min(left.col_sum, left.up.col_sum):
                return left.down
            else:
                return left

    head.right.left = None
    head.right.up = head
    head.down = head.right
    head.right = None

    last_col = head.down
    while last_col.right:
        last_col = last_col.right

    to_be_delete = last_col

    min_sum = math.inf
    while last_col:
        if last_col.col_sum < min_sum:
            to_be_delete = last_col
            min_sum = last_col.col_sum
        last_col = last_col.down

    while to_be_delete:
        left_delete = find_left(to_be_delete)
        if to_be_delete.up:
            to_be_delete.up.down = to_be_delete.down
        if to_be_delete.down:
            to_be_delete.down.up = to_be_delete.up
        if left_delete:
            to_be_delete.left.right = left_delete.right
            left_delete.right.left = to_be_delete.left

        to_be_delete = left_delete

    head.down.up = None
    head.down.left = head
    head.right = head.down
    head.down = None


def show_img(head):
    rows = []
    cur = head.right
    while cur:
        rows.append(cur)
        cur = cur.down

    img_data = []
    for row in rows:
        img_data.append([])
        cur = row
        while cur:
            img_data[-1].append(cur.color)
            cur = cur.right

    array = np.asarray(img_data, dtype=np.uint8)
    image = Image.fromarray(array, 'RGB')
    return image


def get_acrosslink(damage_sum_row, damage_sum_col, img_data):
    print('construct across link...')
    head = None
    links = []
    for row in tqdm(range(img_data.shape[0])):
        head = Pixel(img_data[row][0][2], img_data[row][0][1], img_data[row][0][0], row, 0,
                     damage_sum_row[row][0], damage_sum_col[row][0])
        cur = head
        for col in range(1, img_data.shape[1]):
            cur.right = Pixel(img_data[row][col][2], img_data[row][col][1], img_data[row][col][0], row, col,
                              damage_sum_row[row][col], damage_sum_col[row][col])
            cur.right.left = cur
            cur = cur.right
        links.append(head)

    head = Pixel(-1, -1, -1, -1, -1, math.inf, math.inf)
    head.right = links[0]
    links[0].left = head
    while links[0]:
        for row, node in enumerate(links):
            if row + 1 < len(links):
                node.down = links[row + 1]
                node.down.up = node
            links[row] = node.right

    return head


def seam_carve(head):
    print('seam carving...')
    row_carve = int(arr_d.shape[0] / 2)
    col_carve = int(arr_d.shape[1] / 2)
    share = min(row_carve, col_carve)
    for _ in tqdm(range(share)):
        seam_carving_by_row(head)
        seam_carving_by_col(head)
    for _ in range(share, row_carve):
        seam_carving_by_col(head)
    for _ in range(share, col_carve):
        seam_carving_by_row(head)

    return head


if __name__ == '__main__':
    assert len(sys.argv) == 2
    img_name = sys.argv[1]

    img_path = img_name
    img_data = cv2.imread(img_path)
    arr_d = get_img_damage(img_data)
    damage_sum_row = get_sum_damage_row(arr_d)
    damage_sum_col = get_sum_damage_col(arr_d)
    head = get_acrosslink(damage_sum_row, damage_sum_col, img_data)
    head = seam_carve(head)
    image = show_img(head)
    image.save('output_' + img_name)

    print('finished!')
