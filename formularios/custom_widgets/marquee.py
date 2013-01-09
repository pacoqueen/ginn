#!/usr/bin/env python
# -*- coding: utf-8 -*-

# By Zoltan Kovacs <kovzol@particio.com>.
# Based on PixbufsDemo, a pygtk example.
# Contains some bugs which will be fixed someday.
# Thanks for some suggestions to Albert Hofkamp <a.t.hofkamp@tue.nl>.

import os
import math
import gobject
import gtk
import pango

hirek_be="[R88] A RÁDIÓ 88 AKTUÁLIS HÍREI: [R88]  Vesztegetés miatt 4 rendõrt és egy határõrt tartóztattott le a Csongrád Megyei Fõügyészség Nyomozóhivatala, azzal gyanúsítják õket, hogy már hosszabb ideje csúszópénzt fogadtak el. [R88]  Ünnepélyesen átadták a magyar-szerb határon a Horgosi Határátkelõt, ez a röszkei határ szerb oldala. A  felújítás, és az oda vezetõ autópályák építése már évekkel ezelõtt elkezdõdött. [R88] Újra megnyitotta kapuit az újszegedi Ligetfürdõ, miután a múlt héten hétfõn bezárták a SZUE medencéjét, és a fürdõt, mert elérkezett a sátorállítás ideje. [R88]  A hidegebbre fordult idõben eddig két hajléktalan halt meg kihûlés miatt a fõvárosban. A hûvös éjszakák sokszor nagyobb veszélyt jelentenek az utcán lévõknek, mint a kemény fagyok, ilyenkor ugyanis az emberek még nincsenek felkészülve a hidegre. [R88] Ma nyújtja be a kormány a parlamentnek a második egészségügyi reformcsomagot, köztük a vizitdíj bevezetésérõl szóló javaslatot, ebben az is le van írva, hogy az orvosok pénzügyi retorzióra számíthatnak, ha nem szedik be a betegektõl a vizitdíjat.[R88] Egy 20 éves férfi elismerte, hogy õ rakta fel az internetre azt a hamis fenyegetést, amely szerint terrortámadások készülnek az amerikai futball stadionok ellen nyolc városban.  [R88] Észak-Korea legfõbb vezetõje egy kínai delegáció elõtt megbánta a kísérleti atomrobbantást, és közölte, hogy hajlandó visszatérni a tárgyalásokhoz, amennyiben Washington felhagy országa gazdasági elszigetelésével. [R88] 61 ország filmjei versenyeznek idén a legjobb külföldi filmnek járó Oscar-díjért, ez pedig rekord. Magyarország Hajdú Szabolcs Fehér Tenyér címû filmjét indítja a megmérettetésen. [R88] RÉSZLETEK A RÁDIÓ 88 ADÁSÁBAN AZ FM 95.4-EN. [R88]  Õszi Kultúrális Fesztivál 2006. október 1-31. www.u-szeged.hu/okf"

i = 0
j = 0
l = len(hirek_be)
p = 0
hirek = ""
hirek2 = ""
MINX = -100

image_names = []
image_pos = []

font = gtk.gdk.Font("-*-helvetica-bold-r-normal--*-120-*-*-*-*-iso8859-1")

while i<l:
    if hirek_be[i]=="[":
        st = i
        while hirek_be[i] != "]":
            i+=1
        en = i
        i+=1
        image_names.append(hirek_be[st+1:en] + '.png')
        image_pos.append(font.string_width(hirek))
        hirek+="   "
        p+=1
    else:
        hirek+=hirek_be[i]
        j+=1
        i+=1


hirek_hossz=font.string_width(hirek)


print image_names
print image_pos

SZELESSEG = 632
FRAME_DELAY = 10
CYCLE_LEN = 10
IMAGE_DIR = os.path.join(os.path.dirname(__file__), '.')
BACKGROUND_NAME = "yellow.png"

