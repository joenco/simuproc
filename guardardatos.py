#! /usr/bin/python
# -*- coding: utf-8 -*-

class Guardar():
    def Guardar(self, datos, datos1, a):
      self.datos = datos #datos de tiempo de espera.
      self.datos1 = datos1 # datos de tiempo del cpu y tiempo de llegada.
      self.a = int(a)

      if self.a==0:
        self.data = open('data/FCFS.dat', 'w')
      elif self.a==1:
        self.data = open('data/SJF.dat', 'w')
      elif self.a==2:
        self.data = open('data/PPSJF.dat', 'w')
      elif self.a==3:
        self.data = open('data/RoundRobin.dat', 'w')

      n = len(self.datos)

      dat = 'N  |  T.E  |  T.CPU  |  T.L  |'
      self.data.write(dat)
      self.data.write('\n')
      for i in xrange(n):
        x1 = str(self.datos[i][0]) #Número de procesos
        y1 = str(self.datos[i][1]) # tiempo de espera
        a1 = str(self.datos1[i][1]) # tiempo de cpu
        z1 = str(self.datos1[i][2]) # tiempo de llegada
        dat = x1+'  |  '+y1+'  |  '+a1+'  |  '+z1+'  |'
        self.data.write(dat)
        self.data.write('\n')

      self.data.close()
