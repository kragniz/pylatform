import pyglet
import pymunk
from pyglet.gl import *


class Object(object):
    '''An object the player can see'''
    def __init__(self, img, x=0, y=0):
        self.objectImage = pyglet.resource.image(img)
        self.sprite = pyglet.sprite.Sprite(self.objectImage, x=x, y=y)

        self.height = self.objectImage.height
        self.width = self.objectImage.width

    def draw(self):
        self.sprite.draw()


class PhysicalObject(Object):
    '''An object which will interact with other physical objects'''
    def __init__(self, img, x=0, y=0,
                     mass=10,
                     friction=0.1,
                     elasticity=0.5,
                     canRotate=True):

        super(PhysicalObject, self, img, x=x, y=y).__init__()

        if canRotate:
            moment = pymunk.moment_for_box(mass, self.width, self.height)
        else:
            moment = float('inf')

        self.body = pymunk.Body(mass, moment)

        self.box = pymunk.Poly(self.body, (
            (-self.width/2, -self.height/2),
            (-self.width/2, +self.height/2),
            (+self.width/2, +self.height/2),
            (+self.width/2, -self.height/2)))

        self.box.friction = friction
        self.box.elasticity = elasticity

    @property
    def velocity(self):
        return self.body.velocity

    def update_sprite(self):
        self.sprite.set_position(
            self.box.body.position[0]+self.width/2,
            self.box.body.position[1]+self.height/2
        )

    def add_to_velocity(self, i, j):
        self.body.velocity = (self.velocity[0] + i, self.velocity[1] + j)


class Player(object):
    '''Represents a player, the character the user controls'''
    def __init__(self, img, x=400, y=70):
        playerImageTile = pyglet.resource.image(img)
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