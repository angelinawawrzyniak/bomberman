class Portal:

    def __init__(self, y, x):
        self.y = y
        self.x = x

    def draw(self, graphic_buffer, _context):
        graphic_buffer[self.y][self.x] = 'P'
