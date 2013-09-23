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

import numpy as np
import scipy.stats as st
import random as r
import math
from separar import Separar
from guardardatos import Guardar

guardar = Guardar()

class Algoritmos():
    """ Clase que permite calcular los diferentes algoritmos."""
    def Cola_Procesos(self, n, te, tcpu, tbcpu, tb, f1, f2, f3, f4):
      """ Función que mete en una cola el número de procesos.

      Esta función mete en una cola cada proceso y le asigna según la seleccion del usuario, un tiempo de llegada, de ejecución, tiempo de bloqueo de cpu y bloqueo de procesos."""
      self.cola_procesos = []
      self.n = int(n) #número de procesos a ejecutar
      self.func_llegada = f1
      self.func_cpu = f2
      self.func_bloqueocpu = f3
      self.func_bloqueo = f4
      self.te = te
      self.tcpu = tcpu
      self.tbcpu = tbcpu
      self.tb = tb
      separar = Separar()

      if self.func_llegada == 'Uniforme':
        self.te = separar.Separar(self.te)
      else:
        self.te = float(te)

      if self.func_cpu == 'Uniforme':
        self.tcpu = separar.Separar(self.tcpu)
      else:
        self.tcpu = float(tcpu)

      if self.func_bloqueocpu == 'Uniforme':
        self.tbcpu = separar.Separar(self.tbcpu)
      else:
        self.tbcpu = float(tbcpu)

      if self.func_bloqueo == 'Uniforme':
        self.tb = separar.Separar(self.tb)
      else:
        self.tb = float(tb)

      for i in xrange(self.n):
        self.cola_procesos.append([]) #agregamos un objeto de tipo lista a la cola
        self.cola_procesos[i].append(i+1)

        if self.func_cpu == 'Constante':
          self.cola_procesos[i].append(self.tcpu)
        elif self.func_cpu == 'Uniforme':
          self.cola_procesos[i].append(round(r.uniform(self.tcpu[0], self.tcpu[1]), 3))
        elif self.func_cpu == 'Exponencial':
          self.cola_procesos[i].append(round(np.random.exponential(self.tcpu), 3))
        elif self.func_cpu == 'Normal':
          self.cola_procesos[i].append(round(st.norm.cdf(self.tcpu), 3))

        if self.func_llegada == 'Constante':
          self.cola_procesos[i].append(self.te)
        elif self.func_llegada == 'Uniforme':
          self.cola_procesos[i].append(round(r.uniform(self.te[0], self.te[1]), 3))
        elif self.func_llegada == 'Exponencial':
          self.cola_procesos[i].append(round(np.random.exponential(self.te), 3))
        elif self.func_llegada == 'Normal':
          self.cola_procesos[i].append(round(st.norm.cdf(self.te), 3))

        if self.func_bloqueocpu == 'Constante':
          self.cola_procesos[i].append(self.tbcpu)
        elif self.func_bloqueocpu == 'Uniforme':
          self.cola_procesos[i].append(round(r.uniform(self.tbcpu[0], self.tbcpu[1]), 3))
        elif self.func_bloqueocpu == 'Exponencial':
          self.cola_procesos[i].append(round(np.random.exponential(self.tbcpu), 3))
        elif self.func_bloqueocpu == 'Normal':
          self.cola_procesos[i].append(round(st.norm.cdf(self.tbcpu), 3))

        if self.func_bloqueo == 'Constante':
          self.cola_procesos[i].append(self.tb)
        elif self.func_bloqueo == 'Uniforme':
          self.cola_procesos[i].append(round(r.uniform(self.tb[0], self.tb[1]), 3))
        elif self.func_bloqueo == 'Exponencial':
          self.cola_procesos[i].append(round(np.random.exponential(self.tb), 3))
        elif self.func_bloqueo == 'Normal':
          self.cola_procesos[i].append(round(st.norm.cdf(self.tb), 3))

      self.cola_procesos[0][2]=self.cola_procesos[0][2]-self.cola_procesos[0][2]

      return self.cola_procesos

