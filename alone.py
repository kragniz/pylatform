import pyglet
import pymunk
from pymunk.util import *
from math import pi

class Player(object):
    def __init__(self, x=400, y=70):
        playerImage = pyglet.resource.image('man.png')
        self.sprite = pyglet.sprite.Sprite(playerImage, x=x, y=y)

        self.height = playerImage.height
        self.width = playerImage.width
        mass = 10

        self.body = pymunk.Body(mass, float('inf')) #infinity!
        self.body.position = (x, y)

        #self.body.velocity = (10, 0)

        self.box = pymunk.Poly(self.body, (
            (0, 0),
            (0, self.height),
            (self.width, self.height),
            (self.width, 0)))
        self.box.friction = 1
        
    def update_position(self):
    	self.sprite.set_position(
    	    self.box.body.position[0],
    	    self.box.body.position[1]
    	)
    	self.sprite.rotation = -self.box.body.angle * 180/pi

    @property
    def position(self):
    	return self.sprite.position

    @position.setter
    def position(self, p):
    	self.sprite.position = p

    def move_x(self, dx):
    	self.sprite.x += dx