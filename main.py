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

win = Window(fullscreen=False, visible=False)
clockDisplay = clock.ClockDisplay()
glClearColor(0.4, 0.2, 0.3, 0)
camera = Camera((0, 0), 100)

player = alone.Player()

space = pymunk.Space() #2
space.gravity = (0.0, -20.0)

balls = []
lines = []
BOX_WIDTH = 10
boxes = []

level = (
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (0, 0, 0, 0, 0, 0, 0, 1, 1, 1),
    (1, 0, 1, 1, 1, 0, 1, 1, 1, 1),
    (1, 1, 1, 0, 0, 0, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
)

def add_ball(space):
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
    space.add(body, shape) # 5
    return shape

def add_static_box(space, x=0, y=0):
    body = pymunk.Body()
    body.position = (x, y)    
    box = pymunk.Poly(body, (
        (-BOX_WIDTH, -BOX_WIDTH),
        (-BOX_WIDTH, +BOX_WIDTH),
        (+BOX_WIDTH, +BOX_WIDTH),
        (+BOX_WIDTH, -BOX_WIDTH)))
    space.add_static(box)
    return box

#build the level
for y, row in enumerate(reversed(level)):
    for x, boxHere in enumerate(row):
        if boxHere:
            boxes.append(add_static_box(space, x*(BOX_WIDTH+100), y*(BOX_WIDTH+100)))

def draw_box(box):
    p = int(box.body.position.x), int(box.body.position.y)
    glBegin(GL_POLYGON)
    glColor3ub(255, 100, 100)
    glVertex2f(-BOX_WIDTH + p[0], -BOX_WIDTH + p[1])
    glVertex2f(-BOX_WIDTH + p[0], +BOX_WIDTH + p[1])
    glVertex2f(+BOX_WIDTH + p[0], +BOX_WIDTH + p[1])
    glVertex2f(+BOX_WIDTH + p[0], -BOX_WIDTH + p[1])
    glEnd()


def draw_line(line):
    body = line.body
    pv1 = body.position + line.a.rotated(body.angle)
    pv2 = body.position + line.b.rotated(body.angle)

    glLineWidth (3)                                                                
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,                                    
        ('v2i', (int(pv1[0]), int(pv1[1]), int(pv2[0]), int(pv1[1])))                                                
    )

def draw_ball(ball):
    p = int(ball.body.position.x), int(ball.body.position.y)
    glBegin(GL_POLYGON)
    glColor3ub(255, 255, 000)
    glVertex2f(-4 + p[0], -4 + p[1])
    glVertex2f(+0 + p[0], +4 + p[1])
    glVertex2f(+4 + p[0], -4 + p[1])
    glEnd()

@win.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_LINE_SMOOTH);
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    camera.update()
    camera.focus(win.width, win.height)

    for ball in balls:
        draw_ball(ball)

    for box in boxes:
        draw_box(box)

    space.step(1/50.0)
    player.sprite.draw()

    camera.hud_mode(win.width, win.height)
    #glColor3ub(50, 50, 50)
    clockDisplay.draw()

# on_draw is triggered after all events by default. This 'null' event
# is scheduled just to force a screen redraw for every frame
clock.schedule(lambda _: None)

key_handlers = {
    key.ESCAPE: lambda: win.close(),
    key.PAGEUP: lambda: camera.zoom(2),
    key.PAGEDOWN: lambda: camera.zoom(0.5),
    key.LEFT: lambda: camera.setTarget(camera.x - 30, camera.y),
    key.RIGHT: lambda: camera.setTarget(camera.x + 30, camera.y),
    key.DOWN: lambda: camera.setTarget(camera.x, camera.y - 30),
    key.UP: lambda: camera.setTarget(camera.x, camera.y + 30),
    key.COMMA: lambda: camera.tilt(-1),
    key.PERIOD: lambda: camera.tilt(+1),
    key.SPACE: lambda: balls.append(add_ball(space)),
}

@win.event
def on_key_press(symbol, modifiers):
    handler = key_handlers.get(symbol, lambda: None)
    handler()
    
win.set_visible()
app.run()
