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
from rafaga import Rafaga

guardar = Guardar()

class Algoritmos():
    """ Clase que permite calcular los diferentes algoritmos."""
    def Cola_Procesos(self, n, te, tcpu, f1, f2):
      """ Función que mete en una cola el número de procesos.

      Esta función mete en una cola cada proceso y le asigna según la seleccion del usuario, un tiempo de llegada, de ejecución."""
      self.cola_procesos = []
      self.n = int(n) #número de procesos a ejecutar
      self.func_llegada = f1 #tiempo de llegada entre procesos
      self.func_cpu = f2 #tiempo de procesos en cpu
      self.te = te
      self.tcpu = tcpu
      separar = Separar()

      if self.func_llegada == 'Uniforme':
        self.te = separar.Separar(self.te)
      else:
        self.te = float(te)

      if self.func_cpu == 'Uniforme':
        self.tcpu = separar.Separar(self.tcpu)
      else:
        self.tcpu = float(tcpu)

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

      self.cola_procesos[0][2]=self.cola_procesos[0][2]-self.cola_procesos[0][2]

      return self.cola_procesos

    #Obtener rafaga y tiempo de bloqueo
    def rafaga_bloqueo(self, tbcpu, tb, f3, f4):
      """ Función que retorna rafaga y tiempo de bloqueo"""
      self.tbloqueocpu=float(0.0)
      self.tbloqueo=float(0.0)
      self.func_bloqueocpu = f3 #rafaga de cpu
      self.func_bloqueo = f4 #bloqueo de cpu
      self.tbcpu = tbcpu
      self.tb = tb
      separar = Separar()

      if self.func_bloqueocpu == 'Uniforme':
        self.tbcpu = separar.Separar(self.tbcpu)
      else:
        self.tbcpu = float(tbcpu)

      if self.func_bloqueo == 'Uniforme':
        self.tb = separar.Separar(self.tb)
      else:
        self.tb = float(tb)

      if self.func_bloqueocpu == 'Constante':
        self.tbloqueocpu=self.tbcpu
      elif self.func_bloqueocpu == 'Uniforme':
        self.tbloqueocpu=round(r.uniform(self.tbcpu[0], self.tbcpu[1]), 3)
      elif self.func_bloqueocpu == 'Exponencial':
        self.tbloqueocpu=round(np.random.exponential(self.tbcpu), 3)
      elif self.func_bloqueocpu == 'Normal':
        self.tbloqueocpu=round(st.norm.cdf(self.tbcpu), 3)

      if self.func_bloqueo == 'Constante':
        self.tbloqueo=self.tb
      elif self.func_bloqueo == 'Uniforme':
        self.tbloqueo=round(r.uniform(self.tb[0], self.tb[1]), 3)
      elif self.func_bloqueo == 'Exponencial':
        self.tbloqueo=round(np.random.exponential(self.tb), 3)
      elif self.func_bloqueo == 'Normal':
        self.tbloqueo=round(st.norm.cdf(self.tb), 3)

      return self.tbloqueocpu, self.tbloqueo

