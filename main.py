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
space.gravity = (0.0, -500.0)

balls = []
lines = []

def add_ball(space):
    mass = 1
    radius = 4
    inertia = pymunk.moment_for_circle(mass, 0, radius) # 1
    body = pymunk.Body(mass, inertia) # 2
    x = random.randint(120,380) / 10.0
    body.position = x, 20 # 3
    shape = pymunk.Circle(body, radius) # 4
    space.add(body, shape) # 5
    return shape

def add_static_L(space):
    body = pymunk.Body() # 1
    body.position = (30,-10)    
    l1 = pymunk.Segment(body, (-15, 0), (25.0, 0.0), 5.0) # 2
    l2 = pymunk.Segment(body, (-15.0, 0), (-15.0, 50.0), 5.0)
            
    space.add_static(l1, l2) # 3
    return l1,l2

lines = add_static_L(space)

def draw_line(line):
    body = line.body
    pv1 = body.position + line.a.rotated(body.angle)
    pv2 = body.position + line.b.rotated(body.angle)

    glLineWidth (3)                                                                
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,                                    
        ('v2i', (int(pv1[0]), int(pv1[1]), int(pv2[0]), int(pv1[1])))                                                
    )            

    # glBegin(GL_LINES)
    # glColor3ub(255, 255, 255)
    # glVertex2f(*pv1)
    # glVertex2f(*pv2)
    # glEnd();


def draw_ball(ball):
    p = int(ball.body.position.x), int(ball.body.position.y)
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 000)
    glVertex2f(-4 + p[0], -4 + p[1])
    glVertex2f(+0 + p[0], +4 + p[1])
    glVertex2f(+4 + p[0], -4 + p[1])
    glEnd()


verts = [
    ((255, 000, 000), (+5, +4)),
    ((000, 255, 000), (+0, -4)),
    ((000, 000, 255), (-5, +4)),
]

@win.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_LINE_SMOOTH);
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    camera.update()
    camera.focus(win.width, win.height)

    glBegin(GL_TRIANGLES)
    for color, position in verts:
        glColor3ub(*color)
        glVertex2f(*position)
    glEnd()

    for ball in balls:
        draw_ball(ball)

    for line in lines:
        draw_line(line)

    space.step(1/50.0)

    glColor3ub(255, 255, 0)
    player.sprite.draw()

    camera.hud_mode(win.width, win.height)
    #print camera.x, camera.y
    #glColor3ub(50, 50, 50)
    clockDisplay.draw()

# on_draw is triggered after all events by default. This 'null' event
# is scheduled just to force a screen redraw for every frame
clock.schedule(lambda _: None)

key_handlers = {
    key.ESCAPE: lambda: win.close(),
    key.PAGEUP: lambda: camera.zoom(2),
    key.PAGEDOWN: lambda: camera.zoom(0.5),
    key.LEFT: lambda: camera.pan(camera.scale, -pi/2),
    key.RIGHT: lambda: camera.pan(camera.scale, +pi/2),
    key.DOWN: lambda: camera.pan(camera.scale, pi),
    key.UP: lambda: camera.pan(camera.scale, 0),
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
