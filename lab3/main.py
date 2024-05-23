import math

tabl3 = [
    [1, 0, None, 0.02],
    [1, 0, 0, 0.12],
    [1, 0, 1, 0.35],
    [1, 1, None, -0.015],
    [1, 1, 0, -0.5],
    [1, 1, 1, 0.24],
    [2, 0, None, -0.084],
    [2, 0, 0, -0.33],
    [2, 0, 1, 0.27],
    [2, 1, None, 0.037],
    [2, 1, 0, -0.08],
    [2, 1, 1, 0.79],
    [3, 0, None, 0.04],
    [3, 0, 0, 0.062],
    [3, 0, 1, 0.64],
]

x = []

delta = [None, None, None]

n = 0.8

A = 1
a = [0, 1]


def f(s):
    return 1 / (1 + math.exp(-A * s))


def w(n, q, i, j):
    return -n * delta[q - 1][j] * (1 if i is None else x[(q - 2) * 2 + i][-1])


def iterachiya(index):
    global tabl3, x, delta, n, A, a

    print()
    print()
    print()
    print('$' * 30 + ' ' * 10 + f'Итерация {index + 1}' + ' ' * 10 + '$' * 30)
    print()
    print()
    print()

    if index == 2:
        a = [1, 1]

    x = []
    print('Таблица 3')
    for line in tabl3:
        print(*line)
    print()

    first_layer = [(1, i, f(tabl3[1 + 3 * i][-1] * a[0] +
                            tabl3[2 + 3 * i][-1] * a[1] +
                            tabl3[0 + 3 * i][-1]))
                   for i in range(2)]  # Расчет 1 слоя

    x += first_layer

    second_layer = [(2, i, f(tabl3[7 + 3 * i][-1] * first_layer[0][-1] +
                             tabl3[8 + 3 * i][-1] * first_layer[1][-1] +
                             tabl3[6 + 3 * i][-1]))  # Расчет 2 слоя
                    for i in range(2)]
    x += second_layer

    output_layer = (3, 0, f(tabl3[13][-1] * second_layer[0][-1] +
                            tabl3[14][-1] * second_layer[1][-1] +
                            tabl3[12][-1]))  # Расчет выходного слоя
    x.append(output_layer)

    print('Таблица 4')
    for line in x:
        print(*line)
    print()

    y = 1
    E2 = 0.5 * ((y - x[-1][-1]) ** 2)
    print(f'Ошибка ИНС E2={E2}')
    print()

    delta[2] = [A * x[-1][-1] * (1 - x[-1][-1]) * (x[-1][-1] - y)]
    print(f'delta3 {delta[2]}')

    delta[1] = [A * x[-3 + i][-1] * (1 - x[-3 + i][-1]) * delta[2][0] * tabl3[4 * 3 + 1 + i][-1] for i in range(2)]
    print(f'delta2 {delta[1]}')

    delta[0] = [A * x[-5 + i][-1] * (1 - x[-5 + i][-1]) * sum(
        [delta[1][j] * tabl3[2 * 3 + 1 + i + j * 3][-1] for j in range(2)]) for i in range(2)]
    print(f'delta1 {delta[0]}')
    print()

    res = []

    print('Новые веса связей ИНС')
    for q in [1, 2, 3]:
        for j in [0, 1]:
            for i in [None, 0, 1]:
                founded = list(filter(lambda x: x[0] == q and x[1] == j and x[2] == i, tabl3))
                if len(founded) != 0:
                    aaa = founded[0][-1]
                    print(f"{i} {j} {q} {aaa + w(n, q, i, j)}")
                    res.append([q, j, i, aaa + w(n, q, i, j)])

    tabl3 = res


if __name__ == '__main__':
    for i in range(3):
        iterachiya(i)
