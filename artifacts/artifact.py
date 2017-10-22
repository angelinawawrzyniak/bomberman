from abc import abstractmethod


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
