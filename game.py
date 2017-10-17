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

    def draw(self, graphic_buffer, _context):
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

    def draw(self, graphic_buffer, _context):
        graphic_buffer[self.y][self.x] = 'U'

    def is_brick_there(self, bricks, y, x):
        for brick in bricks:
            if (y, x) == (brick.y, brick.x):
                return True
        return False

    def make_step(self, context):
        chosen_direction = input('w/a/s/d/space')
        if chosen_direction == 'a':
            new_x = self.x - self.step
            if not context.board.is_field_occupied(self.y, new_x) and not self.is_brick_there(context.bricks, self.y, new_x):
                self.x -= self.step
        elif chosen_direction == 'd':
            new_x = self.x + self.step
            if not context.board.is_field_occupied(self.y, new_x) and not self.is_brick_there(context.bricks, self.y, new_x):
                self.x += self.step
        elif chosen_direction == 'w':
            new_y = self.y - self.step
            if not context.board.is_field_occupied(new_y, self.x) and not self.is_brick_there(context.bricks, new_y, self.x):
                self.y -= self.step
        elif chosen_direction == 's':
            new_y = self.y + self.step
            if not context.board.is_field_occupied(new_y, self.x) and not self.is_brick_there(context.bricks, new_y, self.x):
                self.y += self.step
        elif chosen_direction == ' ':
            context.bombs.append(Bomb(context.user))


class Brick:

    REWARD = 10

    def __init__(self, board, user, bricks):
        self.set_up_brick(board, user, bricks)

    def draw(self, graphic_buffer, _context):
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


class Portal:

    def __init__(self, y, x):
        self.y = y
        self.x = x

    def draw(self, graphic_buffer, _context):
        graphic_buffer[self.y][self.x] = 'P'


class Bomb:

    def __init__(self, user):
        self.y = user.y
        self.x = user.x
        self.time = 4

    def draw(self, graphic_buffer, context):
        graphic_buffer[self.y][self.x] = '@'
        for bomb in context.bombs:
            if (self.y, self.x) != (context.user.y, context.user.x):
                graphic_buffer[self.y][self.x] = 'B'

    def make_step(self, context):
        if self.time > 0:
            self.time -= 1
        if self.time == 0 and self not in context.dead_list:
            context.dead_list.append(self)
            offsets = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1),]
            for brick in context.bricks:
                if brick not in context.dead_list:
                    for (offset_y, offset_x) in offsets:
                        if (brick.y, brick.x) == (self.y + offset_y, self.x + offset_x):
                            context.dead_list.append(brick)
                            self.add_point(context.user, brick)
                            if context.portal is None:
                                context.portal = Portal(brick.y, brick.x)

            for (offset_y, offset_x) in offsets:
                if (context.user.y, context.user.x) == (self.y + offset_y, self.x + offset_x):
                    context.user.life -= 1
                    break

    def add_point(self, user, destroyed_objects):
        user.points += destroyed_objects.REWARD


class Context:

    def __init__(self):
        self.board = Board()
        self.user = User(1, self.board)
        self.bricks = []
        self.portal = None
        self.bombs = []
        self.dead_list =[]
        for _ in range(20):
            self.bricks.append(Brick(self.board,self. user, self.bricks))

context = Context()

graphic_buffer = [
    [' ' for index_x in range(len(context.board.fields[index_y]))] for index_y in range(len(context.board.fields))
]

while True:
    context.board.draw(graphic_buffer, context)
    for brick in context.bricks:
        brick.draw(graphic_buffer, context)
    context.user.draw(graphic_buffer, context)
    for bomb in context.bombs:
        bomb.draw(graphic_buffer, context)
    if context.portal is not None:
        context.portal.draw(graphic_buffer, context)
    for row in graphic_buffer:
        print(' '.join(row))
    print('Lives: {}, Points: {}'.format(context.user.life, context.user.points))
    for bomb in context.bombs:
        print('Bomb time: {}'.format(bomb.time))
    context.user.make_step(context)
    for bomb in context.bombs:
        bomb.make_step(context)
    for element in context.dead_list:
        if isinstance(element, Bomb):
            context.bombs.remove(element)
        if isinstance(element, Brick):
            context.bricks.remove(element)
    context.dead_list = []



# TODO:
# portal ending level
# level
# game over
# artifacts - bigger range of bomb explosion, add life, more points
# monster - random place, random number
# kill monster
# points for monster
# unit testy

