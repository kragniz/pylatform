import pyglet
import pymunk
from pymunk.util import *
from math import pi

class Player(object):
    def __init__(self, x=400, y=70):
        playerImageTile = pyglet.resource.image('man.png')
        self.playerRight = playerImageTile.get_region(
            0, 0, 64, 64
            )
        self.playerLeft = playerImageTile.get_region(
            64, 0, 64, 64
            )

        self.sprite = pyglet.sprite.Sprite(self.playerLeft, x=x, y=y)

        self.height = self.playerRight.height
        self.width = self.playerRight.width
        mass = 10

        self.maxSpeed = 200

        self.body = pymunk.Body(mass, float('inf')) #infinity!
        self.body.position = (x, y)

        #self.body.velocity = (10, 0)

        self.box = pymunk.Poly(self.body, (
            (0, 0),
            (0, self.height),
            (self.width, self.height),
            (self.width, 0)))
        self.box.friction = 1
        self.box.elasticity = 0.4

        self.touchingObject = False

        self._dx = 0
        self._v_step = 25

    def jump(self):
    	if self.touchingObject:
    		self.body.apply_impulse((0, 4000))
        
    def update_position(self):
    	v_x = self.body.velocity[0]
    	v_y = self.body.velocity[1]

    	if not abs(v_x + self.dx * self._v_step) >= self.maxSpeed:
    		self.body.velocity = (v_x + self.dx * self._v_step, v_y)

    	self.sprite.set_position(
    	    self.box.body.position[0],
    	    self.box.body.position[1]
    	)
    	self.sprite.rotation = -self.box.body.angle * 180/pi
    	self.touchingObject = False

    @property
    def dx(self):
    	return self._dx

    def __set_player_image(self):
    	if self._dx > 0:
    		if self.sprite.image != self.playerRight:
    			self.sprite.image = self.playerRight
    	if self._dx < 0:
     		if self.sprite.image != self.playerLeft:
    			self.sprite.image = self.playerLeft
    
    @dx.setter
    def dx(self, x):
    	self._dx = x
    	self.__set_player_image()

    def set_dx(self, x):
    	self._dx = x
    	self.__set_player_image()

    @property
    def center(self):
    	return self.box.body.position[0] + self.width / 2, \
    	       self.box.body.position[1] + self.height / 2