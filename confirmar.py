#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: confirmar.py
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

class ConfirmarDatos(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)

        #if CFG['fifo'] == True:
        msg_fifo = '● Primero en llegar primero en servirse(FCFS) - Fisrt-come, First-serverd"{0}".'.format(CFG['fifo'])
        msg_menortiempo = '● Mmenor tiempo restante(SRT) - Short Remaining Time"{0}".'.format(CFG['menortiempo'])
        msg_roundrobin = '● planificación por turno rotatorio(RR) - Round Robin"{0}".'.format(CFG['roundrobin'])
        msg_soprtunidad = '● Reemplazo del reloj(segunda oportunidad)"{0}".'.format(CFG['soprtunidad'])

        msg_mensaje1 = '● Función de ejecución:"{0}" tiempo: "{1}'.format(CFG['ejecucion'], CFG['tejecucion'])
        msg_mensaje2 = '● Función de uso del CPU:"{0}" tiempo: "{1}'.format(CFG['cpu'], CFG['tcpu'])
        msg_mensaje3 = '● Función de bloqueo:"{0}" tiempo: "{1}'.format(CFG['bloqueo'], CFG['tbloqueo'])
        msg_mensaje4 = '● Número de procesos a ejcutar:"{0}"'.format(CFG['nproceso'])

        msg_final = 'Presione el botón "Adelante" para iniciar la Corrida. Después de este paso no podrá detener la corrida, así que asegúrese de que sus datos son correctos.'
        msg_titulo = '¡Todo listo!'
        msg_intro = 'Estos son los datos para la corrida:'

        attr = pango.AttrList()
        size = pango.AttrSize(20000, 0, -1)
        attr.insert(size)

        self.lbltitulo = gtk.Label(msg_titulo)
        self.lbltitulo.set_size_request(640, 40)
        self.lbltitulo.set_alignment(0, 0)
        self.lbltitulo.set_attributes(attr)
        self.lbltitulo.set_line_wrap(True)
        self.put(self.lbltitulo, 50, 90)

        self.lblintro = gtk.Label(msg_intro)
        self.lblintro.set_size_request(640, 20)
        self.lblintro.set_alignment(0, 0)
        self.lblintro.set_line_wrap(True)
        self.put(self.lblintro, 50, 120)

        self.lblnp = gtk.Label(msg_mensaje4)
        self.lblnp.set_size_request(640, 20)
        self.lblnp.set_alignment(0, 0)
        self.lblnp.set_line_wrap(True)
        self.put(self.lblnp, 50, 140)

        self.lblfifo = gtk.Label(msg_fifo)
        self.lblfifo.set_size_request(640, 20)
        self.lblfifo.set_alignment(0, 0)
        self.lblfifo.set_line_wrap(True)
        self.put(self.lblfifo, 50, 160)

        self.lblmtiempo = gtk.Label(msg_menortiempo)
        self.lblmtiempo.set_size_request(640, 20)
        self.lblmtiempo.set_alignment(0, 0)
        self.lblmtiempo.set_line_wrap(True)
        self.put(self.lblmtiempo, 50, 180)

        self.lblrr = gtk.Label(msg_roundrobin)
        self.lblrr.set_size_request(640, 20)
        self.lblrr.set_alignment(0, 0)
        self.lblrr.set_line_wrap(True)
        self.put(self.lblrr, 50, 200)

        self.lbso = gtk.Label(msg_soprtunidad)
        self.lbso.set_size_request(640, 20)
        self.lbso.set_alignment(0, 0)
        self.lbso.set_line_wrap(True)
        self.put(self.lbso, 50, 220)

        self.lbmensaje1 = gtk.Label(msg_mensaje1)
        self.lbmensaje1.set_size_request(640, 20)
        self.lbmensaje1.set_alignment(0, 0)
        self.lbmensaje1.set_line_wrap(True)
        self.put(self.lbmensaje1, 50, 240)

        self.lbmensaje2 = gtk.Label(msg_mensaje2)
        self.lbmensaje2.set_size_request(640, 20)
        self.lbmensaje2.set_alignment(0, 0)
        self.lbmensaje2.set_line_wrap(True)
        self.put(self.lbmensaje2, 50, 260)

        self.lbmensaje3 = gtk.Label(msg_mensaje3)
        self.lbmensaje3.set_size_request(640, 20)
        self.lbmensaje3.set_alignment(0, 0)
        self.lbmensaje3.set_line_wrap(True)
        self.put(self.lbmensaje3, 50, 280)

        self.lblmsg = gtk.Label(msg_final)
        self.lblmsg.set_size_request(640, 50)
        self.lblmsg.set_alignment(0, 0)
        self.lblmsg.set_line_wrap(True)
        self.put(self.lblmsg, 50, 330)

