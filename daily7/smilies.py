# originally from
# http://www.reddit.com/r/Python/comments/1pjsde/

import pyglet, random
from ctypes import *
from pyglet import clock

# Disable error checking for increased performance
pyglet.options['debug_gl'] = False

WINDOWWIDTH = 1920
WINDOWHEIGHT = 1080
FPS = 60.0

batch = pyglet.graphics.Batch()
window = pyglet.window.Window(WINDOWWIDTH,WINDOWHEIGHT)
fps_display = pyglet.clock.ClockDisplay()

image = pyglet.resource.image("smiley-512x512.png")

SMILIES_AMT = 120

class Square(pyglet.sprite.Sprite):
    def __init__(self,x,y):
        pyglet.sprite.Sprite.__init__(self,img = image,batch=batch)
        self.x = x
        self.y = y
        w = random.random() - 0.5
        self.v_x = random.random() * 400. - 200.
        self.v_y = random.random() * 400. - 200.
	self.scale = random.random() + .3

    def update(self,dt):
        if self.x > WINDOWWIDTH:
            self.v_x *= -1
        elif self.x < -image.width * .5:
            self.v_x *= -1
        if self.y > WINDOWHEIGHT:
            self.v_y *= -1
        elif self.y < -image.height * .5:
            self.v_y *= -1

        self.x += self.v_x * dt
        self.y += self.v_y * dt 

sqrs = []
for _ in range(SMILIES_AMT):
    sqrs.append( Square(random.randint(0,WINDOWWIDTH-1),random.randint(0,WINDOWHEIGHT-1)) )

def update(dt):
    for s in sqrs:
        s.update(dt)




@window.event
def on_draw():
    window.clear()
    batch.draw()
    fps_display.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.F:
        window.set_fullscreen(not window.fullscreen)



clock.schedule_interval(update, 1.0/FPS)

if __name__ == '__main__':
    pyglet.app.run()
