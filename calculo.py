#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: calculo.py
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
import random
import numpy as np
import scipy.stats as st
from time import sleep

class Algoritmos(gtk.HBox):
    def RoundRobin(self, n, te, ts, fe, fs ,q):
      self.cola_procesos = []
      self.total_llegada = 0
      self.total_servicio=0
      self.total_esperado=0
      self.promedio_llegada=0
      self.promedio_servicio=0
      self.promedio_de_espera=0
      random.seed(5000)
      self.n = int(n) #número de procesos.
      self.te = float(te) #tiempo de llegada de los procesos
      self.ts = float(ts) #tiempo de duracion de los procesos.
      self.func_llegada = fe #función para los tiempos de llegada.
      self.func_servicio = fs #función para el tiempo de duracion.
      self.aux = 0
      self.q = float(q)
      self.ncpu = 0
      self.tiempo_parcial = 0

      for i in xrange(self.n+1):

        self.cola_procesos.append([])#agregamos un objeto de tipo lista a la cola
        self.cola_procesos[i].append(i)
        
	#tiempo de duracion
        if self.func_servicio == 'Constante':
         self.cola_procesos[i].append(self.ts)
        elif self.func_servicio == 'Uniforme':
          self.cola_procesos[i].append(np.random.randint(0, self.ts))
        elif self.func_servicio == 'Exponencial':
          self.cola_procesos[i].append(np.random.exponential(self.ts))
        elif self.func_servicio == 'Normal':
          self.cola_procesos[i].append(st.norm.cdf(self.ts))

	#tiempo de llegada   
	if self.func_llegada == 'Constante':
          self.cola_procesos[i].append(self.te)
        elif self.func_llegada == 'Uniforme':
          self.cola_procesos[i].append(np.random.randint(0, self.te))
        elif self.func_llegada == 'Exponencial':
          self.cola_procesos[i].append(np.random.exponential(self.te))
        elif self.func_llegada == 'Normal':
          self.cola_procesos[i].append(st.norm.cdf(self.te))

        self.cola_procesos[i].append(0);         



      while(self.aux<self.n):
	self.aux=0;
	for i in xrange(self.n):
          if(self.cola_procesos[i][1]>0):
            if(self.cola_procesos[i][1]-self.q > 0):
              self.tiempo_parcial = self.q
            else:
	      self.tiempo_parcial = self.cola_procesos[i][1]	
            for j in xrange(self.n):
              if (i!=j):
                  if(self.cola_procesos[j][1]>0):
                    self.cola_procesos[j][3] += self.tiempo_parcial
            self.cola_procesos[i][1]=self.cola_procesos[i][1]-self.q
	    self.ncpu = self.ncpu+1
            self.total_servicio += self.tiempo_parcial
	  else:      
	    self.aux=self.aux+1
        

      
      for i in xrange(self.n):
        self.total_llegada += self.cola_procesos[i][2]
        self.total_esperado +=  self.cola_procesos[i][3]
        
      self.promedio_llegada = float(self.total_llegada/self.n)
      self.promedio_servicio = float(self.total_servicio/self.ncpu)
      self.promedio_de_espera = float(self.total_esperado/self.n)
      print 'Tiempo total de llegada: ',self.total_llegada
      print 'Tiempo total de proceso: ',self.total_servicio
      print 'Tiempo promedio de llegada: ',(self.promedio_llegada)
      print 'Tiempo promedio de proceso: ',(self.promedio_servicio)
      print 'Tiempo promedio esperado: ',(self.promedio_de_espera)

        
      return self.total_llegada, self.promedio_llegada, self.total_servicio, self.promedio_servicio, self.promedio_de_espera, self.cola_procesos	

