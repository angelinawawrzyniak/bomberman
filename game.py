from abc import abstractmethod
from random import randint, random


class GameOverError(Exception):
    pass


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

    def __init__(self, step, board, life, points):
        self._set_up_user(board)
        self.step = step
        self.points = points
        self.life = life

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
                                if random() <= 1/len(context.bricks):
                                    context.portal = Portal(brick.y, brick.x)
                            if context.portal is None:
                                if random() <= 0.2:
                                    context.artifacts.append(Life(brick.y, brick.x))

            offsets.append((0, 0))
            for (offset_y, offset_x) in offsets:
                if (context.user.y, context.user.x) == (self.y + offset_y, self.x + offset_x):
                    context.user.life -= 1
                    if context.user.life == 0:
                        raise GameOverError('GAME OVER')
                    break

    def add_point(self, user, destroyed_objects):
        user.points += destroyed_objects.REWARD


class Artifact:
    SYMBOL = '?'

    def __init__(self, y, x):
        self.x = x
        self.y = y

    def draw(self, graphic_buffer, context):
        graphic_buffer[self.y][self.x] = self.SYMBOL

    @abstractmethod
    def make_step(self, context):
        pass


class Life(Artifact):

    SYMBOL = 'L'

    def make_step(self, context):
        if (context.user.y, context.user.x) == (artifact.y, artifact.x):
            context.dead_list.append(artifact)
            context.user.life += 1


class Context:

    def __init__(self):
        self.game_level = 1
        self._reset_context(3, 0)

    def level_up(self):
        self.game_level += 1
        self._reset_context(self.user.life, self.user.points)

    def _reset_context(self, user_life, user_points):
        self.board = Board()
        self.user = User(1, self.board, user_life, user_points)
        self.bricks = []
        self.portal = None
        self.bombs = []
        self.dead_list =[]
        self.game_over = False
        self.artifacts = []

        for _ in range(20):
            self.bricks.append(Brick(self.board, self.user, self.bricks))


def draw_scene(context, graphic_buffer):
    context.board.draw(graphic_buffer, context)
    for brick in context.bricks:
        brick.draw(graphic_buffer, context)
    context.user.draw(graphic_buffer, context)
    for bomb in context.bombs:
        bomb.draw(graphic_buffer, context)
    if context.portal is not None:
        context.portal.draw(graphic_buffer, context)
    for artifact in context.artifacts:
        artifact.draw(graphic_buffer, context)
    if context.game_over:
        letters = list('GAME OVER')
        offset = int((len(graphic_buffer[0]) - len(letters)) / 2)
        for x in range(0, len(letters)):
            graphic_buffer[int(len(graphic_buffer) / 2)][x + offset] = letters[x]
    for row in graphic_buffer:
        print(' '.join(row))
    print('Level: {}, Lives: {}, Points: {}'.format(context.game_level, context.user.life,
                                                    context.user.points))
    for bomb in context.bombs:
        print('Bomb time: {}'.format(bomb.time))


context = Context()
graphic_buffer = [
    [' ' for index_x in range(len(context.board.fields[index_y]))] for index_y in range(len(context.board.fields))
]


while True:
    draw_scene(context, graphic_buffer)
    context.user.make_step(context)
    for artifact in context.artifacts:
        artifact.make_step(context)
    if context.portal is not None:
        if (context.user.y, context.user.x) == (context.portal.y, context.portal.x):
            context.level_up()
            continue
    try:
        for bomb in context.bombs:
            bomb.make_step(context)
    except GameOverError as error:
        context.game_over = True
        draw_scene(context, graphic_buffer)
        break
    for element in context.dead_list:
        if isinstance(element, Bomb):
            context.bombs.remove(element)
        if isinstance(element, Brick):
            context.bricks.remove(element)
        if isinstance(element, Life):
            context.artifacts.remove(element)
    context.dead_list = []



# TODO:
# artifacts - bigger range of bomb explosion, more points
# monster - random place, random number
# kill monster
# points for monster
# unit testy

