#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: graficos.py
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

import gtk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

class Graficar(gtk.Window):
  def graficar(self, datos, datos1, titulo):
    datos = datos # valores del tiempo de espera.
    datos1 = datos1 # valores de tiempo de cpu, tiempo de llegada y numeró de procesos.
    titulo = titulo
    x1 = []
    y1 = []
    y2 = []

    n = len(datos)
    for i in xrange(n):
      x1.append(datos1[i][0]) #Numero de proceso
      y1.append(datos[i][1]) #Tiempo de espera
      y2.append(datos1[i][1]) #tiempo de uso del cpu

    self.win = gtk.Window()
    self.win.set_default_size(600,480)
    self.win.set_position(gtk.WIN_POS_CENTER)
    self.win.set_title(titulo)

    f = Figure(figsize=(5,4), dpi=100)
    a = f.add_subplot(111)
    a.plot(x1, y1, color='blue', label='(Procesos, Tiempo de espera)')
    a.legend(loc = 2)
    a.set_title(titulo, color='red', size=14)
    a.set_xlabel(u'Número de procesos', color='red', size=14)
    a.set_ylabel('Tiempo de espera ', color='red', size=14)
    """
    # gráfica procesos vs tiempo de cpu
    #g = Figure(figsize=(5,4), dpi=100)
    b = f.add_subplot(111)
    b.plot(x1, y2, color='red', label='(Procesos, Tiempo de CPU)')
    b.set_xlabel(u'Número de procesos', color='red', size=14)
    b.set_ylabel('Tiempo de CPU ', color='red', size=14)
    """

    vbox = gtk.VBox(False, 5)

    canvas = FigureCanvas(f)
    canvas.show()
    #canvas1 = FigureCanvas(g)
    #canvas1.show()

    vbox.pack_start(canvas, True, True, 0)
    #vbox.pack_start(canvas1, True, True, 0)

    cerrar = gtk.Button(stock=gtk.STOCK_CLOSE)
    cerrar.connect("activate", self.close)
    vbox.pack_start(cerrar, False, False, 0)

    self.win.add(vbox)

    self.win.show_all()

  def close(self, widget=None, event=None):
    self.win.hide()