#First Come First Served(FCFS)
    def FCFS(self, n, te, tcpu, f1, f2):
      self.cola_procesos = []
      self.n = int(n)
      self.te = float(te) #float(te) #tiempo de llegada
      self.tcpu = float(tcpu) #float(tcpu) #tiempo de uso del CPU
      self.func_llegada = f1
      self.func_cpu = f2
      self.avergwt=float(0.0)
      self.avergtt=float(0.0)

      for i in xrange(self.n):
        self.cola_procesos.append([]) #agregamos un objeto de tipo lista a la cola
        self.cola_procesos[i].append(i)

        if self.func_cpu == 'Constante':
          self.cola_procesos[i].append(self.tcpu)
        elif self.func_cpu == 'Uniforme':
          self.cola_procesos[i].append(np.random.randint(0, self.tcpu))
        elif self.func_cpu == 'Exponencial':
          self.cola_procesos[i].append(np.random.exponential(self.tcpu))
        elif self.func_cpu == 'Normal':
          self.cola_procesos[i].append(st.norm.cdf(self.tcpu))

        if self.func_llegada == 'Constante':
          self.cola_procesos[i].append(self.te)
        elif self.func_llegada == 'Uniforme':
          self.cola_procesos[i].append(np.random.randint(0, self.te))
        elif self.func_llegada == 'Exponencial':
          self.cola_procesos[i].append(np.random.exponential(self.te))
        elif self.func_llegada == 'Normal':
          self.cola_procesos[i].append(st.norm.cdf(self.te))

      s=float(0.0)
      self.sum=float(0.0)
      s1=0
      self.stb=0
      ss=0
      print 'Nombre del proceso\t\t Tiempo de espera \t \tTiempo de rafaga'
      for i in xrange(self.n):
        print self.cola_procesos[i][0],'\t\t',self.cola_procesos[i][1],'\t\t',self.cola_procesos[i][2]
        self.cola_procesos[i].append(s) #wt
        s= round(s+self.cola_procesos[i][1],2)
        self.sum = round(self.sum+s-self.cola_procesos[i][2])
        self.cola_procesos[i].append(self.cola_procesos[i][1]+self.cola_procesos[i][2]) #tt
        self.stb=round(self.stb+self.cola_procesos[i][1], 2)

      self.avergwt = round(self.sum/self.n, 2)
      self.avergtt = round(self.stb/self.n, 2)
      print "\nel tiempo total de espera de los procesos es: ",self.sum
      print "el tiempo total  de uso del CPU es: ",self.stb
      print "el tiempo promedio de espera es: ",self.avergwt
      print "el tiempo promedio de uso es: ",self.avergtt

      return self.n, self.sum, self.stb, self.avergwt, self.avergtt, self.cola_procesos

#Shortest Job First(SJF)
    def SJF(self, n, te, tcpu, f1, fcpu):
      cola_procesos = []
      self.n = int(n) #número de procesos
      self.te = float(te) #float(te) #tiempo de llegada
      self.tcpu = float(tcpu) #float(tcpu) #tiempo de uso del CPU
      self.func_llegada = f1
      self.func_cpu = fcpu
      avergwt=0
      avergtt=0

      for i in xrange(self.n):
        cola_procesos.append([]) #agregamos un objeto de tipo lista a la cola
        cola_procesos[i].append(i)

        if self.func_cpu == 'Constante':
          cola_procesos[i].append(self.tcpu)
        elif self.func_cpu == 'Uniforme':
          cola_procesos[i].append(np.random.randint(0, self.tcpu))
        elif self.func_cpu == 'Exponencial':
          cola_procesos[i].append(np.random.exponential(self.tcpu))
        elif self.func_cpu == 'Normal':
          cola_procesos[i].append(st.norm.cdf(self.tcpu))

        if self.func_llegada == 'Constante':
          cola_procesos[i].append(self.te)
        elif self.func_llegada == 'Uniforme':
          cola_procesos[i].append(np.random.randint(0, self.te))
        elif self.func_llegada == 'Exponencial':
          cola_procesos[i].append(np.random.exponential(self.te))
        elif self.func_llegada == 'Normal':
          cola_procesos[i].append(st.norm.cdf(self.te))

      self.cola_procesos.sort(key = lambda cola_procesos:cola_procesos[2])

      s=0
      s1=0
      self.sumdo=0
      self.stb=0
      ss=0
      print 'Nombre del proceso\t\t Tiempo de espera \t \tTiempo de rafaga'
      for i in xrange(self.n):
        print cola_procesos[i][0],'\t\t',cola_procesos[i][1],'\t\t',cola_procesos[i][2]
        self.cola_procesos[i].append(s) #wt
        s=round(s+self.cola_procesos[i][1],2)
        self.sum = round(self.cola_procesos[i][3]-self.cola_procesos[i][2])
        s1=round(s1+s-self.cola_procesos[i][1], 2)
        self.cola_procesos[i].append(s1) #tt
        self.stb=round(self.stb+cola_procesos[i][1], 2)
        ss=round(ss+self.cola_procesos[i][2], 2)

      self.avergwt=float(round(self.sum/self.n, 2))
      self.avergtt=float(round(self.stb/self.n, 2))
      print "\nel tiempo total de espera de los procesos es: ",self.sum
      print "el tiempo total  de uso del CPU es: ",self.stb
      print "el tiempo promedio de espera es: ",self.avergwt
      print "el tiempo promedio de uso es: ",self.avergtt

      return self.sum, self.stb, self.avergwt, self.avergtt, self.cola_procesos