#First Come First Served(FCFS)
    def FCFS(self, cola_procesos):
      """First Come First Served(FCFS).

      Función que permite hacer los calculos del algoritmo Primero en llegar, primero en ser servido, retorna los promedios de: tiempo de espera, rendimiento del CPu, promedio de ejecución."""
      self.cola_procesos = cola_procesos
      self.t_espera = []
      self.wt=float(0.0) #tiempo total de espera
      self.tpe  = float(0.0) #tiempo promedio de espera.
      self.teje = float(0.0) #tiempo total de ejecucion
      self.tpeje = float(0.0) #tiempo promedio de ejecucion.
      self.wt1=float(0.0)
      self.usocpu = float(0.0)
      self.n = len(self.cola_procesos)

      for i in xrange(self.n):
        self.t_espera.append([])
        self.t_espera[i].append(i)

      self.t_espera[0].append(0)
      for i in xrange(self.n):
        for j in xrange(1, self.n):
          self.t_espera[j].append(round(self.t_espera[i][1]-self.cola_procesos[j][2]+self.cola_procesos[i][3]))
        if self.cola_procesos[i][1]-self.cola_procesos[i][3]>0:
          if (self.cola_procesos[i][1]-self.cola_procesos[i][3])/self.cola_procesos[i][3]<1:
            self.t_espera[i][1]= self.t_espera[i][1]+self.cola_procesos[i][4]
          else:
            self.t_espera[i][1]= self.t_espera[i][1]+math.trunc((self.cola_procesos[i][1]-self.cola_procesos[i][3])/self.cola_procesos[i][3])*self.cola_procesos[i][4]+self.cola_procesos[i][4]
        if self.t_espera[i][1]<0:
          self.wt1 += self.t_espera[i][1]*-1
          self.t_espera[i][1]=self.t_espera[i][1]*-1*0
        else:
          self.wt += self.t_espera[i][1]
        self.teje += round(self.cola_procesos[i][1], 4)

      guardar.Guardar(self.t_espera, self.cola_procesos, 0)

      self.tpe=round(self.wt/self.n, 4)
      if self.wt1+self.wt==0:
        self.usocpu = round(1.0-self.wt1, 4)
      else:
        self.usocpu = round(1.0-self.wt1/(self.wt1+self.wt), 4)
      self.tpeje= round(self.teje/self.n, 4)

      return self.usocpu, self.tpeje, self.tpe, self.t_espera

#Shortest Job First(SJF)
    def SJF(self, cola_procesos):
      """Shortest Job First(SJF).

      Función que permite calcular el algoritmo del menor tiempo, retorna:
      Promedio del tiempo de espera, Rendimiento del CPU y promedio del uso del CPU."""
      self.cola_procesos = cola_procesos
      self.t_espera = []
      self.n = len(self.cola_procesos) #Almacena los tiempo de espera de cada proceso.
      self.wt=float(0.0) #tiempo total de espera
      self.tpe  = float(0.0) #tiempo promedio de espera.
      self.teje = float(0.0) #tiempo total de ejecucion
      self.tpeje = float(0.0) #tiempo promedio de ejecucion.
      self.wt1 = float(0.0)
      self.usocpu = float(0.0)

      for i in xrange(self.n):
        self.t_espera.append([])
        self.t_espera[i].append(i)

      self.cola_procesos.sort(key = lambda cola_procesos:cola_procesos[1])
      self.t_espera[0].append(0)
      for i in xrange(self.n):
        for j in xrange(1, self.n):
          self.t_espera[j].append(round(self.t_espera[i][1]-self.cola_procesos[j][2]+self.cola_procesos[i][3]))
        if self.cola_procesos[i][1]-self.cola_procesos[i][3]>0:
          if (self.cola_procesos[i][1]-self.cola_procesos[i][3])/self.cola_procesos[i][3]<1:
            self.t_espera[i][1]= self.t_espera[i][1]+self.cola_procesos[i][4]
          else:
            self.t_espera[i][1]= self.t_espera[i][1]+math.trunc((self.cola_procesos[i][1]-self.cola_procesos[i][3])/self.cola_procesos[i][3])*self.cola_procesos[i][4]+self.cola_procesos[i][4]
        if self.t_espera[i][1]<0:
          self.wt1 += self.t_espera[i][1]*-1
          self.t_espera[i][1]=self.t_espera[i][1]*-1*0
        else:
          self.wt += self.t_espera[i][1]
        self.teje += round(self.cola_procesos[i][1], 4)

      self.t_espera.sort(key = lambda t_espera:t_espera[1])
      guardar.Guardar(self.t_espera, self.cola_procesos, 1)

      self.tpe=round(self.wt/self.n, 4)
      if self.wt1+self.wt==0:
        self.usocpu = round(1.0-self.wt1, 4)
      else:
        self.usocpu = round(1.0-self.wt1/(self.wt1+self.wt), 4)
      self.tpeje= round(self.teje/self.n, 4)

      return self.usocpu, self.tpeje, self.tpe, self.t_espera, self.cola_procesos

