from artifacts.artifact import Artifact


class Point(Artifact):

    SYMBOL = '$'

    def make_step(self, context):
        if (context.user.y, context.user.x) == (self.y, self.x):
            context.dead_list.append(self)
            context.user.points += 50