#First Come First Served(FCFS)
    def FCFS(self, cola_procesos, tbcpu, tb, f3, f4):
      """First Come First Served(FCFS).

      Función que permite hacer los calculos del algoritmo Primero en llegar, primero en ser servido, retorna los promedios de: tiempo de espera, rendimiento del CPu, promedio de ejecución."""
      self.cola_procesos = cola_procesos
      self.t_espera = []
      self.p_bloqueados = []
      self.p_ejecucion= []
      self.tllegada= float(0.0)
      self.wt=float(0.0) #tiempo total de espera
      self.tpe  = float(0.0) #tiempo promedio de espera.
      self.teje = float(0.0) #tiempo total de ejecucion
      self.tpeje = float(0.0) #tiempo promedio de ejecucion.
      self.wt1=float(0.0)
      self.usocpu = float(0.0)
      self.n = len(self.cola_procesos)
      tbcpu= tbcpu
      tb = tb
      f3 = f3
      f4 = f4
      tproc=float(0.0)
      t=int(0)
      tejecutado=float(0.0)

      for i in xrange(self.n):
        self.t_espera.append([])
        self.p_bloqueados.append([])
        self.p_ejecucion.append([])
        self.t_espera[i].append(i)
        self.t_espera[i].append(0)
        self.p_bloqueados[i].append(i)
        self.p_bloqueados[i].append(0)
        self.p_ejecucion[i].append(i)
        self.p_ejecucion[i].append(self.cola_procesos[i][1])
        tproc= tproc+self.p_ejecucion[i][1]

      self.min=float(self.t_espera[0][1])
      self.max=float(self.t_espera[0][1])
      while tproc!=0:
        tproc=0.0
        for j in xrange(self.n):
          print "dentro del for ", j
          self.rafagabloqueo = self.rafaga_bloqueo(tbcpu, tb, f3, f4) # rafaga de bloqueo del proceso anterior
          if self.p_ejecucion[j][1]-self.rafagabloqueo[0]>0:
            print "proceso ",i," a lista de bloqueados"
            self.t_espera[j][1]=self.t_espera[j][1]+self.rafagabloqueo[1]
            self.p_bloqueados[j][1]=self.p_bloqueados[j][1]+self.rafagabloqueo[1]
            tejecutado=self.rafagabloqueo[0]
          elif self.p_ejecucion[j][1]-self.rafagabloqueo[0]==0:
            print "las rafagas son iguales a la jecucion del proceso ", j
            self.t_espera[j][1]=self.t_espera[j][1]
            tejecutado=self.rafagabloqueo[0]
            self.p_bloqueados[j][1]=self.p_bloqueados[j][1]
          elif self.p_ejecucion[j][1]-self.rafagabloqueo[0]<0:
            print "la rafagas son menores al proceso ", j
            self.t_espera[j][1]=self.t_espera[j][1]
            tejecutado=self.p_ejecucion[j][1]
            self.p_bloqueados[j][1]=self.p_bloqueados[j][1]

          if self.n>1:
            for i in xrange(1, self.n):
              if self.tllegada-self.p_bloqueados[j][1]>0:
                #if self.p_ejecucion[i][1]-self.rafagabloqueo[0]>0:
                self.t_espera[j][1]=self.t_espera[j][1]-self.cola_procesos[i][2]+self.p_ejecucion[i][1]-self.p_bloqueados[j][1]
              self.cola_procesos[i][2]=self.cola_procesos[i][2]-tejecutado
              self.tllegada=self.tllegada+self.cola_procesos[i][2]

          self.p_ejecucion[j][1]=self.p_ejecucion[j][1]-tejecutado

          if self.cola_procesos[j][2]<0:
            self.cola_procesos[j][2]=self.cola_procesos[j][2]-self.cola_procesos[j][2]

          t=t+1
          print"el valor de t = ", t
          tproc=tproc+self.p_ejecucion[j][1]

      for i in xrange(self.n):
        self.teje=self.teje+self.cola_procesos[i][1]
        if self.t_espera[i][1]>=0:
          self.wt=self.wt+self.t_espera[i][1]
        else:
          self.wt1=self.wt1+self.t_espera[i][1]*-1
          self.t_espera[i][1]=self.t_espera[i][1]*-1*0
        if self.min>self.t_espera[i][1]:
          self.min=self.t_espera[i][1]
        if self.max<self.t_espera[i][1]:
          self.max=self.t_espera[i][1]
        print " t espera ", i," es = ", self.t_espera[i][1]
      print "el t de espera minimo es = ", self.min
      print "el t de espera maximo es = ", self.max

      guardar.Guardar(self.t_espera, self.cola_procesos, 0)
      print " wt ", self.wt

      self.tpe=round(self.wt/self.n, 4)
      if self.wt1+self.wt==0:
        self.usocpu = round(1.0-self.wt1, 4)
      else:
        self.usocpu = round(1.0-self.wt1/(self.wt1+self.wt), 4)
      self.tpeje= round(self.teje/t, 4)

      return self.usocpu, self.tpeje, self.tpe, self.t_espera, self.min, self.max