#Round Robin
    def RoundRobin(self, cola_procesos, q):
      self.cola_procesos = cola_procesos
      self.ejecucion = []
      self.esperado = []
      self.total_llegada = float(0.0)
      self.total_servicio=float(0.0)
      self.total_esperado=float(0.0)
      self.promedio_llegada=float(0.0)
      self.promedio_servicio=float(0.0)
      self.promedio_de_espera=float(0.0)
      self.n = len(self.cola_procesos)
      self.aux = 0
      self.q = float(q)
      self.ncpu = 0
      self.tiempo_parcial = 0
      self.usocpu = float(0.0)
      self.wt1 = float(0.0)
      self.llegaron=0
      self.llegando=0

      for i in xrange(self.n-1):
        if self.cola_procesos[i][1]-self.cola_procesos[i+1][2]<0:
          self.wt1 += (self.cola_procesos[i][1]-self.cola_procesos[i+1][2])*(-1)
               
      for i in xrange(self.n):
        self.esperado.append([])
        self.esperado[i].append(i)
        self.esperado[i].append(0)

      #Llegadas
      for i in xrange(self.n-1):
        self.ejecucion.append(self.cola_procesos[i][1])
        self.llego=0
        self.aux=0
        while (self.aux<i):
          self.aux=0
          for j in xrange(len(self.ejecucion)):
            if(self.ejecucion[j]>0):
              if (self.ejecucion[j]-self.q>0):
                self.tiempo_parcial = self.q
              else:
                self.tiempo_parcial = self.ejecucion[j]
              if(self.cola_procesos[i+1][2]-self.tiempo_parcial>0):
                self.cola_procesos[i+1][2]-=self.tiempo_parcial
              else:
                self.llego = 1
              for k in xrange(len(self.ejecucion)):
                if ((k != j)and(k!=0)):
                  if (self.ejecucion[k]>0):
                    self.esperado[k][1]+=self.tiempo_parcial 
              self.ejecucion[j]-=self.tiempo_parcial 
              self.total_servicio+=self.tiempo_parcial
              self.ncpu+=1
            else:
              self.aux+=1
            if (self.llego ==1):
              self.aux=i+1
      
      self.ejecucion.append(self.cola_procesos[self.n-1][1])
      self.aux=0
      while (self.aux<len(self.ejecucion)):
        self.aux=0
        for j in xrange(len(self.ejecucion)):
          if(self.ejecucion[j]>0):
            if (self.ejecucion[j]-self.q>0):
              self.tiempo_parcial = self.q
            else:
              self.tiempo_parcial = self.ejecucion[j]
            for k in xrange(len(self.ejecucion)):
              if ((k != j)and(k!=0)):
                if (self.ejecucion[k]>0):
                  self.esperado[k][1]+=self.tiempo_parcial 
            self.ejecucion[j]-=self.tiempo_parcial 
            self.total_servicio+=self.tiempo_parcial
            self.ncpu+=1
          else:
            self.aux+=1
          
      for i in xrange(self.n):
        self.total_llegada += round(self.cola_procesos[i][2], 4)
        self.total_esperado += round(self.esperado[i][1], 4)

      guardar.Guardar(self.esperado, self.cola_procesos, 3)
      self.promedio_llegada = round(self.total_llegada/self.n, 4)
      self.promedio_servicio = round(self.total_servicio/self.ncpu, 4)
      self.promedio_de_espera = round(self.total_esperado/self.n, 4)
      self.usocpu = round(1 - self.wt1/(self.wt1+self.total_servicio), 4)

      #print "tiempo de espera"
      #for i in xrange(self.n):
      #  print "n: ",self.esperado[i][0]
      #  print "espera: ",self.esperado[i][1]
      print "Round Robin"
      print "Tiempo total de proceso: ",self.total_servicio
      print "Tiempo promedio de proceso: ",(self.promedio_servicio)
      print "Tiempo total de espera: ",(self.total_esperado)
      print "Tiempo promedio esperado: ",(self.promedio_de_espera)
      print "Uso de cpu: ",self.usocpu

      return self.usocpu, self.promedio_servicio, self.promedio_de_espera, self.esperado, self.cola_procesos

