from random import choice
import os

lo_shu_main = {2: [0, 0], 9: [0, 1], 4: [0, 2], 7: [1, 0], 5: [1, 1], 3: [1, 2], 6: [2, 0], 1: [2, 1], 8: [2, 2]}
lo_shu = lo_shu_main.copy()
weight_main = {3: [5], 2: [2, 4, 6, 8], 1: [1, 3, 7, 9]}
weight = weight_main.copy()

path = [(1,5,9), (1,6,8), (2,4,9), (2,5,8), (2,6,7), (3,4,8), (3,5,7), (4,5,6)]
weight_path = [0 for i in range(8)]
path_zip = dict(zip(path, weight_path))
path_zip_comp = path_zip.copy()
path_zip_meatbag = path_zip.copy()

win = False

A = [['-']*3 for i in range(3)]
# В показывает куда тыкать игроку
B = [['-']*3 for i in range(3)]
z = -1
for i in range(3):
    for j in range(3):
        z += 1
        B[i][j] = int(list(lo_shu_main.keys())[z])

# Защита от дурака
def xo_choose():
    while True:
        print('Игра в крестики/нолики - это про магический квадрат.')
        print('Где любой набор из 3 чисел - по диагонали/вертикали/горизонтали дает выигрышные 15 очков.')
        print('Таких наборов всего 8.')
        print('Выбирать ход следует 1 цифрой магического квадрата.')
        xo = input('Выбери на английской раскладке x или o: ', )
        try:
            if xo == 'x' or xo == 'o':
                break
            else:
                print('Будь внимательнее - введите корректный символ.')
        except ValueError:
            print('Будь внимательнее - введите корректный символ.')
    return xo


def del_key():
    for ya in weight.keys():
        if not len(weight[ya]):
            del weight[ya]
            #print('Удалил его', weight)
            return del_key()


def del_list(choose_element):
    for ya in weight.values():
        if choose_element in ya:
            ya.remove(choose_element)
           # print(ya)
   # print(weight)


def isitawin():
    global win
    if 3 in (path_zip_comp.values() or path_zip_meatbag.values()):
        print('WIN')
        win = True
        return win
    else:
        if not weight:
            print('DRAW')
            win = True
            return win

# Удаляем стратегии в которых заняты 2 + 1 клетки в ряд
def del_path():
    keys = [key for key, value in path_zip_comp.items() if value == 2]
    for ya in keys:
        if path_zip_meatbag[ya] == 1:
            del path_zip_meatbag[ya]
            del path_zip_comp[ya]
    keys = [key for key, value in path_zip_meatbag.items() if value == 2]
    for ya in keys:
        if path_zip_comp[ya] == 1:
            del path_zip_meatbag[ya]
            del path_zip_comp[ya]


# Ход компьютера
def move_comp():
    del_path()
    # Стратегия - если можешь победить - сделай это
    if 2 in path_zip_comp.values():
        keys = [key for key, value in path_zip_comp.items() if value == 2]
        for ya in range(3):
            if A[lo_shu[keys[0][ya]][0]][lo_shu[keys[0][ya]][1]] == '-':
                choose_element = keys[0][ya]
                print('Хочу победить!', choose_element)
             #   break
            else:
                if ya == 2:
                    print('Некуда ствить')
                    continue
    # Стратегия - помешай победить противнику
    elif 2 in path_zip_meatbag.values():
        keys = [key for key, value in path_zip_meatbag.items() if value == 2]
        for ya in range(3):
            if A[lo_shu[keys[0][ya]][0]][lo_shu[keys[0][ya]][1]] == '-':
                choose_element = keys[0][ya]
                print('Тебе не победить!',choose_element)
            else:
                # max_key = max(weight.keys())
                # choose_element = choice(weight[max_key])
                continue
    else:
        max_key = max(weight.keys())
        choose_element = choice(weight[max_key])
    del_list(choose_element)
    return choose_element

# Ход человека
def move_meatbag():
    # Проверка свободных полей в матрице. keys[] - это список со свободными полями
    keys = []
    for ya in range(3):
        for i in range(3):
            if A[ya][i] == '-':
                keys += [key for key, value in lo_shu.items() if value == [ya, i]]
    while True:
        choose_element = int(input('Делай ход: ',))
        try:
            if any([i == choose_element for i in keys]):
                break
            else:
                print('Будь внимательнее - туда уже ходили.')
        except ValueError:
            print('Будь внимательнее - туда уже ходили.')
    del_list(choose_element)
    return choose_element

# Рисуем игровое поле
def show_matrix(A):
    for row in A:
        for element in row:
            print(element, end=' ')
        print()

# Выбираем из словаря path_zip_comp те стратегии, которые могут быть использованы при выборе choose_element
def filt_comp(choose_element):
    return list(filter(lambda ya: choose_element in ya, path_zip_comp.keys()))

# Стратегия для игрока
def filt_meatbag(choose_element):
    return list(filter(lambda ya: choose_element in ya, path_zip_meatbag.keys()))

# Добавляем +1 в values в словарь path_zip для использованных стратегий
# Если в values будет 2 - то остается 1 ход до выигрыша и необходимо срочно поставить в свободное поле х или о
def plus_comp(filt_comp):
    for ya in filt_comp:
        path_zip_comp[ya] += 1


def plus_meatbag(filt_meatbag):
    for ya in filt_meatbag:
        path_zip_meatbag[ya] += 1


### Begin!!!

side = xo_choose() == 'x'
if side:
    print("Выбран х")
    while not win:
        # ход человека
        choose_element = move_meatbag()
        A[lo_shu[choose_element][0]][lo_shu[choose_element][1]] = 'x' # Заполняем матрицу А в соответсвующей клетке
        os.system('cls||clear')
        show_matrix(B)
        show_matrix(A)
        filt_meatbag(choose_element)
        plus_meatbag(filt_meatbag(choose_element))
        del_key()
        isitawin()
        if win:
            break
        # ход компьютера
        choose_element = move_comp()
        A[lo_shu[choose_element][0]][lo_shu[choose_element][1]] = 'o' # Заполняем матрицу А в соответсвующей клетке
        os.system('cls||clear')
        show_matrix(B)
        show_matrix(A)
        filt_comp(choose_element)
        plus_comp(filt_comp(choose_element))
        del_key()
        isitawin()
else:
    print("Выбран o")
    while not win:
        # ход компьютера
        choose_element = move_comp()
        A[lo_shu[choose_element][0]][lo_shu[choose_element][1]] = 'x' # Заполняем матрицу А в соответсвующей клетке
        os.system('cls||clear')
        show_matrix(B)
        show_matrix(A)
        filt_comp(choose_element)
        plus_comp(filt_comp(choose_element))
        del_key()
        isitawin()
        if win:
            break
        # ход человека
        choose_element = move_meatbag()
        A[lo_shu[choose_element][0]][lo_shu[choose_element][1]] = 'o'  # Заполняем матрицу А в соответсвующей клетке
        os.system('cls||clear')
        show_matrix(B)
        show_matrix(A)
        filt_meatbag(choose_element)
        plus_meatbag(filt_meatbag(choose_element))
        del_key()
        isitawin()