#Shortest Job First(SJF)
    def SJF(self, cola_procesos, tbcpu, tb, f3, f4):
      """Shortest Job First(SJF).

      Función que permite calcular el algoritmo del menor tiempo, retorna:
      Promedio del tiempo de espera, Rendimiento del CPU y promedio del uso del CPU."""
      self.cola_procesos = cola_procesos
      self.t_espera = []
      self.p_bloqueados = []
      self.p_ejecucion= []
      self.tllegada= float(0.0)
      self.wt=float(0.0) #tiempo total de espera
      self.tpe  = float(0.0) #tiempo promedio de espera.
      self.teje = float(0.0) #tiempo total de ejecucion
      self.tpeje = float(0.0) #tiempo promedio de ejecucion.
      self.wt1=float(0.0)
      self.usocpu = float(0.0)
      self.n = len(self.cola_procesos)
      tbcpu= tbcpu
      tb = tb
      f3 = f3
      f4 = f4
      tproc=float(0.0)
      t=int(0)
      tejecutado=float(0.0)

      for i in xrange(self.n):
        self.t_espera.append([])
        self.p_bloqueados.append([])
        self.p_ejecucion.append([])
        self.t_espera[i].append(i)
        self.t_espera[i].append(0)
        self.p_bloqueados[i].append(i)
        self.p_bloqueados[i].append(0)
        self.p_ejecucion[i].append(i)
        self.p_ejecucion[i].append(self.cola_procesos[i][1])
        tproc= tproc+self.p_ejecucion[i][1]

      self.cola_procesos.sort(key = lambda cola_procesos:cola_procesos[1])
      self.p_ejecucion.sort(key = lambda p_ejecucion:p_ejecucion[1])
      self.min=float(self.t_espera[0][1])
      self.max=float(self.t_espera[0][1])
      while tproc!=0:
        tproc=0.0
        self.p_ejecucion.sort(key = lambda p_ejecucion:p_ejecucion[1])
        for j in xrange(self.n):
          print "dentro del for ", j
          self.rafagabloqueo = self.rafaga_bloqueo(tbcpu, tb, f3, f4) # rafaga de bloqueo del proceso anterior
          if self.p_ejecucion[j][1]-self.rafagabloqueo[0]>0:
            print "proceso ",i," a lista de bloqueados"
            self.t_espera[j][1]=self.t_espera[j][1]+self.rafagabloqueo[1]
            self.p_bloqueados[j][1]=self.p_bloqueados[j][1]+self.rafagabloqueo[1]
            tejecutado=self.rafagabloqueo[0]
          elif self.p_ejecucion[j][1]-self.rafagabloqueo[0]==0:
            print "las rafagas son iguales a la jecucion del proceso ", j
            self.t_espera[j][1]=self.t_espera[j][1]
            tejecutado=self.rafagabloqueo[0]
          elif self.p_ejecucion[j][1]-self.rafagabloqueo[0]<0:
            print "la rafagas son menores al proceso ", j
            self.t_espera[j][1]=self.t_espera[j][1]
            tejecutado=self.p_ejecucion[j][1]

          self.p_ejecucion.sort(key = lambda p_ejecucion:p_ejecucion[1])
          if self.n>1:
            for i in xrange(1, self.n):
              if self.tllegada-self.p_bloqueados[j][1]>0:
                if self.p_ejecucion[i][1]>self.p_ejecucion[j][1]:
                  self.p_ejecucion[i][1]=self.p_ejecucion[o][1]-tejecutado
                  self.t_espera[j][1]=self.t_espera[j][1]-self.cola_procesos[i][2]+self.p_ejecucion[i][1]-self.p_bloqueados[j][1]
              self.cola_procesos[i][2]=self.cola_procesos[i][2]-tejecutado
              self.tllegada=self.tllegada+self.cola_procesos[i][2]

          self.p_ejecucion[j][1]=self.p_ejecucion[j][1]-tejecutado
          self.p_ejecucion.sort(key = lambda p_ejecucion:p_ejecucion[1])

          if self.cola_procesos[j][2]<0:
            self.cola_procesos[j][2]=self.cola_procesos[j][2]-self.cola_procesos[j][2]

          t=t+1
          print"el valor de t = ", t
          tproc=tproc+self.p_ejecucion[j][1]

      for i in xrange(self.n):
        self.teje=self.teje+self.cola_procesos[i][1]
        if self.t_espera[i][1]>=0:
          self.wt=self.wt+self.t_espera[i][1]
        else:
          self.wt1=self.wt1+self.t_espera[i][1]*-1
          self.t_espera[i][1]=self.t_espera[i][1]*-1*0
        if self.min>self.t_espera[i][1]:
          self.min=self.t_espera[i][1]
        if self.max<self.t_espera[i][1]:
          self.max=self.t_espera[i][1]
        print " t espera ", i," es = ", self.t_espera[i][1]
      print "el t de espera minimo es = ", self.min
      print "el t de espera maximo es = ", self.max

      guardar.Guardar(self.t_espera, self.cola_procesos, 0)
      print " wt ", self.wt

      self.tpe=round(self.wt/self.n, 4)
      if self.wt1+self.wt==0:
        self.usocpu = round(1.0-self.wt1, 4)
      else:
        self.usocpu = round(1.0-self.wt1/(self.wt1+self.wt), 4)
      self.tpeje= round(self.teje/t, 4)

      return self.usocpu, self.tpeje, self.tpe, self.t_espera, self.min, self.max

