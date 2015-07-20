#!/usr/bin/python

'''
A cross between cairo curve example and zetcode tutorial
Add control points to curve.
'''

from math import sqrt
from gi.repository import Gtk, Gdk
import cairo

def curve_at(t, p0, p1, p2, p3):    
    cx = 3. * (p1[0] - p0[0])
    bx = 3. * (p2[0] - p1[0]) - cx
    ax = p3[0] - p0[0] - cx - bx

    cy = 3. * (p1[1] - p0[1])
    by = 3. * (p2[1] - p1[1]) - cy
    ay = p3[1] - p0[1] - cy - by

    x = (ax * (t ** 3.)) + (bx * (t ** 2.)) + (cx * t) + p0[0]
    y = (ay * (t ** 3.)) + (by * (t ** 2.)) + (cy * t) + p0[1]

    return x, y

def distance(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return sqrt(dx * dx + dy * dy)

def path_length(cr):
    length = 0
    cx, cy = cr.get_current_point()
    for t, data in cr.copy_path_flat():
        if t == cairo.PATH_LINE_TO:
            x, y = data
            length += distance((cx, cy), (x, y))
            cx, cy = x, y
    return length

def path_at(t, cr):
    p=cr.copy_path()

    for t, data in p:
        print(t, data)
        #if t == cairo.PATH_LINE_TO:
        #    x, y = data
        #    length += distance((cx, cy), (x, y))
        #    cx, cy = x, y
    
    pass


def roundedrect(cr,x,y,width,height,radius=5):
    #/* a custom shape, that could be wrapped in a function */
    #radius = 5  #/*< and an approximate curvature radius */        
    x0       = x+radius/2.0   #/*< parameters like cairo_rectangle */
    y0       = y+radius/2.0
    rect_width  = width - radius
    rect_height = height - radius

    cr.save()
    #cr.set_line_width (0.04)
    #self.snippet_normalize (cr, width, height)

    x1=x0+rect_width
    y1=y0+rect_height
    #if (!rect_width || !rect_height)
    #    return
    if rect_width/2<radius:
        if rect_height/2<radius:
            cr.move_to  (x0, (y0 + y1)/2)
            cr.curve_to (x0 ,y0, x0, y0, (x0 + x1)/2, y0)
            cr.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
            cr.curve_to (x1, y1, x1, y1, (x1 + x0)/2, y1)
            cr.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
        else:
            cr.move_to  (x0, y0 + radius)
            cr.curve_to (x0 ,y0, x0, y0, (x0 + x1)/2, y0)
            cr.curve_to (x1, y0, x1, y0, x1, y0 + radius)
            cr.line_to (x1 , y1 - radius)
            cr.curve_to (x1, y1, x1, y1, (x1 + x0)/2, y1)
            cr.curve_to (x0, y1, x0, y1, x0, y1- radius)

    else:
        if rect_height/2<radius:
            cr.move_to  (x0, (y0 + y1)/2)
            cr.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
            cr.line_to (x1 - radius, y0)
            cr.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
            cr.curve_to (x1, y1, x1, y1, x1 - radius, y1)
            cr.line_to (x0 + radius, y1)
            cr.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
        else:
            cr.move_to  (x0, y0 + radius)
            cr.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
            cr.line_to (x1 - radius, y0)
            cr.curve_to (x1, y0, x1, y0, x1, y0 + radius)
            cr.line_to (x1 , y1 - radius)
            cr.curve_to (x1, y1, x1, y1, x1 - radius, y1)
            cr.line_to (x0 + radius, y1)
            cr.curve_to (x0, y1, x0, y1, x0, y1- radius)

    cr.close_path ()

    cr.restore()

class MouseButtons:
    
    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3
    
    
class Example(Gtk.Window):

    def __init__(self, title=""):
        super(Example, self).__init__()
        
        self.init_ui(title)
        
        
    def init_ui(self, title=""):

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.darea.set_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK | Gdk.EventMask.POINTER_MOTION_MASK )
        self.add(self.darea)
        
        self.cpoints = [
            [25.6, 128.0],
            [102.4, 230.4]
        ]
        self.selected_cpoint = None
        self.dragging_cpoint = None
                     
        self.darea.connect("button-press-event", self.on_button_press)
        self.darea.connect("button-release-event", self.on_button_release)
        self.darea.connect("motion-notify-event", self.on_motion)

        self.set_title(title)
        self.resize(300, 300)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        
    
    def on_draw(self, wid, cr):
        # draw control points
        x, y = self.cpoints[0]
        x1, y1 =self.cpoints[1]

        cr.set_source_rgba ( 0.2, 1, 0.2, 0.6)
        for p in self.cpoints:
            cr.rectangle(p[0]-7, p[1]-7, 14, 14)
            if p == self.selected_cpoint:
                cr.fill_preserve()
            cr.stroke()
        
        cr.set_line_width (10.0)


        # draw rounded rect
        roundedrect(cr, x, y, x1-x, y1-y)

        cr.stroke ()

                         
                         
    def on_button_press(self, w, e):
        if e.type == Gdk.EventType.BUTTON_PRESS \
            and e.button == MouseButtons.LEFT_BUTTON:
            
            for p in self.cpoints:
                if (p[0] - 7 < e.x < p[0] + 7) and (p[1] - 7 < e.y < p[1] + 7):
                    self.dragging_cpoint = p
                    self.selected_cpoint = p
                    self.darea.queue_draw()
                    break

            
        if e.type == Gdk.EventType.BUTTON_PRESS \
            and e.button == MouseButtons.RIGHT_BUTTON:
            
            self.darea.queue_draw()

    def on_motion(self, w, e):
        if self.dragging_cpoint:
            self.dragging_cpoint[0], self.dragging_cpoint[1] = e.x, e.y
            self.darea.queue_draw()

    def on_button_release(self, w, e):
        self.dragging_cpoint = None
                                                        
    
def main():
    
    app = Example("points along a path")
    Gtk.main()
        
        
if __name__ == "__main__":    
    main()
