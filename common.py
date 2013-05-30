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

import re, subprocess, math, cairo, gtk, hashlib, random, string, urllib2, os, glob, parted, crypt, threading, shutil, filecmp

from translator import msj
from config import APP_NAME, APP_COPYRIGHT, APP_DESCRIPTION, \
    APP_URL, LICENSE_FILE, AUTHORS_FILE, TRANSLATORS_FILE, VERSION_FILE, ABOUT_IMAGE, \
    FSPROGS, FSMIN, FSMAX

def AboutWindow(widget=None):
    about = gtk.AboutDialog()
    about.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    about.set_logo(gtk.gdk.pixbuf_new_from_file(ABOUT_IMAGE))
    about.set_name(APP_NAME)
    about.set_copyright(APP_COPYRIGHT)
    about.set_comments(APP_DESCRIPTION)
    about.set_website(APP_URL)

    try:
        f = open(LICENSE_FILE, 'r')
        license = f.read()
        f.close()
    except Exception, msg:
        license = 'NOT FOUND'

    try:
        f = open(AUTHORS_FILE, 'r')
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
        version = 'NOT FOUND'

    about.set_translator_credits(translators)
    about.set_authors(authors)
    about.set_license(license)
    about.set_version(version)

    about.run()
    about.destroy()

def espacio_usado(fs, particion):
    if os.path.exists(particion):
        assisted_umount(sync=False, plist=[['', '/mnt', '']])
        assisted_mount(
            sync=False, bind=False, plist=[[particion, '/mnt', fs]]
            )
        s = os.statvfs('/mnt')
        used = float(((s.f_blocks - s.f_bfree) * s.f_frsize) / 1024)
        assisted_umount(sync=False, plist=[['', '/mnt', '']])
    else:
        used = 'unknown'

    return used

def mounted_targets(mnt):
    m = []
    _mnt = mnt.replace('/', '\/')
    cmd = "awk '$2 ~ /^" + _mnt + "/ {print $2}' /proc/mounts | sort"
    salida = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        ).communicate()[0].split()

    for i in salida:
        m.append(['', i, ''])

    return m

def activar_swap(plist):
    for p, m, fs in plist:
        if fs == 'swap':
            cmd = 'swapon {0}'.format(p)
            salida = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                ).communicate()[0].split()
    return True

def mounted_parts(disk):
    m = []
    _disk = disk.replace('/', '\/')
    cmd = "awk '$1 ~ /^" + _disk + "/ {print $2}' /proc/mounts | sort"
    salida = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        ).communicate()[0].split()

    for i in salida:
        m.append(['', i, ''])

    return m

def get_windows_part_in(drive):
    cmd = "os-prober | grep -i 'Windows' | grep '"+drive+"' | awk -F: '{print $1}'"
    salida = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        ).communicate()[0].split()

    if len(salida) > 0:
        return salida[0]
    else:
        return ''

def assisted_mount(sync, bind, plist):
    i = 0
    n = len(plist)

    if bind:
        bindcmd = '-o bind'
    else:
        bindcmd = ''

    for p, m, fs in plist:
        if fs == 'fat32' or fs == 'fat16':
            fs = 'vfat'
        elif fs == 'hfs+':
            fs = 'hfsplus'

        if fs:
            fscmd = '-t {0}'.format(fs)
        else:
            fscmd = ''

        if not os.path.isdir(m):
            os.makedirs(m)

        if fs != 'swap':
            if not os.path.ismount(m):
                if ProcessGenerator(
                    'mount {0} {1} {2} {3}'.format(bindcmd, fscmd, p, m)
                    ).returncode == 0:
                    i += 1
            else:
                i += 1
        else:
            i += 1

    if sync:
        ProcessGenerator('sync')

    if i == n:
        return True
    else:
        return False

def assisted_umount(sync, plist):
    i = 0
    n = len(plist)
    plist.reverse()

    for p, m, fs in plist:
        if os.path.ismount(m):
            if ProcessGenerator('umount {0}'.format(m)).returncode == 0:
                i += 1
        else:
            i += 1

    if sync:
        ProcessGenerator('sync')

    if i == n:
        return True
    else:
        return False

def preseed_debconf_values(mnt, debconflist):
    content = '\n'.join(debconflist)
    destination = '{0}/tmp/debconf'.format(mnt)

    f = open(destination, 'w')
    f.write(content)
    f.close()

    if ProcessGenerator(
        'chroot {0} /usr/bin/debconf-set-selections < {1}/tmp/debconf'.format(mnt, mnt)
        ).returncode == 0:
        return True
    else:
        return False