class PixbufsDemo(gtk.Window):
    frame  = None      # frame of the background image
    background = None  # background-pixbuf
    images     = []    # list of pixbufs
    back_width  = 0    # width of background image
    back_height = 0    # height of background image
    timeout_id  = 0    # timeout id
    frame_num   = 0    # number of the current frame
    timeout_id = None
    mx = SZELESSEG
    mmx = mx
    hirek2 = hirek

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect("destroy", lambda *w: gtk.main_quit())
        self.connect("destroy", self.cleanup_callback)
        self.set_title(self.__class__.__name__)
        self.set_resizable(False)
        self.set_decorated(False)
        self.set_size_request(SZELESSEG,60)
        self.parse_geometry("+8+410")

        if not self.load_pixbufs():
                sys.exit(1)
        else:

            self.frame = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8,
                self.back_width, self.back_height)

            da = gtk.DrawingArea()
            da.connect("expose_event", self.expose_cb)
            self.add(da)

            self.timeout_id = gtk.timeout_add(FRAME_DELAY, self.timeout)

            self.show_all()

    def load_pixbufs(self):
        ''' Loads the images for the demo and returns whether the
            operation succeeded.
        '''
        if self.background is not None:
            return True   # already loaded earlier

        # look in the the current directory where the file is installed
        try:
            self.background = gtk.gdk.pixbuf_new_from_file(
                os.path.join(IMAGE_DIR, BACKGROUND_NAME))
        except gobject.GError, error:
            return False

        self.back_width  = self.background.get_width()
        self.back_height = self.background.get_height()

        for filename in image_names:
            try:
                self.images.append(gtk.gdk.pixbuf_new_from_file(
                    os.path.join(IMAGE_DIR, filename)))
            except gobject.GError, error:
                return False

        return True

    def expose_cb(self, draw_area, event):
        ''' Expose callback for the drawing area. '''
        rowstride = self.frame.get_rowstride()

        pixels = self.frame.get_pixels()

        gc = draw_area.window.new_gc()
        
        draw_area.window.draw_rgb_image(
            draw_area.style.black_gc,
            event.area.x, event.area.y,
            event.area.width, event.area.height,
            'normal',
            pixels, rowstride,
            event.area.x, event.area.y)

        style = draw_area.get_style().copy()
        color=gtk.gdk.Color(blue=0,red=255,green=255)
        style.bg[gtk.STATE_NORMAL]=color
        style.black=color

        draw_area.window.draw_text(font,gc,self.mmx,48,self.hirek2) # 42

        self.mx -= 1
        self.mmx -= 1
        if self.mx < -hirek_hossz:
            self.mx = SZELESSEG
            self.mmx = self.mx
            self.hirek2 = hirek
            

#        print self.mx, self.mmx
        while self.mmx < MINX:
            self.mmx += font.string_width(self.hirek2[0])
#            print self.mmx
            self.hirek2=self.hirek2[1:len(self.hirek2)]

        return True

    def cleanup_callback(self, win):
        if self.timeout_id is not None:
            gtk.timeout_remove(self.timeout_id)
            self.timeout_id = None

    def timeout(self):
        ''' Timeout handler to regenerate the frame. '''
        self.background.copy_area(0, 0, self.back_width, self.back_height,
            self.frame, 0, 0)

###

        N_IMAGES = len(image_names)
        for i in range(0,N_IMAGES):

            iw = self.images[i].get_width()
            ih = self.images[i].get_height()

            xpos = image_pos[i] + self.mx + (48-iw)/2
            ypos = (60-ih)/2

            r1 = gtk.gdk.Rectangle()
            r1.x = xpos
            r1.y = ypos
            r1.width  = iw
            r1.height = ih

            r2 = gtk.gdk.Rectangle()
            r2.x = 0
            r2.y = 0
            r2.width  = self.back_width
            r2.height = self.back_height

            dest = r1.intersect(r2)

            if dest is not None:
                self.images[i].composite(
                    self.frame,
                    dest.x, dest.y, dest.width, dest.height,
#                        xpos, ypos, # hova
#                        iw, ih, # mekkorában
                        xpos, ypos,
                        1.0, 1.0,
                        gtk.gdk.INTERP_BILINEAR, 255)

###

        if self is not None:
            self.queue_draw()

        self.frame_num += 1
        return True

def main():
    PixbufsDemo()
    gtk.main()

if __name__ == '__main__':
    main()

