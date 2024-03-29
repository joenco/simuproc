#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: mostrar.py
# COPYRIGHT:
#       (C) 2013 Jorge E. Ortega A. <joenco@esdebian.org>
#       (C) 2013 Jesus Perez <perezj89@gmail.com>
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
from calculo import Algoritmos, FCFS
from simulacion import Simulacion, ventana
from graficos import Graficar

calculo = Algoritmos()

"""creamos el objeto calculo para usarlo."""

Graficar = Graficar()

"""creamos el objeto graficar, para poder graficar."""

class MostrarResultados(gtk.HBox):

    """ ventana que muestra los resultados al usuario en una tabla"""

    def __init__(self, CFG):
        gtk.HBox.__init__(self)

        table = gtk.Table(20, 7, True)

        attr = pango.AttrList()
        size = pango.AttrSize(18000, 0, -1)
        attr.insert(size)

        self.lbltitle1 = gtk.Label("Espere mientras hacemos los calculos")
        self.lbltitle1.set_alignment(0, 0.5)
        self.lbltitle1.set_attributes(attr)
        table.attach(self.lbltitle1, 0, 4, 0, 1)

        self.n=int(CFG['nproceso'])
        self.n1=self.n/8
        self.intervalo = 0.02
        if self.n1<100:
            self.n1=100
            self.intervalo=0.03

        self.pbar = gtk.ProgressBar()
        self.pbar.set_size_request(70, 20)
        self.pbar.show()
        table.attach(self.pbar, 0, 6, 6, 7)
        self.timer = gobject.timeout_add (self.n1, self.progress_timeout, CFG, self)

        self.txt1 = gtk.Label(' ')
        self.txt1.set_alignment(0, 0.5)
        table.attach(self.txt1, 0, 1, 1, 2)

        self.txt2 = gtk.Label(' ')
        self.txt2.set_alignment(0, 0.5)
        table.attach(self.txt2, 1, 2, 1, 2)

        #self.txt3 = gtk.Label(' ')
        #self.txt3.set_alignment(0, 0.5)
        #table.attach(self.txt3, 2, 3, 1, 2)

        self.txt4 = gtk.Label(' ')
        self.txt4.set_alignment(0, 0.5)
        table.attach(self.txt4, 2, 3, 1, 2)

        self.txt5 = gtk.Label(' ')
        self.txt5.set_alignment(0, 0.5)
        table.attach(self.txt5, 3, 4, 1, 2)

        self.txt6 = gtk.Label(' ')
        self.txt6.set_alignment(0, 0.5)
        table.attach(self.txt6, 4, 5, 1, 2)

        self.txt7 = gtk.Label(' ')
        self.txt7.set_alignment(0, 0.5)
        table.attach(self.txt7, 5, 7, 1, 2)

        self.listafuncion = gtk.ListStore(str)

        if CFG['fifo']==True:
          self.txtfifo = gtk.Label(' ')
          self.txtfifo.set_alignment(0, 0.5)
          table.attach(self.txtfifo, 0, 1, 2, 3)

          self.txtfifo1 = gtk.Label(' ')
          self.txtfifo1.set_alignment(0, 0.5)
          table.attach(self.txtfifo1, 1, 2, 2, 3)

          #self.txtfifo2 = gtk.Label(' ')
          #self.txtfifo2.set_alignment(0, 0.5)
          #table.attach(self.txtfifo2, 2, 3, 2, 3)

          self.txtfifo3 = gtk.Label(' ')
          self.txtfifo3.set_alignment(0, 0.5)
          table.attach(self.txtfifo3, 2, 3, 2, 3)

          self.txtfifo4 = gtk.Label(' ')
          self.txtfifo4.set_alignment(0, 0.5)
          table.attach(self.txtfifo4, 3, 4, 2, 3)

          self.txtfifo5 = gtk.Label(' ')
          self.txtfifo5.set_alignment(0, 0.5)
          table.attach(self.txtfifo5, 4, 5, 2, 3)

          self.txtfifo6 = gtk.Label(' ')
          self.txtfifo6.set_alignment(0, 0.5)
          table.attach(self.txtfifo6, 5, 6, 2, 3)

          self.listafuncion.append(["FCFS"])

        # SJF
        if CFG['menortiempo']==True:
          self.txtmt = gtk.Label(' ')
          self.txtmt.set_alignment(0, 0.5)
          table.attach(self.txtmt, 0, 1, 3, 4)

          self.txtmt1 = gtk.Label(' ')
          self.txtmt1.set_alignment(0, 0.5)
          table.attach(self.txtmt1, 1, 2, 3, 4)

          #self.txtmt2 = gtk.Label(' ')
          #self.txtmt2.set_alignment(0, 0.5)
          #table.attach(self.txtmt2, 2, 3, 3, 4)

          self.txtmt3 = gtk.Label(' ')
          self.txtmt3.set_alignment(0, 0.5)
          table.attach(self.txtmt3, 2, 3, 3, 4)

          self.txtmt4 = gtk.Label(' ')
          self.txtmt4.set_alignment(0, 0.5)
          table.attach(self.txtmt4, 3, 4, 3, 4)

          self.txtmt5 = gtk.Label(' ')
          self.txtmt5.set_alignment(0, 0.5)
          table.attach(self.txtmt5, 4, 5, 3, 4)

          self.txtmt6 = gtk.Label(' ')
          self.txtmt6.set_alignment(0, 0.5)
          table.attach(self.txtmt6, 5, 6, 3, 4)

          self.listafuncion.append(["SJF"])
        # Round Robin
        if CFG['roundrobin']==True:
          self.txtrr = gtk.Label(' ')
          self.txtrr.set_alignment(0, 0.5)
          table.attach(self.txtrr, 0, 1, 4, 5)

          self.txtrr1 = gtk.Label(' ')
          self.txtrr1.set_alignment(0, 0.5)
          table.attach(self.txtrr1, 1, 2, 4, 5)

          #self.txtrr2 = gtk.Label(' ')
          #self.txtrr2.set_alignment(0, 0.5)
          #table.attach(self.txtrr2, 2, 3, 4, 5)

          self.txtrr3 = gtk.Label(' ')
          self.txtrr3.set_alignment(0, 0.5)
          table.attach(self.txtrr3, 2, 3, 4, 5)

          self.txtrr4 = gtk.Label(' ')
          self.txtrr4.set_alignment(0, 0.5)
          table.attach(self.txtrr4, 3, 4, 4, 5)

          self.txtrr5 = gtk.Label(' ')
          self.txtrr5.set_alignment(0, 0.5)
          table.attach(self.txtrr5, 4, 5, 4, 5)

          self.txtrr6 = gtk.Label(' ')
          self.txtrr6.set_alignment(0, 0.5)
          table.attach(self.txtrr6, 5, 6, 4, 5)

          self.listafuncion.append(["RR"])

        # PSJF
        if CFG['soprtunidad']==True:
          self.txtso = gtk.Label(' ')
          self.txtso.set_alignment(0, 0.5)
          table.attach(self.txtso, 0, 1, 5, 6)

          self.txtso1 = gtk.Label(' ')
          self.txtso1.set_alignment(0, 0.5)
          table.attach(self.txtso1, 1, 2, 5, 6)

          #self.txtso2 = gtk.Label(' ')
          #self.txtso2.set_alignment(0, 0.5)
          #table.attach(self.txtso2, 2, 3, 5, 6)

          self.txtso3 = gtk.Label(' ')
          self.txtso3.set_alignment(0, 0.5)
          table.attach(self.txtso3, 2, 3,5, 6)

          self.txtso4 = gtk.Label(' ')
          self.txtso4.set_alignment(0, 0.5)
          table.attach(self.txtso4, 3, 4, 5, 6)

          self.txtso5 = gtk.Label(' ')
          self.txtso5.set_alignment(0, 0.5)
          table.attach(self.txtso5, 4, 5, 5, 6)

          self.txtso6 = gtk.Label(' ')
          self.txtso6.set_alignment(0, 0.5)
          table.attach(self.txtso6, 5, 6, 5, 6)

          self.listafuncion.append(["PSJF"])

        self.listaalgoritmo = gtk.combo_box_new_text()
        self.listaalgoritmo.set_size_request(40, 10)
        self.listaalgoritmo.set_model(self.listafuncion)
        self.listaalgoritmo.set_active(0)
        table.attach(self.listaalgoritmo, 0, 1, 6, 7)

        self.ver = gtk.Button("Gráfica")
        self.ver.set_size_request(100, 20)
        self.ver.connect('clicked', self.Ver)
        table.attach(self.ver, 2, 3, 6, 7)

        self.simulacion = gtk.Button("Simulación")
        self.simulacion.set_size_request(120, 20)
        self.simulacion.connect('clicked', self.Simulacion)
        table.attach(self.simulacion, 4, 5, 6, 7)

        self.pack_start(table, padding=40)

    def Ver(self, widget=None, event=None):

      """Función que permite abrir la grafica del algoritmo seleccionado."""

      if self.listaalgoritmo.get_active_text() == 'FCFS':
        grafico = Graficar.graficar(self.datos, self.cola, u'Gráfico FCFS')
      if self.listaalgoritmo.get_active_text() == 'SJF':
        grafico  = Graficar.graficar(self.datos1,self.cola, u'Gráfico SJF')
      if self.listaalgoritmo.get_active_text() == 'RR':
        grafico = Graficar.graficar(self.datos2, self.cola, u'Gráfico RR')
      if self.listaalgoritmo.get_active_text() == 'PSJF':
        grafico = Graficar.graficar(self.datos3, self.cola, u'Gráfico PSJF')

    def Simulacion(self, widget=None, event=None):

      """Función que permite abrir la simulación del algoritmo seleccionado."""

      if self.n>10:
        self.n=10
      gtk.gdk.threads_init()
      win = ventana()
      semaforo = Semaphore(1)
      if self.listaalgoritmo.get_active_text() == 'FCFS':
        win.set_title('Simulación del Algoritmo FCFS')
        for x in xrange(self.n):
          hilo = Simulacion(win.label, win.label1, win.label3, win.label5, self.n, x, self.t_e, semaforo)
          hilo.start()
      if self.listaalgoritmo.get_active_text() == 'SJF':
        win.set_title('Simulación del Algoritmo SJF')
        for x in xrange(self.n):
          hilo = Simulacion(win.label, win.label1, win.label3, win.label5, 10, x, self.t_e1, semaforo)
          hilo.start()
      win.show()

    def progress_timeout(pbobj, CFG, self):

        """Función que va verificando el progreso de los calculos, cuando termina, muestra los resultados."""

        new_val = pbobj.pbar.get_fraction() + self.intervalo

        if new_val < 0.2:
            self.cola = calculo.Cola_Procesos(self.n, CFG['tejecucion'], CFG['tcpu'], CFG['tbloqueocpu'], CFG['tbloqueo'], CFG['ejecucion'], CFG['cpu'], CFG['bloqueocpu'], CFG['bloqueo'])
            self.intervalo=0.05

        #fifo = FCFS(self.cola) # creamos el hilo
        if new_val > 0.3 and new_val < 0.35:
          if CFG['fifo'] == True:
            CFG['calculofifo'] = calculo.FCFS(self.cola)
            #fifo.start() #iniciamos el hilo
        if new_val > 0.4 and new_val < 0.45:
          if CFG['menortiempo'] == True:
            CFG['mtiempo'] = calculo.SJF(self.cola)
        if new_val > 0.6 and new_val < 0.65:
          if CFG['roundrobin'] == True:
            CFG['calculorr'] = calculo.RoundRobin(self.cola, CFG['trr'],CFG['tbloqueocpu'], CFG['tbloqueo'],  CFG['bloqueocpu'], CFG['bloqueo'])
        if new_val > 0.8 and new_val < 0.85:
          if CFG['soprtunidad'] == True:
            CFG['psjf'] = calculo.PSJF(self.cola,CFG['tbloqueocpu'], CFG['tbloqueo'],  CFG['bloqueocpu'], CFG['bloqueo'])

        #if CFG['fifo'] == True || new_val>0.1 || new_val>0.1:
        #if CFG['fifo'] == True:
          #CFG['calculofifo'] = fifo.resultados
          #fifo.join() #esperamos a que termine
        if new_val > 1.0:
            self.lbltitle1.set_text('Resultados de la corrida')
            self.pbar.hide()
            self.txt1.set_text("Algoritmos")
            self.txt2.set_text("Procesos")
            #self.txt3.set_text("Uso del CPU")
            self.txt4.set_text("CPU promedio")
            self.txt5.set_text("Espera min")
            self.txt6.set_text("Espera max")
            self.txt7.set_text("Espera promedio")

            if CFG['fifo']==True:
                self.txtfifo.set_text("FCFS")
                self.txtfifo1.set_text(str(self.n))
                #self.txtfifo2.set_text(str(CFG['calculofifo'][0]))
                self.txtfifo3.set_text(str(CFG['calculofifo'][1]))
                self.t_e = CFG['calculofifo'][2]
                self.txtfifo4.set_text(str(CFG['calculofifo'][4]))
                self.txtfifo5.set_text(str(CFG['calculofifo'][5]))
                self.txtfifo6.set_text(str(CFG['calculofifo'][2]))
                self.datos = CFG['calculofifo'][3]
            if CFG['menortiempo']==True:
                self.txtmt.set_text("SJF")
                self.txtmt1.set_text(str(self.n))
                #self.txtmt2.set_text(str(CFG['mtiempo'][0]))
                self.txtmt3.set_text(str(CFG['mtiempo'][1]))
                self.txtmt4.set_text(str(CFG['mtiempo'][4]))
                self.txtmt5.set_text(str(CFG['mtiempo'][5]))
                self.txtmt6.set_text(str(CFG['mtiempo'][2]))
                self.t_e1 = CFG['mtiempo'][2]
                self.datos1 = CFG['mtiempo'][3]
            if CFG['roundrobin']==True:
                self.txtrr.set_text("RR")
                self.txtrr1.set_text(str(self.n))
                #self.txtrr2.set_text(str(CFG['calculorr'][0]))
                self.txtrr3.set_text(str(CFG['calculorr'][1]))
                self.txtrr4.set_text(str(CFG['calculorr'][4]))
                self.txtrr5.set_text(str(CFG['calculorr'][5]))
                self.txtrr6.set_text(str(CFG['calculorr'][2]))
                self.t_e2 = CFG['calculorr'][2]
                self.datos2 = CFG['calculorr'][3]
            if CFG['soprtunidad']==True:
                self.txtso.set_text("PSJF")
                self.txtso1.set_text(str(self.n))
                #self.txtso2.set_text(str(CFG['psjf'][0]))
                self.txtso3.set_text(str(CFG['psjf'][1]))
                self.txtso4.set_text(str(CFG['psjf'][4]))
 		self.txtso5.set_text(str(CFG['psjf'][5]))
                self.txtso6.set_text(str(CFG['psjf'][2]))
                self.datos3 = CFG['psjf'][3]
            CFG['w'].anterior.show()
        CFG['w'].cancelar.show()
        CFG['w'].acerca.show()

        pbobj.pbar.set_fraction(new_val)

        return True
