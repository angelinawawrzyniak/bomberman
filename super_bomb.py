from bomb import Bomb


class SuperBomb(Bomb):
    _OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0), (-2, 0), (2, 0), (0, -2), (0, 2)]
