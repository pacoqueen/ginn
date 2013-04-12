#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
#                          Diego Muñoz Escalante.                             #
# (pacoqueen@users.sourceforge.net, escalant3@users.sourceforge.net)          #
#                                                                             #
# This file is part of GeotexInn.                                             #
#                                                                             #
# GeotexInn is free software; you can redistribute it and/or modify           #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# GeotexInn is distributed in the hope that it will be useful,                #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with GeotexInn; if not, write to the Free Software                    #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################


###################################################################
## informes.py - Ventana que lanza los informes en PDF. 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 29 de noviembre de 2005 -> Inicio 
## 30 de noviembre de 2005 -> 50% funcional
###################################################################
## TODO:
## - Mostrar opciones de filtro de datos a imprimir 
## 
###################################################################

import pygtk
pygtk.require('2.0')
import os
import sys
from formularios import utils

def abrir_pdf(pdf):
    """
    Ejecuta una aplicación para visualizar el pdf en pantalla.
    Si es MS-Windows tiro de adobre acrobat (a no ser que encuentre
    algo mejor, más portable y empotrable). Si es UNIX-like lanzo
    el evince, que es más completito que el xpdf.
    Ni que decir tiene que todo eso debe instalarse aparte.
    """
    if not pdf or pdf is None:
        return 
    # TODO: Problemón. Al ponerle el ampersand para mandarlo a segundo plano, 
    # sh siempre devuelve 0 como salida del comando, así que no hay manera de 
    # saber cuándo se ha ejecutado bien y cuándo no.
    if os.name == 'posix':
        # OJO(Diego) Lo he cambiado por un problema de dependencias y el evince
        if not ((not os.system("evince %s &" % pdf)) or \
                (not os.system("acroread %s &" % pdf)) or \
                (not os.system("xdg-open %s &" % pdf)) or \
                (not os.system("gnome-open %s &" % pdf)) or \
                (not os.system("xpdf %s &" % pdf))):
            utils.dialogo_info(titulo = "VISOR PDF NO ENCONTRADO", 
                               texto = "No se encontró evince, acroread ni xpdf en el sistema.\nNo fue posible mostrar el archivo %s." % (pdf))
    else:
        # OJO: Esto no es independiente de la plataforma:
        os.startfile(pdf)  # @UndefinedVariable

def abrir_csv(csv, ventana_padre = None):
    """
    Si la plataforma es MS-Windows abre el archivo con la aplicación 
    predeterminada para los archivos CSV (por desgracia me imagino que 
    MS-Excel). Si no, intenta abrirlo con OpenOffice.org Calc.
    """
    # TODO: Problemón. Al ponerle el ampersand para mandarlo a segundo plano, sh siempre devuelve 0 como salida del comando, 
    # así que no hay manera de saber cuándo se ha ejecutado bien y cuándo no.
    if sys.platform != 'win32':     # Más general que os.name (que da "nt" en 
                                    # los windows 2000 de las oficinas).
        try:
            res = os.system('xdg-open "%s" &' % csv)
            assert res == 0
        except AssertionError:
            if not ( (not os.system('oocalc2 "%s" || oocalc "%s" &'%(csv,csv)))
                    or (not os.system('oocalc "%s" &' % csv)) 
                   ):
                utils.dialogo_info(titulo = "OOO NO ENCONTRADO", 
                                   texto = "No se encontró OpenOffice.org en el sistema.\nNo fue posible mostrar el archivo %s." % (csv), 
                                   padre = ventana_padre) 
    else:
        # OJO: Esto no es independiente de la plataforma:
        os.startfile(csv)  # @UndefinedVariable

