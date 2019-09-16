#!/usr/bin/env python
# coding: utf-8

import random
import math


# генерация вариантов
def generate_variant():
    k = 0
    # степень e
    while (k == 0):
        k = random.randint(-30, 30)

    # вторая функция
    n = random.randint(1, 99)

    if (n <= 33):
        n = 'sin(x)'
        order = 0
    elif (n <= 66):
        n = 'cos(x)'
        order = 0
    else:
        n = random.randint(1, 20)
        order = n

        n = 'x^{%i}' % n
        if (order == 1):
            n = 'x'

    return ([n, k, order])


# Евклид для сокращения дробей
def GCD(a, b):
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    return a + b


# меняет текущий знак
def change_sign(prev_sign, sign):
    if prev_sign == '' and sign == ' + ':
        return ""

    elif prev_sign == ' + ':
        if sign == ' + ' or sign == "":
            return ' + '
        else:
            return ' - '

    elif prev_sign == ' - ':
        if sign == ' + ' or sign == "":
            return ' - '
        else:
            return ' + '
    return sign


# d(exp^kx) и интегрирование по частям
def change(f, k, new_k, sign, beginning, cur_k=''):
    ans = beginning + sign + r'%s\int %s\,d(e^{%sx})' % (new_k, f, k)

    ans += ' = '

    ans += beginning + sign + r'%se^{%sx}*%s %s %s\int e^{%sx}\,d(%s)' % (
        new_k, k, f, change_sign(' - ', sign), new_k, k, f)

    ans += ' = '
    return ans


# расписывает решение для синуса и косинуса
def solve_sin_cos(f, k, new_k, order):
    # знак текущего множителя
    sign = ' + '

    if k == '-' or k != '' and k < 0:
        sign = ' - '
        if (k == '-'):
            new_k = ''

    # первое интегрирование по частям
    ans = change(f, k, new_k, change_sign('', sign), "")
    # часть без интеграла, запоминаем ее
    old = change_sign('', sign) + r'%se^{%sx}*%s' % (new_k, k, f)

    # смена функции под интегралом и текущего знака(берем производную)
    if (f == 'sin(x)'):
        f = r'cos(x)'
        cur_sign = change_sign(' - ', sign)
    else:
        f = r'sin(x)'
        cur_sign = sign

    # переход к dx
    ans += old + r'%s%s\int e^{%sx}*%s\,dx' % (cur_sign, new_k, k, f) + ' = '

    # знак текущего слагаемого
    sign = change_sign(cur_sign, sign)

    # новый множитель перед интегралом
    if (k == '-' or k == ''):
        new_k = ''
    else:
        new_k = r'%i^{-1}' % (k * k)
    # второе интегрирование по частям
    ans += change(f, k, new_k, sign, old)

    old += sign + r'%se^{%sx}*%s' % (new_k, k, f)

    # берем производную
    if (f == 'sin(x)'):
        f = r'cos(x)'
        cur_sign = change_sign(' - ', sign)
    else:
        f = r'sin(x)'
        cur_sign = sign

    # переход к dx
    ans += old + r'%s%s\int e^{%sx}*%s\,dx$$' % (cur_sign, new_k, k, f) + ' ,\n\n'
    # запись решения
    solve.write(ans)

    if (new_k == ''):
        return r'\frac{%s}{2} + C' % (old)
    # ответ
    return r'\frac{%s}{1+%s} + C' % (old, new_k)


# задает новую дробь по делимому и делителю
def set_fraction(divider, divisor):
    if (divisor != 1):
        frac = r'\frac{%s}{%s}' % (divider, divisor)
    elif divider != 1:
        frac = r'%s' % divider
    else:
        frac = ''

    if (frac == 1 or frac == -1):
        frac = ''

    return frac


