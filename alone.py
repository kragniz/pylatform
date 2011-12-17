import pyglet

class Player(object):
    def __init__(self):
        self.image = pyglet.resource.image('man.png')
        self.x = 0
        self.y = 0