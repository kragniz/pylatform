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
        self.win = Window(fullscreen=False, visible=False)
        self.clockDisplay = clock.ClockDisplay()
        glClearColor(0.2, 0.2, 0.2, 1)
        self.camera = Camera((0, 0), 200)

        self.space = pymunk.Space() #2
        self.space.gravity = (0, -50.0)

        self.player = alone.Player()
        self.space.add(self.player.box, self.player.body)

        self.balls = []
        self.lines = []

        self.BOX_WIDTH = 40
        self.boxes = []

        level = (
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1),
            (0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1),
            (1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1),
            (1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0),
            (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0)
        )

        #build the level
        for y, row in enumerate(reversed(level)):
            for x, boxHere in enumerate(row):
                if boxHere:
                    self.boxes.append(self.add_static_box(
                            x*(self.BOX_WIDTH*2),
                            y*(self.BOX_WIDTH*2) - 200)
                        )

        self.camera.setTarget(0, 0)

    def move_camera(self):
        self.camera.setTarget(*self.player.position)

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

    def add_static_box(self, x=0, y=0):
        body = pymunk.Body()
        body.position = (x, y)
        w = self.BOX_WIDTH
        box = pymunk.Poly(body, (
            (-w, -w),
            (-w, +w),
            (+w, +w),
            (+w, -w)))
        box.friction = 0.5
        self.space.add_static(box)
        return box

    def draw_box(self, box):
        p = int(box.body.position.x), int(box.body.position.y)
        glBegin(GL_POLYGON)
        glColor3ub(100, 100, 100)
        w = self.BOX_WIDTH
        glVertex2f(-w + p[0], -w + p[1])
        glVertex2f(-w + p[0], +w + p[1])
        glVertex2f(+w + p[0], +w + p[1])
        glVertex2f(+w + p[0], -w + p[1])
        glEnd()


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

        points = (Vector2(-4, -4),
                  Vector2(+0, +4),
                  Vector2(+4, -4))
        m = Matrix3.new_rotate(ball.body.angle)
        m1 = Matrix3.new_translate(p[0], p[1])
        m *= m1
        glVertex2f(*(m * points[0]))
        glVertex2f(*(m * points[1]))
        glVertex2f(*(m * points[2]))
        glEnd()

    def update_objects(self):
        self.move_camera()

        self.player.update_position()

        self.space.step(1/50.0)

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH);
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        self.camera.update()
        self.camera.focus(self.win.width, self.win.height)

        for box in self.boxes:
            self.draw_box(box)

        for ball in self.balls:
            self.draw_ball(ball)

        self.player.sprite.draw()

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
    key.SPACE: lambda: game.balls.append(game.add_ball()),
}

key_release_handlers = {
    key.LEFT: lambda: game.set_camera_dx(0),
    key.RIGHT: lambda: game.set_camera_dx(0),
    key.DOWN: lambda: game.set_camera_dy(0),
    key.UP: lambda: game.set_camera_dy(0),
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

game.win.set_visible()
app.run()
