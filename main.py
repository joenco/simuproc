#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: main.py
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

# Módulos globales
import gtk, re, Image

# Módulos locales
from bienvenida import BienvenidaUsuario
from solicitud import SolicitudDatos
from confirmar import ConfirmarDatos
from calculo import CalculoFifo
from mostrar import MostrarResultados
from common import UserMessage, AboutWindow, aconnect, \
    debug_list

class Ventana(gtk.Window):
    def __init__(self, ancho, alto, titulo):
        self.pasos = {}
        self.actual = ''

        # Creo la ventana
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
        self.titulo = titulo
        self.set_title(titulo)
        self.set_size_request(ancho, alto)
        self.set_resizable(0)
        self.set_border_width(0)

        # Creo el contenedor principal
        self.c_principal = gtk.Fixed()
        self.add(self.c_principal)

        # Calculo tamaño del banner
        #self.banner_img = Image.open(banner)
        #self.banner_w = self.banner_img.size[0]
        #self.banner_h = self.banner_img.size[1]

        # Creo el banner
        #self.banner = gtk.Image()
        #self.banner.set_from_file(banner)
        #self.banner.set_size_request(ancho, self.banner_h)
        #self.c_principal.put(self.banner, 0, 0)

        # Creo el contenedor de los pasos
        self.c_pasos = gtk.VBox()
        self.c_pasos.set_size_request((ancho - 10), (alto - 30))
        self.c_principal.put(self.c_pasos, 5, 5)

        # Creo la botonera
        self.botonera = gtk.Fixed()
        self.botonera.set_size_request(ancho, 40)
        self.c_principal.put(self.botonera, 0, (alto - 20))

        # Creo la linea divisoria
        self.linea = gtk.HSeparator()
        self.linea.set_size_request(ancho, 5)
        self.botonera.put(self.linea, 0, 0)

        # siguiente
        self.siguiente = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
        self.siguiente.set_size_request(100, 30)
        self.botonera.put(self.siguiente, (ancho - 110), 10)

        # Cancelar
        self.cancelar = gtk.Button(stock=gtk.STOCK_QUIT)
        self.cancelar.set_size_request(100, 30)
        self.cancelar.connect('clicked', self.close)
        self.botonera.put(self.cancelar, 10, 10)

        self.show_all()

        # Anterior
        self.anterior = gtk.Button(stock=gtk.STOCK_GO_BACK)
        self.anterior.set_size_request(100, 30)
        self.botonera.put(self.anterior, (ancho - 210), 10)

        # ejecutar
        self.ejecutar = gtk.Button(stock=gtk.STOCK_EXECUTE)
        self.ejecutar.set_size_request(100, 30)
        self.botonera.put(self.ejecutar, (ancho - 110), 10)

        # Acerca
        #self.acerca = gtk.Button(stock=gtk.STOCK_ABOUT)
        #self.acerca.set_size_request(100, 30)
        #self.acerca.connect('clicked', AboutWindow)
        #self.botonera.put(self.acerca, 110, 10)

        self.connect("destroy", self.close)
        self.connect("delete-event", self.close)

    def close(self, widget=None, event=None):
        '''
            Cierra la ventana
        '''
        return UserMessage(
            '¿Está seguro que desea salir del programa?', '',
            gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO, c_1=gtk.RESPONSE_YES,
            f_1=gtk.main_quit, p_1=()
            )

    def next(self, nombre, init, params, paso):
        '''
            muestra el paso especificado en nombre
        '''
        if not nombre in self.pasos:
            if self.actual != nombre:
                if self.actual != '':
                    self.pasos[self.actual].hide_all()
                self.actual = nombre

            init(params)
            self.pasos[nombre] = paso
            self.c_pasos.add(self.pasos[nombre])
            self.pasos[nombre].show_all()

    def previous(self, nombre, init, params):
        '''
            muestra el paso especificado en nombre
        '''
        if nombre in self.pasos:
            if self.actual != nombre:
                if self.actual != '':
                    self.pasos[self.actual].hide_all()
                    self.c_pasos.remove(self.pasos[self.actual])
                    del self.pasos[self.actual]
                self.actual = nombre

            init(params)
            self.pasos[nombre].show_all()

    def formulario(self, nombre):
        '''
            devulve el objeto asociado al paso
        '''
        if nombre in self.pasos:
            return self.pasos[nombre]
        else:
            return False

