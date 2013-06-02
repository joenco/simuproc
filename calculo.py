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

class CalculoFifo(gtk.HBox):
    def calcular(self, n, te, tp, funcion1, funcion2):
      self.cola_procesos = []
      self.total_llegada = 0
      self.promedio_llegada=0
      self.total_servicio=0
      self.promedio_llegada=0
      self.promedio_servicio=0
      self.total_esperado=0
      self.promedio_de_espera=0
      random.seed(5000)
      self.n = float(n) #número de procesos.
      self.te = float(te) #tiempo de llegada de los procesos
      self.tp = float(tp) #tiempo de servicio de los procesos.
      self.func_llegada = funcion1 #función para los tiempos de llegada.
      self.func_servicio = funcion2 #función para el tiempo de servicio.

      for i in xrange(self.n):
        self.cola_procesos.append([])#agregamos un objeto de tipo lista a la cola
        self.cola_procesos[i].append(i)
        if self.func_servicio == 'Constante':
          self.cola_procesos[i].append(self.tp)
        elif self.func_servicio == 'Uniforme':
          self.cola_procesos[i].append(np.random.randint(0, self.tp))
        elif self.func_servicio == 'Exponencial':
          self.cola_procesos[i].append(np.random.exponential(self.tp))
        elif self.func_servicio == 'Normal':
          self.cola_procesos[i].append(st.norm.cdf(self.tp))

        if self.func_llegada == 'Constante':
          self.cola_procesos[i].append(self.te)
        elif self.func_llegada == 'Uniforme':
          self.cola_procesos[i].append(np.random.randint(0, self.tp))
        elif self.func_llegada == 'Exponencial':
          self.cola_procesos[i].append(np.random.exponential(self.te))
        elif self.func_llegada == 'Normal':
          self.cola_procesos[i].append(st.norm.cdf(self.te))

      self.cola_procesos[0][2]=self.cola_procesos[0][2]-self.cola_procesos[0][2]
      for i in xrange(self.n):
        self.total_servicio += self.cola_procesos[i][1]
        self.total_llegada += self.cola_procesos[i][2]
        self.total_esperado +=  self.cola_procesos[i][1]-self.cola_procesos[i][2]
        print self.cola_procesos[i][0],'\t\t',self.cola_procesos[i][1],'\t\t',self.cola_procesos[i][2]

      self.promedio_llegada = float(self.total_llegada/self.n)
      self.promedio_servicio = float(self.total_servicio/self.n)
      self.promedio_de_espera = float(self.total_esperado/self.n)
      print 'Tiempo total de llegada: ',self.total_llegada
      print 'Tiempo total de proceso: ',self.total_servicio
      print 'Tiempo promedio de llegada: ',(self.promedio_llegada)
      print 'Tiempo promedio de proceso: ',(self.promedio_servicio)
      print 'Tiempo promedio esperado: ',(self.promedio_de_espera)

        #return self.total_llegada, self.promedio_llegada
      return self.total_llegada, self.promedio_llegada, self.total_servicio, self.promedio_servicio, self.promedio_de_espera, self.cola_procesos
