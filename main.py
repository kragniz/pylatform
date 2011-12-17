import pyglet
from pyglet.window import key
from pyglet.window import mouse

import alone

window = pyglet.window.Window()
player = alone.Player()
fps_display = pyglet.clock.ClockDisplay()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        print 'The " " key was pressed.'
    elif symbol == key.LEFT:
        player.x -= 1
    elif symbol == key.RIGHT:
        player.x += 1

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print 'The left mouse button was pressed at', x, y


@window.event
def on_draw():
    window.clear()
    player.image.blit(player.x, player.y)
    fps_display.draw()

pyglet.app.run()