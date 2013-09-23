#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: rafaga.py
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

from separar import Separar
import numpy as np
import scipy.stats as st
import random as r

class Rafaga():
    
    #Obtener rafaga y tiempo de bloqueo
    def rafaga_bloqueo(self, tbcpu, tb, f3, f4):
        """ Función que retorna rafaga y tiempo de bloqueo"""
        self.cola_procesos = []
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
          self.cola_procesos.append(self.tbcpu)
        elif self.func_bloqueocpu == 'Uniforme':
          self.cola_procesos.append(round(r.uniform(self.tbcpu[0], self.tbcpu[1]), 3))
        elif self.func_bloqueocpu == 'Exponencial':
          self.cola_procesos.append(round(np.random.exponential(self.tbcpu), 3))
        elif self.func_bloqueocpu == 'Normal':
          self.cola_procesos.append(round(st.norm.cdf(self.tbcpu), 3))

        if self.func_bloqueo == 'Constante':
          self.cola_procesos.append(self.tb)
        elif self.func_bloqueo == 'Uniforme':
          self.cola_procesos.append(round(r.uniform(self.tb[0], self.tb[1]), 3))
        elif self.func_bloqueo == 'Exponencial':
          self.cola_procesos.append(round(np.random.exponential(self.tb), 3))
        elif self.func_bloqueo == 'Normal':
          self.cola_procesos.append(round(st.norm.cdf(self.tb), 3))

        return self.cola_procesos

    def siguiente_turno(self, ejecucion,iterador):
      self.ejecucion = ejecucion
      self.iterador = iterador

      if (len(self.ejecucion)==1):
         return self.iterador

      for i in xrange(iterador,len(self.ejecucion)):
        if (ejecucion[i]>0):
          return i

      for i in xrange(len(self.ejecucion)):
        if (ejecucion[i]>0):
          return i

      return 0

      




     
