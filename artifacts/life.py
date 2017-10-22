from artifacts.artifact import Artifact


class Life(Artifact):

    SYMBOL = 'L'

    def make_step(self, context):
        if (context.user.y, context.user.x) == (self.y, self.x):
            context.dead_list.append(self)
            context.user.life += 1
