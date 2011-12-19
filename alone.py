import pyglet
import pymunk
from pyglet.gl import *
import numpy as np
from numpy.random import random_integers as rnd
import random

class Player(object):
    '''Represents a player, the character the user controls'''
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

        self.maxSpeed = 300
        self.maxJumpSpeed = 200

        self.body = pymunk.Body(mass, float('inf')) #infinity!
        self.body.position = (x, y)

        #self.body.velocity = (10, 0)

        self.box = pymunk.Poly(self.body, (
            (0, 0),
            (0, self.height),
            (self.width, self.height),
            (self.width, 0)))
        self.box.friction = 0.2
        self.box.elasticity = 0.4

        self.touchingObject = False

        self._dx = 0
        self._v_step = 10

    def jump(self):
        if self.touchingObject and self.body.velocity[1] < self.maxJumpSpeed:
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

    def draw(self):
        self.sprite.draw()


class Spirit(object):
    '''Represents a spirit, an npc the player must guide'''
    def __init__(self, x=0, y=0):
        spiritImage = pyglet.resource.image('spirit.png')
        self.sprite = pyglet.sprite.Sprite(spiritImage, x=x, y=y)

        self.height = self.playerRight.height
        self.width = self.playerRight.width
        mass = 0.001

        self.maxSpeed = 100

        self.body = pymunk.Body(mass, float('inf')) #infinity!
        self.body.position = (x, y)

        self.box = pymunk.Poly(self.body, (
            (0, 0),
            (0, self.height),
            (self.width, self.height),
            (self.width, 0)))
        self.box.sensor = True

    def update_position(self):
        v_x = self.body.velocity[0]
        v_y = self.body.velocity[1]

        if not abs(v_x + self.dx * self._v_step) >= self.maxSpeed:
            self.body.velocity = (v_x + self.dx * self._v_step, v_y)

        self.sprite.set_position(
            self.box.body.position[0],
            self.box.body.position[1]
        )
        self.touchingObject = False

class Lamp(object):
    '''A lamp object, something the spirits are attracted towards'''
    def __init__(self, x=0, y=0):
        self._x, self._y = 0, 0

        flareScale = 4

        lampImage = pyglet.resource.image('lamp.png')
        flareImage = pyglet.resource.image('lampGlow.png')

        self._lamp = pyglet.sprite.Sprite(lampImage, x=x, y=y)

        self._flare = pyglet.sprite.Sprite(flareImage)
        self._flare.scale = flareScale
        self._flare.opacity = 100

        self.x, self.y = x, y

    def draw(self):
        self._lamp.draw()
        
    def draw_flare(self):
        pass#self._flare.draw()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x
        self._lamp.x = self.x - self._lamp.width
        print self._lamp.x
        self._flare.x = (self._lamp.x / self._flare.scale) + self._flare.width/self._flare.scale
        print self._flare.width * self._flare.scale

    @property
    def y(self):
        return self._y

    @x.setter
    def y(self, new_y):
        self._y = new_y
        self._lamp.y = self._y
        self._flare.y = self.y - self._flare.height

        print self._flare.y

    @property
    def center(self):
        return self.x + self._lamp.width / 2, \
               self.y + self._lamp.height / 2

def maze(width=81, height=51, complexity=.75, density =.75):
    # Only odd shapes
    shape = ((height//2)*2+1, (width//2)*2+1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity*(5*(shape[0]+shape[1])))
    density    = int(density*(shape[0]//2*shape[1]//2))
    # Build actual maze
    Z = np.zeros(shape, dtype=bool)
    # Fill borders
    Z[0,:] = Z[-1,:] = 1
    Z[:,0] = Z[:,-1] = 1
    # Make isles
    for i in range(density):
        x, y = rnd(0,shape[1]//2)*2, rnd(0,shape[0]//2)*2
        Z[y,x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:           neighbours.append( (y,x-2) )
            if x < shape[1]-2:  neighbours.append( (y,x+2) )
            if y > 1:           neighbours.append( (y-2,x) )
            if y < shape[0]-2:  neighbours.append( (y+2,x) )
            if len(neighbours):
                y_,x_ = neighbours[rnd(0,len(neighbours)-1)]
                if Z[y_,x_] == 0:
                    Z[y_,x_] = 1
                    Z[y_+(y-y_)//2, x_+(x-x_)//2] = 1
                    x, y = x_, y_
    return Z

def make_map(w=40, h=20):
    l = [random.randint(1, h) for i in range(w/4)]
    print l



class Map(object):
    '''Manages and draws items on a map'''
    def __init__(self, space, level=maze(20, 20)):
        self.space = space

        make_map()

        self.level = level
        self.BLOCK_WIDTH = 200
        self.blocks = []

        self.build_blocks()

        self.c = 0
        self.inc = 1

    def build_blocks(self):
        for y, row in enumerate(reversed(self.level)):
            for x, place_block in enumerate(row):
                if place_block:
                    self.blocks.append(self.add_static_block(
                            x*(self.BLOCK_WIDTH*2),
                            y*(self.BLOCK_WIDTH*2)+self.BLOCK_WIDTH*2)
                        )

    def add_static_block(self, x=0, y=0):
        body = pymunk.Body()
        body.position = (x/2, y/2)
        w = self.BLOCK_WIDTH
        block = pymunk.Poly(body, (
            (0, 0),
            (w, 0),
            (w, -w),
            (0, -w)))
        block.friction = 0.5
        block.elasticity = 0.5
        self.space.add_static(block)
        return block

    def draw_block(self, block):
        p = int(block.body.position.x), int(block.body.position.y)
        glBegin(GL_POLYGON)
        glColor3ub(255 , 255 , 255)
        w = self.BLOCK_WIDTH
        glVertex2f(p[0], p[1])
        glVertex2f(p[0] + w, p[1])
        glVertex2f(+w + p[0], -w + p[1])
        glVertex2f(p[0], -w + p[1])
        glEnd()

    def draw(self):
        for block in self.blocks:
            self.draw_block(block)

    def to_world(self, x, y):
        '''Return the realworld coordinates from a pair of map coordinates
            -> map coordinates are counted from the bottom left of the map and
               increment by one every block'''
        return x*self.BLOCK_WIDTH, y*self.BLOCK_WIDTH

class Powerup(object):
    def __init__(self, x=0, y=0):
        powerupImage = pyglet.resource.image('powerup.png')
        self.sprite = pyglet.sprite.Sprite(powerupImage, x=x, y=y)

        self.height = self.sprite.height
        self.width = self.sprite.width

        mass = 1

        self.body = pymunk.Body(mass, float('inf'))
        self.body.position = (x, y)

        self.box = pymunk.Poly(self.body, (
            (0, 0),
            (0, self.height),
            (self.width, self.height),
            (self.width, 0)))
        self.box.sensor = True

    def draw(self):
        self.sprite.draw()