def instalar_paquetes(mnt, dest, plist):
    i = 0
    n = len(plist)

    for loc, name in plist:
        if os.path.isdir(loc):
            pkglist = glob.glob(loc + '/' + name + '_*.deb')

            if pkglist:
                pkg = os.path.basename(pkglist[0])
                pkgpath = pkglist[0]
            else:
                return False

            if not os.path.isdir(mnt + dest):
                os.makedirs(mnt + dest)

            if ProcessGenerator(
                'cp {0} {1}'.format(pkgpath, mnt + dest + '/')
                ).returncode == 0:
                i += 1

            if ProcessGenerator(
                'chroot {0} env DEBIAN_FRONTEND="noninteractive" dpkg -i {1}/{2}'.format(mnt, dest, pkg)
                ).returncode == 0:
                i += 1

    if i == n * 2:
        return True
    else:
        return False

def desinstalar_paquetes(mnt, plist):
    i = 0
    n = len(plist)

    for name in plist:
        if ProcessGenerator(
            'chroot {0} aptitude purge --assume-yes --allow-untrusted -o DPkg::Options::="--force-confmiss" -o DPkg::Options::="--force-confnew" -o DPkg::Options::="--force-overwrite" {1}'.format(mnt, name)
            ).returncode == 0:
            i += 1

    if i == n:
        return True
    else:
        return False

def reconfigurar_paquetes(mnt, plist):
    i = 0
    n = len(plist)

    for name in plist:
        p = ProcessGenerator(
            'chroot {0} dpkg-reconfigure {1}'.format(mnt, name)
            )
        if p.returncode == 0:
            i += 1

    if i == n:
        return True
    else:
        return False

def actualizar_sistema(mnt):
    i = 0

    if ProcessGenerator(
        'chroot {0} dhclient'.format(mnt)
        ).returncode == 0:
        i += 1

    if ProcessGenerator(
        'chroot {0} aptitude update'.format(mnt)
        ).returncode == 0:
        i += 1

    if ProcessGenerator(
        'chroot {0} env DEBIAN_FRONTEND="noninteractive" aptitude full-upgrade --assume-yes --allow-untrusted -o DPkg::Options::="--force-confmiss" -o DPkg::Options::="--force-confnew" -o DPkg::Options::="--force-overwrite"'.format(mnt)
        ).returncode == 0:
        i += 1

    if i == 4:
        return True
    else:
        return False

def crear_usuarios(mnt, a_user, a_pass, n_name, n_user, n_pass):
    i = 0
    content = a_user + ':' + a_pass + '\n'
    destination = '{0}/tmp/passwd'.format(mnt)
    home = '/home/{0}'.format(n_user)
    shell = '/bin/bash'
    password = crypt_generator(n_pass)

    f = open(destination, 'w')
    f.write(content)
    f.close()

    if ProcessGenerator(
        'chroot {0} /usr/sbin/chpasswd < {1}/tmp/passwd | '.format(mnt, mnt)
        ).returncode == 0:
        i += 1

    if ProcessGenerator(
        'chroot {0} /usr/sbin/useradd -m -d "{1}" -s "{2}" -c "{3}" -p "{4}" {5}'.format(
            mnt, home, shell, n_name, password, n_user
            )
        ).returncode == 0:
        i += 1

    if i == 2:
        return True
    else:
        return False

def crear_etc_network_interfaces(mnt, cfg):
    content = ''
    destination = mnt + cfg
    interdir = '/sys/class/net/'
    interlist = next(os.walk(interdir))[1]

    for i in interlist:
        if i == 'lo':
            content += '\nauto lo'
            content += '\niface lo inet loopback\n'
        elif re.sub('\d', '', i) == 'eth':
            content += '\nallow-hotplug {0}'.format(i)
            content += '\niface {0} inet dhcp\n'.format(i)

    f = open(destination, 'w')
    f.write(content)
    f.close()

    return True

def crear_etc_hostname(mnt, cfg, maq):
    content = maq + '\n'
    f = open(mnt + cfg, 'w')
    f.write(content)
    f.close()

    return True

def crear_etc_hosts(mnt, cfg, maq):
    content = '127.0.0.1\t\t{0}\t\tlocalhost\n'.format(maq)
    content += '::1\t\tlocalhost\t\tip6-localhost ip6-loopback\n'
    content += 'fe00::0\t\tip6-localnet\n'
    content += 'ff00::0\t\tip6-mcastprefix\n'
    content += 'ff02::1\t\tip6-allnodes\n'
    content += 'ff02::2\t\tip6-allrouters\n'
    content += 'ff02::3\t\tip6-allhosts'

    f = open(mnt + cfg, 'w')
    f.write(content)
    f.close()

    return True

