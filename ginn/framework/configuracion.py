#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008 Francisco José Rodríguez Bogado,                    #
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

"""
Parámetros aceptados en fichero de configuración ginn.conf:
nombre_parametro            : (valores aceptados|"tipo") [valor por defecto] Descripción
tipobd                      : (postgres, sqlite, mysql, firebird) [postgres] Tipo de base de datos a la que conecar.
user                        : ("string") [] Nombre de usuario para la conexión.
pass                        : ("string") [] Contraseña para acceder a la BD. 
dbname                      : ("string") [] Nombre de la base de datos a la que conectar.
host                        : ("string") [] IP del servidor.
logo                        : ("string") [logo_gtx.jpg] Logotipo que aparecerá en el menú principal e informes.
title                       : ("string") [Geotex-INN] Nombre de la aplicación.
port                        : ("int") [5432] Puerto para conectar al SGBD. 
diradjuntos                 : ("string") [adjuntos] Directorio donde guardar los ficheros adjuntos.
anchoticket                 : ("int") [48] Número de columnas de la impresora de tiques.
largoticket                 : ("int") [0] Número de líneas a avanzar al terminarde imprimir el tique y antes del corte.
codepageticket              : (0|1) [1] Si 0 el TPV no intentará usar códigos de escape cambiando el juego de caracteres de la impresora.
cajonserie                  : (0|1) [0] 0: Puerto paralelo para abrir el cajón portamonedas (LPT1, /dev/lp0). 1: Puerto serie (COM1, /dev/ttyS0). 
mostrarcontactoenticket     : (0|1) [1] Si 1, muestra el nombre del contacto de la empresa bajo el nombre de la propia empresa en el ticket.
puerto_ticketera            : (/dev/lp{0-9}|LPT{1-9}) [/dev/lp0|LPT1] Puerto donde está conectada la impresora de tiques. Si el programa se ejecuta en una plataforma UNIX-like, el valor por defecto es /dev/lp0. Si es Windos, LPT1.
desplegar_tickets           : (0|1) [1] Indica, si es 1, que debe desglosar los tiques en la ventana de TPV por defecto.
oki                         : (0|1) [0] Si 0 se asume que la impresora es OKIPOS -derivado de comandos STAR-. Si 1 se usarán comandos POS estándar.
valorar_albaranes           : (0|1) [0] Si 1 imprime los albaranes de salida valorados.
valorar_albaranes_con_iva   : (0|1) [1] Si 1 imprime la valoración de los albaranes con el IVA incluido.
carta_portes                : (0|1) [0] Si 1 se imprime una carta de portes en los albaranes de salida. Si es 0, en su lugar ofrecerá la opción de generar un impreso CMR.
multipagina                 : (0|1) [0] Si 1 usa un formato multipágina para albaranes y facturas. Incompatible con albaranes valorados. Mayor prioridad que la opción valorar_albaranes*.
diastpv                     : ("int") [3] Número de días a mostrar en el histórico de tiques de la ventana Terminal Punto de Venta.
ventanas_sobre              : (cf|fc) [cf] Orden horizontal de las direcciones al imprimir albaranes y facturas: Dirección de correspondencia y fiscal o al contrario.
modelo_presupuesto          : ("string") [presupuesto] Nombre del módulo a importar (sin el «.py») para generar el PDF de los presupuestos.
"""

import os

class Singleton(type):
    """
    Patrón Singleton para evitar que una misma instancia del programa trabaje 
    con varias configuraciones:
    """
    def __init__(self, *args):
        type.__init__(self, *args)
        self._instances = {}
    def __call__(self, *args):
        if not args in self._instances:
            self._instances[args] = type.__call__(self, *args)
        return self._instances[args]

