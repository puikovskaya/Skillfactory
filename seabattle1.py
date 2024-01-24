from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Зафиксирована попытка выстрела за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "В эту клетку уже был выстрел!"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x},{self.y})'


class Ship:
    def __init__(self, head, orientation, l):
        self.head = head
        self.l = l
        self.orientation = orientation
        self.life = l

    @property
    def get_dots(self):
        ship_dots = []
        for i in range(self.l):
            body_x = self.head.x
            body_y = self.head.y
            if self.orientation == 0:
                body_x += i
            elif self.orientation == 1:
                body_y += i
            ship_dots.append(Dot(body_x, body_y))
        return ship_dots

    def shooting(self, shot):
        return shot in self.get_dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size  # размер поля
        self.hid = hid  # видимость корабля

        self.count = 0  # счетчик подбитых кораблей
        self.field = [['0'] * size for _ in range(size)]
        self.busy = []  # занятые точки
        self.ships = []

    def __str__(self):
        res = ''
        res += '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " | "

        if self.hid:
            res = res.replace('■', 'O')
        return str(res)

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for d in ship.get_dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.get_dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()

        for d in ship.get_dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)
        for ship in self.ships:
            if ship.shooting(d):
                ship.life -= 1
                self.field[d.x][d.y] = 'X'
                if ship.life == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Корабль полностью уничтожен!')
                    return False
                else:
                    print('Корабль ранен')
                    return True
        self.field[d.x][d.y] = '.'
        print('Мимо!')
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютера: {d.x + 1} {d.y + 1}')
        return d


class User(Player):
    def ask(self):
        while True:
            coord = input("Ваш ход: ").split()
            if len(coord) != 2:
                print('Введите две координаты!')
                continue

            x, y = coord
            if not (x.isdigit()) or not (y.isdigit()):
                print('Введите числа! ')
                continue

            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        board_player = self.random_board()
        board_comp = self.random_board()
        board_comp.hid = True
        self.ai = AI(board_comp, board_player)
        self.us = User(board_player, board_comp)

    def try_random_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1), l)
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_random_board()
        return board

    @staticmethod
    def greet():
        print('Вы в игре Морской Бой\n Для хода введите значение координаты x (номер строки) и y (номер столбца) '
              'через пробел, куда хотите ударить')

    def loop(self):
        num = 0
        while True:
            print("Доска пользователя: \n", self.us.board)
            print('Доска компьютера: \n', self.ai.board)
            if num % 2 == 0:
                print('Ход пользователя')
                repeat = self.us.move()
            else:
                print('Ход компьютера')
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print('Победа пользователя!')
                break
            if self.us.board.count == 7:
                print('Победа компьютера!')
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
