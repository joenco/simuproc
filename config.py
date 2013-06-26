#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: config.py "este archivo es tomado del instalador de canaima"
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

curdir = os.path.normpath(os.path.join(os.path.realpath(__file__), '..', '..'))

if curdir == '/usr/share/pyshared':
    GUIDIR = '/usr/share/pyshared/simuproc'
    SHAREDIR = '/usr/share/git-simuproc'
else:
    GUIDIR = curdir + '/simuproc'
    SHAREDIR = curdir

ABOUT_IMAGE = GUIDIR + '/imagenes/logo.png'

VERSION_FILE = SHAREDIR + '/VERSION'
AUTHORS_FILE = SHAREDIR + '/AUTHORS'
LICENSE_FILE = SHAREDIR + '/LICENSE'
TRANSLATORS_FILE = SHAREDIR + '/TRANSLATORS'

APP_NAME = 'SIMUPROC'
APP_COPYRIGHT = 'Copyright (C) 2013 - Varios autores'
APP_URL = 'https://libretecnologia@code.google.com/p/simuproc/'
APP_DESCRIPTION = 'Simulador de un planificador de procesos'

CFG = {
    's': []
    }
