import pyglet

class Player(object):
    def __init__(self, x=50, y=0):
        playerImage = pyglet.resource.image('man.png')
        self.sprite = pyglet.sprite.Sprite(playerImage, x=x, y=y)
        
    @property
    def position(self):
    	return self.sprite.position

    @position.setter
    def position(self, p):
    	self.sprite.position = p

    def move_x(self, dx):
    	self.sprite.x += dx