# варианты для x^n
def solve_x(f, k, order):
    divisor = 1

    # знак текущего множителя
    sign = ' + '

    if (k == '-' or k != '' and k < 0):
        sign = ' - '
        if (k == '-'):
            new_k = ''

    ans = ""
    prev_sign = ''
    old = ""
    divider = 1

    while (order > 0):
        # делитель домножается на степень e(когда заносим e^k под знак дифференциала)
        if (k != '-' and k != ''):
            divisor *= math.fabs(int(k))

        frac = set_fraction(int(divider), int(divisor))

        # интегрирование по частям
        ans += change(f, k, frac, change_sign(prev_sign, sign), old)
        # часть без интеграла, запоминаем ее
        old += change_sign(prev_sign, sign) + r'%se^{%sx}*%s' % (frac, k, f)

        # знак перед интегральной частью
        prev_sign = change_sign(' - ', change_sign(prev_sign, sign))

        # сокращаем дробь при выносе степени x
        gcd = GCD(divisor, divider * order)
        divider, divisor = divider * order / gcd, divisor / gcd

        frac = set_fraction(int(divider), int(divisor))

        order -= 1
        f = 'x^{%i}' % order
        if (order == 1):
            f = 'x'
        # финальная итерация
        if (order == 0):
            if (k != '-' and k != ''):
                divisor *= math.fabs(int(k))

            gcd = GCD(divisor, divider)
            divider, divisor = divider / gcd, divisor / gcd

            frac = set_fraction(int(divider), int(divisor))
            res = old + r'%s%se^{%sx}' % (change_sign(prev_sign, sign), frac, k)
            break
        # переход к dx
        ans += old + r'%s%s\int e^{%sx}*%s\,dx' % (prev_sign, frac, k, f) + ' = '

    ans += res + " + C$$"
    solve.write(ans)
    return (res)


# проверка на корректность кол-ва вариантов
while True:
    try:
        N = int(input("Enter the number of variants (not more than 200) "))
    except ValueError:
        print("Invalid input ")
        continue
    else:
        if (N > 200 or N < 1):
            print("Invalid input ")
            continue
        break

# проверка на корректность имени файла
while True:
    try:
        name = input("Enter filename: ")
        f = open(name + '.tex', 'w', encoding='utf-8')
    except OSError:
        print("Invalid file name ")
        continue
    else:
        if (not name == ""):
            break

random.seed();
# для проверки уникальности вариантов
variants = []

with open(name + '_solve.tex', 'w', encoding='utf-8') as solve:
    with open(name + '_ans.tex', 'w', encoding='utf-8') as ans:
        for i in range(N):

            # f-условия,solve-решения,ans-условия+ответы
            f.write('Вариант ' + str(i + 1) + '\n')
            solve.write('Вариант ' + str(i + 1) + '\n')
            ans.write('Вариант ' + str(i + 1) + '\n')

            var = generate_variant()

            # проверка варианта на уникальность
            while ([i for i in variants if i == var] != []):
                var = generate_variant()

            variants.append(var)

            # функция
            h = var[0]
            # степень экспоненты
            k = var[1]
            # степень x
            order = var[2]

            # k-строковое представление степени e,new_k - строковое представление abs(k)^-1
            if (k == 1):
                new_k = ''
                k = ''

            elif (k == -1):
                new_k = '-'
                k = '-'
            else:
                new_k = r'%i^{-1}*' % math.fabs(k)

            f.write(r'$$\int e^{%sx}%s\,dx$$' % (k, h) + '\n')
            solve.write(r'$$\int e^{%sx}%s\,dx' % (k, h) + ' = ')

            if (h == 'sin(x)' or h == 'cos(x)'):
                answer = r'$$\int e^{%sx}\%s\,dx' % (k, h) + ' = ' + solve_sin_cos(h, k, new_k, order) + '$$'
                solve.write(answer)
                ans.write(answer + '\n')
            else:
                ans.write(r'$$\int e^{%sx}%s\,dx' % (k, h) + ' = ')
                ans.write(solve_x(h, k, order) + " + C$$")

            solve.write('\n')
            ans.write('\n')

f.close()
print("Generated")

