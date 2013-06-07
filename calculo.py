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
import numpy as np
import scipy.stats as st
import random as r

class Algoritmos(gtk.HBox):
    def RoundRobin(self, n, te, ts, fe, fs ,q):
      self.cola_procesos = []
      self.total_llegada = float(0.0)
      self.total_servicio=float(0.0)
      self.total_esperado=float(0.0)
      self.promedio_llegada=float(0.)
      self.promedio_servicio=float(0.0)
      self.promedio_de_espera=float(0.0)
      #random.seed(5000)
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
          self.cola_procesos[i].append(r.uniform(self.ts))
        elif self.func_servicio == 'Exponencial':
          self.cola_procesos[i].append(np.random.exponential(self.ts))
        elif self.func_servicio == 'Normal':
          self.cola_procesos[i].append(st.norm.cdf(self.ts))

        #tiempo de llegada   
        if self.func_llegada == 'Constante':
          self.cola_procesos[i].append(self.te)
        elif self.func_llegada == 'Uniforme':
          self.cola_procesos[i].append(r.uniform(0, self.te))
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
        self.total_llegada += round(self.cola_procesos[i][2], 2)
        self.total_esperado += round(self.cola_procesos[i][3], 2)

      self.promedio_llegada = round(self.total_llegada/self.n, 2)
      self.promedio_servicio = round(self.total_servicio/self.ncpu, 2)
      self.promedio_de_espera = round(self.total_esperado/self.n, 2)
      print 'Tiempo total de llegada: ',self.total_llegada
      print 'Tiempo total de proceso: ',self.total_servicio
      print 'Tiempo promedio de llegada: ',(self.promedio_llegada)
      print 'Tiempo promedio de proceso: ',(self.promedio_servicio)
      print 'Tiempo promedio esperado: ',(self.promedio_de_espera)

      return self.total_llegada, self.promedio_llegada, self.total_servicio, self.promedio_servicio, self.promedio_de_espera, self.cola_procesos

#First Come First Served(FCFS)
    def FCFS(self, n, te, tcpu, f1, f2):
      self.cola_procesos = []
      self.n = int(n) #número de procesos a ejecutar
      self.te = float(te) #tiempo de espera de llegada de los procesos.
      self.tcpu = float(tcpu) #tiempo de rafaga del CPU
      self.func_llegada = f1
      self.func_cpu = f2
      self.wt=float(0.0) #tiempo total de espera
      self.tpe  = float(0.0) #tiempo promedio de espera.
      self.teje = float(0.0) #tiempo total de ejecucion
      self.tpeje = float(0.0) #tiempo promedio de ejecucion.

      datos = open('FCFS.dat', 'w')

      for i in xrange(self.n):
        self.cola_procesos.append([]) #agregamos un objeto de tipo lista a la cola
        self.cola_procesos[i].append(i)

        if self.func_cpu == 'Constante':
          self.cola_procesos[i].append(self.tcpu)
        elif self.func_cpu == 'Uniforme':
          self.cola_procesos[i].append(r.uniform(0, self.tcpu))
        elif self.func_cpu == 'Exponencial':
          self.cola_procesos[i].append(np.random.exponential(self.tcpu))
        elif self.func_cpu == 'Normal':
          self.cola_procesos[i].append(st.norm.cdf(self.tcpu))

        if self.func_llegada == 'Constante':
          self.cola_procesos[i].append(self.te)
        elif self.func_llegada == 'Uniforme':
          self.cola_procesos[i].append(r.uniform(0, self.te))
        elif self.func_llegada == 'Exponencial':
          self.cola_procesos[i].append(np.random.exponential(self.te))
        elif self.func_llegada == 'Normal':
          self.cola_procesos[i].append(st.norm.cdf(self.te))

      self.cola_procesos[0][2]=self.cola_procesos[0][2]-self.cola_procesos[0][2]
      print 'Nombre del proceso\t\t Tiempo de espera \t \tTiempo de rafaga'
      for i in xrange(self.n):
        print self.cola_procesos[i][0],'\t\t',self.cola_procesos[i][2],'\t\t',self.cola_procesos[i][1]
        self.wt += round(self.cola_procesos[i][1]-self.cola_procesos[i][2], 2) #restamos al uso del CPU, el tiempo de llegada.
        self.teje += round(self.cola_procesos[i][1], 1)
        for j in xrange(3):
          data=str(self.cola_procesos[i][j])
          datos.write(' '+data)
        datos.write('\n')

      self.wt = self.wt-self.cola_procesos[self.n-1][1]
      self.wt = round(self.wt-self.cola_procesos[self.n-1][1], 2)
      self.tpe=round(self.wt/self.n, 2)
      self.tpeje= round(self.teje/self.n, 2)
      print "\nel tiempo total de espera de los procesos es: ",self.wt
      print "el tiempo total  de uso del CPU es: ",self.teje
      print "el tiempo promedio de espera es: ",self.tpe
      print "el tiempo promedio de uso es: ",self.tpeje
      datos.close()

      return self.teje, self.tpeje, self.wt, self.tpe, self.cola_procesos

