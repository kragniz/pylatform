#!/usr/bin/python -O
from __future__ import division
from sys import stdout
from math import pi
from pyglet import app, clock
from pyglet.window import key, Window, mouse
from pyglet.window.key import symbol_string
from pyglet.gl import *
from camera import Camera

from libs.pyeuclid import *

import pyglet
import pymunk 

import alone

import random

class Game(object):
    def __init__(self):
        self.win = Window(fullscreen=True, visible=False)
        self.clockDisplay = clock.ClockDisplay()
        glClearColor(0.2, 0.2, 0.2, 1)
        self.camera = Camera((0, 0), 250)

        self.space = pymunk.Space() #2
        self.space.gravity = (0, -500.0)
        self.space.damping = 0.999

        self.player = alone.Player()
        self.space.add(self.player.box, self.player.body)
        self.space.add_collision_handler(0, 0, None, None, self.print_collision, None)

        self.map = alone.Map(self.space)


        self.balls = []
        self.lines = []

        self.lamps = [alone.Lamp()]

        self.camera.setTarget(0, 0)

    def print_collision(self, arb, surface):
        if self.player.box in surface.shapes:
            #check to see if the player is touching an object
            self.player.touchingObject = True

    def move_camera(self):
        self.camera.setTarget(*self.player.center)

    def set_camera_dx(self, dx):
        self.dx_camera = dx

    def set_camera_dy(self, dy):
        self.dy_camera = dy

    def add_ball(self, x=0, y=0):
        mass = 1
        radius = 4
        inertia = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, inertia)
        if not x:
            x = random.randint(120,380) / 10.0
        if not y:
            y = 100
        body.position = x, y
        #shape = pymunk.Circle(body, radius) # 4
        shape = pymunk.Poly(body, (
            (-4, -4),
            (+0, +4),
            (+4, -4)))
        shape.friction = 0.5
        self.space.add(body, shape)
        return shape

    def draw_line(self, line):
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)

        glLineWidth (3)                                                                
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,                                    
            ('v2i', (int(pv1[0]), int(pv1[1]), int(pv2[0]), int(pv1[1])))                                                
        )

    def draw_ball(self, ball):
        p = int(ball.body.position.x), int(ball.body.position.y)
        glBegin(GL_POLYGON)
        glColor3ub(255, 255, 000)

        points = ((-4 + p[0], -4 + p[1]),
                  (+0 + p[0], +4 + p[1]),
                  (+4 + p[0], -4 + p[1]))
        glVertex2f(*points[0])
        glVertex2f(*points[1])
        glVertex2f(*points[2])
        glEnd()

    def update_objects(self):
        self.move_camera()

        self.player.update_position()

        self.space.step(1/50.0)

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.camera.update()
        self.camera.focus(self.win.width, self.win.height)

        self.map.draw()

        for ball in self.balls:
            self.draw_ball(ball)

        for lamp in self.lamps:
            lamp.draw()

        self.player.draw()

        glBegin(GL_POLYGON)
        glColor3ub(255, 255, 255)
        glVertex2f(-1, -1)
        glVertex2f(-1, 1)
        glVertex2f(1, 1)
        glVertex2f(1, -1)
        glEnd()

        self.camera.hud_mode(self.win.width, self.win.height)
        #glColor3ub(50, 50, 50)
        self.clockDisplay.draw()

game = Game()

@game.win.event
def on_draw():
    game.draw()
    game.update_objects()

# on_draw is triggered after all events by default. This 'null' event
# is scheduled just to force a screen redraw for every frame
clock.schedule(lambda _: None)

key_press_handlers = {
    key.ESCAPE: lambda: game.win.close(),
    key.PAGEUP: lambda: game.camera.zoom(2),
    key.PAGEDOWN: lambda: game.camera.zoom(0.5),
    key.LEFT: lambda: game.set_camera_dx(-1),
    key.RIGHT: lambda: game.set_camera_dx(1),
    key.DOWN: lambda: game.set_camera_dy(-1),
    key.UP: lambda: game.set_camera_dy(1),
    key.COMMA: lambda: game.camera.tilt(-pi/2),
    key.PERIOD: lambda: game.camera.tilt(+pi/2),

    key.SPACE: lambda: game.player.jump(),
    key.A: lambda: game.player.set_dx(-1),
    key.D: lambda: game.player.set_dx(1),
    key.W: lambda: game.player.set_dx(-1),
    key.S: lambda: game.player.set_dx(1),
}

key_release_handlers = {
    key.LEFT: lambda: game.set_camera_dx(0),
    key.RIGHT: lambda: game.set_camera_dx(0),
    key.DOWN: lambda: game.set_camera_dy(0),
    key.UP: lambda: game.set_camera_dy(0),

    key.A: lambda: game.player.set_dx(0),
    key.D: lambda: game.player.set_dx(0),
    key.W: lambda: game.player.set_dx(0),
    key.S: lambda: game.player.set_dx(0),
}

@game.win.event
def on_key_press(symbol, modifiers):
    handler = key_press_handlers.get(symbol, lambda: None)
    handler()

@game.win.event
def on_key_release(symbol, modifiers):
    handler = key_release_handlers.get(symbol, lambda: None)
    handler()

@game.win.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        game.balls.append(game.add_ball(x, y))



glEnable(GL_LINE_SMOOTH);
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)

game.win.set_visible()
app.run()