# Вариант 1
# $$\int e^{16x}cos(x)\,dx = 16^{-1}*\int cos(x)\,d(e^{16x}) = 16^{-1}*e^{16x}*cos(x)  -  16^{-1}*\int e^{16x}\,d(cos(x)) = 16^{-1}*e^{16x}*cos(x) + 16^{-1}*\int e^{16x}*sin(x)\,dx = 16^{-1}*e^{16x}*cos(x) + 256^{-1}\int sin(x)\,d(e^{16x}) = 16^{-1}*e^{16x}*cos(x) + 256^{-1}e^{16x}*sin(x)  -  256^{-1}\int e^{16x}\,d(sin(x)) = 16^{-1}*e^{16x}*cos(x) + 256^{-1}e^{16x}*sin(x) - 256^{-1}\int e^{16x}*cos(x)\,dx$$ ,
# 
# $$\int e^{16x}\cos(x)\,dx = \frac{16^{-1}*e^{16x}*cos(x) + 256^{-1}e^{16x}*sin(x)}{1+256^{-1}} + C$$
# Вариант 2
# $$\int e^{-x}sin(x)\,dx =  - \int sin(x)\,d(e^{-x}) =  - e^{-x}*sin(x)  +  \int e^{-x}\,d(sin(x)) =  - e^{-x}*sin(x) + \int e^{-x}*cos(x)\,dx =  - e^{-x}*sin(x) - \int cos(x)\,d(e^{-x}) =  - e^{-x}*sin(x) - e^{-x}*cos(x)  +  \int e^{-x}\,d(cos(x)) =  - e^{-x}*sin(x) - e^{-x}*cos(x) - \int e^{-x}*sin(x)\,dx$$ ,
# 
# $$\int e^{-x}\sin(x)\,dx = \frac{ - e^{-x}*sin(x) - e^{-x}*cos(x)}{2} + C$$
# Вариант 3
# $$\int e^{-6x}cos(x)\,dx =  - 6^{-1}*\int cos(x)\,d(e^{-6x}) =  - 6^{-1}*e^{-6x}*cos(x)  +  6^{-1}*\int e^{-6x}\,d(cos(x)) =  - 6^{-1}*e^{-6x}*cos(x) - 6^{-1}*\int e^{-6x}*sin(x)\,dx =  - 6^{-1}*e^{-6x}*cos(x) + 36^{-1}\int sin(x)\,d(e^{-6x}) =  - 6^{-1}*e^{-6x}*cos(x) + 36^{-1}e^{-6x}*sin(x)  -  36^{-1}\int e^{-6x}\,d(sin(x)) =  - 6^{-1}*e^{-6x}*cos(x) + 36^{-1}e^{-6x}*sin(x) - 36^{-1}\int e^{-6x}*cos(x)\,dx$$ ,
# 
# $$\int e^{-6x}\cos(x)\,dx = \frac{ - 6^{-1}*e^{-6x}*cos(x) + 36^{-1}e^{-6x}*sin(x)}{1+36^{-1}} + C$$
# Вариант 4
# $$\int e^{-2x}sin(x)\,dx =  - 2^{-1}*\int sin(x)\,d(e^{-2x}) =  - 2^{-1}*e^{-2x}*sin(x)  +  2^{-1}*\int e^{-2x}\,d(sin(x)) =  - 2^{-1}*e^{-2x}*sin(x) + 2^{-1}*\int e^{-2x}*cos(x)\,dx =  - 2^{-1}*e^{-2x}*sin(x) - 4^{-1}\int cos(x)\,d(e^{-2x}) =  - 2^{-1}*e^{-2x}*sin(x) - 4^{-1}e^{-2x}*cos(x)  +  4^{-1}\int e^{-2x}\,d(cos(x)) =  - 2^{-1}*e^{-2x}*sin(x) - 4^{-1}e^{-2x}*cos(x) - 4^{-1}\int e^{-2x}*sin(x)\,dx$$ ,
# 
# $$\int e^{-2x}\sin(x)\,dx = \frac{ - 2^{-1}*e^{-2x}*sin(x) - 4^{-1}e^{-2x}*cos(x)}{1+4^{-1}} + C$$
# Вариант 5
# $$\int e^{-15x}cos(x)\,dx =  - 15^{-1}*\int cos(x)\,d(e^{-15x}) =  - 15^{-1}*e^{-15x}*cos(x)  +  15^{-1}*\int e^{-15x}\,d(cos(x)) =  - 15^{-1}*e^{-15x}*cos(x) - 15^{-1}*\int e^{-15x}*sin(x)\,dx =  - 15^{-1}*e^{-15x}*cos(x) + 225^{-1}\int sin(x)\,d(e^{-15x}) =  - 15^{-1}*e^{-15x}*cos(x) + 225^{-1}e^{-15x}*sin(x)  -  225^{-1}\int e^{-15x}\,d(sin(x)) =  - 15^{-1}*e^{-15x}*cos(x) + 225^{-1}e^{-15x}*sin(x) - 225^{-1}\int e^{-15x}*cos(x)\,dx$$ ,
# 
# $$\int e^{-15x}\cos(x)\,dx = \frac{ - 15^{-1}*e^{-15x}*cos(x) + 225^{-1}e^{-15x}*sin(x)}{1+225^{-1}} + C$$
# 

# $$\int e^{74x}\sin(x)\,dx = \frac{74^{-1}*e^{74x}*sin(x) - 5476^{-1}e^{74x}*cos(x)}{1+5476^{-1}} + C$$
# 

# $$\int e^{k*x}*x^n\,dx  \int e^{k*x}*\cos(x)\,dx   \int e^{k*x}*\sin(x)\,dx$$
# 

