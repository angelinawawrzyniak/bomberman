from random import random

from artifacts.points import Point

from artifacts.life import Life
from artifacts.super_bomb_artifact import SuperBombArtifact
from game_over_error import GameOverError
from monster import Monster
from portal import Portal
from user import User


class Bomb:

    _OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]

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
            for monster in context.monsters:
                if monster not in context.dead_list:
                    for (offset_y, offset_x) in self._OFFSETS:
                        if (monster.y, monster.x) == (self.y + offset_y, self.x + offset_x):
                            context.dead_list.append(monster)
                            self._add_point(context.user, monster)
            for (offset_y, offset_x) in self._OFFSETS:
                if (context.user.y, context.user.x) == (self.y + offset_y, self.x + offset_x):
                    context.user.life -= 1
                    context.user.bomb_class = User.DEFAULT_BOMB_CLASS
                    if context.user.life == 0:
                        raise GameOverError('GAME OVER')
                    break
            for brick in context.bricks:
                if brick not in context.dead_list:
                    for (offset_y, offset_x) in self._OFFSETS:
                        if (brick.y, brick.x) == (self.y + offset_y, self.x + offset_x):
                            context.dead_list.append(brick)
                            self._add_point(context.user, brick)
                            self._add_random_artifact(context, brick)
                            break

    def _add_point(self, user, destroyed_objects):
        user.points += destroyed_objects.REWARD
        if user.points != 0:
            if user.points % 200 == 0:
                user.life += 1

    def _add_random_artifact(self, context, brick):
        if context.portal is None:
            if random() <= 1 / len(context.bricks):
                context.portal = Portal(brick.y, brick.x)
                return
        if random() <= 0.1:
            context.artifacts.append(Life(brick.y, brick.x))
            return
        if random() <= 0.3:
            context.artifacts.append(SuperBombArtifact(brick.y, brick.x))
            return
        if random() <= 0.3:
            context.artifacts.append(Point(brick.y, brick.x))
            return
        if random() <= 0.4:
            context.monsters.append(Monster(context.board, context.user, 1, brick.y, brick.x))
            return
