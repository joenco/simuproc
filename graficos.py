#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: graficos.py
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

import gtk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

class Graficar(gtk.Window):
  def graficar(self, datos, titulo):
    datos = datos
    titulo = titulo
    x1 = []
    y1 = []

    n = len(datos)
    for i in xrange(n):
      x1.append(datos[i][0]) #Numero de proceso
      y1.append(datos[i][1]) #Tiempo de espera

    self.win = gtk.Window()
    self.win.set_default_size(600,480)
    self.win.set_title(titulo)

    f = Figure(figsize=(5,4), dpi=100)
    a = f.add_subplot(111)
    a.plot(x1, y1, color='blue', label='(Procesos, Tiempo de espera)')
    a.legend(loc = 2)
    a.set_title(titulo, color='red', size=14)
    a.set_xlabel(u'Número de procesos', color='red', size=14)
    a.set_ylabel('Tiempo de espera', color='red', size=14)

    vbox = gtk.VBox(False, 5)

    canvas = FigureCanvas(f)  # a gtk.Draself.wingArea
    canvas.show()
    vbox.pack_start(canvas, True, True, 0)

    cerrar = gtk.Button(stock=gtk.STOCK_CLOSE)
    cerrar.connect("activate", self.close)
    vbox.pack_start(cerrar, False, False, 0)

    self.win.add(vbox)

    self.win.show_all()

  def close(self, widget=None, event=None):
    self.win.hide()