#Preemptive Shortest Job First(PSJF)
    def PSJF(self, cola_procesos):
      self.cola_procesos = cola_procesos
      self.procesos_actuales = []
      self.espera_procesos_actuales = []
      self.n = len(self.cola_procesos)
      self.wt=float(0.0) #tiempo total de espera
      self.tpe  = float(0.0) #tiempo promedio de espera.
      self.teje = float(0.0) #tiempo total de ejecucion
      self.tpeje = float(0.0) #tiempo promedio de ejecucion.
      self.usocpu = float(0.0)
      self.wt1 = float(0.0)
      self.aux = 0
      self.actual = 0	
      self.pos = 0		
      self.tam=0
      self.tparcial = 0
      self.promedio_llegada = 0
      self.total_llegada = 0

      for i in xrange(self.n-1):
        if self.cola_procesos[i][1]-self.cola_procesos[i+1][2]<0:
          self.wt1 += (self.cola_procesos[i][1]-self.cola_procesos[i+1][2])*(-1)

      for i in xrange(self.n):
        self.espera_procesos_actuales.append([])
        self.espera_procesos_actuales[i].append(i)
        self.espera_procesos_actuales[i].append(0)
          
      #Simulando las llegadas
      for i in xrange(self.n):
        if i != 0:
          self.procesos_actuales.append(self.cola_procesos[i][1])
          #self.espera_procesos_actuales.append(0)
          self.tam += 1
          self.tparcial = self.procesos_actuales[self.actual]
          self.procesos_actuales[self.actual]-= self.cola_procesos[i][2]
          for k in xrange(self.tam):
            if(self.procesos_actuales[k]>0):
              self.espera_procesos_actuales[k][1] += self.cola_procesos[i][2]
          if self.procesos_actuales [self.actual] > 0:
            self.teje += self.cola_procesos[i][2]
            if self.cola_procesos[i][1] < self.procesos_actuales[self.actual]:  
              self.actual = i
          else:
            self.teje += self.tparcial
            self.pos= self.actual +1
            for j in xrange(self.tam):
              if (self.procesos_actuales[j] < self.procesos_actuales[self.pos]) and (self.procesos_actuales[j] > 0):
                self.pos = j
            self.actual=self.pos    
        else:
          self.procesos_actuales.append(self.cola_procesos[0][1])
          #self.espera_procesos_actuales.append(0)
	  self.tam += 1

      self.procesos_actuales.sort(key = lambda procesos_actuales:procesos_actuales)  
      self.actual = 0
      for h in xrange(self.tam):
        if (self.procesos_actuales[h]>0):
          self.actual = h
          break

      #Ahora, el menor tiempo primero
      for h in xrange(self.actual,self.tam):
        self.teje += self.procesos_actuales[h]
        self.procesos_actuales[h] -= self.procesos_actuales[h]
        for l in xrange(self.tam):
            if(self.procesos_actuales[l]>0):
              self.espera_procesos_actuales[l][1] += self.procesos_actuales[h]
  
      for h in xrange(self.tam):
        self.wt += self.espera_procesos_actuales[h][1]

      for i in xrange(self.n):
        self.total_llegada += round(self.cola_procesos[i][2], 4)

      guardar.Guardar(self.espera_procesos_actuales, self.cola_procesos, 2)
      
      self.tpe=round(self.wt/self.n, 4)
      self.tpeje= round(self.teje/self.n, 4)
      self.promedio_llegada = round(self.total_llegada/self.n, 4)
      self.usocpu = round(1 - self.wt1/(self.wt1+self.teje), 4)
      print "Preemptive Shortest Job First"
      print "Tiempo total de espera de los procesos es: ",self.wt
      print "Tiempo total de uso del CPU es: ",self.teje
      print "Tiempo promedio de espera es: ",self.tpe
      print "Tiempo promedio de uso del CPU es: ",self.tpeje

      return self.usocpu, self.tpeje, self.tpe, self.espera_procesos_actuales, self.cola_procesos