def crear_etc_default_keyboard(mnt, cfg, key):
    pattern = "^XKBLAYOUT=*"
    re_obj = re.compile(pattern)
    new_value = "XKBLAYOUT=\"" + key + "\"\n"

    file_path = mnt + cfg
    infile = open(file_path, "r")
    string = ''

    # Busca el valor del pattern
    is_match = False
    for line in infile:
        match = re_obj.search(line)
        if match :
            is_match = True
            string += new_value
        else:
            string += line
    infile.close()

    # Si no encuentra el pattern lo agrega al final con el valor asignado
    if not is_match:
        string += new_value

    # Escribe el archivo modificado
    outfile = open(file_path, "w")
    outfile.write(string)
    outfile.close()

    return True

def crear_etc_fstab(mnt, cfg, mountlist, cdroms):
    defaults = 'defaults\t0\t0'
    content = '#<filesystem>\t<mountpoint>\t<type>\t<options>\t<dump>\t<pass>\n'
    content += '\nproc\t/proc\tproc\t{0}'.format(defaults)

    for part, point, fs in mountlist:
        uuid = get_uuid(part)
        point = point.replace(mnt, '')

        if fs == 'swap':
            content += "\n{0}\tnone\tswap\tsw\t0\t0".format(uuid)
        else:
            content += '\n{0}\t{1}\t{2}\t{3}'.format(uuid, point, fs, defaults)
            ProcessGenerator('mkdir -p {0}'.format(mnt + point))

    for cd in cdroms:
        num = cd[-1:]
        content += '\n/dev/{0}\t/media/cdrom{1}\tudf,iso9660\tuser,noauto\t0\t0'.format(cd, num)
        ProcessGenerator('mkdir -p {0}'.format(mnt + '/media/cdrom' + num))

    content += '\n'
    f = open(mnt + cfg, 'w')
    f.write(content)
    f.close()

    return True

def crear_passwd_group_inittab_mtab(mnt):
    if not filecmp.cmp('/usr/share/sysvinit/inittab', '{0}/etc/inittab'.format(mnt)):
        shutil.copy2('/usr/share/sysvinit/inittab', '{0}/etc/inittab'.format(mnt))

    f = open('{0}/etc/mtab'.format(mnt), 'w')
    f.write('')
    f.close()

    return True

def lista_cdroms():
    info = '/proc/sys/dev/cdrom/info'
    if os.path.exists(info):
        cmd = 'cat {0}| grep "drive name:" | sed "s/drive name://g"'.format(info)
        salida = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            ).communicate()[0].split()
    else:
        salida = []

    return salida

def get_uuid(particion):
    uid = particion
    cmd = '/sbin/blkid -p {0}'.format(particion)
    salida = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        ).communicate()[0].split()

    for i in salida:
        if re.search('^UUID=*', i):
            uid = i            

    return uid.replace('"', '')

# Orden de las columnas en la tabla de particiones
class TblCol:
    DISPOSITIVO = 0
    TIPO = 1
    FORMATO = 2
    MONTAJE = 3
    TAMANO = 4
    USADO = 5
    LIBRE = 6
    INICIO = 7
    FIN = 8
    FORMATEAR = 9
    ESTADO = 10

class PStatus:
    NORMAL = 'NORM'
    NEW = 'NUEV'
    REDIM = 'REDI'
    USED = 'USAR'
    FREED = 'LIBE'

def givemeswap():
    r = ram()
    if r >= float(1024 * 1024):
        return r
    else:
        return r * 2

class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"

def draw_rounded(cr, area, radius):
    x1, y1, x2, y2 = area
    cr.arc(x1 + radius, y1 + radius, radius, 2 * (math.pi / 2), 3 * (math.pi / 2))
    cr.arc(x2 - radius, y1 + radius, radius, 3 * (math.pi / 2), 4 * (math.pi / 2))
    cr.arc(x2 - radius, y2 - radius, radius, 0 * (math.pi / 2), 1 * (math.pi / 2))
    cr.arc(x1 + radius, y2 - radius, radius, 1 * (math.pi / 2), 2 * (math.pi / 2))
    cr.close_path()
    return cr

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv / 3], 16) for i in range(0, lv, lv / 3))

def process_color(item, start, end):
    start = hex_to_rgb(start) + (0,)
    end = hex_to_rgb(end) + (1,)

    r1, g1, b1, pos = start
    r3, g3, b3, pos = end
    r2, g2, b2, pos = (int(r1 + r3) / 2, int(g1 + g3) / 2, int(b1 + b3) / 2, 0.5)
    mid = (r2, g2, b2, pos)

    for i in start, mid, end:
        rgb = float(i[3]), float(i[0]) / 255, float(i[1]) / 255, float(i[2]) / 255
        item.add_color_stop_rgb(*rgb)

