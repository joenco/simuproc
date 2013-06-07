#!/usr/bin/env python

import gtk, pango
from matplotlib.figure import Figure
from numpy import arange
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
import random as r

class Graficos():
    def Graficar(self, n, x, y, f):
      self.x= float(x)
      self.y = float(y)
      self.n = int(n)
      self.f = f
      self.x1 = []
      self.y1 = []

      for i in xrange(self.n):
        self.x1.append(i)
        self.y1.append(r.uniform(0, self.x))

      self.f = Figure(figsize=(5,4), dpi=100)
      self.a = self.f.add_subplot(111)
      self.a.plot(self.x1,self.y1)

      self.canvas = FigureCanvas(self.f)  # a gtk.DrawingArea

      return self.canvas
