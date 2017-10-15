from random import randint


class Board:

    def __init__(self):
        self.fields = [
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
        ]

    def draw(self, graphic_buffer):
        for index_y in range(len(self.fields)):
            for index_x in range(len(self.fields[index_y])):
                if self.fields[index_y][index_x] == 'o':
                    graphic_buffer[index_y][index_x] = ' '
                else:
                    graphic_buffer[index_y][index_x] = 'x'

    def is_field_occupied(self, index_y, index_x):
        if self.fields[index_y][index_x] == 'x':
            return True
        return False


class User:

    def __init__(self, step, board):
        self._set_up_user(board)
        self.step = step
        self.points = 0
        self.life = 3

    def _set_up_user(self, board):
        while True:
            y = randint(0, 10)
            x = randint(0, 16)
            if board.is_field_occupied(y, x):
                continue
            else:
                self.y = y
                self.x = x
                break

    def draw(self, graphic_buffer):
        graphic_buffer[self.y][self.x] = 'U'

    def is_brick_there(self, bricks, y, x):
        for brick in bricks:
            if (y, x) == (brick.y, brick.x):
                return True
        return False

    def make_step(self, board, bricks):
        chosen_direction = input('w/a/s/d')
        if chosen_direction == 'a':
            new_x = self.x - self.step
            if not board.is_field_occupied(self.y, new_x) and not self.is_brick_there(bricks, self.y, new_x):
                self.x -= self.step
        elif chosen_direction == 'd':
            new_x = self.x + self.step
            if not board.is_field_occupied(self.y, new_x) and not self.is_brick_there(bricks, self.y, new_x):
                self.x += self.step
        elif chosen_direction == 'w':
            new_y = self.y - self.step
            if not board.is_field_occupied(new_y, self.x) and not self.is_brick_there(bricks, new_y, self.x):
                self.y -= self.step
        elif chosen_direction == 's':
            new_y = self.y + self.step
            if not board.is_field_occupied(new_y, self.x) and not self.is_brick_there(bricks, new_y, self.x):
                self.y += self.step


class Brick:

    def __init__(self, board, user, bricks):
        self.set_up_brick(board, user, bricks)

    def draw(self, graphic_buffer):
        graphic_buffer[self.y][self.x] = '|'

    def is_field_occupied(self, bricks, y, x):
        for brick in bricks:
            if (y, x) == (brick.y, brick.x):
                return True
        return False

    def set_up_brick(self, board, user, bricks):
        while True:
            y = randint(0, 10)
            x = randint(0, 16)
            if self.is_field_occupied(bricks, y, x):
                continue
            if (y, x) == (user.y, user.x):
                continue
            if board.is_field_occupied(y, x):
                continue
            else:
                self.y = y
                self.x = x
                break


class Bomb:
    pass

board = Board()
user = User(1, board)
bricks = []
for _ in range(20):
    bricks.append(Brick(board, user, bricks))

graphic_buffer = [
    [' ' for index_x in range(len(board.fields[index_y]))] for index_y in range(len(board.fields))
]

while True:
    board.draw(graphic_buffer)
    for brick in bricks:
        brick.draw(graphic_buffer)
    user.draw(graphic_buffer)
    for row in graphic_buffer:
        print(' '.join(row))
    print('Lives: {}, Points: {}'.format(user.life, user.points))
    user.make_step(board, bricks)


# TODO:
# Bombs destroy bricks
# monster - random place, random number
# portal ending level
# level
# points
# lives
# artifacts - bigger range of bomb explosion, add life, more points
