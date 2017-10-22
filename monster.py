from random import randint


class Monster:

    REWARD = 20

    def __init__(self, board, user, step, y=None, x=None):
        if y is None and x is None:
            self._set_up_monster(board, user)
        else:
            self.y = y
            self.x = x
        self.step = step

    def draw(self, graphic_buffer, context):
        graphic_buffer[self.y][self.x] = 'M'

    def _set_up_monster(self, board, user):
        while True:
            y = randint(0, 10)
            x = randint(0, 16)
            if board.is_field_occupied(y, x):
                continue
            if (y, x) == (user.y, user.x):
                continue
            else:
                self.y = y
                self.x = x
                break