#Shortest Job First(SJF)
    def SJF(self, n, te, tcpu, f1, fcpu):
      self.cola_procesos = []
      self.n = int(n) #número de procesos a ejecutar
      self.te = float(te) #tiempo de espera de llegada de los procesos.
      self.tcpu = float(tcpu) #tiempo de rafaga del CPU
      self.func_llegada = f1
      self.func_cpu = fcpu
      self.wt=float(0.0) #tiempo total de espera
      self.tpe  = float(0.0) #tiempo promedio de espera.
      self.teje = float(0.0) #tiempo total de ejecucion
      self.tpeje = float(0.0) #tiempo promedio de ejecucion.

      for i in xrange(self.n):
        self.cola_procesos.append([]) #agregamos un objeto de tipo lista a la cola
        self.cola_procesos[i].append(i)

        if self.func_cpu == 'Constante':
          self.cola_procesos[i].append(self.tcpu)
        elif self.func_cpu == 'Uniforme':
          self.cola_procesos[i].append(r.uniform(0, self.tcpu))
        elif self.func_cpu == 'Exponencial':
          self.cola_procesos[i].append(np.random.exponential(self.tcpu))
        elif self.func_cpu == 'Normal':
          self.cola_procesos[i].append(st.norm.cdf(self.tcpu))

        if self.func_llegada == 'Constante':
          self.cola_procesos[i].append(self.te)
        elif self.func_llegada == 'Uniforme':
          self.cola_procesos[i].append(r.uniform(0, self.te))
        elif self.func_llegada == 'Exponencial':
          self.cola_procesos[i].append(np.random.exponential(self.te))
        elif self.func_llegada == 'Normal':
          self.cola_procesos[i].append(st.norm.cdf(self.te))

      self.cola_procesos.sort(key = lambda cola_procesos:cola_procesos[1])

      self.cola_procesos[0][2]=self.cola_procesos[0][2]-self.cola_procesos[0][2]
      print 'Nombre del proceso\t\t Tiempo de espera \t \tTiempo de rafaga'
      for i in xrange(self.n):
        print self.cola_procesos[i][0],'\t\t',self.cola_procesos[i][2],'\t\t',self.cola_procesos[i][1]
        self.wt += round(self.cola_procesos[i][1]-self.cola_procesos[i][2], 2) #restamos al uso del CPU, el tiempo de llegada.
        self.teje += round(self.cola_procesos[i][1], 1)

      self.wt = round(self.wt-self.cola_procesos[self.n-1][1], 2)
      self.tpe=round(self.wt/self.n, 2)
      self.tpeje= round(self.teje/self.n, 2)
      print "\nel tiempo total de espera de los procesos es: ",self.wt
      print "el tiempo total  de uso del CPU es: ",self.teje
      print "el tiempo promedio de espera es: ",self.tpe
      print "el tiempo promedio de uso es: ",self.tpeje

      return self.teje, self.tpeje, self.wt, self.tpe, self.cola_procesos
