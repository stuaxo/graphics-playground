#!/usr/bin/python

'''
A cross between cairo curve example and zetcode tutorial
Add control points to curve.
'''

from math import sqrt
from gi.repository import Gtk, Gdk, GLib
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

class MouseButtons:
    
    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3
    
    
class Example(Gtk.Window):

    def __init__(self, title=""):
        super(Example, self).__init__()
        
        self.init_ui(title)
        self.t = 0.0
        
        
    def init_ui(self, title=""):

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.darea.set_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK | Gdk.EventMask.POINTER_MOTION_MASK )
        self.add(self.darea)
        
        self.cpoints = [
            [25.6, 128.0],
            [102.4, 230.4],
            [153.6, 25.6],
            [230.4, 128.0]
        ]
        self.selected_cpoint = None
        self.dragging_cpoint = None
                     
        self.darea.connect("button-press-event", self.on_button_press)
        self.darea.connect("button-release-event", self.on_button_release)
        self.darea.connect("motion-notify-event", self.on_motion)


        GLib.timeout_add(14, self.inc_timer)
        
        self.set_title(title)
        self.resize(300, 300)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        
    def inc_timer(self):
        self.t = (self.t + 0.01) % 1.0
        self.darea.queue_draw()
        return True
    
    def on_draw(self, wid, cr):
        # draw control points
        x, y = self.cpoints[0]
        x1, y1 =self.cpoints[1]
        x2, y2 =self.cpoints[2]
        x3, y3 =self.cpoints[3]

        cr.set_source_rgba ( 0.2, 1, 0.2, 0.6)
        for p in self.cpoints:
            cr.rectangle(p[0]-7, p[1]-7, 14, 14)
            if p == self.selected_cpoint:
                cr.fill_preserve()
            cr.stroke()
        
        cr.set_line_width (10.0)
        # draw curve
        cr.move_to (x, y)
        cr.curve_to (x1, y1, x2, y2, x3, y3)

        _length = path_length(cr)
        cr.stroke ()
        
        cr.set_source_rgba(0, 0, 0, 1)
        cr.move_to(20, 30);


        cr.set_font_size(16);
        cr.show_text("Length {0:.2f}".format(_length))
        
        cr.set_source_rgba ( 1, 0.2, 0.2, 0.6)
        cr.set_line_width (6.0)
        cr.move_to (x,y)
        cr.line_to (x1,y1)
        cr.move_to (x2,y2)
        cr.line_to (x3,y3)
        cr.stroke ()
        
        
        cr.set_line_width(1)
        cr.set_source_rgba (0, 0, 1, .5)
        for t in (t * 0.1 for t in range(1, 10)):
            pos = curve_at(t, (x, y), (x1, y1), (x2, y2), (x3, y3))
            cr.rectangle(pos[0]-7, pos[1]-7, 14, 14)
        cr.stroke()

        pos = curve_at(self.t, (x, y), (x1, y1), (x2, y2), (x3, y3))
        cr.rectangle(pos[0]-7, pos[1]-7, 14, 14)
        cr.fill()

                         
                         
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
    
    app = Example("curve points")
    Gtk.main()
        
        
if __name__ == "__main__":    
    main()