def mandar_a_imprimir_con_ghostscript(fichero):
    """
    Lanza un trabajo de impresión a través de acrobat reader.
    Usa parámetros no documentados y oficialmente no soportados 
    por acrobat. Esta función es temporal, hasta que encuentre 
    un visor/impresor de PDF desde línea de comandos.
    Win-only. No funciona en posix ni aún teniendo el reader
    para esa plataforma (creo).
    NO USAR CON ROLLOS: No cuadra bien la etiqueta y además deja abierta la 
    ventana después.
    Impresora CAB harcoded (y además no es el nombre por defecto de la 
    impresora).
    ¡MENTIRA COCHINA! Lo hace a través de Ghostscript.
    """
    # OJO: Ruta al reader harcoded !!!
    #    comando = """"C:\\Archivos de programa\\Adobe\\Acrobat 6.0\\Reader\\AcroRd32.exe" /t "%s" GEMINI2 """ % (fichero)
    #    comando = """start /B AcroRd32 /t "%s" CAB """ % (fichero)
    comando = """gswin32c.exe -dQueryUser=3 -dNoCancel -dNOPAUSE -dBATCH"""\
              """ -sDEVICE=mswinpr2 -sOutputFile="%%printer%%CAB" %s """ % (
                fichero)
    # NOTA: Necesita que: 
    # 1.- La impresora CAB esté como predeterminada en la "carpeta" 
    #     impresoras de Windows.
    # 2.- Tenga la configuración adecuada por defecto (apaisado, tamaño de 
    #     etiqueta, etc.
    # 3.- gs esté en el PATH (añadiendo C:\Archivos de programa...\bin en la 
    #     variable de entorno PATH desde las propiedades avanzadas de Mi PC.)
    if os.system(comando):
        print "No se pudo hacer la impresión directa. Lanzo el visor."
        abrir_pdf(fichero)

def mandar_a_imprimir_con_foxit(fichero):
    """
    Lanza un trabajo de impresión a través de foxit reader o 
    LPR si el sistema es UNIX. 
    OJO: Siempre manda a la impresora por defecto.
    """
    import time
    time.sleep(1)  # Pausa para evitar que el PDF aún no esté en disco.
    if os.name == "posix":
        comando = """lpr %s""" % (fichero)
    else:
        # OJO: Ruta al reader harcoded !!!
        comando = """"C:\Archivos de programa\Foxit Software\Foxit Reader\Foxit Reader.exe" /p %s """ % (fichero)
    # print comando
    if os.system(comando):
        print "No se pudo hacer la impresión directa con:\n%s\n\nLanzo el visor." % comando
        abrir_pdf(fichero)

def get_ruta_ghostscript():
    """
    Devuelve la ruta al ejecutable gswin32.exe.
    Si no lo encuentra, devuelve None.
    """
    ruta = None
    ruta_por_defecto = os.path.join("C:\\", "Archivos de programa", "gs", "gs8.54", "bin", "gswin32c.exe")
    if os.path.exists(ruta_por_defecto):
        ruta = ruta_por_defecto
    else:
        pass
        # TODO: Debería buscar la ruta con os.walk y tal.
    return ruta

def imprimir_con_gs(fichero, impresora = None, blanco_y_negro = False):
    """
    Imprime el fichero (PDF o PostScript) a través de GhostScript.
    Si impresora es None, imprime sin intervención del usuario en la impresora
    por defecto.
    ¡SOLO PARA SISTEMAS MS-WINDOWS!
    """
    if os.name == "posix":
        abrir_pdf(fichero)
    else:
        # Anoto aquí las impresoras que hay rulando, aunque no se use.
        impresoras = {'oficina': ("RICOH Aficio 1224C PCL 5c", "OFICINA"),  # @UnusedVariable
                      'etiquetas': ("CAB", "CAB MACH 4 200DPI", "GEMINI2")}
        # XXX 
        ruta_a_gs = get_ruta_ghostscript()
        if ruta_a_gs == None:
            print "informes.py (imprimir_con_gs): GhostScript no encontrado."
            abrir_pdf(fichero)
        else:
            if impresora == None:
                por_defecto = " -dQueryUser=3 "
                impresora = ""
            else:
                por_defecto = "" 
                impresora = ' -sOutputFile="\\spool\%s" ' % (impresora)
            if blanco_y_negro:
                blanco_y_negro = " -dBitsPerPixel=1 "
            else:
                blanco_y_negro = ""
            comando = r'""%s" %s -dNOPAUSE -dBATCH -sDEVICE=mswinpr2 %s -dNoCancel %s "%s""' \
                % (ruta_a_gs, por_defecto, impresora, blanco_y_negro, fichero)
            try:
                salida = os.system(comando)
            except:
                salida = -1
            if salida != 0 and salida != 1: #gs devuelve 1 si le da a Cancelar.
                print "informes.py (imprimir_con_gs): No se pudo imprimir. "\
                      "Lanzo el visor."
                abrir_pdf(fichero)
            if salida == 1:     # Si cancela la impresión a lo mejor quiere 
                                # verlo en pantalla.
                abrir_pdf(fichero)

