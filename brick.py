from random import randint


class Brick:

    REWARD = 10

    def __init__(self, board, user, bricks, monsters):
        self.set_up_brick(board, user, bricks, monsters)

    def draw(self, graphic_buffer, _context):
        graphic_buffer[self.y][self.x] = '|'

    def is_field_occupied(self, bricks, y, x):
        for brick in bricks:
            if (y, x) == (brick.y, brick.x):
                return True
        return False

    def set_up_brick(self, board, user, bricks, monsters):
        while True:
            y = randint(0, 10)
            x = randint(0, 16)
            if self.is_field_occupied(bricks, y, x):
                continue
            if (y, x) == (user.y, user.x):
                continue
            if board.is_field_occupied(y, x):
                continue
            for monster in monsters:
                if (y, x) == (monster.y, monster.x):
                    continue
            else:
                self.y = y
                self.x = x
                break