# $$\int e^{105x}\cos(x)\,dx = 105^{-1}*\int cos(x)\,d(e^{105x}) = 105^{-1}*e^{105x}*cos(x)  -  105^{-1}*\int e^{105x}\,d(cos(x)) = 105^{-1}*e^{105x}*cos(x) + 105^{-1}*\int e^{105x}*sin(x)\,dx = 105^{-1}*e^{105x}*cos(x) + 11025^{-1}\int sin(x)\,d(e^{105x}) = 105^{-1}*e^{105x}*cos(x) + 11025^{-1}e^{105x}*sin(x)  -  11025^{-1}\int e^{105x}\,d(sin(x)) = 105^{-1}*e^{105x}*cos(x) + 11025^{-1}e^{105x}*sin(x) - 11025^{-1}\int e^{105x}*cos(x)\,dx$$ ,
# 
# $$\int e^{105x}\cos(x)\,dx = \frac{105^{-1}*e^{105x}*cos(x) + 11025^{-1}e^{105x}*sin(x)}{1+11025^{-1}} + C$$
# 
# 

# $$\int e^{-16x}\cos(x)\,dx =  - 16^{-1}*\int cos(x)\,d(e^{-16x}) =  - 16^{-1}*e^{-16x}*cos(x)  +  16^{-1}*\int e^{-16x}\,d(cos(x)) =  - 16^{-1}*e^{-16x}*cos(x) - 16^{-1}*\int e^{-16x}*sin(x)\,dx =  - 16^{-1}*e^{-16x}*cos(x) + 256^{-1}\int sin(x)\,d(e^{-16x}) =  - 16^{-1}*e^{-16x}*cos(x) + 256^{-1}e^{-16x}*sin(x)  -  256^{-1}\int e^{-16x}\,d(sin(x)) =  - 16^{-1}*e^{-16x}*cos(x) + 256^{-1}e^{-16x}*sin(x) - 256^{-1}\int e^{-16x}*cos(x)\,dx$$ ,
# 
# $$\int e^{-16x}\cos(x)\,dx = \frac{ - 16^{-1}*e^{-16x}*cos(x) + 256^{-1}e^{-16x}*sin(x)}{1+256^{-1}} + C$$

# $$\int e^{45x}\sin(x)\,dx = 45^{-1}*\int sin(x)\,d(e^{45x}) = 45^{-1}*e^{45x}*sin(x)  -  45^{-1}*\int e^{45x}\,d(sin(x)) = 45^{-1}*e^{45x}*sin(x) - 45^{-1}*\int e^{45x}*cos(x)\,dx = 45^{-1}*e^{45x}*sin(x) - 2025^{-1}\int cos(x)\,d(e^{45x}) = 45^{-1}*e^{45x}*sin(x) - 2025^{-1}e^{45x}*cos(x)  +  2025^{-1}\int e^{45x}\,d(cos(x)) = 45^{-1}*e^{45x}*sin(x) - 2025^{-1}e^{45x}*cos(x) - 2025^{-1}\int e^{45x}*sin(x)\,dx$$ ,
# 
# $$\int e^{45x}\sin(x)\,dx = \frac{45^{-1}*e^{45x}*sin(x) - 2025^{-1}e^{45x}*cos(x)}{1+2025^{-1}} + C$$

# $$\int e^{-66x}\sin(x)\,dx =  - 66^{-1}*\int sin(x)\,d(e^{-66x}) =  - 66^{-1}*e^{-66x}*sin(x)  +  66^{-1}*\int e^{-66x}\,d(sin(x)) =  - 66^{-1}*e^{-66x}*sin(x) + 66^{-1}*\int e^{-66x}*cos(x)\,dx =  - 66^{-1}*e^{-66x}*sin(x) - 4356^{-1}\int cos(x)\,d(e^{-66x}) =  - 66^{-1}*e^{-66x}*sin(x) - 4356^{-1}e^{-66x}*cos(x)  +  4356^{-1}\int e^{-66x}\,d(cos(x)) =  - 66^{-1}*e^{-66x}*sin(x) - 4356^{-1}e^{-66x}*cos(x) - 4356^{-1}\int e^{-66x}*sin(x)\,dx$$ ,
# 
# $$\int e^{-66x}\sin(x)\,dx = \frac{ - 66^{-1}*e^{-66x}*sin(x) - 4356^{-1}e^{-66x}*cos(x)}{1+4356^{-1}} + C$$