class ConfigConexion:
    """
    Clase que recoge los parámetros de configuración
    a partir de un archivo.
    """
    __metaclass__ = Singleton

    def __init__(self, fileconf = 'ginn.conf'):
        if fileconf == None:
            fileconf = "ginn.conf"
        if os.sep in fileconf:
            fileconf = os.path.split(fileconf)[-1]
        self.__set_conf(fileconf)

    def __set_conf(self, fileconf):
        """
        Abre el fichero de configuración y parsea la información del mismo.
        """
        self.__fileconf = fileconf
        if not os.path.exists(self.__fileconf):
            self.__fileconf = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), fileconf)
        if not os.path.exists(self.__fileconf):
            self.__fileconf = os.path.join('framework', fileconf)
        if not os.path.exists(self.__fileconf):
            self.__fileconf = os.path.join('..', 'framework', fileconf)
        if not os.path.exists(self.__fileconf):
            # Es posible que estemos en un directorio más interno. Como por 
            # ejemplo, cuando se genera la documentación.
            self.__fileconf = os.path.join('..', '..', 'framework', fileconf)
        try:
            self.__fileconf = open(self.__fileconf)
        except IOError:
            print "ERROR: configuracion::__set_conf -> Fichero de "\
                  "configuración %s no encontrado (%s)." % (fileconf, 
                                                            self.__fileconf)
            self.__fileconf = None
            self.__conf = {}
        else:
            self.__conf = self.__parse()
            self.__fileconf.close()

    def set_file(self, fileconf):
        """
        Cambia el fichero de configuración y la configuración en sí por el recibido.
        """
        self.__set_conf(fileconf)

    def __parse(self):
        conf = {}
        l = self.__fileconf.readline()
        while l != '':
            l = l.replace('\t', ' ').replace('\n', '').split()
            if l and not l[0].startswith("#"):   
                # Ignoro líneas en blanco y las que comienzan con #
                conf[l[0]] = " ".join([p for p in l[1:] if p.strip() != ""])
            l = self.__fileconf.readline()
        return conf

    def get_tipobd(self):
        return self.__conf['tipobd']
        
    def get_user(self):
        return self.__conf['user']
    
    def get_pass(self):
        return self.__conf['pass']

    def get_dbname(self):
        return self.__conf['dbname']
        
    def get_host(self):
        return self.__conf['host']

    def get_logo(self):
        try:
            logo = self.__conf['logo']
        except KeyError:
            logo = "logo_gtx.png"       # Logo genérico
        return logo

    def get_title(self):
        """
        Título de la aplicación que se mostrará en el menú principal.
        """
        try:
            title = self.__conf['title']
        except KeyError:
            title = "Geotex-INN"
        return title
    
    def get_puerto(self):
        """
        Devuelve el puerto de la configuración o el puerto por defecto 5432 
        si no se encuentra.
        """
        try:
            puerto = self.__conf['port']
        except KeyError:
            puerto = '5432'
        return puerto

    def get_dir_adjuntos(self):
        """
        Devuelve el directorio donde se guardarán los adjuntos. Por defecto 
        "adjuntos". La ruta debe ser un único nombre de directorio y se 
        alojará como subdirectorio del "raíz" de la aplicación. Al mismo 
        nivel que "framework", "formularios", etc.
        """
        try:
            ruta = self.__conf['diradjuntos']
        except KeyError:
            ruta = "adjuntos"
        return ruta

    def get_anchoticket(self):
        try:
            ancho = int(self.__conf['anchoticket'])
        except (KeyError, TypeError, ValueError):
            ancho = 48
        return ancho

    def get_largoticket(self):
        """
        Líneas del ticket por detrás de la última línea
        antes de enviar el corte al puerto.
        """
        try:
            largo = int(self.__conf['largoticket'])
        except (KeyError, TypeError, ValueError):
            largo = 0
        return largo

    def get_codepageticket(self):
        """
        Algunas ticketeras no soportan codepages configurables 
        mediante códigos de escape (p. ej. la SAMSUNG SRP 270 C).
        Si este parámetro de configuración es False no intentará
        cambiar el codepage en el TPV.
        """
        try:
            set_c = bool(int(self.__conf['codepageticket']))
        except (KeyError, TypeError, ValueError):
            set_c = True
        return set_c

    def get_cajonserie(self):
        """
        Devuelve True si el cajón portamonedas opera por puerto 
        serie. False si opera a través de la impresora de ticket 
        por el puerto paralelo.
        Si en la configuración no se especifica toma la última
        opción (paralelo) por defecto.
        """
        try:
            cajonserie = bool(int(self.__conf['cajonserie']))
        except (KeyError, TypeError, ValueError):
            cajonserie = False
        return cajonserie

    def get_mostrarcontactoenticket(self):
        """
        Devuelve True si se debe mostrar el nombre de contacto bajo el 
        nombre de la empresa en el ticket.
        False en caso contrario.
        Valor por defecto es True.
        """
        try:
            mostrarcontactoenticket = bool(int(self.__conf['mostrarcontactoenticket']))
        except (KeyError, TypeError, ValueError):
            mostrarcontactoenticket = False
        return mostrarcontactoenticket

    def get_puerto_ticketera(self):
        """
        Devuelve el puerto paralelo por donde opera la impresora de tickets.
        Por defecto /dev/lp0 si el sistema es UNIX y LPT1 en otro caso.
        """
        from os import name as osname
        try:
            puerto = self.__conf['puerto_ticketera']
        except KeyError:
            if osname == "posix":
                puerto = "/dev/lp0"
            else:
                puerto = "LPT1"
        return puerto

    def get_desplegar_tickets(self):
        """
        Devuelve True si se deben desplegar todos los tickets en el TPV.
        False para desplegar únicamente el último.
        Por defecto True.
        """
        try:
            desplegar = bool(int(self.__conf['desplegar_tickets']))
        except (KeyError, TypeError, ValueError):
            desplegar = True
        return desplegar

    def get_oki(self):
        """
        Devuelve True si en la configuración hay una entrada «oki 1».
        Por defecto es False (impresora de tickets es POS estándar y no 
        OKIPOS -derivado de comandos STAR-).
        """
        try:
            okipos = bool(int(self.__conf['oki']))
        except (KeyError, TypeError, ValueError):
            okipos = False
        return okipos

    def get_valorar_albaranes(self):
        """
        Devuelve True si los albaranes deben imprimirse valorados.
        Por defecto es False.
        """
        try:
            valorar = bool(int(self.__conf['valorar_albaranes']))
        except (KeyError, TypeError, ValueError):
            valorar = False
        return valorar

    def get_valorar_albaranes_con_iva(self):
        """
        Devuelve True si los albaranes deben imprimirse valorados con IVA 
        incluido en precio unitario y total del línea.
        Por defecto es True.
        """
        try:
            valorar = bool(int(self.__conf['valorar_albaranes_con_iva']))
        except (KeyError, TypeError, ValueError):
            valorar = True
        return valorar

    def get_carta_portes(self):
        """
        Devuelve True si los albaranes deben imprimirse en forma de 
        carta de portes.
        Por defecto es False.
        CMR y carta_portes son excluyentes (ver albaranes_de_salida.py).
        """
        try:
            carta_portes = bool(int(self.__conf['carta_portes']))
        except (KeyError, TypeError, ValueError):
            carta_portes = False
        return carta_portes

    def get_multipagina(self):
        """
        Devuelve 1 si los albaranes y facturas deben imprimirse  
        con el formato multipágina (alias "sobrio con tabla continua").
        Si devuelve 2, entonces solo los albaranes se imprimen con este 
        formato. Las facturas salen con el formato tradicional.
        Por defecto es 0 (False).
        NOTA: Esta opción tiene prioridad sobre la de valorar albaranes.
        """
        try:
            #multipagina = bool(int(self.__conf['multipagina']))
            multipagina = int(self.__conf['multipagina'])
        except (KeyError, TypeError, ValueError):
            #multipagina = False
            multipagina = 0
        return multipagina

    def get_diastpv(self):
        """
        Número de días a mostrar en la lista de últimas 
        ventas del TVP.
        """
        try:
            dias = int(self.__conf['diastpv'])
        except (KeyError, TypeError, ValueError):
            dias = 3
        return dias

    def get_orden_ventanas(self):
        """
        Orden de las ventanas "Dirección correspondencia" y "Dirección 
        fiscal" en las facturas de venta. Por defecto "cf" (correspondencia 
        a la izquierda, fiscal a la derecha).
        """
        try:
            orden = self.__conf['ventanas_sobre'].strip().lower()
            assert len(orden) == 2 and 'c' in orden and 'f' in orden
        except(KeyError, ValueError, TypeError, AssertionError):
            orden = "cf"
        return orden

    def get_modelo_presupuesto(self):
        """
        Devuelve una cadena con el nombre del módulo que contiene el modelo 
        de presupuesto (el que no es tipo carta).
        Si no se especifica, se usa el por defecto: presupuesto
        Por supuesto, si se implementan modelos nuevos deben cumplir la 
        interfaz -no definida formalmente de momento- con los procedimientos 
        "go", "go_from_presupuesto", etc.
        """
        try:
            modulo = self.__conf["modelo_presupuesto"].strip().lower()
        except (KeyError, ValueError, TypeError):
            modulo = "presupuesto"
        return modulo

    def get_precision(self):
        """
        Devuelve la precisión con la que calcular los subtotales de las 
        líneas de venta. Por defecto es None, que significa sin redondear.
        Se puede poner a cualquier entero positivo o dejar vacío para None.
        """
        try:
            precision = self.__conf["precision"].strip().lower()
            if precision != "" and precision != None:
                precision = int(precision)
                assert precision >= 0
        except (KeyError, ValueError, TypeError):
            precision = None 
        except AssertionError:
            print "configuracion::precision debe ser entero positivo o None."
            precision = None
        return precision

