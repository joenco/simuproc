#! /usr/bin/python
# -*- coding: utf-8 -*-

class Guardar():
    def Guardar(self, datos, a):
      self.nombre = datos
      self.a = int(a)

      if self.a==0:
        self.datos = open('data/FCFS.dat', 'w')
      elif self.a==1:
        self.datos = open('data/SJF.dat', 'w')
      elif self.a==2:
        self.datos = open('data/PPSJF.dat', 'w')
      elif self.a==3:
        self.datos = open('data/RoundRobin.dat', 'w')

      n = len(self.nombre)
      for i in xrange(n):
        for j in xrange(2):
          data=str(self.nombre[i][j])
          self.datos.write(' '+data)
        self.datos.write('\n')

      self.datos.close()
