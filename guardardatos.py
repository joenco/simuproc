#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: guardar.py
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

import os

class Guardar():
    def Guardar(self, datos, datos1, a):
      self.datos = datos #datos de tiempo de espera.
      self.datos1 = datos1 # datos de tiempo del cpu,  tiempo de llegada, bloqueo de cpu, bloqueo de procesos.
      self.a = int(a)

      os.system('mkdir data')

      if self.a==0:
        self.data = open('data/FCFS.dat', 'w')
      elif self.a==1:
        self.data = open('data/SJF.dat', 'w')
      elif self.a==2:
        self.data = open('data/PPSJF.dat', 'w')
      elif self.a==3:
        self.data = open('data/RoundRobin.dat', 'w')

      n = len(self.datos)

      dat = 'N  |  T.E  |  T.CPU  |  T.L  |  TBCPU  |  TB  |'
      self.data.write(dat)
      self.data.write('\n')
      for i in xrange(n):
        x1 = str(self.datos1[i][0]) #Número de procesos
        y1 = str(self.datos[i][1]) # tiempo de espera
        a1 = str(self.datos1[i][1]) # tiempo de cpu
        z1 = str(self.datos1[i][2]) # tiempo de llegada
        z2 = str(self.datos1[i][3]) # tiempo de bloqueo de cpu
        z3 = str(self.datos1[i][4]) # tiempo de bloqueo de los procesos.
        dat = x1+'  |  '+y1+'  |  '+a1+'  |  '+z1+'  |  '+z2+'  |  '+z3+'  |'
        self.data.write(dat)
        self.data.write('\n')

      self.data.close()