def unittest():
    """
    Pruebas unitarias del patrón Singleton.
    """
    class Test:
        __metaclass__=Singleton
        def __init__(self, *args): pass
            
    ta1, ta2 = Test(), Test()
    assert ta1 is ta2
    tb1, tb2 = Test(5), Test(5)
    assert tb1 is tb2
    assert ta1 is not tb1

def guess_class(modulo):
    # Lo mismo es mejor con esto: http://docs.python.org/2/library/imp.html
    exec "from formularios import " + modulo
    exec "moduler = " + modulo
    clases = [c for c in dir(moduler) if c[0].isupper() 
                                        and c != "Ventana" 
                                        and c != "VentanaGenerica"]
    return clases[0]
    
    
def parse_params():
    """
    Analiza los parámetros recibidos en línea de comandos y devuelve usuario 
    y contraseña, que pueden ser None si no se han especificado.
    Si encuentra fichero de configuración y opciones verbose|debug las activa 
    internamente, pero no devuelve su estado. Para saber qué valores han 
    tomado se debe consultar a la clase ConfigConexion o a pclases.
    """
    import optparse
    desc = "Inicia la aplicación con el usuario especificado según la "\
           "configuración indicada. Si no se recibe fichero, se usará por "\
           "defecto «ginn.conf». Si no se escribe contraseña, se solicitará."
    parser = optparse.OptionParser(description = desc)
    parser.add_option('-u', '--user', help = "Usuario a autenticar", 
                      action = "store", type = "string", dest = "user")
    parser.add_option('-p', '--password', help = "Contraseña", 
                      action = "store", type ="string", dest = "password")
    parser.add_option('-c', '--config', help = "Fichero de configuración", 
                      action = "store", type = "string", dest = "config", 
                      default = "ginn.conf")
    parser.add_option('-v', action = "store_true", dest = "verbose", 
                      default = False)
    parser.add_option('-d', action = "store_true", dest = "debug", 
                      default = False)
    parser.add_option('-w', "--window", help = "Ventana a iniciar", 
                      action = "store", type = "string", dest = "ventana")
    parser.add_option('-o', "--object", 
                      help = "Objeto a abrir al inicio de la ventana", 
                      action = "store", type = "string", dest = "puid", 
                      default = None)
    (opts, args) = parser.parse_args()
    # Por compatibilidad hacia atrás, voy a tomar los argumentos posicionales 
    # como usuario y contraseña si no se especifica nada en las opciones.
    if not opts.user:
        try:
            user = args[0]
        except IndexError:
            user = None
    else:
        user = opts.user
    if not opts.password:
        try:
            password = args[1]
        except IndexError:
            password = None
    else:
        password = opts.password
    # Fichero de configuración
    if not os.path.exists(opts.config):
        config = os.path.join(
                os.path.abspath(os.path.dirname(os.path.realpath(__file__))), 
                "..", "framework", opts.config)
    else:
        config = opts.config
    config = os.path.realpath(config)
    ConfigConexion().set_file(config) # Lo hago así porque en todos sitios se 
        # llama al constructor sin parámetros, y quiero instanciar al 
        # singleton por primera vez aquí.
        # Después pongo la configuración correcta en el archivo y en sucesivas
        # llamadas al constructor va a devolver el objeto que acabo de crear y
        # con la configuración que le acabo de asignar. En caso de no recibir
        # fichero de configuración, la siguiente llamada al constructor será
        # la que cree el objeto y establezca la configuración del programa.
        # OJO: Dos llamadas al constructor con parámetros diferentes crean
        # objetos diferentes.    
    # Ventana: módulo + clase
    # A partir del nombre de la ventana, saco el fichero y clase a instanciar.
    if opts.ventana:
        if opts.ventana.endswith(".py"):
            modulo = opts.ventana[:-3]
        else:
            modulo = opts.ventana
        modulo = os.path.basename(modulo)
        try:
            clase = guess_class(modulo)
        except:
            clase = None    # PORASQUI: Habría que determinar el nombre de la 
                            # clase de la ventana. ¿Puedo tirar de pclases para
                            # saberlo según la tabla de ventanas, o me tiro a 
                            # por un grep? ¿Y en Windows, que no hay grep, qué?
                            # ¿Parseo el .py completo hasta encontrar class *?
    else:
        modulo, clase = None, None
    # Resto de parámetros
    verbose = opts.verbose
    debug = opts.debug
    return user, password, modulo, clase, config, verbose, debug, opts.puid

