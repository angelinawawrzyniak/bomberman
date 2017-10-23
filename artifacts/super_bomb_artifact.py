from artifacts.artifact import Artifact


class SuperBombArtifact(Artifact):

    SYMBOL = '^'

    def make_step(self, context):
        if (context.user.y, context.user.x) == (self.y, self.x):
            context.dead_list.append(self)
            # cyclic import solved
            from super_bomb import SuperBomb
            context.user.bomb_class = SuperBomb
