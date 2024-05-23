import numpy as np

P = np.matrix(
    [
        [0.6, 0.1, 0.1, 0.2],
        [0.1, 0.6, 0.0, 0.3],
        [0.1, 0.0, 0.6, 0.3],
        [0.0, 0.0, 0.0, 1],
    ]
)
print(f"Проверка корректности задания матрицы: {np.all(np.sum(P, axis=1) == 1)}")
p1 = np.array([1, 0, 0, 0])
count_times = 3

for current_count_times in range(1, count_times + 1):
    p_res = p1.dot(np.linalg.matrix_power(P, current_count_times))
    print(f"Вероятность состояния устройства на день {current_count_times} {p_res}")
    print(f"Перепроверка корректности: {np.sum(p_res) == 1}")

P = np.matrix(
    [
        [0.4, 0.6, 0.0, 0.0],  # 3%
        [0.2, 0.5, 0.3, 0.0],  # 3.5%
        [0.1, 0.4, 0.3, 0.2],  # 4%
        [0.0, 0.3, 0.4, 0.3],  # 4.5%
    ]
)

print(f"Проверка корректности задания матрицы: {np.all(np.sum(P, axis=1) == 1)}")
p1 = np.array([0, 0, 1, 0])
count_times = 3

p_res = p1.dot(np.linalg.matrix_power(P, count_times))
print(f"Вероятность состояния банка в конце квартала {count_times} {p_res}")
print(f"Перепроверка корректности: {np.sum(p_res) == 1}")

count_times = 3
p = np.array([0.4, 0.6])
P = np.matrix(
    [
        [0.8, 0.2],
        [0.7, 0.3],
    ]
)

R = np.matrix([
    [6, 10],
    [3, 7], ]
)

q = np.matrix(
    [
        np.sum([P[i, j] * R[i, j]
                for j in range(P.shape[1])
                ])
        for i in range(P.shape[0])]
)
print(q)

v = [[0] * P.shape[0]]

for k in range(1, count_times + 1):
    v.append(
        [
            q[0, i] + np.sum([P[i, j] * v[k - 1][j]
                              for j in range(P.shape[1])])
            for i in range(P.shape[0])]
    )

for i in range(len(v)):
    print(f'v[{i}]: {v[i]}')
