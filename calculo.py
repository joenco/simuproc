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

class CalculoFifo():
    def calcular(self, n, te, tr):
      cola_procesos = []
      total_wtime = 0

      self.n = int(n)
      self.te = int(te)
      self.tr = int(tr)

      for i in xrange(self.n):
        cola_procesos.append([])#agregamos un objeto de tipo lista a la cola
        cola_procesos[i].append(i)
        cola_procesos[i].append(self.te)
        total_wtime += cola_procesos[i][1]
        cola_procesos[i].append(self.tr)
        print ''

      cola_procesos.sort(key = lambda cola_procesos:cola_procesos[1])

      print 'Nombre del proceso\t\t Tiempo de espera \t \tTiempo de rafaga'
      for i in xrange(self.n):
        print cola_procesos[i][0],'\t\t',cola_procesos[i][1],'\t\t',cola_procesos[i][2]

      Total_promedio = int(total_wtime/self.n)
      print 'Tiempo total de espera: ',total_wtime
      print 'Tiempo promedio de espera: ',(Total_promedio)

      return total_wtime, Total_promedio