class Bienvenida(gtk.Window):
    '''
        Le da la bienvenida al usuario.
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, (CFG))
        CFG['w'].anterior.set_sensitive(False)

    def init(self, CFG):
        CFG['w'].next('Bienvenida', Bienvenida, (CFG), BienvenidaUsuario(CFG))

    def siguiente(self, CFG):
        CFG['w'].next('Solicitud', Solicitud, (CFG), SolicitudDatos(CFG))
        CFG['w'].anterior.show()

class Solicitud():
    '''
        Pide la solicitud de los datos.
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, (CFG))
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, (CFG))
        CFG['w'].anterior.set_sensitive(True)

    def init(self, CFG):
        CFG['w'].next('Solicitud', Solicitud, (CFG), SolicitudDatos(CFG))

    def anterior(self, CFG):
        CFG['w'].previous('Bienvenida', Bienvenida, (CFG))
        CFG['w'].siguiente.set_sensitive(True)

    def siguiente(self, CFG):
        CFG['fifo'] = CFG['w'].formulario('Solicitud').FCFS.get_active()
        CFG['menortiempo'] = CFG['w'].formulario('Solicitud').SRT.get_active()
        CFG['roundrobin'] = CFG['w'].formulario('Solicitud').rr.get_active()
        CFG['soprtunidad'] = CFG['w'].formulario('Solicitud').so.get_active()
        CFG['ejecucion'] = CFG['w'].formulario('Solicitud').tiempoejecucion.get_active_text()
        CFG['cpu'] = CFG['w'].formulario('Solicitud').tiempocpu.get_active_text()
        CFG['bloqueo'] = CFG['w'].formulario('Solicitud').tiempobloqueo.get_active_text()
        CFG['tejecucion'] = CFG['w'].formulario('Solicitud').txttejecucion.get_text()
        CFG['tcpu'] = CFG['w'].formulario('Solicitud').txttcpu.get_text()
        CFG['tbloqueo'] = CFG['w'].formulario('Solicitud').txttbloqueo.get_text()
        CFG['nproceso'] = CFG['w'].formulario('Solicitud').txtn.get_text()

        if CFG['fifo'] == False:
          if CFG['menortiempo'] == False:
            if CFG['roundrobin'] == False:
              if CFG['soprtunidad'] == False:
                message = "Debe seleccionar por lo menos un algoritmo para la corrida."
                UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                return

        if CFG['tejecucion'].strip() == '':
            message = "El campo del tiempo de ejecución esta vacío, debe colocar un valor numérico."
            UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
            return

        if re.compile('\d{1,}').search(CFG['tejecucion']) == None:
            message = "El tiempo de ejecución es inválido, debe ser un valornumérico."
            UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
            return

        if CFG['tcpu'].strip() == '':
            message = "El campo del tiempo de uso del CPU esta vacío, debe colocar un valor numérico."
            UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
            return

        if re.compile('\d{1,}').search(CFG['tcpu']) == None:
            message = "El valor del uso del CPU es inválido, debe ser un valor numérico"
            UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
            return

        if CFG['tbloqueo'].strip() == '':
            message = "El campo del tiempo del bloqueo esta vacío, debe colocar un valor numérico."
            UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
            return

        if re.compile('\d{1,}').search(CFG['tbloqueo']) == None:
            message = "El tiempo de bloqueo es inválido, debe ser un valor numérico."
            UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
            return

        if CFG['nproceso'].strip() == '':
            message = "El campo del número de procesos esta vacío, debe colocar un valor entero."
            UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
            return

        if re.compile('\d{1,}').search(CFG['nproceso']) == None:
            message = "El tiempo de bloqueo es inválido, debe ser un valor entero."
            UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
            return

        CFG['w'].siguiente.hide()
        CFG['w'].ejecutar.show()
        CFG['w'].next('Confirmar', Confirmar, (CFG), ConfirmarDatos(CFG))

class Calculo():
    '''
        hace los calculos.
    '''
    def init(self, CFG):
        CFG['w'].next('Calculo', Calculo, (CFG), CalculoFifo(CFG))

        CFG['calculofifo'] = CFG['w'].formulario('Calculo').CalculoFifo

class Confirmar():
    '''
        muestra la confirmación de los datos para la corrida.
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].ejecutar, CFG['s'], self.ejecutar, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        CFG['w'].previous('Solicitud', Solicitud, (CFG))

    def ejecutar(self, CFG):
        calculo = CalculoFifo()
        CFG['calculofifo'] = calculo.calcular(CFG['nproceso'], CFG['tejecucion'], CFG['tcpu'])
        CFG['w'].next('Mostrar', Mostrar, (CFG), MostrarResultados(CFG))
        CFG['w'].siguiente.show()
        CFG['w'].ejecutar.hide()

class Mostrar():
    '''
        Muestra los resultados.
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def init(self, CFG):
        CFG['w'].next('Calculo', Calculo, (CFG), CalculoFifo(CFG))

    def anterior(self, CFG):
        CFG['w'].previous('Solicitud', Solicitud, (CFG))

    def siguiente(self, CFG):
        CFG['w'].next('Resultados', Resultados, (MostrarResultados), SolicitudDatos(CFG))

