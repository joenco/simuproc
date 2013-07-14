#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: mostrar.py
# COPYRIGHT:
#       (C) 2013 Jorge E. Ortega A. <joenco@esdebian.org>
#       (C) 2013 
# LICENCIA: GPL-3
# ==============================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# CODE IS POETRY

import gtk, pango, gobject
import gtk.gdk
from threading import Thread, Semaphore
from calculo import Algoritmos
from simulacion import Simulacion, ventana
from graficos import Graficar

calculo = Algoritmos()
Graficar = Graficar()

class MostrarResultados(gtk.HBox):
    def __init__(self, CFG):
        gtk.HBox.__init__(self)

        table = gtk.Table(20, 5)

        attr = pango.AttrList()
        size = pango.AttrSize(18000, 0, -1)
        attr.insert(size)

        self.lbltitle1 = gtk.Label("Espere mientras hacemos los calculos")
        self.lbltitle1.set_alignment(0, 0.5)
        self.lbltitle1.set_attributes(attr)
        table.attach(self.lbltitle1, 0, 2, 0, 1)

        self.n=int(CFG['nproceso'])
        self.n1=int(CFG['nproceso'])/8
        self.intervalo = 0.02
        if self.n1<100:
            self.n1=100
            self.intervalo=0.03

        self.pbar = gtk.ProgressBar()
        self.pbar.show()
        table.attach(self.pbar, 0, 6, 6, 7)
        self.timer = gobject.timeout_add (self.n1, self.progress_timeout, CFG, self)

        self.txt1 = gtk.Label(' ')
        self.txt1.set_alignment(0, 0.5)
        table.attach(self.txt1, 0, 1, 1, 2)

        self.txt2 = gtk.Label(' ')
        self.txt2.set_alignment(0, 0.5)
        table.attach(self.txt2, 1, 2, 1, 2)

        self.txt3 = gtk.Label(' ')
        self.txt3.set_alignment(0, 0.5)
        table.attach(self.txt3, 2, 3, 1, 2)

        self.txt4 = gtk.Label(' ')
        self.txt4.set_alignment(0, 0.5)
        table.attach(self.txt4, 3, 4, 1, 2)

        self.txt5 = gtk.Label(' ')
        self.txt5.set_alignment(0, 0.5)
        table.attach(self.txt5, 4, 5, 1, 2)

        self.listafuncion = gtk.ListStore(str)

        if CFG['fifo']==True:
          self.txtfifo = gtk.Label(' ')
          self.txtfifo.set_alignment(0, 0.5)
          table.attach(self.txtfifo, 0, 1, 2, 3)

          self.txtfifo1 = gtk.Label(' ')
          self.txtfifo1.set_alignment(0, 0.5)
          table.attach(self.txtfifo1, 1, 2, 2, 3)

          self.txtfifo2 = gtk.Label(' ')
          self.txtfifo2.set_alignment(0, 0.5)
          table.attach(self.txtfifo2, 2, 3, 2, 3)

          self.txtfifo3 = gtk.Label(' ')
          self.txtfifo3.set_alignment(0, 0.5)
          table.attach(self.txtfifo3, 3, 4, 2, 3)

          self.txtfifo4 = gtk.Label(' ')
          self.txtfifo4.set_alignment(0, 0.5)
          table.attach(self.txtfifo4, 4, 5, 2, 3)

          self.listafuncion.append(["FCFS"])

        # SJF
        if CFG['menortiempo']==True:
          self.txtmt = gtk.Label(' ')
          self.txtmt.set_alignment(0, 0.5)
          table.attach(self.txtmt, 0, 1, 3, 4)

          self.txtmt1 = gtk.Label(' ')
          self.txtmt1.set_alignment(0, 0.5)
          table.attach(self.txtmt1, 1, 2, 3, 4)

          self.txtmt2 = gtk.Label(' ')
          self.txtmt2.set_alignment(0, 0.5)
          table.attach(self.txtmt2, 2, 3, 3, 4)

          self.txtmt3 = gtk.Label(' ')
          self.txtmt3.set_alignment(0, 0.5)
          table.attach(self.txtmt3, 3, 4, 3, 4)

          self.txtmt4 = gtk.Label(' ')
          self.txtmt4.set_alignment(0, 0.5)
          table.attach(self.txtmt4, 4, 5, 3, 4)

          self.listafuncion.append(["SJF"])
        # Round Robin
        if CFG['roundrobin']==True:
          self.txtrr = gtk.Label(' ')
          self.txtrr.set_alignment(0, 0.5)
          table.attach(self.txtrr, 0, 1, 4, 5)

          self.txtrr1 = gtk.Label(' ')
          self.txtrr1.set_alignment(0, 0.5)
          table.attach(self.txtrr1, 1, 2, 4, 5)

          self.txtrr2 = gtk.Label(' ')
          self.txtrr2.set_alignment(0, 0.5)
          table.attach(self.txt2, 2, 3, 4, 5)

          self.txtrr3 = gtk.Label(' ')
          self.txtrr3.set_alignment(0, 0.5)
          table.attach(self.txtrr3, 3, 4, 4, 5)

          self.txtrr4 = gtk.Label(' ')
          self.txtrr4.set_alignment(0, 0.5)
          table.attach(self.txtrr4, 4, 5, 4, 5)

          self.listafuncion.append(["RR"])

        # PSJF
        if CFG['soprtunidad']==True:
          self.txtso = gtk.Label(' ')
          self.txtso.set_alignment(0, 0.5)
          table.attach(self.txtso, 0, 1, 5, 6)

          self.txtso1 = gtk.Label(' ')
          self.txtso1.set_alignment(0, 0.5)
          table.attach(self.txtso1, 1, 2, 5, 6)

          self.txtso2 = gtk.Label(' ')
          self.txtso2.set_alignment(0, 0.5)
          table.attach(self.txtso2, 2, 3, 5, 6)

          self.txtso3 = gtk.Label(' ')
          self.txtso3.set_alignment(0, 0.5)
          table.attach(self.txtso3, 3, 4,5, 6)

          self.txtso4 = gtk.Label(' ')
          self.txtso4.set_alignment(0, 0.5)
          table.attach(self.txtso4, 4, 5, 5, 6)

          self.listafuncion.append(["PSJF"])

        self.listaalgoritmo = gtk.combo_box_new_text()
        self.listaalgoritmo.set_model(self.listafuncion)
        self.listaalgoritmo.set_active(0)
        table.attach(self.listaalgoritmo, 0, 1, 6, 7)

        self.ver = gtk.Button("Ver gráfica")
        self.ver.hide()
        self.ver.connect('clicked', self.Ver)
        table.attach(self.ver, 2, 3, 6, 7)

        self.simulacion = gtk.Button("Ver Simulación")
        self.simulacion.hide()
        self.simulacion.connect('clicked', self.Simulacion)
        table.attach(self.simulacion, 4, 5, 6, 7)

        self.pack_start(table, padding=40)

    def Ver(self, widget=None, event=None):
      if self.listaalgoritmo.get_active_text() == 'FCFS':
        grafico = Graficar.graficar(self.datos, u'Gráfico FCFS')
      if self.listaalgoritmo.get_active_text() == 'SJF':
        grafico  = Graficar.graficar(self.datos1, u'Gráfico SJF')

    def Simulacion(self, widget=None, event=None):
      gtk.gdk.threads_init()
      win = ventana()
      semaforo = Semaphore(1)
      if self.listaalgoritmo.get_active_text() == 'FCFS':
        win.set_title('Simulación del Algoritmo FCFS')
        for x in xrange(self.n):
          hilo = Simulacion(win.label, win.label1, win.label3, win.label5, self.n, x, semaforo)
          hilo.start()
      win.show()

    def progress_timeout(pbobj, CFG, self):
        new_val = pbobj.pbar.get_fraction() + self.intervalo

        if new_val < 0.2:
            self.cola = calculo.Cola_Procesos(self.n, CFG['tejecucion'], CFG['tcpu'], CFG['ejecucion'], CFG['cpu'])
            self.intervalo=0.05
        if new_val > 0.3 and new_val < 0.35:
          if CFG['fifo'] == True:
            CFG['calculofifo'] = calculo.FCFS(self.cola)
        if new_val > 0.4 and new_val < 0.45:
          if CFG['menortiempo'] == True:
            CFG['mtiempo'] = calculo.SJF(self.cola)
        if new_val > 0.6 and new_val < 0.65:
          if CFG['roundrobin'] == True:
            CFG['calculorr'] = calculo.RoundRobin(self.cola, CFG['trr'])
        if new_val > 0.8 and new_val < 0.85:
          if CFG['soprtunidad'] == True:
            CFG['psjf'] = calculo.PSJF(self.cola)
        if new_val > 1.0:
            self.lbltitle1.set_text('Resultados de la corrida')
            self.pbar.hide()
            self.txt1.set_text("Algoritmos")
            self.txt2.set_text(u"Número de procesos")
            self.txt3.set_text("Uso del CPU")
            self.txt4.set_text("Tiempo promedio del CPU")
            self.txt5.set_text("Tiempo promedio de espera")

            if CFG['fifo']==True:
                self.txtfifo.set_text("FCFS")
                self.txtfifo1.set_text(str(self.n))
                self.txtfifo2.set_text(str(CFG['calculofifo'][0]))
                self.txtfifo3.set_text(str(CFG['calculofifo'][1]))
                self.txtfifo4.set_text(str(CFG['calculofifo'][2]))
                self.datos = CFG['calculofifo'][3]
            if CFG['menortiempo']==True:
                self.txtmt.set_text("SJF")
                self.txtmt1.set_text(str(self.n))
                self.txtmt2.set_text(str(CFG['mtiempo'][0]))
                self.txtmt3.set_text(str(CFG['mtiempo'][1]))
                self.txtmt4.set_text(str(CFG['mtiempo'][2]))
                self.datos1 = CFG['mtiempo'][3]
            if CFG['roundrobin']==True:
                self.txtrr.set_text("RR")
                self.txtrr1.set_text(str(self.n))
                self.txtrr2.set_text(str(CFG['calculorr'][0]))
                self.txtrr3.set_text(str(CFG['calculorr'][1]))
                self.txtrr4.set_text(str(CFG['calculorr'][2]))
            if CFG['soprtunidad']==True:
                self.txtso.set_text("PSJF")
                self.txtso1.set_text(str(self.n))
                self.txtso2.set_text(str(CFG['psjf'][0]))
                self.txtso3.set_text(str(CFG['psjf'][1]))
                self.txtso4.set_text(str(CFG['psjf'][2]))
            CFG['w'].anterior.show()
        CFG['w'].cancelar.show()
        CFG['w'].acerca.show()

        pbobj.pbar.set_fraction(new_val)

        return True
