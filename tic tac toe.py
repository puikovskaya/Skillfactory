#Задаём начальную матрицу игры
field = [[' ', '1', '2', '3'],
         ['1', '-', '-', '-'],
         ['2', '-', '-', '-'],
         ['3', '-', '-', '-']]

#Функция вывода матрицы
def matrix_output():
    for i in field:
        for j in i:
            print(f'{j}', end=' ')
        print()
matrix_output()

#функция определения победы
def wins():
    for i in range(4):
        #по строкам и столбцам
        if ((field[i][1]==field[i][2]==field[i][3] != '-')
                or (field[1][i]==field[2][i]==field[3][i] != '-')):
            return 1
        #по диагонали
        if ((field[1][1]==field[2][2]==field[3][3] != '-')
                or (field[3][1]==field[2][2]==field[1][3] != '-')):
            return 1
    return 0

#функция процесса игры
def motion():
    win = 0
    for i in range(1, 10):
        right = 0
        while not right:
            x = int(input('Выберите столбец для своего хода '))
            y = int(input('А теперь строку '))
            if field[y][x] == '-':
                right = 1
            else:
                print('В этой ячейке значение уже есть, повторите ввод')

        if i % 2 == 0:
            field[y][x] = '0'
        else:
            field[y][x] = 'x'

        matrix_output()

        if wins() and i >= 5:
            if i % 2 == 0:
                print('Победа 0')
                win = 1
                break
            elif i % 2 == 1:
                print('Победа х')
                win = 1
                break
    if win == 0:
        print('Ничья')

motion()