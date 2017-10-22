from random import randint

from bomb import Bomb


class User:

    DEFAULT_BOMB_CLASS = Bomb
    START_POINTS = 0
    START_LIFE = 3

    def __init__(self, board, life, points, bomb_class):
        self._set_up_user(board)
        self.step = 1
        self.points = points
        self.life = life
        self.bomb_class = bomb_class

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
            context.bombs.append(self.bomb_class(context.user))
