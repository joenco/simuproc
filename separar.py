#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: separar.py
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

class Separar():
    """ Acepta un campo con un par de números y devuelve cada número separado, para ser usado con la función Uniforme"""
    def Separar(self, numero):
      self.numero = numero
      j=0
      i=0
      v1 = ' '
      v2 = ' '
      n = len(numero)

      while i<n:
          if j== 0:
            if numero[i] != ' ':
              v1 += numero[i]
              i += 1
            else:
              if numero[i] == ' ':
                i += 1
              j = 1 
          else:
            if j==1:
              v2 += numero[i]
              i += 1

      numero1 = float(v1)
      numero2 = float(v2)

      return numero1, numero2
