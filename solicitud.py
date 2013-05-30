#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: solicitud.py
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

class SolicitudDatos(gtk.HBox):
    def __init__(self, CFG):
        gtk.HBox.__init__(self)

        table = gtk.Table(20, 2)

        attr = pango.AttrList()
        size = pango.AttrSize(18000, 0, -1)
        attr.insert(size)

        self.lbltitle1 = gtk.Label("Solicitud de los Algoritmos")
        self.lbltitle1.set_alignment(0, 0.5)
        self.lbltitle1.set_attributes(attr)
        table.attach(self.lbltitle1, 0, 2, 0, 1)

        self.FCFS = gtk.CheckButton("Algoritmo Primero en llegar primero en servirse(FCFS)")
        #self.FCFS.connect("toggled", self.FCFSchecked)
        table.attach(self.FCFS, 0, 2, 1, 2)

        self.SRT = gtk.CheckButton("Algoritmo Mmenor tiempo restante(SRT)")
        #self.SRT.connect("toggled", self.SRTchecked)
        table.attach(self.SRT, 0, 2, 2, 3)

        self.rr = gtk.CheckButton("Round Robin(RR)")
        table.attach(self.rr, 0, 2, 3, 4)

        self.so = gtk.CheckButton("Reemplazo del reloj(segunda oportunidad)")
        table.attach(self.so, 0, 2, 4, 5)

        self.tejecucion = gtk.Label("Elija el algoritmo y escriba el valor para el tiempo de ejecución de procesos:")
        self.tejecucion.set_alignment(0, 0.5)
        table.attach(self.tejecucion, 0, 1, 5, 6)

        self.tiempoejecucion = gtk.combo_box_new_text()
        self.tiempoejecucion.insert_text(0, 'Uniforme')
        self.tiempoejecucion.set_active(0)
        self.tiempoejecucion.insert_text(1, 'Constante')
        self.tiempoejecucion.insert_text(2, 'Exponencial')
        self.tiempoejecucion.insert_text(3, 'Normal')
        table.attach(self.tiempoejecucion, 0, 1, 6, 7)

        self.txttejecucion = gtk.Entry()
        table.attach(self.txttejecucion, 1, 2, 6, 7)

        self.tcpu = gtk.Label("Elija el algoritmo y escriba el valor para el tiempo de uso del CPU:")
        self.tcpu.set_alignment(0, 0.5)
        table.attach(self.tcpu, 0, 1, 7, 8)

        self.tiempocpu = gtk.combo_box_new_text()
        self.tiempocpu.insert_text(0, 'Uniforme')
        self.tiempocpu.set_active(0)
        self.tiempocpu.insert_text(1, 'Constante')
        self.tiempocpu.insert_text(2, 'Exponencial')
        self.tiempocpu.insert_text(3, 'Normal')
        table.attach(self.tiempocpu, 0, 1, 8, 9)

        self.txttcpu = gtk.Entry()
        table.attach(self.txttcpu, 1, 2, 8, 9)

        self.tbloqueo = gtk.Label("Elija el algoritmo y escriba el valor para el tiempo de bloqueo:")
        self.tbloqueo.set_alignment(0, 0.5)
        table.attach(self.tbloqueo, 0, 1, 9, 10)

        self.tiempobloqueo = gtk.combo_box_new_text()
        self.tiempobloqueo.insert_text(0, 'Uniforme')
        self.tiempobloqueo.set_active(0)
        self.tiempobloqueo.insert_text(1, 'Constante')
        self.tiempobloqueo.insert_text(2, 'Exponencial')
        self.tiempobloqueo.insert_text(3, 'Normal')
        table.attach(self.tiempobloqueo, 0, 1, 10, 11)

        self.txttbloqueo = gtk.Entry()
        table.attach(self.txttbloqueo, 1, 2, 10, 11)

        self.lbltitle2 = gtk.Label("Solicitud de los datos")
        self.lbltitle2.set_alignment(0, 0.5)
        self.lbltitle2.set_attributes(attr)
        table.attach(self.lbltitle2, 0, 2, 12, 13)

        self.lbln = gtk.Label("Número de procesos a ejecutar:")
        self.lbln.set_alignment(0, 0.5)
        table.attach(self.lbln, 0, 1, 13, 14)

        self.txtn = gtk.Entry()
        table.attach(self.txtn, 1, 2, 13, 14)

        self.pack_start(table, padding=40)
