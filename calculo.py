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

class CalculoFifo(gtk.HBox):
    def calcular(self, n, te, tr, funcion1, funcion2, funcion3):
      self.cola_procesos = []
      self.total_llegada = 0
      self.promedio_llegada=0
      self.total_servicio=0
      self.promedio_servicio=0
      random.seed(5000)
      self.n = int(n)
      self.te = int(te)
      self.tr = int(tr)
      self.func_llegada = funcion1
      self.func_servicio = funcion2

      #random.randint(0, self.te)
      if self.func_llegada == 'Constante':
        for i in xrange(self.n):
          self.cola_procesos.append([])#agregamos un objeto de tipo lista a la cola
          self.cola_procesos[i].append(i)
          self.cola_procesos[i].append(self.te)
          self.cola_procesos[i].append(self.tr)
          print ''

      for i in xrange(self.n):
        self.total_llegada += self.cola_procesos[i][1]
        self.total_servicio += self.cola_procesos[i][2]

      for i in xrange(self.n):
        print self.cola_procesos[i][0],'\t\t',self.cola_procesos[i][1],'\t\t',self.cola_procesos[i][2]

      self.promedio_llegada = float(self.total_llegada/self.n)
      self.promedio_servicio = int(self.total_servicio/self.n)
      print 'Tiempo total de llegada: ',self.total_llegada
      print 'Tiempo total de servicio: ',self.total_servicio
      print 'Tiempo promedio de llegada: ',(self.promedio_llegada)
      print 'Tiempo promedio de servicio: ',self.promedio_servicio

        #return self.total_llegada, self.promedio_llegada
      return self.total_llegada, self.promedio_llegada
