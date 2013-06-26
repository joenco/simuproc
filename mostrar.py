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

import gtk, pango
import gtk.gdk

class MostrarResultados(gtk.HBox):
    def __init__(self, CFG):
        gtk.HBox.__init__(self)

        table = gtk.Table(20, 6)

        attr = pango.AttrList()
        size = pango.AttrSize(18000, 0, -1)
        attr.insert(size)

        self.lbltitle1 = gtk.Label("Resultados de la corrida")
        self.lbltitle1.set_alignment(0, 0.5)
        self.lbltitle1.set_attributes(attr)
        table.attach(self.lbltitle1, 0, 2, 0, 1)

        self.txt1 = gtk.Label("Algoritmo")
        self.txt1.set_alignment(0, 0.5)
        table.attach(self.txt1, 0, 1, 1, 2)

        self.txt2 = gtk.Label("Número de procesos")
        self.txt2.set_alignment(0, 0.5)
        table.attach(self.txt2, 1, 2, 1, 2)

        self.txt3 = gtk.Label("Uso del CPU")
        self.txt3.set_alignment(0, 0.5)
        table.attach(self.txt3, 2, 3, 1, 2)

        self.txt4 = gtk.Label("Tiempo promedio del CPU")
        self.txt4.set_alignment(0, 0.5)
        table.attach(self.txt4, 3, 4, 1, 2)

        self.txt5 = gtk.Label("Tiempo promedio de espera")
        self.txt5.set_alignment(0, 0.5)
        table.attach(self.txt5, 4, 5, 1, 2)

        self.txt6 = gtk.Label("Gráfica")
        self.txt6.set_alignment(0, 0.5)
        table.attach(self.txt6, 5, 6, 1, 2)

        if CFG['fifo']==True:
          self.txtcfifo = gtk.Label("FCFS")
          self.txtcfifo.set_alignment(0, 0.5)
          table.attach(self.txtcfifo, 0, 1, 2, 3)

          self.np = gtk.Label(CFG['nproceso'])
          self.np.set_alignment(0, 0.5)
          table.attach(self.np, 1, 2, 2, 3)

          self.tejecucion = gtk.Label(CFG['calculofifo'][0])
          self.tejecucion.set_alignment(0, 0.5)
          table.attach(self.tejecucion, 2, 3, 2, 3)

          self.tpromedio = gtk.Label(CFG['calculofifo'][1])
          self.tpromedio.set_alignment(0, 0.5)
          table.attach(self.tpromedio, 3, 4, 2, 3)

          self.tproceso = gtk.Label(CFG['calculofifo'][2])
          self.tproceso.set_alignment(0, 0.5)
          table.attach(self.tproceso, 4, 5, 2, 3)

          self.gproceso = gtk.Button("Ver Gráfica")
          #self.gproceso.connect('clicked', self.Ver(1))
          table.attach(self.gproceso, 5, 6, 2, 3)

        # SJF
        if CFG['menortiempo']==True:
          self.txtmt = gtk.Label("SJF")
          self.txtmt.set_alignment(0, 0.5)
          table.attach(self.txtmt, 0, 1, 3, 4)

          self.np = gtk.Label(CFG['nproceso'])
          self.np.set_alignment(0, 0.5)
          table.attach(self.np, 1, 2, 3, 4)

          self.tejecucion = gtk.Label(CFG['mtiempo'][0])
          self.tejecucion.set_alignment(0, 0.5)
          table.attach(self.tejecucion, 2, 3, 3, 4)

          self.tpromedio = gtk.Label(CFG['mtiempo'][1])
          self.tpromedio.set_alignment(0, 0.5)
          table.attach(self.tpromedio, 3, 4, 3, 4)

          self.tproceso = gtk.Label(CFG['mtiempo'][2])
          self.tproceso.set_alignment(0, 0.5)
          table.attach(self.tproceso, 4, 5, 3, 4)

          self.gpoceso = gtk.Button('Ver gráfica')
          #self.gproceso.connect('clicked', self.Ver(2))
          table.attach(self.gpoceso, 5, 6, 3, 4)

        # Round Robin
        if CFG['roundrobin']==True:
          self.txtmt = gtk.Label("RR")
          self.txtmt.set_alignment(0, 0.5)
          table.attach(self.txtmt, 0, 1, 4, 5)

          self.np = gtk.Label(CFG['nproceso'])
          self.np.set_alignment(0, 0.5)
          table.attach(self.np, 1, 2, 4, 5)

          self.tejecucion = gtk.Label(CFG['calculorr'][0])
          self.tejecucion.set_alignment(0, 0.5)
          table.attach(self.tejecucion, 2, 3, 4, 5)

          self.tpromedio = gtk.Label(CFG['calculorr'][1])
          self.tpromedio.set_alignment(0, 0.5)
          table.attach(self.tpromedio, 3, 4, 4, 5)

          self.tproceso = gtk.Label(CFG['calculorr'][2])
          self.tproceso.set_alignment(0, 0.5)
          table.attach(self.tproceso, 4, 5, 4, 5)

          self.gpoceso = gtk.Button('Ver gráfica')
          #self.gproceso.connect('clicked', self.Ver(2))
          table.attach(self.gpoceso, 5, 6, 4, 5)

        # PSJF
        if CFG['soprtunidad']==True:
          self.txtmt = gtk.Label("PSJF")
          self.txtmt.set_alignment(0, 0.5)
          table.attach(self.txtmt, 0, 1, 5, 6)

          self.np = gtk.Label(CFG['nproceso'])
          self.np.set_alignment(0, 0.5)
          table.attach(self.np, 1, 2, 5, 6)

          self.tejecucion = gtk.Label(CFG['psjf'][0])
          self.tejecucion.set_alignment(0, 0.5)
          table.attach(self.tejecucion, 2, 3, 5, 6)

          self.tpromedio = gtk.Label(CFG['psjf'][1])
          self.tpromedio.set_alignment(0, 0.5)
          table.attach(self.tpromedio, 3, 4,5, 6)

          self.tproceso = gtk.Label(CFG['psjf'][2])
          self.tproceso.set_alignment(0, 0.5)
          table.attach(self.tproceso, 4, 5, 5, 6)

          self.gpoceso = gtk.Button('Ver gráfica')
          #self.gproceso.connect('clicked', self.Ver(2))
          table.attach(self.gpoceso, 5, 6, 5, 6)

        #self.graficorr = CFG['calculorr'][6]

        self.pack_start(table, padding=40)
