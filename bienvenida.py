#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: bienvenida.py "este archivo es una modificación del tomado en el instalador de canaima"
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

class BienvenidaUsuario(gtk.Fixed):

    """ Muestra al usuario una ventana dandole la bienvenida al sistema."""

    def __init__(self, CFG):
        gtk.Fixed.__init__(self)

        msg_titulo = 'Simulador de planificación de procesos'
        msg_intro = 'Con este programa podrá simular los algoritmos de:'
        msg_disco = '● Primero en llegar primero en servirse(FCFS) - Fisrt-come, First-serverd.'
        msg_memoria = '● Menor tiempo primero(SJF) - Shortest Job First.'
        msg_mensaje1 = '● Planificación por turno rotatorio(RR) - Round Robin.'
        msg_mensaje2 = '● Preemptive Shortest Job First (PSJF)'
        msg_fin = 'Para cualquier comentario o ayuda escriba a: joenco@esdebian.org'

        attr = pango.AttrList()
        size = pango.AttrSize(20000, 0, -1)
        attr.insert(size)

        self.lbltitulo = gtk.Label(msg_titulo)
        self.lbltitulo.set_size_request(640, 80)
        self.lbltitulo.set_alignment(0, 0)
        self.lbltitulo.set_attributes(attr)
        self.lbltitulo.set_line_wrap(True)
        self.put(self.lbltitulo, 50, 90)

        self.lblintro = gtk.Label(msg_intro)
        self.lblintro.set_size_request(640, 40)
        self.lblintro.set_alignment(0, 0)
        self.lblintro.set_line_wrap(True)

        self.put(self.lblintro, 50, 170)

        self.lbldisco = gtk.Label(msg_disco)
        self.lbldisco.set_size_request(640, 20)
        self.lbldisco.set_alignment(0, 0)
        self.lblintro.set_line_wrap(True)
        self.put(self.lbldisco, 50, 220)

        self.lblmemoria = gtk.Label(msg_memoria)
        self.lblmemoria.set_size_request(640, 20)
        self.lblmemoria.set_alignment(0, 0)
        self.lblmemoria.set_line_wrap(True)
        self.put(self.lblmemoria, 50, 240)

        self.lblmensaje1 = gtk.Label(msg_mensaje1)
        self.lblmensaje1.set_size_request(640, 20)
        self.lblmensaje1.set_alignment(0, 0)
        self.lblmensaje1.set_line_wrap(True)
        self.put(self.lblmensaje1, 50, 260)

        self.lblmensaje2 = gtk.Label(msg_mensaje2)
        self.lblmensaje2.set_size_request(640, 20)
        self.lblmensaje2.set_alignment(0, 0)
        self.lblmensaje2.set_line_wrap(True)
        self.put(self.lblmensaje2, 50, 280)

        self.lblfin = gtk.Label(msg_fin)
        self.lblfin.set_size_request(640, 20)
        self.lblfin.set_alignment(0, 0)
        self.lblfin.set_line_wrap(True)
        self.put(self.lblfin, 50, 310)