#Round Robin
    def RoundRobin(self, cola_procesos, q,tbcpu, tb, f3, f4):
      self.cola_procesos = cola_procesos
      self.ejecucion = []
      self.esperado = []
      self.total_servicio=float(0.0)
      self.total_esperado=float(0.0)
      self.promedio_llegada=float(0.0)
      self.promedio_servicio=float(0.0)
      self.promedio_de_espera=float(0.0)
      self.n = len(self.cola_procesos)
      self.aux = 0
      self.q = float(q)
      self.ncpu = 0
      self.usocpu = float(0.0)
      self.rafaga = []
      self.tbcpu = tbcpu
      self.tb = tb
      self.f3 = f3
      self.f4 = f4
      self.nq = 0
      rafagacpu = Rafaga()
                                
      for i in xrange(self.n):
        self.esperado.append([])
        self.esperado[i].append(i)
        self.esperado[i].append(0)

      #Llegadas
      self.rafaga = rafagacpu.rafaga_bloqueo(self.tbcpu,self.tb,self.f3,self.f4)
      self.ncpu +=1
      #self.quantum = self.q
      #self.nq +=1
      self.iterador = 0
      for i in xrange(self.n-1):
        self.ejecucion.append(self.cola_procesos[i][1])
        self.iterador = i
        self.llego=0
        self.quantum=self.q
        self.nq +=1
        while(self.llego == 0):
          self.rafaga[0] -= 1
          self.quantum -= 1
          self.cola_procesos[i+1][2] -= 1
          #Espera
          for j in xrange(i):
            if (self.ejecucion[j]>0)and(j!=i):
              self.esperado[j][1] +=1
          if (self.ejecucion[self.iterador]<=0):
            self.iterador = rafagacpu.siguiente_turno(self.ejecucion,self.iterador)
          else:
             self.ejecucion[self.iterador]-=1
          if(self.rafaga[0]<=0):
            self.cola_procesos[i+1][2]-= self.rafaga[1]
            #Espera
            for j in xrange(i):
              if (self.ejecucion[j]>0)and(j!=i):
                self.esperado[j][1] +=self.rafaga[1]
            self.rafaga = rafagacpu.rafaga_bloqueo(self.tbcpu,self.tb,self.f3,self.f4)
            self.ncpu += 1
          if(self.cola_procesos[i+1][2]<=0)and(self.quantum<=0):
            self.llego = 1
          if(self.quantum<=0):
            self.quantum = self.q
            self.nq += 1
            self.iterador = rafagacpu.siguiente_turno(self.ejecucion,self.iterador)
      """
      print"TIEMPO DE ESPERA PARCIAL" 
      for i in xrange(self.n-1):
        print "Proceso:",i
        print "Tiempo restante de ejecucion:",self.ejecucion[i]
        print "Tiempo de espera parcial:",self.esperado[i][1]"""

      self.ejecucion.append(self.cola_procesos[self.n-1][1])
      #Luego de que llegaron todos
      self.rafaga = rafagacpu.rafaga_bloqueo(self.tbcpu,self.tb,self.f3,self.f4)
      self.ncpu +=1
      self.quantum = self.q
      self.nq += 1
      self.iterador = self.n-1
      self.aux = 0
      while(self.aux < self.n):
        self.rafaga[0] -= 1
        self.quantum -= 1
        #Espera
        for j in xrange(self.n):
          if (self.ejecucion[j]>0)and(j!=self.iterador):
            self.esperado[j][1] += 1
        if (self.ejecucion[self.iterador]<=0):
          self.iterador = rafagacpu.siguiente_turno(self.ejecucion,self.iterador)
          self.aux+=1
        else:
           self.ejecucion[self.iterador]-=1
        if(self.rafaga[0]<=0):
          #Espera
          for j in xrange(self.n):
            if (self.ejecucion[j]>0)and(j!=self.iterador):
              self.esperado[j][1] +=self.rafaga[1]
          self	.rafaga = rafagacpu.rafaga_bloqueo(self.tbcpu,self.tb,self.f3,self.f4)
          self.ncpu += 1
        if(self.quantum<=0):
          self.quantum = self.q
          self.nq+=1
          self.iterador = rafagacpu.siguiente_turno(self.ejecucion,self.iterador)
      """ 
      print"TIEMPO DE ESPERA TOTAL"
      for i in xrange(self.n):
        print "Proceso:",i
        print "Tiempo restante de ejecucion:",self.ejecucion[i]
        print "Tiempo de espera total:",self.esperado[i][1]"""

      #Calculos finales          
      for i in xrange(self.n):
        self.total_servicio += round(self.cola_procesos[i][1], 4)
        self.total_esperado += round(self.esperado[i][1], 4)

      guardar.Guardar(self.esperado, self.cola_procesos, 3)
      print"nq",self.nq
      self.promedio_servicio = round(self.total_servicio/self.nq, 4)
      self.promedio_de_espera = round(self.total_esperado/self.n, 4)
      self.usocpu = round(1 - self.total_esperado/(self.total_esperado+self.total_servicio), 4)
      
      self.min=float(self.esperado[0][1])
      self.max=float(self.esperado[0][1])	
      for i in xrange(self.n):
        if self.min>self.esperado[i][1]:
          self.min=self.esperado[i][1]
        if self.max<self.esperado[i][1]:
          self.max=self.esperado[i][1]   

      print"ROUND ROBIN"
      print"Uso de cpu: ",self.usocpu
      print"Tiempo promedio de servicio: ",self.promedio_servicio
      print"Tiempo promedio de espera: ",self.promedio_de_espera
      
      return self.usocpu, self.promedio_servicio, self.promedio_de_espera, self.esperado, self.min, self.max

