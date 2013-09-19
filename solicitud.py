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

    """ pide al usuario que algoritmos desea simular, cuantos procesos, el tipo de función y su tiempo"""

    def __init__(self, CFG):
        gtk.HBox.__init__(self)

        self.table = gtk.Table(20, 3)

        attr = pango.AttrList()
        size = pango.AttrSize(18000, 0, -1)
        attr.insert(size)

        self.lbltitle1 = gtk.Label("Solicitud de los datos")
        self.lbltitle1.set_alignment(0, 0.5)
        self.lbltitle1.set_attributes(attr)
        self.table.attach(self.lbltitle1, 0, 2, 0, 1)

        self.FCFS = gtk.CheckButton("Algoritmo Primero en llegar primero en servirse (FCFS)")
        """Chekbutton que permite al usuario elejir el algoritmo FCFS"""
        self.table.attach(self.FCFS, 0, 1, 1, 2)

        self.SJF = gtk.CheckButton("Algoritmo Menor tiempo restante (SJF)")
        """Chekbutton que permite al usuario elejir el algoritmo SJF"""
        self.table.attach(self.SJF, 0, 1, 2, 3)

        self.rr = gtk.CheckButton("Round Robin (RR)")
        """Chekbutton que permite al usuario elejir el algoritmo RR"""
        #actionrr.connect_proxy(self.rr)
        self.table.attach(self.rr, 0, 1, 3, 4)

        self.txtrr = gtk.Entry()
        self.txtrr.set_text('Coloque el cuantum de tiempo')
        self.table.attach(self.txtrr, 1, 2, 3, 4)

        self.so = gtk.CheckButton("Preemptive Shortest Job First (PSJF)")
        """Chekbutton que permite al usuario elejir el algoritmo PSJF"""
        self.table.attach(self.so, 0, 1, 4, 5)

        self.listafuncion = gtk.ListStore(str)
        self.listafuncion.append(["Constante"])
        self.listafuncion.append(["Uniforme"])
        self.listafuncion.append(["Exponencial"])
        self.listafuncion.append(["Normal"])

        self.tejecucion = gtk.Label("Elija el algoritmo y escriba el valor para el tiempo de llegada de los procesos:")
        self.tejecucion.set_alignment(0, 0.5)
        self.table.attach(self.tejecucion, 0, 2, 5, 6)

        self.tiempoejecucion = gtk.combo_box_new_text()
        self.tiempoejecucion.set_model(self.listafuncion)
        self.tiempoejecucion.set_active(0)
        self.table.attach(self.tiempoejecucion, 0, 1, 6, 7)

        self.txttejecucion = gtk.Entry()
        self.table.attach(self.txttejecucion, 1, 2, 6, 7)

        self.tcpu = gtk.Label("Elija el algoritmo y escriba el valor para el tiempo de uso del CPU:")
        self.tcpu.set_alignment(0, 0.5)
        self.table.attach(self.tcpu, 0, 1, 7, 8)

        self.tiempocpu = gtk.combo_box_new_text()
        self.tiempocpu.set_model(self.listafuncion)
        self.tiempocpu.set_active(0)
        self.table.attach(self.tiempocpu, 0, 1, 8, 9)

        self.txttcpu = gtk.Entry()
        self.table.attach(self.txttcpu, 1, 2, 8, 9)

        self.tbloqueocpu = gtk.Label("Elija el algoritmo y escriba el valor para el tiempo de bloqueo del CPU:")
        self.tbloqueocpu.set_alignment(0, 0.5)
        self.table.attach(self.tbloqueocpu, 0, 1, 9, 10)

        self.tiempobloqueocpu = gtk.combo_box_new_text()
        self.tiempobloqueocpu.set_model(self.listafuncion)
        self.tiempobloqueocpu.set_active(0)
        self.table.attach(self.tiempobloqueocpu, 0, 1, 10, 11)

        self.txttbloqueocpu = gtk.Entry()
        self.table.attach(self.txttbloqueocpu, 1, 2, 10, 11)

        self.tbloqueo = gtk.Label("Elija el algoritmo y escriba el valor para el tiempo de bloqueo de los procesos:")
        self.tbloqueo.set_alignment(0, 0.5)
        self.table.attach(self.tbloqueo, 0, 1, 11, 12)

        self.tiempobloqueo = gtk.combo_box_new_text()
        self.tiempobloqueo.set_model(self.listafuncion)
        self.tiempobloqueo.set_active(0)
        self.table.attach(self.tiempobloqueo, 0, 1, 12, 13)

        self.txttbloqueo = gtk.Entry()
        self.table.attach(self.txttbloqueo, 1, 2, 12, 13)

        self.lbln = gtk.Label("Número de procesos a ejecutar:")
        self.lbln.set_alignment(0, 0.5)
        self.table.attach(self.lbln, 0, 1, 14, 15)

        self.txtn = gtk.Entry()
        self.table.attach(self.txtn, 1, 2, 14, 15)

        self.pack_start(self.table, padding=40)