def set_color(fs, alto):
    libre = cairo.LinearGradient(0, 0, 0, alto)

    if fs == 'btrfs':
        process_color(libre, '#ff5d2e', '#ff912e')
    elif fs == 'ext2':
        process_color(libre, '#2460c8', '#2e7bff')
    elif fs == 'ext3':
        process_color(libre, '#1b4794', '#2460c8')
    elif fs == 'ext4':
        process_color(libre, '#102b58', '#1b4794')
    elif fs == 'fat16':
        process_color(libre, '#00b900', '#00ff00')
    elif fs == 'fat32':
        process_color(libre, '#008100', '#00b900')
    elif fs == 'ntfs':
        process_color(libre, '#003800', '#008100')
    elif fs == 'hfs+':
        process_color(libre, '#382720', '#895f4d')
    elif fs == 'hfs':
        process_color(libre, '#895f4d', '#e49e80')
    elif fs == 'jfs':
        process_color(libre, '#e49e80', '#ffcfbb')
    elif fs == 'swap':
        process_color(libre, '#650000', '#cc0000')
    elif fs == 'reiser4':
        process_color(libre, '#45374f', '#806794')
    elif fs == 'reiserfs':
        process_color(libre, '#806794', '#b994d5')
    elif fs == 'xfs':
        process_color(libre, '#e89900', '#e8d000')
    elif fs == 'free':
        process_color(libre, '#ffffff', '#ffffff')
    elif fs == 'extended':
        process_color(libre, '#7dfcfe', '#7dfcfe')
    elif fs == 'unknown':
        process_color(libre, '#000000', '#000000')
    elif fs == 'part':
        process_color(libre, '#b8b598', '#b8b598')

    return libre

def floatify(num):
    '''
        Convierte un número escrito en formato para lectura por humanos a
        kilobytes.
        Argumentos:
        - num: un número en formato para lectura por humanos de tipo string
        Salida: el valor en kB de tipo float
    '''
    if not num:
        num = 0

    num = str(num)
    unidad = re.sub('[0123456789.]', '', num.replace(',', '.').upper())
    peso = float(re.sub('[TGMKB]', '', num.replace(',', '.').upper()))

    if unidad == 'TB':      kb = peso * 1024.0 * 1024.0 * 1024.0    # TB a KB
    elif unidad == 'GB':    kb = peso * 1024.0 * 1024.0             # GB a KB
    elif unidad == 'MB':    kb = peso * 1024.0                      # MB a KB
    elif unidad == 'KB':    kb = peso                               # KB a KB
    elif unidad == 'B':     kb = peso / 1024.0                      # B a KB
    else:                   kb = peso                               # Sin unidad
    return float(kb)

def redondear(w, dec=0):
    if type(w) == int : return w
    if dec == 0:
        return int(w) + 1 if int(str(w).split('.')[1][0]) >= 5 else int(w)
    else:
        return float(str(w).split('.')[0] + '.' + str(w).split('.')[1][0:dec])

def humanize(valor):
    valor = float(valor)
    if valor <= 1024.0: return '{0}KB'.format(redondear(valor, 2))
    if valor <= 1048576.0: return '{0}MB'.format(redondear(valor / 1024, 2))
    if valor <= 1073741824.0: return '{0}GB'.format(redondear(valor / 1024 / 1024, 2))
    return valor

def ram():
    return 1024.0 * float(subprocess.Popen(
        'echo "scale=1;$( cat "/proc/meminfo" | grep "MemFree:" | awk \'{print $2}\' )/(10^3)" | bc',
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    ).communicate()[0].split())

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

def random_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return hashlib.sha1(''.join(random.choice(chars) for x in range(size))).hexdigest()

def crypt_generator(arg):
    return crypt.crypt(arg, random_generator())

def ProcessGenerator(command):
    filename = '/tmp/canaimainstalador-' + random_generator()

    if isinstance(command, list):
        strcmd = ' '.join(command)
    elif isinstance(command, str):
        strcmd = command

    print strcmd
    cmd = '{0} 1>{1} 2>&1'.format(strcmd, filename)

    try:
        os.mkfifo(filename)
        fifo = os.fdopen(os.open(filename, os.O_RDONLY | os.O_NONBLOCK))
        process = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
                )
        while process.returncode == None:
            process.poll()
            try:
                line = fifo.readline().strip()
            except:
                continue
            if line != '':
                print line
    finally:
        os.unlink(filename)

    return process

