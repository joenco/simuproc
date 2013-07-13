#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import random
from threading import Thread, Semaphore

import gtk
import gtk.gdk

class Simulacion(Thread):
    def __init__(self, label, label1, label2, label3, n, i, semaforo):
        Thread.__init__(self)
        self.setDaemon(True)
        self.label = label
        self.label1 = label1
        self.label2 = label2
        self.label3 = label3
        self.n = n
        self.test = i
        self.semaforo = semaforo
        self.tiempo = float(0)

    def run(self):
        '''metodo principal del thread, duerme un self.tiempo aleatorio y despues
        cambia el Label'''

        #while True:

        self.semaforo.acquire()
        texto = str(self.test+1)
        texto4 = str(self.test)
        print texto4
        self.label2.set_text(texto4)
        texto5 = str(self.n - self.test)
        print texto5
        self.label3.set_text(texto5)
        texto1 = 'Ejecutando proceso '+texto

        gtk.gdk.threads_enter()
        # zona critica de gtk
        print texto1
        self.label.set_text(texto1)
        if self.test < self.n-1:
          texto3 = 'Proceso en cola esperando '+str(self.test+2)
          print texto3
          self.label1.set_text(texto3)
        else:
          self.label1.set_text(' ')
          texto4 = str(self.test+1)
          print texto4
          self.label2.set_text(texto4)
          texto5 = str(self.n - self.test-1)
          print texto5
          self.label3.set_text(texto5)

        self.tiempo = random.random() * 5
        time.sleep(self.tiempo)
        texto2 = 'Proceso '+texto+' terminado'
        self.label.set_text(texto2)
        print texto2
        gtk.gdk.threads_leave()

        self.semaforo.release()          

class ventana(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_default_size(640, 480)
        self.set_title('gtk con threads')
        self.vbox = gtk.VBox(False, 5)
        self.hbox = gtk.HBox(False, 5)
        self.add(self.hbox)
        self.hbox.pack_start(self.vbox, False, False, 0)

        #Las etiquetas
        self.label = gtk.Label('')
        self.label.set_justify(gtk.JUSTIFY_CENTER)
        self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('red'))
        self.label.realize()
        self.vbox.pack_start(self.label, False, False, 0)
        self.label1 = gtk.Label('')
        self.label1.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('blue'))
        self.label1.realize()
        self.label1.set_justify(gtk.JUSTIFY_CENTER)
        self.vbox.pack_start(self.label1, False, False, 0)
        self.label2 = gtk.Label('Ejecutados ')
        self.label2.set_justify(gtk.JUSTIFY_RIGHT)
        self.hbox.pack_start(self.label2, False, False, 0)
        self.label3 = gtk.Label('')
        self.label3.set_justify(gtk.JUSTIFY_CENTER)
        self.hbox.pack_start(self.label3, False, False, 0)
        self.label4 = gtk.Label('En cola ')
        self.label4.set_justify(gtk.JUSTIFY_RIGHT)
        self.hbox.pack_start(self.label4, False, False, 0)
        self.label5 = gtk.Label('')
        self.label5.set_justify(gtk.JUSTIFY_CENTER)
        self.hbox.pack_start(self.label5, False, False, 0)

        self.label.show()
        self.label1.show()
        self.label2.show()
        self.label3.show()
        self.label4.show()
        self.label5.show()
        self.vbox.show()
        self.hbox.show()