#Preemptive Shortest Job First(PSJF)
    def PSJF(self, cola_procesos,tbcpu, tb, f3, f4):
      self.cola_procesos = cola_procesos
      self.ejecucion = []
      self.esperado = []
      self.n = len(self.cola_procesos)
      self.usocpu = float(0.0)
      self.total_servicio=0
      self.total_esperado=0
      self.promedio_dservicio=0
      self.promedio_de_espera=0
      self.tbcpu=tbcpu
      self.tb=tb
      self.f3=f3
      self.f4=f4
      self.ncpu =0
      self.iterador=0
      self.lledo =0
      self.inicio =0
      self.rafaga =[]
      rafagacpu = Rafaga()

      for i in xrange(self.n):
        self.esperado.append([])
        self.esperado[i].append(i)
        self.esperado[i].append(0)

      #Llegadas
      self.rafaga = rafagacpu.rafaga_bloqueo(self.tbcpu,self.tb,self.f3,self.f4)
      self.ncpu +=1
      self.iterador = 0
      for i in xrange(self.n-1):
        self.ejecucion.append(self.cola_procesos[i][1])
        if(self.ejecucion[i]<self.ejecucion[self.iterador]):
          self.iterador = i
        self.llego=0
        while(self.llego == 0):
          self.rafaga[0] -= 1
          self.cola_procesos[i+1][2] -= 1
          #Espera 1
          for j in xrange(i):
            if (self.ejecucion[j]>0)and(j!=i):
              self.esperado[j][1] +=1
          if (self.ejecucion[self.iterador]<=0):
            self.iterador = rafagacpu.siguiente_turno(self.ejecucion,self.iterador)
          else:
             self.ejecucion[self.iterador]-=1
          if(self.rafaga[0]<=0):
            self.cola_procesos[i+1][2]-= self.rafaga[1]
            #Espera tiempo de bloqueo
            for j in xrange(i):
              if (self.ejecucion[j]>0)and(j!=i):
                self.esperado[j][1] +=self.rafaga[1]
                self.cola_procesos[i+1][2]-= self.rafaga[1]
            self.rafaga = rafagacpu.rafaga_bloqueo(self.tbcpu,self.tb,self.f3,self.f4)
            self.ncpu += 1
          if(self.cola_procesos[i+1][2]<=0):
            self.llego = 1
      self.ejecucion.append(self.cola_procesos[self.n-1][1])
      #Fin llegadas

      """
      print"TIEMPO DE ESPERA PARCIAL" 
      for i in xrange(self.n-1):
        print "Proceso:",i
        print "Tiempo restante de ejecucion:",self.ejecucion[i]
        print "Tiempo de espera parcial:",self.esperado[i][1]
      """
      
      self.ejecucion.sort(key = lambda ejecucion:ejecucion)  
      self.iterador = 0
      for h in xrange(self.n):
        if (self.ejecucion[h]>0):
          self.inicio = h
          break

      #Despues que todos llegaron
      self.rafaga = rafagacpu.rafaga_bloqueo(self.tbcpu,self.tb,self.f3,self.f4)
      self.ncpu +=1
      for i in xrange(self.inicio,self.n):
        self.listo=0
        while(self.listo == 0):
          self.rafaga[0] -= 1
          #Espera 1
          for j in xrange(self.inicio,self.n):
            if (self.ejecucion[j]>0)and(j!=i):
              self.esperado[j][1] +=1
          if (self.ejecucion[i]<=0):
            self.listo = 1
          else:
             self.ejecucion[i]-=1
          if(self.rafaga[0]<=0):
            #Espera tiempo de bloqueo
            for j in xrange(self.inicio,self.n):
              if (self.ejecucion[j]>0)and(j!=i):
                self.esperado[j][1] +=self.rafaga[1]
            self.rafaga = rafagacpu.rafaga_bloqueo(self.tbcpu,self.tb,self.f3,self.f4)
            self.ncpu += 1
      """    
      print"TIEMPO DE ESPERA TOTAL"
      for i in xrange(self.n):
        print "Proceso:",i
        print "Tiempo restante de ejecucion:",self.ejecucion[i]
        print "Tiempo de espera total:",self.esperado[i][1]
      """
      guardar.Guardar(self.esperado, self.cola_procesos, 2)

      #Calculos finales          
      for i in xrange(self.n):
        self.total_servicio += round(self.cola_procesos[i][1], 4)
        self.total_esperado += round(self.esperado[i][1], 4)
      
      self.promedio_servicio = round(self.total_servicio/self.ncpu, 4)
      self.promedio_de_espera = round(self.total_esperado/self.n, 4)
      self.usocpu = round(1 - self.total_esperado/(self.total_esperado+self.total_servicio), 4)
      
      self.min=float(self.esperado[0][1])
      self.max=float(self.esperado[0][1])
      for i in xrange(self.n):
        if self.min>self.esperado[i][1]:
          self.min=self.esperado[i][1]
        if self.max<self.esperado[i][1]:
          self.max=self.esperado[i][1]     

      print"PREEMPTIVE SHORTEST JOB FIRST"
      print"Uso de cpu: ",self.usocpu
      print"Tiempo promedio de servicio: ",self.promedio_servicio
      print"Tiempo promedio de espera: ",self.promedio_de_espera
      
      return self.usocpu, self.promedio_servicio, self.promedio_de_espera, self.esperado,  self.min, self.max

