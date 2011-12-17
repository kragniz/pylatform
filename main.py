#!/usr/bin/python -O
from __future__ import division
from sys import stdout
from math import pi
from pyglet import app, clock
from pyglet.window import key, Window
from pyglet.window.key import symbol_string
from pyglet.gl import *
from camera import Camera

import pyglet
import pymunk 

import alone

import random

class Game(object):
    def __init__(self):
        self.win = Window(fullscreen=False, visible=False)
        self.clockDisplay = clock.ClockDisplay()
        glClearColor(0.4, 0.2, 0.3, 0)
        self.camera = Camera((0, 0), 100)

        self.player = alone.Player()

        self.space = pymunk.Space() #2
        self.space.gravity = (0.0, -20.0)

        self.balls = []
        self.lines = []
        self.BOX_WIDTH = 10
        self.boxes = []

        level = (
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
            (0, 0, 0, 0, 0, 0, 0, 1, 1, 1),
            (1, 0, 1, 1, 1, 0, 1, 1, 1, 1),
            (1, 1, 1, 0, 0, 0, 1, 1, 1, 1),
            (1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        )

        #build the level
        for y, row in enumerate(reversed(level)):
            for x, boxHere in enumerate(row):
                if boxHere:
                    self.boxes.append(self.add_static_box(
                            x*(self.BOX_WIDTH+100),
                            y*(self.BOX_WIDTH+100))
                        )

    def add_ball(self):
        mass = 1
        radius = 4
        inertia = pymunk.moment_for_circle(mass, 0, radius) # 1
        body = pymunk.Body(mass, inertia) # 2
        x = random.randint(120,380) / 10.0
        body.position = x, 100 # 3
        #shape = pymunk.Circle(body, radius) # 4
        shape = pymunk.Poly(body, (
            (-4, -4),
            (+0, +4),
            (+4, -4)))
        self.space.add(body, shape) # 5
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
        self.space.add_static(box)
        return box

    def draw_box(self, box):
        p = int(box.body.position.x), int(box.body.position.y)
        glBegin(GL_POLYGON)
        glColor3ub(255, 100, 100)
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
        glVertex2f(-4 + p[0], -4 + p[1])
        glVertex2f(+0 + p[0], +4 + p[1])
        glVertex2f(+4 + p[0], -4 + p[1])
        glEnd()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH);
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        self.camera.update()
        self.camera.focus(self.win.width, self.win.height)

        for ball in self.balls:
            self.draw_ball(ball)

        for box in self.boxes:
            self.draw_box(box)

        self.space.step(1/50.0)
        self.player.sprite.draw()

        self.camera.hud_mode(self.win.width, self.win.height)
        #glColor3ub(50, 50, 50)
        self.clockDisplay.draw()

game = Game()

@game.win.event
def on_draw():
    game.draw()

# on_draw is triggered after all events by default. This 'null' event
# is scheduled just to force a screen redraw for every frame
clock.schedule(lambda _: None)

key_handlers = {
    key.ESCAPE: lambda: game.win.close(),
    key.PAGEUP: lambda: game.camera.zoom(2),
    key.PAGEDOWN: lambda: game.camera.zoom(0.5),
    key.LEFT: lambda: game.camera.setTarget(game.camera.x - 30, game.camera.y),
    key.RIGHT: lambda: game.camera.setTarget(game.camera.x + 30, game.camera.y),
    key.DOWN: lambda: game.camera.setTarget(game.camera.x, game.camera.y - 30),
    key.UP: lambda: game.camera.setTarget(game.camera.x, game.camera.y + 30),
    key.COMMA: lambda: game.camera.tilt(-1),
    key.PERIOD: lambda: game.camera.tilt(+1),
    key.SPACE: lambda: game.balls.append(add_ball(space)),
}

@game.win.event
def on_key_press(symbol, modifiers):
    handler = key_handlers.get(symbol, lambda: None)
    handler()
    
game.win.set_visible()
app.run()