class ThreadGenerator(threading.Thread):
    def __init__(
        self, reference, function, params,
        gtk=False, window=False, event=False
        ):
        threading.Thread.__init__(self)
        self._gtk = gtk
        self._window = window
        self._function = function
        self._params = params
        self._event = event
        self.start()

    def run(self):
        if self._gtk:
            gtk.gdk.threads_enter()

        if self._event:
            self._event.wait()

        self._function(**self._params)

        if self._gtk:
            gtk.gdk.threads_leave()

        if self._window:
            self._window.hide_all()

def get_sector_size(device):
    'Retorna el tamaño en Kb de cada sector'
    dev = parted.Device(device)
    return dev.sectorSize / 1024.0

def debug_list(the_list, n_spc=0):

    space = ""
    nw_line = ""
    data = ""

    if n_spc > 0:
        space = "\t" * n_spc

    the_type = type(the_list)

    if isinstance(the_list, list) or isinstance(the_list, tuple) or isinstance(the_list, dict):
        nw_line = "\n"
        for fila in the_list:

            if isinstance(the_list, dict):
                data += "{0}{1}{2}:".format(nw_line, '\t' * (n_spc + 1), fila)
                fila = the_list[fila]

            data += nw_line + debug_list(fila, n_spc + 1)
    else:
        data = the_list

    string = "{0}{1} [{2}]{3}".format(space, the_type, data, nw_line)

    return string

def get_row_index(the_list, row):
        '''Obtiene el numero de la fila seleccionada en la tabla'''
        try:
            return the_list.index(list(row))
        except ValueError:
            return None

def has_next_row(the_list, row_index):
    'Verifica si la lista contiene una fila siguiente'
    if  row_index < len(the_list) - 1:
        return True
    else:
        return False

def get_next_row(the_list, row, row_index=None):
    '''Retorna la fila siguiente si existe'''
    if row_index == None:
        row_index = get_row_index(the_list, row)

    if row_index != None and has_next_row(the_list, row_index):
        return the_list[row_index + 1]
    else:
        return None

def is_logic(row):
        'Determina si una particion es lógica'
        return row[TblCol.TIPO] == msj.particion.logica

def is_free(row):
        '''Determina si una particion es un espacio libre, idependientemente
        de si es Primaria o Logica'''
        return row[TblCol.FORMATO] == msj.particion.libre

def has_extended(lista):
        'Determina si existe por lo menos una particion extendida en la lista'
        for fila in lista:
            if fila[TblCol.TIPO] == msj.particion.extendida:
                return True
        return False

def set_partition(the_list, selected_row, new_row, pop=True):
    '''Agrega una nueva particion a la lista en el sitio adecuado segun su
    inicio'''
    index = get_row_index(the_list, selected_row)
    if pop:
        the_list[index] = new_row
    else:
        the_list.append(new_row)

    return the_list

def is_primary(row, with_extended=True):
    'Determina si una particion es primaria'
    p_type = row[TblCol.TIPO]
    if p_type == msj.particion.primaria \
    or (with_extended and p_type == msj.particion.extendida):
        return True
    else:
        return False

def is_usable(selected_row):
    'Determina si una particion puede ser usada (editada) en el part. manual'
    disp = selected_row[TblCol.DISPOSITIVO]
    tipo = selected_row[TblCol.TIPO]
    try:
        # Esta linea comprueba que el dispositivo termine en un entero, esto
        # para comprobar que tiene un formato similar a /dev/sdb3 por ejemplo.
        int(disp[-1])

        # No se usan las particiones extendidas, sino las logicas
        # Tampoco se usan particiones que no estan en estado Normal
        if tipo == msj.particion.extendida:
            return False
        else:
            return True
    except (ValueError, IndexError):
        return False

def is_resizable(fs):
    'Determina si un filesystem tiene herramienta de redimension'
    try:
        if FSPROGS[fs][1][0] == '':
            return False
        else:
            return True
    except KeyError:
        # Retorna False para el caso en que TblCol.FORMATO es igual a '' o a
        # 'Espacio libre' por ejemplo
        return False

def validate_minimun_fs_size(formato, tamano):
    if tamano < FSMIN[formato]:
        return False
    else:
        return True

def validate_maximun_fs_size(formato, tamano):
    if formato in FSMAX and tamano > FSMAX[formato]:
        return False
    else:
        return True

if __name__ == "__main__":
    print debug_list([1, 2])
    print debug_list({"casa":[1]})
    print debug_list("la casa")
    print debug_list(12.0)
    print debug_list(gtk)


