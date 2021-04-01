import time
import pandas as pd
import numpy as np  # 仅用来计算构造对数
import matplotlib.pyplot as plt  # 绘图库


# -------------简单递归求解，复杂度\Theta(a^n)------------
def naive_recursive(n):
    assert n >= 0 and isinstance(n, int)
    if n == 0:
        return 0
    if n == 1:
        return 1
    return naive_recursive(n - 1) + naive_recursive(n - 2)


# -------------递推求解，复杂度\Theta(n)------------
def bottom_up(n):
    assert n >= 0 and isinstance(n, int)
    arr = [0] * (n + 1)
    arr[1] = 1
    for i in range(2, n + 1):
        arr[i] = arr[i - 1] + arr[i - 2]
    return arr[n]


# -------------利用矩阵递归求解，复杂度\Theta(lgn)------------
class Matrix:
    def __init__(self, a_1, a_2, a_3, a_4):
        self.a_1 = a_1
        self.a_2 = a_2
        self.a_3 = a_3
        self.a_4 = a_4


def matrix_multiply(m1, m2):
    c_1 = m1.a_1 * m2.a_1 + m1.a_2 * m2.a_3
    c_2 = m1.a_1 * m2.a_2 + m1.a_2 * m2.a_4
    c_3 = m1.a_3 * m2.a_1 + m1.a_4 * m2.a_3
    c_4 = m1.a_3 * m2.a_2 + m1.a_4 * m2.a_4
    m3 = Matrix(c_1, c_2, c_3, c_4)
    return m3


def matrix_power(n):
    assert n > 0 and isinstance(n, int)
    if n == 1:
        return Matrix(1, 1, 1, 0)
    if n % 2 == 0:
        return matrix_multiply(matrix_power(int(n / 2)), matrix_power(int(n / 2)))
    else:
        m1 = matrix_power(int(n / 2))
        m2 = matrix_multiply(m1, Matrix(1, 1, 1, 0))
        return matrix_multiply(m1, m2)


def recursive_squaring(n):  # 利用矩阵递归求解，复杂度\Theta(lgn)
    result_matrix = matrix_power(n)
    return result_matrix.a_2


# --------------作图----------------
def paint(data):  # data为多元组的列表即可，每个多元组第一个元素代表n
    x = []
    y_all = []
    for i in range(len(data[0]) - 1):
        y_all.append([])

    for i in range(len(data)):
        x.append(data[i][0])
        for t in range(len(data[0]) - 1):
            y_all[t].append(data[i][t + 1])

    # paint
    plt.xlim(xmax=x[-1] * 1.1, xmin=x[0])
    ymax = 0
    for i in range(len(data[0]) - 1):
        if y_all[i][-1] > ymax:
            ymax = y_all[i][-1]
    plt.ylim(ymax=ymax * 1.1, ymin=0)

    for i in range(len(data[0]) - 1):
        plt.plot(x, y_all[i])

    plt.show()


# --------------------制表--------------------
def generate_csv(record,name):
    len_attr = len(record[0]) - 1
    dict = {}
    dict['n'] = [r[0] for r in record]
    for attr in range(len_attr):
        dict[str(attr)] = [r[attr + 1] for r in record]
    df = pd.DataFrame(dict)
    df.to_csv(name+".csv")


# ----------------时间复杂度比较-----------------
def compare_3_methods():
    record = []
    for n in range(1, 15):
        t0 = time.process_time()
        ans1 = naive_recursive(n)
        t1 = time.process_time()
        ans2 = bottom_up(n)
        t2 = time.process_time()
        ans3 = recursive_squaring(n)
        t3 = time.process_time()

        assert ans1 == ans2 and ans2 == ans3

        record.append((n, t1 - t0, t2 - t1, t3 - t2))
        print(record[-1])

    paint(record)
    # generate_csv(record,'exp1')


def compare_2_methods():
    record = []
    for n in [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, ]:
        t1 = time.process_time()
        ans2 = bottom_up(n)
        t2 = time.process_time()
        ans3 = recursive_squaring(n)
        t3 = time.process_time()

        assert ans2 == ans3

        record.append((np.log10(n), t2 - t1, t3 - t2))
        print(record[-1])

    paint(record)
    # generate_csv(record,'exp2')


def compare_recursive_squaring_with_log():
    record = []
    for n in [10000,50000,100000,500000,1000000,5000000,10000000]:
        t2 = time.process_time()
        ans3 = recursive_squaring(n)
        t3 = time.process_time()
        record.append((np.log10(n), np.log10(n), t3 - t2))
        print(record[-1])
    paint(record)
    # generate_csv(record,'exp3')


# ----------------开始测试-----------------
if __name__ == '__main__': #  依次运行以下三行代码即可
    compare_3_methods()
    compare_2_methods()
    compare_recursive_squaring_with_log()
