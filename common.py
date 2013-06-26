#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Simulador de planificación de procesos.
# ARCHIVO: common.py "este archivo es tomado del instalador de canaima"
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

import re, subprocess, math, cairo, gtk, hashlib, random, string, urllib2, os, glob, crypt, threading, shutil, filecmp
from config import APP_NAME, APP_COPYRIGHT, APP_DESCRIPTION, \
    APP_URL, LICENSE_FILE, AUTHORS_FILE, TRANSLATORS_FILE, VERSION_FILE, ABOUT_IMAGE

def AboutWindow(widget=None):
    about = gtk.AboutDialog()
    about.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    about.set_logo(gtk.gdk.pixbuf_new_from_file(ABOUT_IMAGE))
    about.set_name(APP_NAME)
    about.set_copyright(APP_COPYRIGHT)
    about.set_comments(APP_DESCRIPTION)
    about.set_website(APP_URL)

    try:
        f = open('documentos/gpl-3.0.txt', 'r')
        license = f.read()
        f.close()
    except Exception, msg:
        license = 'NOT FOUND'

    try:
        f = open('documentos/autores.txt', 'r')
        a = f.read()
        authors = a.split('\n')
        f.close()
    except Exception, msg:
        authors = 'NOT FOUND'

    try:
        f = open(TRANSLATORS_FILE, 'r')
        translators = f.read()
        f.close()
    except Exception, msg:
        translators = 'NOT FOUND'

    try:
        f = open(VERSION_FILE, 'r')
        version = f.read().split('\n')[0].split('=')[1].strip('"')
        f.close()
    except Exception, msg:
        version = 'Versión 1.0'

    about.set_translator_credits(translators)
    about.set_authors(authors)
    about.set_license(license)
    about.set_version(version)

    about.run()
    about.destroy()

def aconnect(button, signals, function, params):
    '''
        desconecta los eventos existentes en signals y conecta con function
    '''
    for i in signals:
        if button.handler_is_connected(i):
            button.disconnect(i)
    signals.append(button.connect_object('clicked', function, params))

    return signals

def UserMessage(
    message, title, mtype, buttons, c_1=False, f_1=False, p_1='',
    c_2=False, f_2=False, p_2='', c_3=False, f_3=False, p_3='',
    c_4=False, f_4=False, p_4='', c_5=False, f_5=False, p_5=''
    ):
    dialog = gtk.MessageDialog(
        parent=None, flags=0, type=mtype,
        buttons=buttons, message_format=message
        )
    dialog.set_title(title)
    dialog.show_all()
    response = dialog.run()
    dialog.destroy()

    if response == c_1:
        f_1(*p_1)
    if response == c_2:
        f_2(*p_2)
    if response == c_3:
        f_3(*p_3)
    if response == c_4:
        f_4(*p_4)
    if response == c_5:
        f_5(*p_5)

    return response

if __name__ == "__main__":
    print debug_list([1, 2])
    print debug_list({"casa":[1]})
    print debug_list("la casa")
    print debug_list(12.0)
    print debug_list(gtk)


