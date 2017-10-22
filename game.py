from artifacts.life import Life
from artifacts.points import Point
from artifacts.super_bomb_artifact import SuperBombArtifact
from bomb import Bomb
from brick import Brick
from context import Context
from game_over_error import GameOverError
from monster import Monster


def draw_scene(context, graphic_buffer):
    context.board.draw(graphic_buffer, context)
    for brick in context.bricks:
        brick.draw(graphic_buffer, context)
    for monster in context.monsters:
        monster.draw(graphic_buffer, context)
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


def remove_elements(context):
    for element in context.dead_list:
        if isinstance(element, Bomb):
            context.bombs.remove(element)
        if isinstance(element, Brick):
            context.bricks.remove(element)
        if isinstance(element, Life):
            context.artifacts.remove(element)
        if isinstance(element, SuperBombArtifact):
            context.artifacts.remove(element)
        if isinstance(element, Point):
            context.artifacts.remove(element)
        if isinstance(element, Monster):
            context.monsters.remove(element)
    context.dead_list = []

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
    remove_elements(context)


# TODO:
# super bomb - bigger range of bomb explosion
# monster - moving, decrease user life when monster is on user
# user - decrease user life when user is on monster
# unit tests

