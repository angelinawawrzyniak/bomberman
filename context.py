from board import Board
from brick import Brick
from monster import Monster
from user import User


class Context:

    def __init__(self):
        self.game_level = 1
        self._reset_context(User.START_LIFE, User.START_POINTS, User.DEFAULT_BOMB_CLASS)

    def level_up(self):
        self.game_level += 1
        self._reset_context(self.user.life, self.user.points, self.user.bomb_class)

    def _reset_context(self, user_life, user_points, user_bomb_class):
        self.board = Board()
        self.user = User(self.board, user_life, user_points, user_bomb_class)
        self.bricks = []
        self.portal = None
        self.bombs = []
        self.dead_list =[]
        self.game_over = False
        self.artifacts = []
        self.monsters = [
            Monster(self.board, self.user, 1),
            Monster(self.board, self.user, 1),
            Monster(self.board, self.user, 1),
        ]

        for _ in range(20):
            self.bricks.append(Brick(self.board, self.user, self.bricks, self.monsters))
