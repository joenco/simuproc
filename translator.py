#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: translator.py "este archivo es tomado del instalador de canaima"
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

from gettext import gettext as _

MAIN_ROOT_ERROR_MSG = _('Canaima Instalador debe ser ejecutado con permisos de superusuario.')
MAIN_ROOT_ERROR_TITLE = _('Error de permisología')

class msj:
    'Clase para administrar los mensajes mostrados al usuario'

    class particion:
        'Mensajes relacionados a las particiones'

        libre = 'Espacio Libre'
        primaria = 'Primaria'
        extendida = 'Extendida'
        logica = 'Lógica'
        desconocida = 'Desconocido'

        @classmethod
        def get_tipo(self, tipo):
            if tipo == 'free':      return self.libre
            if tipo == 'primary':   return self.primaria
            if tipo == 'extended':  return self.extendida
            if tipo == 'logical':   return self.logica

            return tipo

        @classmethod
        def get_tipo_orig(self, tipo):
            if tipo == self.libre :     return 'free'
            if tipo == self.primaria:   return 'primary'
            if tipo == self.extendida:  return 'extended'
            if tipo == self.logica:     return 'logical'
            if tipo == self.desconocida:return 'unknown'

            return tipo

        @classmethod
        def get_formato(self, formato):
            if formato == 'free':       return self.libre
            if formato == 'unknown':    return self.desconocida
            if formato == 'extended':   return ''

            return formato

        @classmethod
        def get_dispositivo(self, disp, num):
            if num == -1:       return ''

            return disp
