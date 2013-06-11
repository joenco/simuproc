#!/usr/bin/env python

import gtk, pango
from matplotlib.figure import Figure
from numpy import arange
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
import random as r

class Graficos():
    def Graficar(self, procesos):
      self.x1 = []
      self.y1 = []
      self.y2 = []
      self.procesos = procesos
      
      n = len(self.procesos)
      for i in xrange(n):
        self.x1.append(self.procesos[i][0])#Numero de proceso
        self.y1.append(self.procesos[i][1])#Tiempo de ejecucion
        self.y2.append(self.procesos[i][3])#Tiempo de espera
        
      self.f = Figure(figsize=(5,4), dpi=100)
      self.a = self.f.add_subplot(111)
      self.a.plot(self.x1,self.y1)
      self.a.plot(self.x1,self.y2)
         
      self.canvas = FigureCanvas(self.f)  # a gtk.DrawingArea
      
      return self.canvas