def que_simpatico_es_el_interprete_de_windows(comando, parametro):
    """
    El os.system llama a cmd /C y/o /K, y el cmd.exe es muy simpático y se 
    comporta como le da la gana. No sabe ni escapar los espacios de sus propias rutas, 
    por lo que como intentes ejecutar algo dentro de Archivos de programa... total, 
    que hay que encerrar todo entre comillas y otra vez entre comillas.
    mi nota: PUTAMIERDA
    ver: http://jason.diamond.name/weblog/2005/04/14/dont-quote-me-on-this
    """
    command = '"%s" "%s"' % (comando, parametro)
    if sys.platform[:3] == 'win':
        command = '"%s"' % command
    os.system(command)

## ---------------------- Rutina principal ------------------------
if __name__=='__main__':
    if len(sys.argv) < 1:
        print "ERROR: No se pasó el nombre de ningún informe"
        sys.exit(0)

    from informes import geninformes
    informe = ' '.join(sys.argv[1:])
    if informe == 'Clientes y consumo': 
        nombrepdf = geninformes.pedidosCliente()
    elif informe == 'Albaranes por cliente': 
        nombrepdf = geninformes.albaranesCliente()
    elif informe == 'Compras': 
        nombrepdf = geninformes.compras()
    elif informe == 'Ventas': 
        nombrepdf = geninformes.ventas()
    elif informe == 'Vencimientos pendientes de pago': 
    #   nombrepdf = geninformes.vecimientosPendientesDePago()
        utils.dialogo_info('FUNCIONALIDAD NO IMPLEMENTADA', 'Este informe aún no se puede generar.')
        sys.exit(0)
    elif informe == 'Vencimientos pendientes de pagar': 
        utils.dialogo_info('FUNCIONALIDAD NO IMPLEMENTADA', 'Este informe aún no se puede generar.')
        sys.exit(0)
    #   nombrepdf = geninformes.()
    #===========================================================================
    # elif informe == 'Productos bajo mínimo': 
    #     nombrepdf = geninformes.productosBajoMinimos()
    # elif informe == 'Albaranes por facturar': 
    #     nombrepdf = geninformes.albaranesPorFacturar()
    #===========================================================================
    elif informe == 'Albaranes facturados': 
        nombrepdf = geninformes.albaranesFacturados()
    elif informe == 'Existencias': 
        nombrepdf = geninformes.existencias()
    elif informe == 'Incidencias':
        nombrepdf = geninformes.incidencias()
    elif informe == 'Informes de laboratorio': 
        utils.dialogo_info('FUNCIONALIDAD NO IMPLEMENTADA', 'Este informe aún no se puede generar.')
        sys.exit(0)
    #   nombrepdf = geninformes.()
    elif informe == 'Comparativa de cobros y pagos':
        utils.dialogo_info('FUNCIONALIDAD NO IMPLEMENTADA', 'Este informe aún no se puede generar.')
        sys.exit(0)
    #   nombrepdf = geninformes.()
    else:
        print "El informe %s no existe" % informe
        sys.exit(0)
    abrir_pdf(nombrepdf)
    #os.unlink(nombrepdf)
    # Si lo borro no va a dar tiempo ni a que lo abra el evince. Que se
    # machaque la siguiente vez que se ejecute el mismo listado y punto.
    # (Hasta que se me ocurra algo mejor)

