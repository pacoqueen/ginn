#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2014  Francisco José Rodríguez Bogado,                   #
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
## albaranes.py -- Albaranes de salida de mercancía (ventas). 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 14 de octubre de 2005 -> Inicio
## 17 de octubre de 2005 -> 90% funcional
## 17 de octubre de 2005 -> 95% funcional
## 18 de octubre de 2005 -> 99% funcional
## 6 de diciembre de 2005 -> Añadido "multi" al añadir LDV de las
##                           ventas pendientes.
##                           Arreglado bug por un typo en un 
##                           articuloVenta que se había colado (en
##                           lugar de articuloventa, que es lo 
##                           correcto).
##                           Añanidos botones de smart_add y por 
##                           lotes.
## 9 de diciembre de 2005 -> Añadido IVA por defecto.
## 11 de enero de 2005 -> Añadido botón de imprimir.
## 19 de enero de 2005 -> Fork a v02
## 23 de enero de 2005 -> Encapsulado a clase.
## 27 de enero de 2005 -> Cambiada provincia por teléfono, pero 
##                        SOLO en la ventana. En la BD el campo 
##                        sigue teniendo el mismo nombre.
##                        Las observaciones que se imprimen son las
##                        del envío, ya no lo pide por diálogo.
## 27 de enero de 2006 -> Cambiado totalmente provincia por telefono, 
##                        tanto en la BD como en el formulario.
## 6 de junio de 2006 -> Añadidos servicios también al albarán.
## 12 de junio de 2006 -> Condición para que pregunte si debe 
##                        redistribuir únicamente si el albarán es
##                        nuevo o se ha modificado.
###################################################################
## + DONE: El funcionamiento del drop_ldv está pendiente de 
##         comprobar. Lo he ajustado lo más posible al caso de uso.
##         Es posible que genere demasiados pedidos vacíos, pero
##         al menos funciona como debería. De todas formas, hay que
##         probarlo más a fondo antes de poner en producción.
## + DONE: Falta bloquear el albarán después de 24/48 horas. ¿Cómo?
##         Forget about it. CWT: Se bloquea en cuanto se imprime.
## TODO: Al crear los vencimientos de la factura al imprimir no 
##       tiene en cuenta el IRPF.
## DONE: ES ***EXTREMADAMENTE*** LENTO CON LOS ALBARANES DE BOLSAS.
## TODO: Cuando se vendan cajas sueltas, la caja debe ser el bulto
##       en lugar del palé. Pero solo en ese caso.
###################################################################
## NOTAS: 
## Atención a las líneas de devolución. Ahora se cuentan sus 
## artículos incluso después de haberlos desvinculado del albarán.
## No hay problemas con volverlos a devolver en otro abono, ya que
## un mismo artículo soporta estar en varias líneas de devolución. 
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
from formularios.reports import abrir_pdf
pygtk.require('2.0')
import gtk, time
import sys
from framework import pclases
from informes import geninformes
from formularios.utils import ffloat
import mx.DateTime
from formularios.postomatic import attach_menu_notas
from formularios.ventana_progreso import VentanaProgreso


class AlbaranesDeSalida(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.modificado = False # Para detectar si el albarán en pantalla 
                                # se ha modificado en la sesión actual. 
        self.nuevo = False      # Para detectar si un albarán es nuevo.
        Ventana.__init__(self, 'albaranes_de_salida.glade', objeto,
                         usuario = self.usuario)
        connections = {'b_salir/clicked': self.pre_salir,
                       'b_fecha/clicked': self.buscar_fecha,
                       'b_drop_ldv/clicked': self.drop_ldv,
                       'b_add_pedido/clicked': self.add_pedido,
                       'b_add_producto/clicked': self.pedir_rango,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_borrar/clicked': self.borrar_albaran,
                       'b_nuevo/clicked': self.crear_nuevo_albaran,
                       'b_buscar/clicked': self.buscar_albaran,
                       'b_imprimir/clicked': self.imprimir,
                       'b_guardar_transportista/clicked': 
                            self.guardar_transportista,
                       'b_guardar_destino/clicked': self.guardar_destino,
                       'b_leyenda/clicked': self.ver_leyenda,
                       'b_packinglist/clicked': self.packinglist,
                       'b_add_srv/clicked': self.add_srv,
                       'b_drop_srv/clicked': self.drop_srv,
                       'ventana_leyenda/delete_event': self.ocultar_leyenda, 
                       'b_drop_transporteACuenta/clicked': 
                            self.drop_transporte_a_cuenta,
                       'b_add_transporteACuenta/clicked': 
                            self.add_transporte_a_cuenta, 
                       'b_drop_comision/clicked': self.drop_comision, 
                       'b_add_comision/clicked': self.add_comision, 
                       'expander1/activate': self.expandirme_solo_a_mi, 
                       'expander2/activate': self.expandirme_solo_a_mi, 
                       'expander3/activate': self.expandirme_solo_a_mi,
                       'expander4/activate': self.expandirme_solo_a_mi, 
                       'b_phaser/clicked': self.descargar_de_terminal, 
                       'cbe_almacenOrigenID/changed': self.check_almacenes, 
                       'cbe_almacenDestinoID/changed': self.check_almacenes, 
                       'ch_facturable/toggled': self.sombrear_entry_motivo, 
                       'cbe_cliente/changed': self.resaltar_credito
                      }
        self.add_connections(connections)
        if pclases.DEBUG:
            antes = time.time()
            print "Voy a inicializar la ventana..."
        self.inicializar_ventana()
        if pclases.DEBUG:
            print "    ... ventana inicializada. ", time.time() - antes
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def resaltar_credito(self, combo):
        """
        Colorea el combo del cliente para mostrar si tiene o no crédito.
        """
        idcliente = utils.combo_get_value(combo)
        if idcliente:
            cliente = pclases.Cliente.get(idcliente)
            cliente.sync()
            credito = cliente.calcular_credito_disponible()
            if credito == sys.maxint:   # ¿maxint, te preguntarás? Ver 
                                        # docstring de calcular_credito
                                        # y respuesta hallarás.
                strcredito = "∞"
                color = None
            else:
                strcredito = utils.float2str(credito)
                if credito <= 0:
                    color = combo.child.get_colormap().alloc_color("IndianRed1")
                else:
                    color = None
            # strfdp = cliente.textoformacobro
        else:
            strcredito = "¡UN «GRITÓN» DE DÓLARES!"
            # strfdp = "Subasta (de lata de anchoas)"
            color = None
        combo.set_tooltip_text(
            "Crédito disponible (sin contar el importe del albarán): %s\n"
            % strcredito)
        combo.child.modify_base(gtk.STATE_NORMAL, color)

    def sombrear_entry_motivo(self, ch):
        """
        Si el albarán es facturable sombrea el entry donde se escribe el 
        motivo por el que no sería facturable, y viceversa.
        """
        if self.objeto:
            self.wids['e_motivo'].set_sensitive(not self.objeto.facturable)
        else:
            self.wids['e_motivo'].set_sensitive(not ch.get_active())
        
    def check_almacenes(self, combo):
        """
        Comprueba que no se haya seleccionado el mismo almacén en los dos 
        desplegables y que el almacén origen no sea None.
        """
        ido = utils.combo_get_value(self.wids['cbe_almacenOrigenID'])
        idd = utils.combo_get_value(self.wids['cbe_almacenDestinoID'])
        # 1.- El almacén origen no puede ser None.
        if ido == None:
            utils.dialogo_info(titulo = "ERROR ALMACÉN ORIGEN", 
                texto = "Debe seleccionar un almacén origen. Se usará el\n"
                        "almacén principal como origen de la mercancía.", 
                padre = self.wids['ventana'])
            self.objeto.almacenOrigen = pclases.Almacen.get_almacen_principal()
            self.objeto.syncUpdate()
            utils.combo_set_from_db(self.wids['cbe_almacenOrigenID'], 
                                    self.objeto.almacenOrigenID, 
                                    forced_value = self.objeto.almacenOrigen 
                                        and self.objeto.almacenOrigen.nombre 
                                        or None)
            self.wids['cbe_almacenOrigenID'].child.set_text(
                self.objeto.almacenOrigen.nombre)
        # 2.- Si el almacén origen y destino son el mismo muestra diálogo de 
        # advertencia y pone el destino a None.
        elif ido == idd: 
            utils.dialogo_info(titulo = "ERROR ALMACENES", 
                texto = 
                  "No puede asignar el mismo almacén como origen y destino.", 
                padre = self.wids['ventana'])
            utils.combo_set_from_db(self.wids['cbe_almacenOrigenID'], 
                            pclases.Almacen.get_almacen_principal_id_or_none())
            utils.combo_set_from_db(self.wids['cbe_almacenDestinoID'], None)

    def expandirme_solo_a_mi(self, expander):
        """
        Oculta los otros 3 expanders de la página para no ocupar tanto sitio.
        """
        expanders = (self.wids['expander1'], self.wids['expander2'], self.wids['expander3'], self.wids['expander4']) 
        for ex in expanders:
            if ex != expander:
                ex.set_expanded(False)

    # --------------- Funciones auxiliares ------------------------------
    def inicializar_leyenda(self):
        ws = []
        ws.append(self.wids['dwg_amarillo'].window)
        ws.append(self.wids['dwg_naranja'].window)
        ws.append(self.wids['dwg_rojo'].window)
        ws.append(self.wids['dwg_blanco'].window)
        ws.append(self.wids['dwg_verde'].window)
        ws.append(self.wids['dwg_azul'].window)
        cs = ("yellow", "orange", "red", "white", "green", "blue")
        for i in xrange(len(cs)):   # Debe haber otra forma más "pythónica" 
                                    # de hacerlo, seguro.
            color = ws[i].get_colormap().alloc_color(cs[i])
            ws[i].set_background(color)
        self.wids['ventana_leyenda'].hide()
 
    def ocultar_leyenda(self, w, e):
        self.wids['ventana_leyenda'].hide()
        self.wids['b_leyenda'].set_active(False)
        return True #Quiero que siga vivo, que no me lo elimine.

    def ver_leyenda(self, w):
        if w.get_active():
            ws = []
            ws.append(self.wids['dwg_amarillo'].window)
            ws.append(self.wids['dwg_naranja'].window)
            ws.append(self.wids['dwg_rojo'].window)
            ws.append(self.wids['dwg_blanco'].window)
            ws.append(self.wids['dwg_verde'].window)
            ws.append(self.wids['dwg_azul'].window)
            ws.append(self.wids['dwg_RosyBrown3'].window)
            # TODO: Falta el gris de los productos C, que no ajustan 
            # cantidades según bultos agregados. Pero el glade-gtk2 
            # me da una violación de segmento.
            cs = ("yellow", "orange", "red", "white", "green", "blue", 
                  "RosyBrown3")
            for i in xrange(len(cs)):   # Debe haber otra forma más 
                                        # "pythónica" de hacerlo, seguro.
                color = ws[i].get_colormap().alloc_color(cs[i])
                ws[i].set_background(color)
            self.wids['ventana_leyenda'].show()
        else:
            self.wids['ventana_leyenda'].hide()

    def actualizar_destino(self, iddest):
        t = pclases.Destino.get(iddest)
        t.nombre = self.wids['cbe_nom'].child.get_text()
        t.direccion = self.wids['e_direccion'].get_text()
        t.cp = self.wids['e_cp'].get_text()
        t.ciudad = self.wids['e_ciudad'].get_text()
        t.telefono = self.wids['e_telf'].get_text()
        t.pais = self.wids['e_pais'].get_text()
        
    def actualizar_transportista(self, idtransp):
        t = pclases.Transportista.get(idtransp)
        t.nombre = self.wids['e_nombre'].get_text()
        t.dni = self.wids['cbe_dni'].child.get_text()
        t.telefono = self.wids['e_telefono'].get_text()
        t.agencia = self.wids['e_agencia'].get_text()
        t.matricula = self.wids['e_matricula'].get_text()
        
    def crear_nuevo_destino(self):
        destinos = pclases.Destino.select(pclases.AND(
            pclases.Destino.q.nombre == self.wids['cbe_nom'].child.get_text(), 
            pclases.Destino.q.direccion == self.wids['e_direccion'].get_text(), 
            pclases.Destino.q.cp == self.wids['e_cp'].get_text(), 
            pclases.Destino.q.ciudad == self.wids['e_ciudad'].get_text(), 
            pclases.Destino.q.telefono == self.wids['e_telf'].get_text(), 
            pclases.Destino.q.pais == self.wids['e_pais'].get_text()))
        if destinos.count() > 0:
            t = destinos[0]
        else:
            t = pclases.Destino(nombre = self.wids['cbe_nom'].child.get_text(), 
                                direccion=self.wids['e_direccion'].get_text(), 
                                cp = self.wids['e_cp'].get_text(), 
                                ciudad = self.wids['e_ciudad'].get_text(), 
                                telefono = self.wids['e_telf'].get_text(), 
                                pais = self.wids['e_pais'].get_text())
            pclases.Auditoria.nuevo(t, self.usuario, __file__)
            self.wids['cbe_nom'].get_model().append((t.id, t.nombre))
        utils.combo_set_from_db(self.wids['cbe_nom'], t.id)
        return t
        
    def crear_nuevo_transportista(self):
        t = pclases.Transportista(nombre = self.wids['e_nombre'].get_text(),
                                  dni = self.wids['cbe_dni'].child.get_text(),
                                  telefono = self.wids['e_telefono'].get_text(),
                                  agencia = self.wids['e_agencia'].get_text(),
                                  matricula = self.wids['e_matricula'].get_text())
        pclases.Auditoria.nuevo(t, self.usuario, __file__)
        self.wids['cbe_dni'].get_model().append((t.id, t.dni))
        utils.combo_set_from_db(self.wids['cbe_dni'], t.id)
    
    def refinar_busqueda_productos(self, resultados):
        filas_res = []
        for r in resultados:
            filas_res.append((r.id, r.codigo, r.nombre, r.descripcion, 
                              r.get_existencias(), r.get_stock()))
        idproducto = utils.dialogo_resultado(filas_res,
                                             titulo = 'Seleccione producto',
                                             cabeceras = ('ID Interno', 'Código', 'Nombre', 'Descripción', 'Existencias', 'Stock'), 
                                             padre = self.wids['ventana']) 
        if idproducto < 0:
            return None
        else:
            return idproducto

    def add_duplicado(self, codigo, albaran):
        """
        Añade el rollo o bala con código "codigo" al albarán siempre y 
        cuando el producto se hubiese pedido.
        Si codigo no es de la forma [rRbBcC]\d+[dD] da mensaje de error y 
        sale.
        NO ACEPTA RANGOS.
        Devuelve el objeto artículo añadido o None si no se pudo.
        """
        articulo_annadido = None
        import re
        recodigo = re.compile("[rRbBcC]\d+[Dd]")
        res = recodigo.findall(codigo)
        if res == []:
            utils.dialogo_info(titulo = "ERROR CÓDIGO", 
                               texto = "El texto %s no es un código válido.\nSi está intentando introducir productos duplicados por motivos excepcionales\n(su código acaba en D) no pueden ser añadidos por lote.\n\nIntrodúzcalos uno a uno usando el código de trazabilidad completo,\nes decir, comenzando por R, B o C y acabando en D.\nPor ejemplo: R78042D.", 
                               padre = self.wids['ventana'])
        else:
            codigo = res[0].upper()
            try:
                if codigo.startswith("R"):
                    articulo = pclases.Rollo.select(
                        pclases.Rollo.q.codigo == codigo)[0].articulos[0]
                elif codigo.startswith("B"):
                    articulo = pclases.Bala.select(
                        pclases.Bala.q.codigo == codigo)[0].articulos[0]
                elif codigo.startswith("C"):
                    articulo = pclases.Bigbag.select(
                        pclases.Bigbag.q.codigo == codigo)[0].articulos[0]
            except (IndexError, AttributeError):
                utils.dialogo_info(titulo = "CÓDIGO NO ENCONTRADO", 
                            texto = "Código %s no encontrado." % (codigo), 
                            padre = self.wids['ventana'])
            else:
                self.crear_ldv([articulo])
                self.objeto.calcular_comisiones()
                self.actualizar_ventana()
                articulo_annadido = articulo
        return articulo_annadido

    def pedir_rango(self, producto):
        """
        Pide un rango de números de bala o rollo.
        Devuelve una lista con los identificadores de
        artículo pertenecientes al producto de venta
        recibido que entran en el rango y no están 
        relacionados ya con otros albaranes.
        """
        if (self.objeto.cliente 
            and self.objeto.cliente.calcular_credito_disponible(
                base=self.objeto.calcular_total(iva_incluido = True, 
                                                segun_factura = False)) <= 0):
            utils.dialogo_info(titulo = "CLIENTE SIN CRÉDITO", 
                               texto = "El cliente ha sobrepasado el "
                                       "crédito concedido.", 
                               padre = self.wids['ventana'])
            self.to_log("[pedir_rango] Crédito sobrepasado.", 
                        {"cliente": self.objeto.cliente.get_info(), 
                         "albarán": self.objeto.numalbaran, 
                         "crédito disponible": 
                            self.objeto.cliente.calcular_credito_disponible(
                                base=self.objeto.calcular_total(
                                                iva_incluido = True, 
                                                segun_factura = False)), 
                         "importe albarán": self.objeto.calcular_total(
                                                iva_incluido = True, 
                                                segun_factura = False)
                        })
            return
        if self.comprobar_cliente_deudor():
            try:
                infocliente = self.objeto.cliente.get_info()
                credicliente = self.objeto.cliente.calcular_credito_disponible(
                                base=self.objeto.calcular_total(
                                                iva_incluido = True, 
                                                segun_factura = False))
            except AttributeError:
                infocliente = credicliente = "¿Sin self.objeto.cliente?"
            self.to_log("[pedir_rango] Cliente deudor.", 
                        {"cliente": infocliente, 
                         "albarán": self.objeto.numalbaran, 
                         "crédito disponible": credicliente, 
                         "importe albarán": self.objeto.calcular_total(
                                                iva_incluido = True, 
                                                segun_factura = False)
                        })
            return
        # DONE: Portar ventana de pedir rango que acepta guiones, 
        #       comas, etc. aquí.
        strrango = utils.dialogo_entrada(titulo = 'INTRODUZCA RANGO',
                                      texto = """
        Rango de número de balas/rollos o el código indovidual.
        Escriba el rango de códigos de la forma "xxxx-yyyy", ambos inclusive.
        En caso de ambigüedad, introdúzcalos precedidos de R para geotextiles,
        B para fibra, C para fibra de cemento, Z para balas de cable, X para 
        rollos de longitud insuficiente,  Y para geotextiles «C», H para 
        palés, J para cajas de bolsas de fibra de cemento y K para bolsas 
        sueltas.
                                                                                            
        También puede introducir varios rangos separados por coma o espacio.
                                                                                            
        Por ejemplo:                                                                        
            123-145     Intentará añadir los rollos 123 a 145, ambos inclusive.             
                         Si no los encuentra, los buscará entre las balas de fibra.         
            R123-145    Añadirá los rollos 123 a 145, ambos inclusive.                      
            R123-R145   Hace lo mismo que el caso anterior.                                 
            B123-145    Añadirá, si se encuentran y están debidamente analizadas y          
                        catalogadas, las balas de fibra 123 a 145, ambas inclusive.         
            B123-B145   Hace lo mismo que en el caso anterior.                              
            C10-C15     BigBags de GEOCEM del número 10 al 15.                              
            B100-B105, R4000 C101   Introduce el rango de balas de 100 a 105, ambas         
                        inclusive; el rollo 4000 y el bigbag 101.
            H31/40      Palé 31, de 14 cajas con 40 bolsas por caja.
        """, 
                                      padre = self.wids['ventana'])
        articulos = []
        if strrango == '' or strrango == None:
            return
        self.logger.warning("%salbaranes_de_salida -> Iniciando pedir_rango"
            " (salida de artículos manual)" 
            % (self.usuario and self.usuario.usuario + ": " or ""))
        ## ----------------
        tokens = []
        for token in strrango.split():
            tokens += token.split(",")
        tokens = [i.strip() for i in tokens if i.strip() != ""]
        for rango in tokens: 
            # Casos especiales: ROLLOS Y BALAS DUPLICADOS. AAARGGGHHHH!!!
            if (("R" in rango.upper() and "D" in rango.upper()) 
                or ("B" in rango.upper() and "D" in rango.upper())):
                articulo = self.add_duplicado(rango, self.objeto)
                if articulo != None:
                    articulos.append(articulo)
                continue
            # -------------------------------------------------------------
            if "B" in rango.upper():
                tipocodigo = "B"
                rango = rango.replace("B", "")
                rango = rango.replace("b", "")
            elif "R" in rango.upper():
                tipocodigo = "R"
                rango = rango.replace("R", "")
                rango = rango.replace("r", "")
            elif "C" in rango.upper():
                tipocodigo = "C"
                rango = rango.replace("C", "")
                rango = rango.replace("c", "")
            elif "Z" in rango.upper():
                tipocodigo = "Z"
                rango = rango.replace("Z", "")
                rango = rango.replace("z", "")
            elif "X" in rango.upper():
                tipocodigo = "X"
                rango = rango.replace("X", "")
                rango = rango.replace("x", "")
            elif "Y" in rango.upper():
                tipocodigo = "Y"
                rango = rango.replace("Y", "")
                rango = rango.replace("y", "")
            # Palés. H00/00
            elif "H" in rango.upper():
                tipocodigo = "H"
                rango = rango.replace("H", "")
                rango = rango.replace("h", "")
            # Cajas. 
            elif "J" in rango.upper():
                tipocodigo = "J"
                rango = rango.replace("J", "").replace("j", "")
            # Bolsas sueltas.
            #elif "K" in rango.upper():
            #    tipocodigo = "K"
            #    rango = rango.replace("K", "").replace("k", "")
            else:
                tipocodigo = ""
            if '-' in rango:
                if tipocodigo == "H":   # Quito el /bolsas_por_caja antes de 
                                        # procesar.
                    _rango = []
                    for tokenpale in rango.split("-"):
                        if "/" in tokenpale:
                            tokenpale = tokenpale[:tokenpale.index("/")]
                        _rango.append(tokenpale)
                    rango = "-".join(_rango)
                try:
                    ini, fin = rango.split('-')
                except ValueError:
                    utils.dialogo_info(titulo = "RANGO INCORRECTO", 
                        texto = "Asegúrese de que el texto introducido (%s) "
                                "es correcto." % rango, 
                        padre = self.wids['ventana'])
                    continue
                try:
                    ini = int(ini)
                    fin = int(fin)
                except ValueError:
                    utils.dialogo_info(titulo = "RANGO NO VÁLIDO", 
                        texto = "El texto introducido (%s) no corresponde "
                                "a un rango válido." % (rango),
                        padre = self.wids['ventana'])
                    continue
                if fin < ini:
                    ini, fin = fin, ini
                rangocodigos = xrange(ini, fin+1)
                total = len(rangocodigos)
                actual = 0.0
                vpro = VentanaProgreso(padre = self.wids['ventana'])
                vpro.set_valor(0.0, "Añadiendo artículos...")
                vpro.mostrar()
                try:
                    for codigo in rangocodigos:
                        vpro.set_valor(actual/total, None) 
                        actual += 1.0
                        len_antes = len(articulos)
                        articulos = self.add_producto(codigo, 
                                                      articulos, 
                                                      tipocodigo)
                        len_despues = len(articulos)
                        if len_antes == len_despues:    
                            # No se han añadido artículos porque el código era 
                            # incorrecto. 
                            # Voy a preguntar si quiere seguir, porque como haya 
                            # metido un rango de 1000 códigos y no esté ninguno, 
                            # el usuario se va a hinchar de darle a aceptar.
                            txt = """
                            El código %s%d no se encontró. ¿Desea continuar 
                            e intentar añadir al albarán el resto de códigos?                                  
                            """ % (tipocodigo, codigo)
                            if not utils.dialogo(titulo = "¿CONTINUAR?", 
                                                 texto = txt, 
                                                 padre = self.wids['ventana']):
                                break
                finally:
                    vpro.ocultar()
            else:
                if tipocodigo == "H":   # Quito el /bolsas_por_caja antes de 
                                        # procesar.
                    if "/" in rango:
                        rango = rango[:rango.index("/")]
                try:
                    articulos = self.add_producto(int(rango), 
                                                  articulos, 
                                                  tipocodigo)
                except ValueError:
                    self.logger.error("albaranes_de_salida.py: "
                      "pedir_rango. Error al convertir a entero: %s." %  rango)
        ## ----------------
        if articulos == []:
            utils.dialogo_info(titulo = 'NO ENCONTRADO', 
                               texto = 'Los códigos introducidos no se '
                                       'encontraron o no estaban '
                                       'debidamente catalogados.', 
                               padre = self.wids['ventana'])
        ## ----------------
        articulos_baja_calidad = []
        for articulo in articulos:
            if articulo.es_de_baja_calidad():
                articulos_baja_calidad.append(articulo)
        texto = """
        Los siguientes artículos se han considerado que son         
        de baja calidad. ¿Continuar?                                
                                                                    
        %s  
        """ % ("\n".join([a.codigo for a in articulos_baja_calidad]))
        if (articulos_baja_calidad == [] 
            or utils.dialogo(titulo = "ARTÍCULOS DE BAJA CALIDAD", 
                             texto = texto, 
                             padre = self.wids['ventana'])):
            self.crear_ldv(articulos)   # En realidad no crea, asocia 
                                        # artículos al albarán
            self.objeto.calcular_comisiones()
            self.actualizar_ventana()

    def add_producto(self, codigo, articulos, tipocodigo = ""):
        """
        Codigo es un número de rollo o bala. Viene como entero.
        articulos es una lista de objetos articulos al que añade
        el artículo o los artículos encontrados andes de devolverla.
        """
        # PLAN: WTF: Limpiar un poco y refactorizar esta función.
        if tipocodigo == "":
            articulo = pclases.Rollo.select(pclases.Rollo.q.numrollo == codigo)
            if articulo.count() == 0:
                # No es un código de rollo. Busco bala
                articulo = pclases.Bala.select(pclases.Bala.q.numbala == codigo)
                antes_de_chequear_analizadas = articulo.count()
                articulo = [b for b in articulo if b.analizada()]
                # OJO: NOTA: Las balas "vendibles" son aquellas cuyo lote ya 
                # ha sido analizado y por tanto tiene código.
                if len(articulo) == 0:
                    if antes_de_chequear_analizadas == 0: 
                        # No se ha encontrado, código incorrecto.
                        utils.dialogo_info(titulo = 'CÓDIGO INCORRECTO', 
                                    texto = 'Código %s incorrecto.' % (codigo), 
                                    padre = self.wids['ventana'])
                    else:
                        # Se ha encontrado pero no se puede vender.
                        utils.dialogo_info(titulo = 'FIBRA NO ANALIZADA', 
                        texto = """
                        La bala de fibra %s no ha sido analizada en el
                        laboratorio. No se puede vender fibra sin antes                     
                        determinar que cumple los criterios necesarios.                     
                        Asegúrese de que al menos se han determinado las                    
                        siguientes características: tenacidad, elongación, 
                        rizo y encogimiento.
                        """ % (codigo), 
                        padre = self.wids['ventana'])
                    return articulos    # Devuelvo sin añadir nada.
        elif tipocodigo == "R": # Sólo busco rollos.
            articulo = pclases.Rollo.select(pclases.Rollo.q.numrollo == codigo)
            if articulo.count() == 0:
                return articulos    # No lo encuentro, devuelvo sin añadir nada.
        elif tipocodigo == "C": # Sólo busco fibra de cemento.
            articulo = pclases.Bigbag.select(pclases.Bigbag.q.numbigbag == codigo)
            if articulo.count() == 0:
                return articulos    # No lo encuentro, devuelvo sin añadir nada.
        elif tipocodigo == "Z": # Sólo busco cable de fibra.
            articulo = pclases.BalaCable.select(pclases.BalaCable.q.codigo == "Z%d" % codigo)
            if articulo.count() == 0:
                return articulos    # No lo encuentro, devuelvo sin añadir nada.
        elif tipocodigo == "X": # Sólo busco rollos defectuosos.
            articulo = pclases.RolloDefectuoso.select(
                pclases.RolloDefectuoso.q.codigo == "X%d" % codigo)
            if articulo.count() == 0:
                return articulos    # No lo encuentro, devuelvo sin añadir nada.
        elif tipocodigo == "Y": # Sólo busco rollos defectuosos.
            articulo = pclases.RolloC.select(
                pclases.RolloC.q.codigo == "Y%d" % codigo)
            if articulo.count() == 0:
                return articulos    # No lo encuentro, devuelvo sin añadir nada.
        elif tipocodigo == "B": # Sólo busco balas.
            articulo = pclases.Bala.select(pclases.Bala.q.numbala == codigo)
            antes_de_chequear_analizadas = articulo.count()
            articulo = [b for b in articulo if b.analizada()]
            # OJO: NOTA: Las balas "vendibles" son aquellas cuyo lote ya ha 
            # sido analizado y por tanto tiene código.
            if len(articulo) == 0:
                if antes_de_chequear_analizadas == 0: 
                    # No se ha encontrado, código incorrecto.
                    utils.dialogo_info(titulo = 'CÓDIGO INCORRECTO', 
                                       texto = 'Código %s incorrecto.'%codigo, 
                                       padre = self.wids['ventana'])
                else:
                    # Se ha encontrado pero no se puede vender.
                    utils.dialogo_info(titulo = 'FIBRA NO ANALIZADA', 
                                       texto = """
                    La bala de fibra %s no ha sido analizada en el
                    laboratorio. No se puede vender fibra sin antes                     
                    determinar que cumple los criterios necesarios.                     
                    Asegúrese de que al menos se han determinado las                    
                    siguientes características: tenacidad, elongación, 
                    rizo y encogimiento.
                    """ % (codigo), 
                                       padre = self.wids['ventana'])
                return articulos    # Devuelvo sin añadir nada.
        elif tipocodigo == "H": # Palés (completos o resto) de fibra de cemento
            pale = pclases.Pale.select(pclases.Pale.q.numpale == codigo)
            articulo = []
            for p in pale:
            #    for c in p.cajas:
            #        for b in c.bolsas:
            #            articulo.append(b)
            # Optimizando, que es gerundio:
                #articulo += p.get_bolsas_en_almacen(self.objeto.almacenOrigen)
                articulo += p.get_cajas_en_almacen(self.objeto.almacenOrigen)
                if pclases.VERBOSE:
                    print __file__, len(articulo)
        elif tipocodigo == "J": # Una caja suelta de fibra de cemento
            cajas = pclases.Caja.select(pclases.Caja.q.codigo == "J%d"%codigo)
            articulo = []
            for c in cajas:  # @UnusedVariable
                # for b in c.bolsas:
                articulo.append(c)
        #elif tipocodigo == "K": # Una única bolsa de fibra de cemento
        #    articulo = pclases.Bolsa.select(
        #        pclases.Bolsa.q.codigo == "K%d" % codigo)
        #    if articulo.count() == 0:
        #        return articulos  # No lo encuentro, devuelvo sin añadir nada.
        else:
            self.logger.error("albaranes_de_salida.py. Se solicitó añadir artículos que no son balas, rollos, rollos defectuosos, balas de cable ni geocem. tipocodigo = %s" % (tipocodigo))
        # Aquí ya tengo un resultado válido, tanto si se ha buscado rollo 
        # como balas o ambas cosas:
        # articulo es un objeto bala o rollo. Ambos tienen una lista de 
        # articulos con un articulo relacionado.
        #articulo = articulo[0].articulos[0]
        avisado_error_pale = False  # No quiero avisar por cada una de las 
            # 560 bolsas de un palé.
        listaarticulos = articulo
        for _articulo in listaarticulos:
            articulo = _articulo.articulo
            # Compruebo que no esté relacionado ya con algún albarán, en cuyo 
            # caso muestro mensaje de error.
            # XXX: Optimizo:
            if tipocodigo == "H":
                articulos.append(articulo)
                continue    # Ya he filtrado que estuvieran en el almacén 
                            # antes, en el get_bolsas_..., que solo devuelve 
                            # bolsas del palé en el almacén indicado.
            # XXX: EOOptimización
            if not articulo.en_almacen(almacen = self.objeto.almacenOrigen):
                if ((tipocodigo=="H" or tipocodigo=="J" or tipocodigo=="K") 
                    and avisado_error_pale):
                    continue
                if articulo.albaranSalida != None:
                    motivo_salida = "Salió del mismo en el albarán %s." % (
                        articulo.albaranSalida.numalbaran)
                elif (articulo.bala != None 
                      and articulo.bala.partidaCarga != None):
                    motivo_salida = "Se empleó en producción, en la partida "\
                        "de carga %s." % (articulo.bala.partidaCarga.codigo)
                else:
                    motivo_salida = ""
                txt = """
                El producto seleccionado con código %s no está en el almacén.
                %s
                Verifique si esto es correcto y elimine el producto del 
                albarán indicado si quiere añadirlo a este.
                """ % (articulo.codigo_interno, motivo_salida)
                utils.dialogo_info(titulo = "ERROR: PRODUCTO NO ENCONTRADO "\
                                            "EN ALMACÉN", 
                                   texto = txt, 
                                   padre = self.wids['ventana'])
                if (tipocodigo=="K" or tipocodigo=="J" or tipocodigo=="H"):
                    avisado_error_pale = True
            else:
                articulos.append(articulo)
        return articulos

    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        # NOTA: No hay que preocuparse por el exceso de cómputo. Estas 
        # comparaciones son bastante rápidas al tener python -como los 
        # lenguajes de verdad y no los jueguetes tipo VB- las operaciones 
        # lógicas cortocircuitadas, de forma que si condición pasa a False 
        # no se evalúa lo que esté detrás del and en las instrucciones 
        # posteriores.
        albaran = self.objeto
        if albaran == None: 
            return False    # Si no hay albaran activo, devuelvo que no hay 
                            # cambio respecto a la ventana
        condicion = albaran.numalbaran == self.wids['e_numalbaran'].get_text()
        if pclases.DEBUG and not condicion: print "numalbaran", albaran.numalbaran
        condicion = condicion and (utils.str_fecha(albaran.fecha) == self.wids['e_fecha'].get_text())
        if pclases.DEBUG and not condicion: print "fecha", albaran.fecha
        cliente = albaran.cliente
        cbe_cliente = utils.combo_get_value(self.wids['cbe_cliente'])
        if cliente == None: 
            mismocliente = cbe_cliente == None
        else:
            mismocliente = cliente.id == cbe_cliente
        condicion = condicion and mismocliente
        if pclases.DEBUG and not condicion: print "cliente", albaran.cliente
        condicion = condicion and self.wids['ch_facturable'].get_active() == self.objeto.facturable
        if pclases.DEBUG and not condicion: print "facturable", albaran.facturable
        condicion = condicion and self.wids['e_motivo'].get_text() == self.objeto.motivo
        if pclases.DEBUG and not condicion: print "motivo", albaran.motivo
        condicion = condicion and self.wids['ch_bloqueado'].get_active() == albaran.bloqueado
        if pclases.DEBUG and not condicion: print "bloqueado", albaran.bloqueado
        condicion = condicion and self.wids['cbe_nom'].child.get_text() == albaran.nombre
        if pclases.DEBUG and not condicion: print "nombre", albaran.nombre
        condicion = condicion and self.wids['e_cp'].get_text() == albaran.cp 
        if pclases.DEBUG and not condicion: print "cp", albaran.cp
        condicion = condicion and self.wids['e_ciudad'].get_text() == albaran.ciudad 
        if pclases.DEBUG and not condicion: print "ciudad", albaran.ciudad
        condicion = condicion and self.wids['e_pais'].get_text() == albaran.pais
        if pclases.DEBUG and not condicion: print "pais", albaran.pais 
        condicion = condicion and self.wids['e_telf'].get_text() == albaran.telefono
        if pclases.DEBUG and not condicion: print "telefono", albaran.telefono
        condicion = condicion and self.wids['e_direccion'].get_text() == albaran.direccion
        if pclases.DEBUG and not condicion: print "direccion", albaran.direccion
        buff = self.wids['tv_observaciones'].get_buffer()
        condicion = condicion and buff.get_text(buff.get_start_iter(), buff.get_end_iter()) == albaran.observaciones 
        if pclases.DEBUG and not condicion: print "observaciones", albaran.observaciones
        condicion = condicion and utils.combo_get_value(self.wids['cbe_dni']) == albaran.transportistaID
        if pclases.DEBUG and not condicion: print "transportista", albaran.transportista
        condicion = condicion and utils.combo_get_value(self.wids['cbe_nom']) == albaran.destinoID
        if pclases.DEBUG and not condicion: print "destino", albaran.destino
        condicion = (condicion and 
            utils.combo_get_value(self.wids['cbe_almacenOrigenID']) 
            == albaran.almacenOrigenID)
        condicion = (condicion and 
            utils.combo_get_value(self.wids['cbe_almacenDestinoID']) 
            == albaran.almacenDestinoID)
        return not condicion    # "condicion" verifica que sea igual

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
        utils.dialogo_info('ACTUALIZAR',
                           'El albarán ha sido modificado remotamente.\nDebe '
                           'actualizar la información mostrada en pantalla.\n'
                           'Pulse el botón «Actualizar»', 
                           padre = self.wids['ventana'])
        self.wids['b_actualizar'].set_sensitive(True)

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        self.inicializar_leyenda()
        self.activar_widgets(False)
        # Inicialización del resto de widgets:
        cols = (('Cantidad', 'gobject.TYPE_FLOAT', True, True, False, 
                    self.cambiar_cantidad_srv),
                ('Concepto', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_concepto_srv),
                ('Precio', 'gobject.TYPE_FLOAT', True, True, False, 
                    self.cambiar_precio_srv),
                ('Descuento', 'gobject.TYPE_FLOAT', True, True, False, 
                    self.cambiar_descuento_srv),
                ('Total', 'gobject.TYPE_FLOAT', False, True, False, None),
                ('ID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_servicios'], cols)
        attach_menu_notas(self.wids['tv_servicios'], pclases.Servicio, 
                          self.usuario, 1)
        cols = (('Concepto', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_concepto_tac),
                ('Precio', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_precio_tac),
                ('Proveedor', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_proveedor_tac),
                ('Observaciones', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_observaciones_tac),
                ('Fecha', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_fecha_tac),
                ('Factura compra', 'gobject.TYPE_STRING', False, True, False, 
                    None), 
                ('ID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_transportesACuenta'], cols)
        self.wids['tv_transportesACuenta'].get_selection().set_mode(
            gtk.SELECTION_MULTIPLE)
        cols = (('Concepto', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_concepto_comision),
                ('Precio', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_precio_comision),
                ('Observaciones', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_observaciones_comision),
                ('Comercial', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_comercial_comision),
                ('Porcentaje', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_porcentaje_comision),
                ('Factura compra', 'gobject.TYPE_STRING', False, True, False, 
                    None), 
                ('ID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_comisiones'], cols)
        self.wids['tv_comisiones'].get_selection().set_mode(
            gtk.SELECTION_MULTIPLE)
        utils.rellenar_lista(self.wids['cbe_cliente'], 
                             [(c.id, "%s (%s, %s - %s)" % (
                                c.nombre, 
                                c.cif, 
                                c.ciudad, 
                                c.provincia)) 
                              for c in 
                              pclases.Cliente.select(orderBy='nombre')])
        cols = (('Bultos añadidos al albarán', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', 
                    False, True, True, None),
                ('Cantidad solicitada', 'gobject.TYPE_FLOAT', 
                    True, True, False, self.cambiar_cantidad),
                ('Cantidad añadida', 'gobject.TYPE_FLOAT', 
                    False, True, False, None),
                ('IDLDV', 'gobject.TYPE_STRING', False, False, False, None)
               )
        utils.preparar_treeview(self.wids['tv_ldvs'], cols)
        self.wids['tv_ldvs'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.wids['tv_ldvs'].connect("row-activated", self.abrir_pedido)
        attach_menu_notas(self.wids['tv_ldvs'], pclases.LineaDeVenta, 
                          self.usuario, 2)
        transportistas = [(t.id, t.dni) for t 
                          in pclases.Transportista.select(orderBy = 'dni')]
        utils.rellenar_lista(self.wids['cbe_dni'], transportistas)
        self.wids['cbe_dni'].connect('changed', 
            self.combo_transportista_cambiado)
        self.wids['cbe_dni'].child.connect('changed', 
            self.activar_guardar_transportista)
        self.wids['e_nombre'].connect('changed', 
            self.activar_guardar_transportista)
        self.wids['e_agencia'].connect('changed', 
            self.activar_guardar_transportista)
        self.wids['e_matricula'].connect('changed', 
            self.activar_guardar_transportista)
        self.wids['e_telefono'].connect('changed', 
            self.activar_guardar_transportista)
        destinos = [(t.id, t.nombre) 
                        for t in pclases.Destino.select(orderBy = 'nombre')]
        utils.rellenar_lista(self.wids['cbe_nom'], destinos)
        self.wids['cbe_nom'].connect('changed', self.combo_destino_cambiado)
        self.wids['cbe_nom'].child.connect('changed', 
            self.activar_guardar_destino)
        self.wids['e_cp'].connect('changed', self.activar_guardar_destino)
        self.wids['e_ciudad'].connect('changed', self.activar_guardar_destino)
        self.wids['e_pais'].connect('changed', self.activar_guardar_destino)
        self.wids['e_telf'].connect('changed', self.activar_guardar_destino)
        self.wids['e_direccion'].connect('changed', 
            self.activar_guardar_destino)
        cols = (('Abono', 'gobject.TYPE_STRING', False, True, False, None),
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', False,True,True,None),
                ('Código trazabilidad', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('IDLDD', 'gobject.TYPE_STRING', False, False, False, None)
               )
        utils.preparar_treeview(self.wids['tv_abonado'], cols)
        utils.rellenar_lista(self.wids['cbe_almacenOrigenID'], 
                        [(a.id, a.nombre) 
                         for a in pclases.Almacen.select(
                             pclases.Almacen.q.activo == True, 
                             orderBy = "nombre")])
        utils.rellenar_lista(self.wids['cbe_almacenDestinoID'], 
                        [(a.id, a.nombre) 
                         for a in pclases.Almacen.select(
                             pclases.Almacen.q.activo == True, 
                             orderBy = "nombre")])
        # Si el negocio no vende artículos individuales, ¿para qué mostrar el 
        # botón de añadir rangos?
        if (pclases.Rollo.select().count() +
            pclases.RolloC.select().count() + 
            pclases.RolloDefectuoso.select().count() + 
            pclases.Bigbag.select().count() + 
            pclases.Bala.select().count() + 
            pclases.BalaCable.select().count() == 0):
            self.wids['b_add_producto'].set_property("visible", False)
            self.wids['b_phaser'].set_property("visible", False)

    def abrir_pedido(self, tv, path, vc):
        model = tv.get_model()
        if model[path].parent == None:
            idldv = model[path][-1]
            #ldv = pclases.LineaDeVenta.get(idldv)
            ldv = pclases.getObjetoPUID(idldv)
            if ldv.pedidoVenta != None:
                from formularios import pedidos_de_venta
                pedidos_de_venta.PedidosDeVenta(ldv.pedidoVenta)
        else:
            idarticulo = model[path][-1]
            objeto = pclases.getObjetoPUID(idarticulo)
            if isinstance(objeto, pclases.Articulo):
                if objeto.bala != None:
                    objeto = objeto.bala
                elif objeto.rollo != None:
                    objeto = objeto.rollo
                #elif objeto.bolsa != None:
                #    objeto = objeto.bolsa
                elif objeto.caja != None:
                    objeto = objeto.caja
            elif isinstance(objeto, (pclases.Caja, pclases.Pale)):
                pass  # I don't need to be forgiven. Yeah, yeah, yeah, no, no!
            else:
                objeto = None
            if objeto != None:
                from trazabilidad_articulos import TrazabilidadArticulos
                TrazabilidadArticulos(objeto)

    def rellenar_servicios(self):
        model = self.wids['tv_servicios'].get_model()
        model.clear()
        for servicio in self.objeto.servicios:
            model.append((servicio.cantidad,
              servicio.concepto, 
              servicio.precio, 
              servicio.descuento, 
              servicio.precio * (1.0 - servicio.descuento) * servicio.cantidad,
              servicio.get_puid()))

    def cantidad_anadida_a_ldv(self, ldv):
        """
        Devuelve la cantidad total de los artículos 
        pertenecientes al albarán que se correspondan
        con el producto recibido y se hayan agregado
        a la LDV recibida.
        """
        cantidad = 0.0
        articulos_anadidos = self.__ldvs[ldv.id]['articulos']
        for a in articulos_anadidos:
            if a.rolloID != None: # Es un rollo
                cantidad += (
                    a.productoVenta.camposEspecificosRollo.metrosLineales 
                    * a.productoVenta.camposEspecificosRollo.ancho)
            elif a.balaID != None:   # Es una bala
                cantidad += a.bala.pesobala
            elif a.es_bigbag():
                cantidad += a.bigbag.pesobigbag
            elif a.es_bala_cable():
                cantidad += a.peso
            elif a.es_rollo_defectuoso():
                cantidad += a.superficie
            elif a.es_rolloC():
                cantidad += a.peso
            elif a.es_caja():
                cantidad += a.peso
        return cantidad

    def cantidad_anadida(self, producto):
        """
        Devuelve la cantidad total de los artículos 
        pertenecientes al albarán que se correspondan
        con el producto recibido.
        Solo funciona con productos de venta (para 
        productos de compra no se añaden artículos).
        OJO: También se tienen en cuenta las devoluciones (CWT)
        """
        cantidad = 0.0
        if isinstance(producto, pclases.ProductoVenta):
            albaran = self.objeto
            if producto.es_caja():
                #queryres_ids = pclases.Caja._queryAll("""
                #    SELECT caja.id FROM caja, bolsa, articulo 
                #    WHERE bolsa.id = articulo.bolsa_id 
                #      AND caja.id = bolsa.caja_id 
                #      AND articulo.albaran_salida_id = %d 
                #      AND articulo.producto_venta_id = %d 
                #    GROUP BY caja.id 
                #    -- ORDER BY caja.id;""" % (albaran.id, producto.id))
                queryres_ids = pclases.Caja._queryAll( 
                    """SELECT caja.id FROM caja, articulo 
                    WHERE caja.id = articulo.caja_id 
                      AND articulo.albaran_salida_id = %d 
                      AND articulo.producto_venta_id = %d 
                    -- GROUP BY caja.id 
                    -- ORDER BY caja.id;
                    """ % (albaran.id, producto.id))
                cajas = [pclases.Caja.get(tupla[0]) for tupla in queryres_ids]
                cantidad = sum([c.peso for c in cajas])
            else:
                articulos_anadidos = (
                [a for a in albaran.articulos if a.productoVenta == producto] 
                + [ldd.articulo for ldd in albaran.lineasDeDevolucion 
                    if ldd.articulo.productoVenta == producto] 
                + [ldm.articulo for ldm in albaran.lineasDeMovimiento 
                    if ldm.articulo.productoVenta == producto])
                for a in utils.unificar(articulos_anadidos):
                    if a.es_rollo(): 
                        cantidad += a.productoVenta.camposEspecificosRollo.metrosLineales * a.productoVenta.camposEspecificosRollo.ancho
                    elif a.es_bala(): 
                        cantidad += a.bala.pesobala
                    elif a.es_bigbag():
                        cantidad += a.bigbag.pesobigbag
                    elif a.es_rollo_defectuoso():
                        cantidad += a.superficie
                    elif a.es_bala_cable() or a.es_rolloC(): # or a.es_caja():
                        cantidad += a.peso
        return cantidad

    def cambiar_cantidad(self, cell, path, nuevo_texto):
        if self.wids['tv_ldvs'].get_model()[path].parent != None:
            # Es un artículo, no una LDV. No dejo que lo cambie.
            utils.dialogo_info(titulo = 'NO SE PUEDEN EDITAR LOS PRODUCTOS', 
                texto = 'La cantidad de un producto concreto no es editable.\n'
                        'Tal vez esté intentando eliminarlo del albarán,\n'
                        'en ese caso selecciónelo y pulse el botón '
                        'correspondiente.', 
                padre = self.wids['ventana'])
            return
        try:
            cantidad = utils._float(nuevo_texto)
            self.modificado = True
        except ValueError:
            utils.dialogo_info(titulo = 'NÚMERO INCORRECTO', 
                texto = 'Introduzca un número válido con . como separador'
                        ' decimal.', 
                padre = self.wids['ventana'])
            return
        idldv = self.wids['tv_ldvs'].get_model()[path][-1]
        #ldv = pclases.LineaDeVenta.get(idldv)
        ldv = pclases.getObjetoPUID(idldv)
        if ((ldv.facturaVentaID != None and ldv.facturaVenta.bloqueada)
            or (ldv.prefacturaID != None and ldv.prefactura.bloqueada)):
            utils.dialogo_info(titulo = "OPERACIÓN NO PERMITIDA",
                texto = "La venta ya ha sido facturada y la factura "
                        "verificada y bloqueada.\nNo puede cambiar la "
                        "cantidad.", 
                padre = self.wids['ventana'])
        else:
            self.redistribuir_ldv(path, cantidad)
        self.actualizar_ventana()

    def redistribuir_ldv(self, path, cantidad = None):
        """
        Si cantidad es None es porque se debe hacer el reajuste automático. 
        Para el ajuste automático, cantidad valdrá la cantidad servida.
        Si la LDV está facturada o el albarán está bloqueado, no cambia la 
        cantidad.
        """
        idldv = self.wids['tv_ldvs'].get_model()[path][-1]
        #ldv = pclases.LineaDeVenta.get(idldv)
        ldv = pclases.getObjetoPUID(idldv)
        if pclases.DEBUG: 
            print "Soy redistribuir_ldv. Vamos con", ldv.producto.descripcion
        if (not self.objeto.bloqueado and 
              ((ldv.facturaVenta == None or not ldv.facturaVenta.bloqueada) 
                or (ldv.prefactura == None or not ldv.prefactura.bloqueada))):
            cantidad_anterior = ldv.cantidad
            cantidad_anadida = self.cantidad_anadida(ldv.productoVenta)
            if cantidad == None:
                cantidad = cantidad_anadida
            ldv.cantidad = cantidad
            ajustar_existencias(ldv, cantidad_anterior)

    def activar_guardar_transportista(self, w):
        self.wids['b_guardar_transportista'].set_sensitive(True)
    
    def activar_guardar_destino(self, w):
        self.wids['b_guardar_destino'].set_sensitive(True)

    def combo_transportista_cambiado(self, c):
        idtransp = utils.combo_get_value(c)
        if idtransp != None:
            self.mostrar_transportista(pclases.Transportista.get(idtransp))

    def combo_destino_cambiado(self, c):
        iddest = utils.combo_get_value(c)
        if iddest != None:
            self.mostrar_destino(pclases.Destino.get(iddest))

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        if (self.objeto and self.objeto.bloqueado and self.usuario 
            and self.usuario.nivel > 2):
            s = False
        ws = ('b_add_producto', 'b_drop_ldv', 'b_borrar', 'e_numalbaran', 
              'ch_bloqueado', 'b_fecha', 'cbe_cliente', 'tv_ldvs', 'e_fecha', 
              'ch_facturable', 'e_motivo', 'b_add_pedido', 'frame1', 'frame2', 
              'hbox19', 'vbox2', # 'b_guardar', 
              'tv_transportesACuenta', 'b_add_transporteACuenta', 
              'b_drop_transporteACuenta', 'tv_comisiones', 'b_add_comision', 
              'b_drop_comision', 'b_phaser') 
        for w in ws:
            self.wids[w].set_sensitive(s)
        for w in ("cbe_almacenOrigenID", "cbe_almacenDestinoID"):
            self.wids[w].set_sensitive(
                s and self.wids[w].get_property("sensitive"))
        # CWT: No bloquear transportes si el usuario tienen nivel <=3 (va por 
        # Rafa, en concreto, pero con más razón que un santo, eso sí).
        if self.usuario and self.usuario.nivel <= 3:
            self.wids['expander3'].set_sensitive(True)
            self.wids['tv_transportesACuenta'].set_sensitive(True)
            self.wids['b_add_transporteACuenta'].set_sensitive(True) 
            self.wids['b_drop_transporteACuenta'].set_sensitive(True)
        self.wids['e_motivo'].set_sensitive(
            s and not self.wids['ch_facturable'].get_active())
        if pclases.DEBUG: 
            print "e_motivo", s and not self.wids['ch_facturable'].get_active()

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        albaran = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if albaran != None: albaran.notificador.desactivar()
            albaran = pclases.AlbaranSalida.select(orderBy = '-id')[0] 
                # Selecciono todos los albaranes de venta y me quedo con el primero de la lista.
            self.modificado = False
            self.nuevo = False
            albaran.notificador.activar(self.aviso_actualizacion)       # Activo la notificación
        except Exception:
            albaran = None  
        self.objeto = albaran
        self.actualizar_ventana()

    def refinar_resultados_busqueda(self, resultados):
        """
        Muestra en una ventana de resultados todos los
        registros de "resultados".
        Devuelve el id (primera columna de la ventana
        de resultados) de la fila seleccionada o None
        si se canceló.
        """
        filas_res = []
        for r in resultados:
            if r.almacenDestino:
                destino = r.almacenDestino.nombre
            elif r.destino != None:
                destino = r.destino.get_info()
            elif r.nombre:
                destino = ", ".join((r.nombre, r.direccion, r.cp, r.ciudad, 
                                     r.pais))
            else:
                destino = ""
            try:
                nombre_alm_origen = r.almacenOrigen.nombre
            except AttributeError:
                r.almacenOrigen = pclases.Almacen.get_almacen_principal()
                r.sync()
                try:
                    nombre_alm_origen = r.almacenOrigen.nombre
                except AttributeError:
                    nombre_alm_origen = "¡SIN ALMACÉN DE ORIGEN!"
                    self.logger.error("%salbaranes_de_salida"
                        "::crear_nuevo_albaran -> Error con albarán %s. No "
                        "tiene almacén de origen." % (
                    self.usuario and self.usuario.usuario+": " or "", 
                    r.get_puid()))
            filas_res.append((r.id, 
                              r.numalbaran, 
                              r.fecha and r.fecha.strftime('%d/%m/%Y') or '', 
                              nombre_alm_origen, 
                              r.clienteID and r.cliente.nombre or "", 
                              destino))
        idalbaran = utils.dialogo_resultado(filas_res,
                        titulo = 'Seleccione albarán',
                        cabeceras = ('ID Interno', 
                                     'Número de albarán', 
                                     'Fecha', 
                                     'Origen', 
                                     'Cliente', 
                                     'Destino'), 
                        padre = self.wids['ventana']) 
        if idalbaran < 0:
            return None
        else:
            return idalbaran

    def colorear(self, ldvs):
        """
        ldvs es el diccionario... bah, mirar abajo, en la invocadora.
        """
        def cell_func(column, cell, model, itr, data):
            i, ldvs = data
            #if model[itr].parent != None:
            try:
                hijo = model[itr].iterchildren().next()
            except StopIteration:
                hijo = None
            if model[itr].parent == None: # Sin padre, línea de venta.
                idldv = int(model[itr][-1].split(":")[-1])
                if isinstance(ldvs[idldv]['ldv'].producto, 
                              pclases.ProductoCompra):
                    color = "PaleGreen"
                elif es_venta_rollos_c(ldvs[idldv]['ldv'].producto):
                    # DONE: Líneas con producto rollo C en otro color. 
                    color = "light grey"
                else:
                    cant_servida = round(ldvs[idldv]['ldv'].cantidad, 3)
                    cant_added = round(ldvs[idldv]['cantidad'], 3)
                    if cant_servida > cant_added:
                        color = "yellow"
                    if cant_servida == cant_added: 
                        color = "green"
                    if cant_servida < cant_added: 
                        color = "red"
                    if cant_added == 0:
                        color = "orange"
            elif not hijo:   # No hijos, es artículo.
                idarticulo = model[itr][-1]
                try:
                    #a = pclases.Articulo.get(idarticulo)
                    a = pclases.getObjetoPUID(idarticulo)
                except pclases.SQLObjectNotFound:
                    color = None
                else:
                    if a.albaranSalida != self.objeto:
                        # Artículo devuelto o transferido+vendido. Se muestra 
                        # en pantalla para poder imprimir "con compatibilidad 
                        # hacia atrás".
                        color = "RosyBrown3"
                    else:
                        color = "white"
            else:   # Nodos intermedios: cajas o palés. Si quiere ver si son 
                    # artículos devueltos o algo (rosita) o normales (línea en 
                    # blanco), que despliegue, porque no puedo marcar todo un 
                    # palé si por ejemplo contiene 4 cajas en rosa y el resto 
                    # en blanco.
                color = "light blue"
            cell.set_property("cell-background", color)
            # NOTA: Esto hay que hacerlo porque el nuevo cell_func machaca el predefinido por defecto
            #       en el utils.preparar_x
            utils.redondear_flotante_en_cell_cuando_sea_posible(column, 
                                                        cell, model, itr, 
                                                        (i, 1))

        cols = self.wids['tv_ldvs'].get_columns()
        for i in xrange(len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                if not isinstance(cell, gtk.CellRendererPixbuf):    # Para no machacar el data_func del icono "notas".
                    column.set_cell_data_func(cell,cell_func, [i, ldvs])

    def rellenar_ldvs(self, albaran):
        if pclases.DEBUG:
            print "Soy rellenar_ldvs. Hasta ahora mismo no he sido invocada."
        model = self.wids['tv_ldvs'].get_model()
        model.clear()
        self.__ldvs = self.agrupar_articulos(albaran)
            # Devuelve un diccionario {idldv: {...}, idldv: {...}} Ver __doc__ 
            # de la función.
        self.colorear(self.__ldvs)
        cajas = {}  # iters de cajas insertadas
        pales = {}  # iters de pales insertados
        opales = {} # Registros palé insertados por producto de venta.
        for idldv in self.__ldvs:
            articulos = self.__ldvs[idldv]['articulos'] 
            pv = self.__ldvs[idldv]['ldv'].productoVenta 
            if pv not in opales:
                opales[pv] = []
            if (pv and pv.es_caja()):
                for a in articulos:
                    if a.caja.pale not in opales[pv]:
                        opales[pv].append(a.caja.pale)
                bultos = len(opales[pv])
            else:
                bultos = len(articulos)     # Bultos añadidos
            ldv = self.__ldvs[idldv]['ldv']
            # Un "porsiaca":
            if ldv.cantidad is None:
                ldv.cantidad = 0.0
                ldv.sync()
            cantidad = ldv.cantidad 
            cantidad_servida = self.cantidad_anadida_a_ldv(ldv)
            iterpadre = model.append(None, (bultos, 
                                            ldv.producto.codigo, 
                                            ldv.producto.descripcion, 
                                            cantidad,
                                            cantidad_servida, 
                                            ldv.get_puid()))
            iterldv = iterpadre
            for a in self.__ldvs[idldv]['articulos']:
                iterpadre, cantidad = self.insert_en_pale(a, pales, model, 
                                        iterldv, cajas, cantidad, iterpadre)
                # Ahora inserto el artículo. Si es una bolsa, iterpadre ahora 
                # valdrá lo que el iter de la caja a la que pertenece, si no 
                # será la línea de producto para colgar el rollo/bala, etc.
                cantidad_bultos_del_articulo = 1
                if a.es_caja():
                    cantidad_bultos_del_articulo = a.caja.numbolsas
                model.append(iterpadre,
                             (cantidad_bultos_del_articulo, 
                              a.codigo_interno, 
                              '',
                              cantidad,
                              cantidad,
                              a.get_puid()))
        self.rellenar_lineas_de_transferencia(opales, cajas, pales)

    def insert_en_pale(self,a,pales,model,iterldv,cajas,cantidad,iterpadre):
        # Insera el nodo del palé y devuelve el iter para que después   
        # se pueda insertar el artículo (la caja en sí) como nodo hijo.
        cantidad = a.get_cantidad()
        if a.es_caja():
            caja = a.caja
            pale = caja.pale
            try:
                iterpale = pales[pale]
            except KeyError:
                iterpale = model.append(iterldv, 
                                        (1, # El palé es el bulto 
                                         pale.codigo, 
                                         "", 
                                         0.0, 
                                         0.0, 
                                         pale.get_puid()))
                pales[pale] = iterpale
            #try:
            #    itercaja = cajas[caja]
            #except KeyError:
            #    itercaja = model.append(iterpale, 
            #                            (1, 
            #                             caja.codigo, 
            #                             "", 
            #                             0.0, 
            #                             0.0, 
            #                             caja.get_puid()))
            #    cajas[caja] = itercaja
            #    #model[pales[pale]][0] += 1 # CWT: Palé es el bulto. 
            #iterpadre = itercaja 
            iterpadre = iterpale
            # Actualizo las cantidades de mi padre caja y abuelo palé.
            #for iterpc in (cajas[caja], pales[pale]):
            for iterpc in (pales[pale], ):
                #model[iterpc][0] += 1
                model[iterpc][3] += cantidad
                model[iterpc][4] += cantidad
        return iterpadre, cantidad

    def rellenar_lineas_de_transferencia(self, opales, cajas, pales):
        """
        Añade al albarán los artículos relancionados con el mismo a través de 
        las líneas de transferencia.
        Como hasta que salgan en otro albarán, el artículo estará relacionado 
        con el albarán actual por dos enlaces (relación artículo-albarán y 
        relación artículo-línea de transferencia-albarán), hay que chequear 
        que no lo voy a meter duplicado en la ventana.
        «opales» es un diccionario de registros palé tratados por producto de 
        venta para llevar el control de bultos.
        """
        model = self.wids['tv_ldvs'].get_model()
        # ids_articulos_added = tuple([a.ide for a in self.objeto.articulos])
        # Esto de arriba ya no es así. Ahora los artículos por LDV ya incluyen 
        # los de transferencia además de los devueltos, así que construyo esta 
        # lista de otra forma:
        larts = []
        for k in self.__ldvs.keys():
            for a in self.__ldvs[k]['articulos']:
                if a not in larts:
                    larts.append(a.id)
        ids_articulos_added = tuple(larts)
        paths_productos = {}
        for row in model:
            ldv_id = row[-1]
            #ide = pclases.LineaDeVenta.get(ldv_id).productoVentaID
            ide = pclases.getObjetoPUID(ldv_id).productoVentaID
            # Puede llegar a crear un paths_productos[None] -> [<path>]. Mejor.
            path = row.path
            try:
                paths_productos[ide].append(path)
            except KeyError:
                paths_productos[ide] = [path]
        for ldt in self.objeto.lineasDeMovimiento:
            a = articulo = ldt.articulo
            if articulo.id not in ids_articulos_added:
                producto_id = articulo.productoVentaID
                path_producto = paths_productos[producto_id][0] 
                    # MUST! Debe estar el producto. Es imposible relacionar 
                    # un artículo con un albarán si el producto no está en 
                    # una LDV (a no ser que hagas trampas directamente contra 
                    # la BD).
                cantidad = articulo.get_cantidad()
                iterpadre = model.get_iter(path_producto)
                iterldv = iterpadre
                iterpadre, cantidad = self.insert_en_pale(a, pales, model, 
                                                       iterldv, cajas, 
                                                       cantidad, iterpadre)
                # Ahora inserto el artículo. Si es una bolsa, iterpadre ahora 
                # valdrá lo que el iter de la caja a la que pertenece, si no 
                # será la línea de producto para colgar el rollo/bala, etc.
                model.append(iterpadre,
                             (1, 
                              articulo.codigo_interno, 
                              '',
                              cantidad,
                              cantidad,
                              articulo.get_puid()))
                if not articulo.es_caja():
                    model[iterpadre][0] += 1
                else:
                    pv = articulo.productoVenta
                    if pv not in opales:
                        opales[pv] = []
                    pale = articulo.caja.pale
                    if pale not in opales[pv]:
                        opales[pv].append(pale)
                        model[iterpadre][0] += 1
                model[iterpadre][4]=utils._float(model[iterpadre][4])+cantidad
 
    def rellenar_widgets(self):
        """
        Introduce la información del albaran actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        self.wids['ventana'].set_title(
          self.objeto.numalbaran+" - Albaranes de venta (salida de material)")
        self.wids['b_guardar'].set_sensitive(False) # Deshabilito el guardar 
            # antes de actualizar para evitar "falsos positivos".
        albaran = self.objeto
        if albaran == None: 
            return
        self.wids['ch_facturable'].set_active(self.objeto.facturable)
        self.wids['e_motivo'].set_text(self.objeto.motivo)
        self.wids['e_numalbaran'].set_text(albaran.numalbaran)
        self.wids['e_fecha'].set_text(utils.str_fecha(albaran.fecha))
        self.wids['ch_bloqueado'].set_active(self.objeto.bloqueado)
        cliente = albaran.cliente
        if cliente == None:
            self.wids['cbe_cliente'].set_active(-1)
            self.wids['cbe_cliente'].child.set_text('')
        else:
            utils.combo_set_from_db(self.wids['cbe_cliente'], cliente.id)
        self.rellenar_ldvs(albaran)
        self.rellenar_servicios()
        self.rellenar_transportes_a_cuenta()
        self.rellenar_comisiones()
        self.rellenar_ldds(albaran)
        if (albaran.destino == None 
            and albaran.nombre != None 
            and albaran.nombre.strip() != ""):
            # Si ya tiene un destino asignado pero no está correctamente 
            # enlazado, lo creo.
            nuevo_destino = self.crear_nuevo_destino()
            albaran.destino = nuevo_destino
        self.mostrar_destino(albaran.destino)
        buff = self.wids['tv_observaciones'].get_buffer()
        buff.set_text(albaran.observaciones)
        self.mostrar_transportista(albaran.transportista)
        self.wids['cbe_nom'].child.set_text(albaran.nombre)
        self.wids['e_cp'].set_text(albaran.cp)
        self.wids['e_ciudad'].set_text(albaran.ciudad)
        self.wids['e_pais'].set_text(albaran.pais)
        self.wids['e_telf'].set_text(albaran.telefono)
        self.wids['e_direccion'].set_text(albaran.direccion)
        self.wids['e_pedidos'].set_text(
            self.get_nums_pedidos(albaran, cortar = False))
        self.wids['e_facturas'].set_text(
            ', '.join([f.numfactura for f in albaran.get_facturas()]))
        pedidos = self.get_pedidos(albaran)
        gastos_envio = False
        for p in pedidos:   # Si al menos uno de los pedidos indica transporte 
                            # a cargo, hay que marcar la casilla.
            gastos_envio = gastos_envio or p.transporteACargo
        self.wids['ch_debellevargastos'].set_active(gastos_envio)
        self.wids['e_total_albaran'].set_text(
            "%s €" % (utils.float2str(self.objeto.calcular_total())))
        self.suspender(self.wids['cbe_almacenOrigenID'])
        self.suspender(self.wids['cbe_almacenDestinoID'])
        utils.combo_set_from_db(self.wids['cbe_almacenOrigenID'], 
                                self.objeto.almacenOrigenID, 
                                forced_value = self.objeto.almacenOrigen 
                                    and self.objeto.almacenOrigen.nombre 
                                    or None)
        utils.combo_set_from_db(self.wids['cbe_almacenDestinoID'], 
                                self.objeto.almacenDestinoID, 
                                forced_value = self.objeto.almacenDestino 
                                    and self.objeto.almacenDestino.nombre 
                                    or None)
        self.revivir(self.wids['cbe_almacenOrigenID'])
        self.revivir(self.wids['cbe_almacenDestinoID'])
        self.wids['b_guardar'].set_sensitive(False) # Deshabilito el guardar 
                        # antes de actualizar para evitar "falsos positivos".
        self.objeto.make_swap()
        self.activar_packing_list()
        # Tipo de albarán
        self.wids['l_str_tipo'].set_text("<i>%s</i>" 
            % self.objeto.get_str_tipo())
        self.wids['l_str_tipo'].set_use_markup(False) # AWKWARD GTK BUG!
        self.wids['l_str_tipo'].set_use_markup(True)
        # No dejo cambiar almacenes de origen ni destino si ya se han metido 
        # líneas de venta, porque al añadir las LDV es cuando se descuentan 
        # existencias de los almacenes. Si lo quiere cambiar, que elimine las 
        # LDVs, cambie el almacén y las vuelva a meter.
        hay_ldvs = bool(self.objeto.lineasDeVenta)
        self.wids['cbe_almacenOrigenID'].set_sensitive(not hay_ldvs)
        self.wids['cbe_almacenDestinoID'].set_sensitive(not hay_ldvs)
        self.sombrear_entry_motivo(self.wids['ch_facturable'])
        self.resaltar_credito(self.wids['cbe_cliente'])

    def activar_packing_list(self):
        """
        Muestra u oculta el botón de packing list dependiendo de si en las 
        líneas de venta hay productos de venta (susceptibles de llevar bultos 
        con código propio) o no (en cuyo caso no se puede imprimir packing 
        list).
        """
        mostrar = len([ldv.productoVenta 
                       for ldv in self.objeto.lineasDeVenta 
                       if ldv.productoVenta != None]) > 0
        self.wids['b_packinglist'].set_property("visible", mostrar)

    def rellenar_ldds(self, albaran):
        """
        Rellena las devoluciones correspondientes a este albarán 
        que se hayan hecho en abonos.
        """
        model = self.wids['tv_abonado'].get_model()
        model.clear()
        ldds = albaran.lineasDeDevolucion
        padres_abonos = {}      # abono: {'iter': iter del treeView, 'productos': {producto: iter_del_producto}
        for ldd in ldds:
            abono = ldd.abono
            if abono not in padres_abonos:
                padres_abonos[abono] = {
                    'iter': model.append(None, (abono.numabono, 
                                                utils.str_fecha(abono.fecha), 
                                                "", 
                                                "", 
                                                "", 
                                                abono.get_puid())), 
                    'productos': {}}
            producto = ldd.articulo.productoVenta
            if producto not in padres_abonos[abono]['productos']:
                padres_abonos[abono]['productos'][producto] = model.append(
                    padres_abonos[abono]['iter'], 
                    ("", 
                     "", 
                     producto.codigo, 
                     producto.descripcion, 
                     "", 
                     producto.get_puid()
                    )
                   )
            model.append(padres_abonos[abono]['productos'][producto], 
                         ("", 
                          "", 
                          "", 
                          "", 
                          ldd.articulo.codigo_interno, 
                          ldd.get_puid()
                         )
                        )

    def get_pedidos(self, albaran):
        pedidos = []
#        pedidos.extend([ldv.pedidoVenta.numpedido for ldv in albaran.lineasDeVenta if ldv.pedidoVenta and ldv.pedidoVenta.numpedido not in pedidos])
        for ldv in albaran.lineasDeVenta:
            if ldv.pedidoVenta != None and ldv.pedidoVenta not in pedidos:
                pedidos.append(ldv.pedidoVenta)
        return pedidos 

    def mostrar_transportista(self, transportista):
        if transportista == None:
            self.wids['cbe_dni'].set_active(-1)
            self.wids['cbe_dni'].child.set_text('')
            self.wids['e_nombre'].set_text('')
            self.wids['e_agencia'].set_text('')
            self.wids['e_matricula'].set_text('')
            self.wids['e_telefono'].set_text('')
        else:
            utils.combo_set_from_db(self.wids['cbe_dni'], transportista.id)
            self.wids['e_nombre'].set_text(transportista.nombre)
            self.wids['e_agencia'].set_text(transportista.agencia)
            self.wids['e_matricula'].set_text(transportista.matricula)
            self.wids['e_telefono'].set_text(transportista.telefono)
        self.wids['b_guardar_transportista'].set_sensitive(False)

    def mostrar_destino(self, destino):
        if destino == None:
            self.wids['cbe_nom'].set_active(-1)
            self.wids['cbe_nom'].child.set_text('')
            self.wids['e_cp'].set_text('')
            self.wids['e_ciudad'].set_text('')
            self.wids['e_pais'].set_text('')
            self.wids['e_telf'].set_text('')
            self.wids['e_direccion'].set_text('')
        else:
            utils.combo_set_from_db(self.wids['cbe_nom'], destino.id)
            self.wids['e_cp'].set_text(destino.cp)
            self.wids['e_ciudad'].set_text(destino.ciudad)
            self.wids['e_pais'].set_text(destino.pais)
            self.wids['e_telf'].set_text(destino.telefono)
            self.wids['e_direccion'].set_text(destino.direccion)
        self.wids['b_guardar_destino'].set_sensitive(False)

    def agrupar_articulos(self, albaran):
        """
        Crea un diccionario cuyas claves son un ID de línea de venta
        los valores son listas de articulos del producto de la LDV.
        No se permite que un mismo artículo se relacione con dos LDVs
        distintas.
        Si la cantidad de los artículos (en m2, kilos, etc...) supera
        de la LDV donde se quiere añadir, se intentará añadir a otra
        LDV del mismo producto. Si no hay más LDV, se añadirá a la 
        LDV que haya.
        NOTA: Marcado como DEPRECATED para próximas versiones.
        """
        return self.objeto.agrupar_articulos()
        # Creo un diccionario con todas las LDVs. Dentro del diccionario irá
        # un campo 'codigo' con el código del producto de la LDV, un 'articulos'
        # con una lista de artículos relacionados a la LDV, un 'cantidad' con 
        # la cantidad añadida y un 'ldv' con el objeto LDV.
        d = {}
        for ldv in [ldv for ldv in albaran.lineasDeVenta]:
            # d[ldv.id] = {'codigo': ldv.productoVenta.codigo, 'articulos': [], 'cantidad' : 0.0, 'ldv': ldv}
            d[ldv.id] = {'codigo': ldv.producto.codigo, 
                         'articulos': [], 
                         'idsarticulos': [], 
                         'cantidad' : 0.0, 
                         'ldv': ldv}
            # for a in albaran.articulos:    # CWT: Hay que contar también con las devoluciones como parte del albarán. Aunque se hayan devuelto. No importa. Al imprimir el albarán DEBEN VOLVER A APARECER AHí. Porque sí, porque... porque sí, ¡se sienten coño!
        for a in utils.unificar(albaran.articulos 
                  + [ldd.articulo for ldd in albaran.lineasDeDevolucion] 
                  + [ldm.articulo for ldm in albaran.lineasDeMovimiento]):
            codigo = a.productoVenta.codigo
            # OJO: NO deberían haber artículos de productos que no se han 
            # pedido. O al menos no debería haber artículos sin LDV (aunque 
            # la LDV no tenga pedido asignado).
            idldv = self.buscar_ldv(d, codigo, a.get_cantidad())
            # TODO: Sería preferible no crear líneas de venta sin pedido y 
            # borrar los artículos que sobran.
            # XXX
            if idldv == None:
                print >> sys.stderr, "WARNING(1)::albaranes_de_salida.py -> "\
                    "No hay línea de venta para el artículo con id %d."%(a.id)
                print >> sys.stderr, "WARNING(2)::albaranes_de_salida.py -> "\
                    "Creando línea de venta sin pedido."
                ldv = pclases.LineaDeVenta(pedidoVenta = None, 
                                           facturaVenta = None, 
                                           productoVenta = a.productoVenta, 
                                           albaranSalida = albaran, 
                                           cantidad = 0)
                pclases.Auditoria.nuevo(ldv, self.usuario, __file__)
                idldv = ldv.id
                d[idldv] = {'codigo': ldv.producto.codigo, 'articulos': [], 
                            'cantidad' : 0.0, 'ldv': ldv, 'idsarticulos': []}
                print >> sys.stderr, "WARNING(3)::albaranes_de_salida.py :"\
                                " Línea de venta con id %d creada." % (idldv)
            # XXX
                utils.dialogo_info(titulo = "REPASE EL CONTENIDO DEL ALBARÁN",
                                   texto = """
                Se han detectado artículos relacionados con el albarán sin pedido asociado.                 
                Se ha creado una línea de venta que contiene esos artículos con cantidad 0.
                Esta nueva línea de venta aparecerá marcada en rojo. Actualice la cantidad
                de acuerdo a las existencias servidas o bórrela si considera que es incorrecta.
                Se enviará un informe de error al salir de la aplicación para evitar que se
                repita esta situación en el futuro.
                """, 
                                   padre = self.wids['ventana'])
            # idldv NO debería ser None. Si lo es, algo grave pasa; 
            # prefiero que salte la excepción.
            d[idldv]['articulos'].append(a)
            d[idldv]['idsarticulos'].append(a.id)
            d[idldv]['cantidad'] += a.get_cantidad()
        return d

    def buscar_ldv(self, d, codigo, cantidad):
        """
        Busca en el diccionario d, la clave cuyo valor (que es otro 
        diccionario) contiene el código c en el campo 'codigo' Y la
        cantidad de la LDV sea superior a la cantidad ya añadida (es
        otro campo del diccionario que hace de valor del primer 
        diccionario) más la que se quiere añadir -cant-.
        Si no se encuentra una LDV donde la cantidad sea superior o 
        igual, devolverá cualquiera de las LDV donde coincida el 
        código, aunque después al añadir se sobrepase la cantidad.
        Suena lioso... pero no lo es... ¿o sí? Que va, viendo el 
        código se ve muy claro.
        Devuelve la clave o None si no se encontró.
        """
        res = None
        for idldv in d:
            # XXX
            # if idldv == 0: return None
            # XXX
            if d[idldv]['codigo'] == codigo:
                res = idldv
                if d[idldv]['cantidad'] + cantidad <= d[idldv]['ldv'].cantidad:
                    res = idldv
                    break
        return res

    # --------------- Manejadores de eventos ----------------------------
    def crear_nuevo_albaran(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        albaran = self.objeto
        #nuevo_numalbaran = pclases.AlbaranSalida.get_siguiente_numero_numalbaran()
        nuevo_numalbaran = pclases.AlbaranSalida.get_siguiente_numero_numalbaran_str()
            # Datos a pedir:
        numalbaran = utils.dialogo_entrada(titulo = "NÚMERO DE ALBARÁN", 
            texto = 'Introduzca un número para el albarán.\nDeje el número '
                    'de albarán por defecto si no está seguro.', 
            valor_por_defecto = nuevo_numalbaran, 
            padre = self.wids['ventana'])
        if numalbaran == None: 
            return
        # numero_numalbaran = utils.parse_numero(numalbaran)
        numero_numalbaran_usuario = utils.parse_numero(numalbaran, 
                                        invertir = True)
        numero_numalbaran_sugerido = utils.parse_numero(nuevo_numalbaran, 
                                        invertir = True)
        #if self.usuario != None and self.usuario.nivel > 1 and numero_numalbaran != None and numero_numalbaran > nuevo_numalbaran:
        if (self.usuario 
            and self.usuario.nivel > 2 
            and numero_numalbaran_usuario != None 
            and numero_numalbaran_usuario > numero_numalbaran_sugerido):
            utils.dialogo_info(titulo = "NÚMERO DE ALBARÁN INCORRECTO", 
                texto = "No es estrictamente necesario que todos los albaranes"
                        " sean consecutivos.\n\nSin embargo, no se aconseja "
                        "crear albaranes con número superior al sugerido.\n\n"
                        "Si considera que debe hacerlo, contacte con un "
                        "usuario con mayor nivel de privilegios.", 
                padre = self.wids['ventana'])
            return
        if albaran != None: albaran.notificador.desactivar()
        # CWT: El programa debe pedir siempre el almacén origen porque se le 
        # va la pinza al usuario, se olvida de elegirlo y se queda con el 
        # principal por defecto, etc.
        almacenes = [(a.id, a.nombre) 
                     for a in pclases.Almacen.select(
                         pclases.Almacen.q.activo == True, 
                         orderBy = "id")]
        almacenppal = pclases.Almacen.get_almacen_principal_id_or_none()
        almo = utils.dialogo_combo(titulo = "ALMACÉN ORIGEN", 
                    texto = "Seleccione el almacén origen de la mercancía",  
                    ops = almacenes, 
                    padre = self.wids['ventana'], 
                    valor_por_defecto = almacenppal)
        if not almo:    # Cancelar
            return
        #try:
        #    almo = pclases.Almacen.select(
        #        pclases.Almacen.q.principal == True, 
        #        orderBy = "id")[0].id
        #except IndexError:
        #    almo = None
        try:
            albaran = pclases.AlbaranSalida(
                numalbaran = numalbaran,
                transportista = None,
                cliente = None, 
                bloqueado = False, 
                facturable = True, 
                destino = None, 
                fecha = mx.DateTime.localtime(), 
                almacenOrigenID = almo, 
                almacenDestinoID = None)
            pclases.Auditoria.nuevo(albaran, self.usuario, __file__)
            # OJO: Con la última modificación de SQLObject el valor por 
            # defecto para los DateTime no es correcto.Mirar si en otros 
            # nuevo_* ocurre lo mismo.
            utils.dialogo_info('ALBARÁN CREADO', 
                'El albarán %s ha sido creado.\n'
                'No olvide asociar las salidas.' % albaran.numalbaran, 
                padre = self.wids['ventana'])
            self.nuevo = True
            self.modificado = False
        except Exception, e:
            #utils.dialogo_info('ERROR: ALBARÁN NO CREADO', 'El albarán %s no ha sido creado.\nCompruebe que el número no esté siendo usado y vuelva a intentarlo.\n\n\nError:\n%s' % (numalbaran, e), padre = self.wids['ventana']) 
            self.logger.error("%salbaranes_de_salida::crear_nuevo_albaran "
                "-> Error al crear nuevo albarán. Excepción capturada: %s" % (
                    self.usuario and self.usuario.usuario+": " or "", e))
            utils.dialogo_info('ERROR: ALBARÁN NO CREADO', 
                'El albarán %s no ha sido creado.\nCompruebe que el número '
                'no esté siendo usado y vuelva a intentarlo.\n\n\n' % (
                    numalbaran), 
                padre = self.wids['ventana']) 
        albaran.notificador.activar(self.aviso_actualizacion)
        self.objeto = albaran
        self.actualizar_ventana()

    def buscar_albaran(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        albaran = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR ALBARÁN", 
                    texto = "Introduzca número de albarán: ", 
                    padre = self.wids['ventana']) 
        if a_buscar != None:
            resultados = pclases.AlbaranSalida.select(
                pclases.AlbaranSalida.q.numalbaran.contains(a_buscar))
            if resultados.count() > 1:
                ## Refinar los resultados
                idalbaran = self.refinar_resultados_busqueda(resultados)
                if idalbaran == None:
                    return
                resultados = [pclases.AlbaranSalida.get(idalbaran)]
                    # Se supone que la comprensión de listas es más rápida que hacer un nuevo get a SQLObject.
                    # Me quedo con una lista de resultados de un único objeto ocupando la primera posición.
                    # (Más abajo será cuando se cambie realmente el objeto actual por este resultado.)
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)', padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            self.preguntar_si_redistribuir()
            if albaran != None:
                albaran.notificador.desactivar()
            # Pongo el objeto como actual
            albaran = resultados[0]
            self.nuevo = False
            self.modificado = False
            # Y activo la función de notificación:
            albaran.notificador.activar(self.aviso_actualizacion)
        self.objeto = albaran
        self.actualizar_ventana()

    def guardar_transportista(self, w):
        idtransp = utils.combo_get_value(self.wids['cbe_dni'])
        if idtransp == None:
            self.crear_nuevo_transportista()
        else:
            self.actualizar_transportista(idtransp)
        self.modificado = True
        self.wids['b_guardar_transportista'].set_sensitive(False)
    
    def guardar_destino(self, w):
        iddest = utils.combo_get_value(self.wids['cbe_nom'])
        if iddest == None:
            self.crear_nuevo_destino()
        else:
            self.actualizar_destino(iddest)
        self.modificado = True
        self.wids['b_guardar_destino'].set_sensitive(False)
    
    def guardar(self, widget, actualizar_ventana = True):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        albaran = self.objeto
        # Campos del objeto que hay que guardar:
        numalbaran = self.wids['e_numalbaran'].get_text()
        fecha = self.wids['e_fecha'].get_text()
        idcliente = utils.combo_get_value(self.wids['cbe_cliente'])
        idalmo = utils.combo_get_value(self.wids['cbe_almacenOrigenID'])
        idalmd = utils.combo_get_value(self.wids['cbe_almacenDestinoID'])
        # Desactivo el notificador momentáneamente
        albaran.notificador.desactivar()
        # Actualizo los datos del objeto
        albaran.almacenOrigenID = idalmo
        albaran.almacenDestinoID = idalmd
        try:
            albaran.numalbaran = numalbaran
        except Exception, msg:
            utils.dialogo_info(titulo = "ERROR AL GUARDAR NÚMERO DE ALBARÁN", 
                    texto = "Ocurrió un error al guardar el número de albarán."
                            "\nCompruebe que el número de albarán no está\n"
                            "duplicado.", 
                    padre = self.wids['ventana'])
        albaran.bloqueado = self.wids['ch_bloqueado'].get_active()
        albaran.facturable = self.wids['ch_facturable'].get_active()
        albaran.motivo = self.wids['e_motivo'].get_text()
        try:
            albaran.fecha = utils.parse_fecha(fecha)
        except:
            albaran.fecha = mx.DateTime.localtime()
        if idcliente != None:
            albaran.cliente = pclases.Cliente.get(idcliente)
        else:
            albaran.cliente = None
        albaran.nombre = self.wids['cbe_nom'].child.get_text()
        albaran.cp = self.wids['e_cp'].get_text()
        albaran.ciudad = albaran.ciudad = self.wids['e_ciudad'].get_text()
        albaran.pais = self.wids['e_pais'].get_text()
        albaran.telefono = self.wids['e_telf'].get_text()
        albaran.direccion = self.wids['e_direccion'].get_text() 
        buff = self.wids['tv_observaciones'].get_buffer()
        albaran.observaciones = buff.get_text(buff.get_start_iter(), buff.get_end_iter())
        self.guardar_transportista(None)
        albaran.transportistaID = utils.combo_get_value(self.wids['cbe_dni'])
        self.guardar_destino(None)
        albaran.destinoID = utils.combo_get_value(self.wids['cbe_nom'])
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo 
        # haga por mí:
        albaran.sync()
        # Vuelvo a activar el notificador
        albaran.notificador.activar(self.aviso_actualizacion)
        self.objeto = albaran
        self.modificado = True
        if actualizar_ventana:
            self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def buscar_fecha(self, boton):
        self.wids['e_fecha'].set_text(utils.str_fecha(utils.mostrar_calendario(fecha_defecto = self.objeto and self.objeto.fecha or None, padre = self.wids['ventana'])))

    def refinar_busqueda_pedido(self, pedidos):
        """
        Recibe un resultado de sqlobject con los pedidos
        buscados.
        Precondiciones: pedidos.count() > 1
        Devuelve una lista con el pedido seleccionado en la
        primera posición o None si se cancela el diálogo.
        """
        peds = [(p.id, "%s: %s - %s" % (p.numpedido, 
                    p.cliente and p.cliente.nombre or 'SIN CLIENTE', 
                    p.fecha and p.fecha.strftime('%d/%m/%Y') or 'SIN FECHA')) 
                for p in pedidos]
        peds.sort(key = lambda p: p[0], reverse = True)
        resp = utils.dialogo_combo(texto = 'Se encontraron varios pedidos con'
                                           ' el mismo número.\nSeleccione uno'
                                           ' de ellos.',
                                   ops = peds, 
                                   padre = self.wids['ventana'])
        if resp == None:
            return None
        return [p for p in pedidos if p.id == resp]

    def add_pedido(self, boton):
        """
        Añade las líneas de venta de un pedido al albarán. En lugar de añadir 
        todas de golpe, permite seleccionar al usuario las que agregará.
        Por defecto seguirán siendo todas.
        """
        if self.objeto and self.objeto.bloqueado:
            if not utils.dialogo(titulo = "ALBARÁN BLOQUEADO", 
                    texto = "El albarán se encuentra bloqueado.\n"
                            "¿Desea continuar?", 
                    padre = self.wids['ventana']):
                return
        copiar_dirobra = False
        if (self.objeto.cliente 
            and self.objeto.cliente.calcular_credito_disponible() <= 0):
                # Aquí todavía no controlo si sumando el pedido o el albarán
                # se pasa del crédito.
            utils.dialogo_info(titulo = "CLIENTE SIN CRÉDITO", 
                               texto = "El cliente ha sobrepasado el "
                                       "crédito concedido.", 
                               padre = self.wids['ventana'])
            self.to_log("[add_pedido] Cliente sin crédito.", 
                        {"cliente": self.objeto.cliente.get_info(), 
                         "albarán": self.objeto.numalbaran, 
                         "crédito disponible": 
                            self.objeto.cliente.calcular_credito_disponible()
                        }, nivel = self.logger.INFO) 
            return
        if self.comprobar_cliente_deudor():
            try:
                infocliente = self.objeto.cliente.get_info()
            except AttributeError:
                infocliente = "¿Sin self.objeto.cliente?"
            self.to_log("[add_pedido] Cliente deudor.", 
                        {"cliente": infocliente, 
                         "albarán": self.objeto.numalbaran, 
                        })
            return
        numpedido = utils.dialogo_entrada(titulo = 'NÚMERO DE PEDIDO',
                        texto = 'Introduzca el número del pedido',
                        padre = self.wids['ventana'])
        if numpedido == None:
            return
        if self.objeto.cliente != None:
            pedidos = pclases.PedidoVenta.select(pclases.AND(
                pclases.PedidoVenta.q.numpedido.contains(numpedido), 
                pclases.PedidoVenta.q.clienteID == self.objeto.cliente.id, 
                pclases.PedidoVenta.q.cerrado == False))
        else:
            pedidos = pclases.PedidoVenta.select(pclases.AND(
                pclases.PedidoVenta.q.numpedido.contains(numpedido), 
                pclases.PedidoVenta.q.cerrado == False))
        if pedidos.count() > 1:
            pedidos = self.refinar_busqueda_pedido(pedidos)
            if pedidos == None:
                return
        try:
            pedido = pedidos[0]
        except:
            # No se encontró
            nombrecliente = (self.objeto and self.objeto.cliente 
                             and "«"+self.objeto.cliente.nombre+"» " or "")
            utils.dialogo_info(titulo = 'NO ENCONTRADO', 
                    texto = 'Pedido no encontrado, no es del cliente %s'
                            'o no admite más albaranes.' % nombrecliente, 
                    padre = self.wids['ventana'])
            return
        pedido.sync()   # Por si ha habido cambios y no 
                        # ha saltado el fallo de caché.
        # Primera comprobación, que el pedido no lleve más de lo ofertado. 
        # Decido hacerlo aquí y no en comprobar las cantidades en la propia 
        # ventana de los pedidos ante cada cambio o incluso mejor que justo 
        # antes de imprimir, así doy más tiempo al usuario a corregirlo.
        prods_pedidos = {}
        for presupuesto in pedido.get_presupuestos():
            presupuesto.sync() #Por si se borrado, recreado, modificado, etc...
            pedido_en_presupuesto = presupuesto.get_pedido_por_producto()
            for producto in pedido_en_presupuesto:
                try:
                    prods_pedidos[producto] = pedido_en_presupuesto[producto]
                except: 
                    prods_pedidos[producto] = pedido_en_presupuesto[producto]
            for ldp in presupuesto.lineasDePresupuesto:
                producto = ldp.producto 
                if not producto:    # Es servicio, clasifico por descripción.
                    producto = ldp.descripcion
                try:
                    prods_pedidos[producto] -= ldp.cantidad
                except: 
                    prods_pedidos[producto] = -ldp.cantidad
        # Y ahora por fin cotejo las cantidades.
        for producto in prods_pedidos:
            if prods_pedidos[producto] > 0:
                utils.dialogo_info(titulo = "PEDIDO EXCEDE OFERTA", 
                        texto = "En el pedido %s la cantidad de %s \n"
                                "excede en %s a la ofertada en %s." % (
                                    pedido.numpedido, 
                                    isinstance(producto, str) and producto or 
                                        producto.descripcion, 
                                    utils.float2str(prods_pedidos[producto]), 
                                    ", ".join([str(p.id) for p 
                                               in pedido.get_presupuestos()])), 
                        padre = self.wids['ventana'])
                return
        # Ahora compruebo validación del pedido.
        if not pedido.validado:
            utils.dialogo_info(titulo = "PEDIDO NO VALIDADO", 
                    texto = "El pedido contiene ventas por debajo del precio\n"
                            " mínimo o bien el cliente no satisface las \n"
                            "condiciones de riesgo:\n\n"
                            "\t· %s\n\n"
                            "Solicite a un usuario con permisos suficientes \n"
                            "la validación del pedido desde la ventana de \n"
                            "pedidos de venta." % (pedido.get_str_estado()), 
                    padre = self.wids['ventana'])
            return
        importe_pedido = pedido.calcular_importe_total(iva = True)
        if pclases.DEBUG:
            print "albaranes_de_salida -> importe_pedido", importe_pedido 
        cliente = pedido.cliente
        try:
            infocliente = cliente.get_info()
            credicliente = cliente.calcular_credito_disponible(
                            base = importe_pedido)
        except AttributeError:
            infocliente = credicliente = "¿Sin self.objeto.cliente?"
        if (pedido.cliente 
            #and pedido.cliente.calcular_credito_disponible(
            #    base = importe_pedido) <= 0):
            and credicliente <= 0):
            if not utils.dialogo(titulo = "CLIENTE SIN CRÉDITO", 
                                 texto = "El cliente sobrepasa el "
                                         "crédito concedido sumando el "
                                         "importe del pedido %s (%s €).\n\n"
                                         "\t\t¿Continuar?" % (
                                            pedido.numpedido, 
                                            utils.float2str(importe_pedido)), 
                                 padre = self.wids['ventana'], 
                                 defecto = gtk.RESPONSE_NO, 
                                 tiempo = 15, 
                                 icono = gtk.STOCK_DIALOG_WARNING):
                self.to_log("[add_pedido] Cliente sin crédito.", 
                            {"cliente": infocliente, 
                             "albarán": self.objeto.numalbaran, 
                             "crédito disponible": credicliente,
                             "base": importe_pedido,
                             "pedido": pedido.numpedido, 
                             "¿continuar?": False
                            }, nivel = self.logger.INFO) 
                return
            else:
                self.to_log("[add_pedido] Cliente sin crédito.", 
                            {"cliente": infocliente, 
                             "albarán": self.objeto.numalbaran, 
                             "crédito disponible": credicliente, 
                             "base": importe_pedido,
                             "pedido": pedido.numpedido, 
                             "¿continuar?": True
                            }, nivel = self.logger.INFO) 
        if self.comprobar_cliente_deudor():
            if self.objeto.cliente:
                infocliente = self.objeto.cliente.get_info()
            else:
                infocliente = "¿Sin self.objeto.cliente?"
            self.to_log("[add_pedido] Cliente deudor.", 
                        {"cliente": infocliente, 
                         "albarán": self.objeto.numalbaran, 
                        })
            return
        if pedido.cerrado:
            utils.dialogo_info(titulo = "PEDIDO CERRADO",
                texto = "El pedido está cerrado y no admite más albaranes.",
                padre = self.wids['ventana'])
        else:
            albaran = self.objeto
            if albaran.cliente == None:
                albaran.cliente = pedido.cliente
            if pedido.cliente != albaran.cliente:
                txtdlg='El cliente del pedido y del albarán debe ser el mismo.'
                utils.dialogo_info(titulo = 'PEDIDO INCORRECTO',
                                   texto = txtdlg, 
                                   padre = self.wids['ventana'])
            else:
                try:
                    ldps_a_incluir, srvs_a_incluir = select_lineas_pedido(
                            pedido, padre = self.wids['ventana'])
                except TypeError: #Ha cancelado y ha devuelto None. No 2 listas
                    return 
                not_included = []
                #for ldp in pedido.lineasDePedido[:]:
                for ldp in ldps_a_incluir:
                    # DONE: No unificar si tiene precios de venta distintos. 
                    # Arreglado directamente en pclases para que devuelva 
                    # cantidades servidas y pedidas teniendo en cuenta también 
                    # el precio.
                    # DONE: Problema: A veces quieren servir la mitad de un 
                    # producto a un precio y la otra mitad a otro. 
                    # ¿Cómo lo hago? Fácil: Pongo a mano en la ventana la 
                    # cantidad de cada línea que quiero servir y el algoritmo 
                    # irá completando las líneas de arriba a abajo.
                    if (not ldp.albaraneada     # Queda algo por servir
                        or (ldp.cantidad < 0 
                            and ldp.cantidadPedida - ldp.cantidadServida != 0)):
                            # CWT: O tiene cantidad negativa por un abono made 
                            #      in BP y no se ha añadido ya a un albarán.
                        # Esto habría que refactorizarlo un día, mientras 
                        # tanto, resumen del estado hasta aquí:
                        # Tenemos una línea de pedido con catidad pendiente 
                        # de servir, que puede ser negativa o positiva, pero 
                        # no cero. Ahora hay que comprobar -si la cantidad 
                        # es postiva- que hay existencias suficientes en 
                        # almacén. Si no, preguntar si servir lo que haya.
                        cantidad_a_servir = (ldp.cantidadPedida 
                                             - ldp.cantidadServida)
                        if self.usuario and self.usuario.nivel > 2:
                            cantidad_a_servir=comprobar_existencias_producto(
                                                ldp, 
                                                self.wids['ventana'], 
                                                cantidad_a_servir, 
                                                self.objeto.almacenOrigen)
                        if not cantidad_a_servir:   # Es 0 o None. Pasando
                            continue    # Next line, please.
                        ldv = pclases.LineaDeVenta(
                                pedidoVentaID = ldp.pedidoVentaID, 
                                facturaVenta = None,
                                productoVentaID = ldp.productoVentaID,
                                productoCompraID = ldp.productoCompraID, 
                                albaranSalidaID = self.objeto.id,
                                fechahora = mx.DateTime.localtime(),
                                cantidad = cantidad_a_servir,
                                precio = ldp.precio, 
                                descuento = ldp.descuento, 
                                notas = ldp.notas)
                        pclases.Auditoria.nuevo(ldv, self.usuario, __file__)
                        ajustar_existencias(ldv)
                    else:
                        # Si no se ha albaraneado porque la cantidad del 
                        # producto viene incluida en una LDP anterior del 
                        # mismo producto, al mismo precio y descuento (a.k.a. 
                        # "se han unificado"), no la considero como "no 
                        # albaraneada".
                        albaranes_de_la_ldp = ldp.albaranesSalida
                        if (not (len(albaranes_de_la_ldp) == 1 
                                 and albaranes_de_la_ldp[0] == self.objeto)):
                            not_included.append(ldp)
                if not_included:
                    def get_nombre_producto(ldp):
                        producto = ldp.get_producto()
                        if hasattr(producto, "nombre"):
                            nombreproducto = producto.nombre
                        elif hasattr(producto, "descripcion"):
                            nombreproducto = producto.descripcion
                        else:
                            nombreproducto = "?"
                        return nombreproducto
                    # TODO: Para pedidos con muchos albaranes, la lista de números de albarán es demasiado larga y el diálogo sobrepasa el ancho de la pantalla.
                    utils.dialogo_info(titulo = 'LÍNEAS NO ALBARANEADAS',
                                       texto = """
                    Las siguientes líneas de venta no se agregaron al albarán                   
                    por estar ya relacionadas con otra salida de material.
                    Modifique el pedido original o los albaranes asociados 
                    si quiere agregarlas al albarán actual:
                    """ + '\n      - ' + '\n      - '.join(["Producto %s. Cantidad %.2f. Albarán de salida número %s" \
                                    % (get_nombre_producto(ldp), ldp.cantidad, ", ".join(utils.unificar([a.numalbaran for a in ldp.albaranesSalida if a != None]))) \
                                    for ldp in not_included]), 
                                        padre = self.wids['ventana'])
                #for srv in pedido.servicios:
                for srv in srvs_a_incluir:
                    if srv.albaranSalida == None:
                        srv.albaranSalida = self.objeto
                # Y ahora copio la dirección de envío.
                copiar_dirobra = True
            self.modificado = True
            self.objeto.calcular_comisiones()
            self.actualizar_ventana()
            # Y ahora sí que sí copio la dirección de envío. Después de 
            # actualizar para que no me machaque la información con la 
            # que tiene guardada el albarán.
            if copiar_dirobra:
                self.copiar_direccion_envio_del_pedido(pedido)

    def copiar_direccion_envio_del_pedido(self, pedido):
        """
        Copia en los entries de la dirección de envío la dirección del 
        pedido de venta.
        """
        if pedido != None:
            self.wids['cbe_nom'].child.set_text(pedido.nombreCorrespondencia)
            self.wids['e_direccion'].set_text(pedido.direccionCorrespondencia)
            self.wids['e_cp'].set_text(pedido.cpCorrespondencia) 
            self.wids['e_ciudad'].set_text(pedido.ciudadCorrespondencia)
            self.wids['e_pais'].set_text(pedido.paisCorrespondencia)
 
    def crear_ldv(self, articulos):
        """
        Verifica que los artículos pertenezcan a una LDV existente.
        Recibe una lista de artículos que deben ser del mismo producto de venta.
        Verifica también que el artículo no esté en otro albarán de salida y 
        que haya sido analizado.
        """
        if len(articulos) == 0:
            return
        albaran = self.objeto
        productos_malos = []
        for articulo in articulos:
            articuloproductoVenta = articulo.productoVenta
            if (articuloproductoVenta not in 
                    [ldv.productoVenta for ldv in albaran.lineasDeVenta]):
                if articuloproductoVenta not in productos_malos:    # Para 
                    # evitar tratar el mismo producto y mismo error una y 
                    # otra vez.
                    productos_malos.append(articulo.productoVenta)
                    res = utils.dialogo(titulo = 'ERROR', 
                            texto = 'El cliente no solicitó el producto %s en'\
                                    ' el pedido.\n\n¿Desea continuar?' % (
                                        articulo.productoVenta.descripcion), 
                            padre = self.wids['ventana'], 
                            icono = gtk.STOCK_DIALOG_ERROR)
                    if not res:
                        return
            else:
                if (articulo.albaranSalida == None 
                    or articulo.albaranSalida == self.objeto 
                    # Ahora la condición para ver si está en almacén es que 
                    # tenga relación con un almacén (obvious comment is 
                    # obvious).
                    or articulo.almacen):
                        # Los artículos D llegan aquí ya añadidos al albarán, 
                        # por eso incluyo el caso de que tenga 
                        # ya albarán pero sea justo al que estamos añadiendo 
                        # artículos. Si no, mostrará el error 
                        # de la rama "else".
                    if (articulo.es_bala_cable() 
                        or articulo.es_rollo_defectuoso() 
                        or articulo.es_rolloC() 
                        or articulo.analizado):     
                        # La fibra de cable y rollos defectuosos no se analizan.
                        articulo.albaranSalida = albaran
                        #articulo.almacen = None
                        #articulo.almacen = self.objeto.almacenDestino   
                        # será None cuando no sea un albarán de transferencia.
                        if self.objeto.almacenDestino:
                            articulo.mover_entre_almacenes(
                                self.objeto.almacenOrigen, 
                                self.objeto.almacenDestino, 
                                self.objeto)
                        else:
                            articulo.almacen = None
                    else:
                        res = utils.dialogo(titulo = 'PRODUCTO NO ANALIZADO', 
                                            texto = """
                        El artículo %s no ha sido analizado en 
                        el laboratorio. No puede vender un producto                 
                        cuyas características de lote o partida                     
                        no han sido verificados.                                    
                                                                                    
                        ¿Desea continuar?
                        """ % (articulo.codigo), 
                                            padre = self.wids['ventana'], 
                                            icono = gtk.STOCK_DIALOG_WARNING)
                        if not res:
                            return
                else:
                    res = utils.dialogo(titulo = 'ERROR', 
                                        texto = """
                El artículo %s salió en el albarán %s.
                Si cree que es incorrecto. Compruebe el             
                albarán, elimine de allí el artículo                
                y vuelva a intentarlo.                              
                                                                    
                """ % (articulo.codigo, articulo.albaranSalida.numalbaran), 
                                        padre = self.wids['ventana'], 
                                        icono = gtk.STOCK_DIALOG_ERROR)
                    if not res:
                        return
        self.modificado = True

    def drop_ldv(self, boton):
        """
        Pone a None el idalbaran de la 
        línea de venta seleccionada y 
        a False la confirmación (aumentando
        la cantidad del artículo).
        """
        if self.wids['tv_ldvs'].get_selection().count_selected_rows() == 0:
            return
        model, paths = self.wids['tv_ldvs'].get_selection().get_selected_rows()
        for path in paths:
            itr = model.get_iter(path)
            if model[itr].parent == None:  # Es una LDV
                idldv = model[itr][-1]
                try:
                    #ldv = pclases.LineaDeVenta.get(idldv)
                    ldv = pclases.getObjetoPUID(idldv)
                except pclases.SQLObjectNotFound:   # Ya se ha borrado.
                    pass
                else:
                    self.desvincular_ldv_del_albaran(ldv)
            else:   # Es un artículo
                idarticulo = model[itr][-1] 
                #articulo = pclases.Articulo.get(idarticulo)
                objeto = pclases.getObjetoPUID(idarticulo)
                if isinstance(objeto, pclases.Pale):
                    vpro = VentanaProgreso(padre = self.wids['ventana'])
                    vpro.mostrar()
                    vpro.set_valor(0.0, "Devolviendo palé al almacén %s..." %
                        self.objeto.almacenOrigen.nombre)
                    total = len(self.objeto.articulos)
                    actual = 0.0
                    try:
                        for a in self.objeto.articulos:
                            actual += 1
                            vpro.set_valor(actual/total, texto = None)
                            if a.cajaID and a.caja.pale == objeto:
                                self.desvincular_articulo(a)
                    finally:
                        vpro.ocultar()
                elif isinstance(objeto, pclases.Caja):
                    vpro = VentanaProgreso(padre = self.wids['ventana'])
                    vpro.mostrar()
                    vpro.set_valor(0.0, "Devolviendo caja al almacén %s..." %
                        self.objeto.almacenOrigen.nombre)
                    total = len(self.objeto.articulos)
                    actual = 0.0
                    try:
                        for a in self.objeto.articulos:
                            actual += 1
                            vpro.set_valor(actual/total, texto = None)
                            if a.cajaID and a.caja == objeto:
                                self.desvincular_articulo(a)
                    finally:
                        vpro.ocultar()
                else:
                    self.desvincular_articulo(objeto)
            self.modificado = True
        self.objeto.calcular_comisiones()
        self.actualizar_ventana()

    def desvincular_articulo(self, articulo):
        """
        Devuelve un objeto artículo al almacén, desvinculándolo del albarán 
        de salida actual, sea cual sea el tipo del mismo y actuando en 
        consecuencia (sacándolo del almacén actual y devolviéndolo al original
        si era un albarán de transferencia, etc.).
        """
        articulo.albaranSalida = None
        if self.objeto.es_de_movimiento():
            fail = articulo.anular_movimiento(
                        self.objeto.almacenOrigen, 
                        self.objeto.almacenDestino, 
                        self.objeto)
            if fail:     # Algo ha fallado.
                articulo.albaranSalida = self.objeto
                utils.dialogo_info(
                    titulo = "ALBARANES DE SALIDA: ERROR", 
                    texto = "Se produjo un error al anular un "
                            "producto en el albarán actual (%d: %s)"
                            "\n\nCódigo de error: %d" % (
                                self.objeto.id, 
                                self.objeto.numalbaran, 
                                fail), 
                    padre = self.wids['ventana'])
                    # Códigos de error en un diálogo de error. Si Jacob 
                    # Nielsen levantara la cabeza... si... si estuviera 
                    # muerto, claro.
        else:
            articulo.almacen = self.objeto.almacenOrigen
            articulo.syncUpdate()
    
    def desvincular_ldv_del_albaran(self, ldv):
        # Primero hay que desvincular los artículos de la LDV.
        productoVenta = ldv.productoVenta
        albaran = self.objeto
        for articulo in albaran.articulos:
            if articulo.productoVenta == productoVenta and \
               len([ldv for ldv in albaran.lineasDeVenta 
                    if ldv.productoVenta == productoVenta]) == 1:    
                #Si hay más líneas del mismo producto no elimino sus artículos.
                self.desvincular_articulo(articulo)
        ajustar_existencias(ldv, 2 * ldv.cantidad)
            # Le paso el doble como cantidad anterior para que al restar quede en positivo e incremente la cantidad
        ldv.albaranSalida = None
        if ldv.facturaVentaID == None and ldv.prefacturaID == None:
            try:
                ldv.destroy(ventana = __file__)
            except:
                txterror = "albarabes_de_salida::desvincular_ldv_del_albaran -> La LDV ID %d no tiene albarán ni factura(s) pero no se pudo eliminar." % (ldv.id)
                print txterror
                self.logger.error(txterror)

    def desvincular_articulos_del_albaran(self, articulos):
        for a in articulos:
            self.desvincular_articulo(a)

    def borrar_albaran(self, boton):
        """
        Elimina el albarán de la BD y anula la relación entre
        él y sus LDVs.
        """
        if not utils.dialogo('Se eliminará el albarán actual y todas sus relaciones con ventas, pedidos, etc.\n¿Está seguro?', 'BORRAR ALBARÁN'): return
        albaran = self.objeto
        albaran.notificador.desactivar()
        for ldv in albaran.lineasDeVenta:
            self.desvincular_ldv_del_albaran(ldv)
        self.desvincular_articulos_del_albaran(albaran.articulos)
        try:
            albaran.destroy(ventana = __file__)
        except:
            utils.dialogo_info('ERROR', 'No se pudo eliminar.\nIntente eliminar primero los productos, servicios, transportes y comisiones del albarán.', padre = self.wids['ventana'])
            return
        self.ir_a_primero()

    def get_nums_pedidos(self, albaran, cortar = True):
        """
        Devuelve una cadena con la lista de 
        pedidos asociados al albarán.
        Si "cortar" es True, devuelve una cadena vacía 
        si hay más de dos pedidos (es para que al imprimir
        no se vaya del espacio reservado a los números de pedido).
        """
        pedidos = self.get_pedidos(albaran)
        if len(pedidos) > 2 and cortar:
            return ''
        else:
            return ', '.join([p.numpedido for p in pedidos])

    def contar_bultos_de_ldvs(self, prods, p):
        bultos = 0
        for ldv in prods[p]:
            try:
                datos_rollo = ldv.productoVenta.camposEspecificosRollo
                m2rollo = datos_rollo.metrosLineales * datos_rollo.ancho
                try:
                    bultos += int(ldv.cantidad / m2rollo)
                except ZeroDivisionError:
                    bultos += 0
            except AttributeError: 
                # producto no tiene campos específicos. Es bala.
                bultos += 0
        return bultos
        
    def preparar_llamada_imprimir(self, albaran):
        """
        Devuelve la lista de parámetros que se 
        pasarán a geninformes.
        """
        cliente = albaran.cliente
        if cliente == None:
            utils.dialogo_info(titulo = 'SIN CLIENTE', 
                texto = 'Debe seleccionar un cliente y guardar el albarán'  
                        ' antes de imprimirlo.', 
                padre = self.wids['ventana'])
            return None, None, None, None, None, None, None, None, None, None
        # Se acabaron las relaciones con Composan, ya no hacen falta sus 
        # albaranes amarillos.
        composan = False 
        #if 'COMPOSAN' in cliente.nombre.upper():
        #    composan = True
        #else:
        #    composan = False
        client = { 'nombre': cliente.nombre or "",
                   'direccion': cliente.direccionfacturacion or "",
                   'cp': cliente.cpfacturacion or "",
                   'ciudad': cliente.ciudadfacturacion or "", 
                   'provincia': cliente.provinciafacturacion or "", 
                   'pais': cliente.paisfacturacion or "",
                   'telf': cliente.telefono or ""
                 }
        if self.wids['e_telf'].get_text() == '':
            telefono = ''
        else:
            telefono = 'Teléfono: %s' % self.wids['e_telf'].get_text()   
        envio ={'nombre': self.wids['cbe_nom'].child.get_text(),
                'direccion': self.wids['e_direccion'].get_text(),
                'cp': self.wids['e_cp'].get_text() ,
                'localidad': self.wids['e_ciudad'].get_text(),
                'telefono': telefono,
                'pais': self.wids['e_pais'].get_text()}
                        
        general = {'albnum': albaran.numalbaran,
                   'fecha': albaran.fecha.strftime('%d/%m/%Y'),
                   'exp': '', 
                   'numcli': cliente.id,
                   'numped': self.get_nums_pedidos(albaran),
                   'numref': '',
                   'sref': ''
              }
        lineas = []
        prods = self.ldvs_agrupadas_por_producto(albaran)
        for producto in prods:
            # OJO: CHANGE: Otro CWT. Si los artículos añadidos a la LDV 
            #              son 0, tomo los del pedido, que se calculan en 
            #              base al producto.
            bultos = 0
            if hasattr(producto, "es_caja") and producto.es_caja():
                #bultospales = []
                #for ldv in prods[producto]:
                #    bultospales += [a.bolsa.caja.pale 
                #                    for a in self.__ldvs[ldv.id]['articulos']]
                #bultospales = utils.unificar(bultospales)
                #bultos = len(bultospales)
                # OPTIMIZACIÓN
                try:
                    idsarticulos = []
                    for ldv in prods[producto]:
                        idsarticulos += [str(ide) 
                            for ide in self.__ldvs[ldv.id]['idsarticulos']]
                    idsarticulos = ", ".join(idsarticulos)
                    sql = """
                    -- SELECT COUNT(*) 
                    SELECT COUNT(DISTINCT(pale.id)) 
                    FROM pale, caja, articulo 
                    WHERE pale.id = caja.pale_id 
                      AND caja.id = articulo.caja_id 
                      AND articulo.id IN (%s);
                    """ % idsarticulos
                    sqlpaleres = pclases.Pale._queryOne(sql)
                    try:
                        bultos = sqlpaleres[0][0] 
                                            # It MUST to work. Si no, prefiero 
                                            # que pete, aunque temporalmente 
                                            # usaré el algoritmo lento.
                    except TypeError, msg:
                        bultos = sqlpaleres[0]
                            # En versiones avanzadas de SQLObject el queryOne 
                            # devuelve por fin ONE registro, no una lista con 
                            # un registro.
                except Exception, msg:
                    print "albaranes_de_salida.py::imprimir ->", msg
                    print bultos
                    bultospales = []
                    for ldv in prods[producto]:
                        bultospales += [a.caja.pale 
                                    for a in self.__ldvs[ldv.id]['articulos']]
                    bultospales = utils.unificar(bultospales)
                    bultos = len(bultospales)
            else:
                try:
                    for ldv in prods[producto]:
                        # if isinstance(ldv, pclases.LineaDeDevolucion):
                        #    bultos += 1     # Las líneas de devolución solo tienen 1 artículo relacionado.
                        # else:
                        articulos = self.__ldvs[ldv.id]['articulos'] 
                        bultos += len(articulos)     # Bultos añadidos
                except ZeroDivisionError, msg:
                    txterror="albaranes_de_salida::preparar_llamada_imprimir"\
                             " -> Excepción al contar bultos para imprimir el"\
                             " albarán: %s" % (msg)
                    print txterror
                    self.logger.error(txterror)
            if bultos == 0:
                bultos = self.contar_bultos_de_ldvs(prods, producto)
            if es_venta_rollos_c(prods[producto][0]):
                cantidad_anadida = 0    # CWT: De este modo ignoro los 
                                        # artículos y uso la cantidad tecleada.
            else:
                try:
                    cantidad_anadida = self.cantidad_anadida(
                                                prods[producto][0].producto)
                except Exception, msg:
                    txterror = "albaranes_de_salida::preparar_llamada_imprimir"\
                               " -> Excepción al contar cantidad añadida al "\
                               "imprimir el albarán: %s" % (msg)
                    self.logger.debug(txterror)
                    print txterror
                    cantidad_anadida = 0
            # Si la cantidad añadida en artículos servidos es 0 y el 
            # producto es un producto especial o un producto de compra,
            # la cantidad servida que aparecerá impresa es la de las LDVs 
            # del pedido.
            if (cantidad_anadida == 0 and 
                (isinstance(producto, pclases.ProductoCompra) 
                 or (hasattr(producto, "camposEspecificosEspecialID") 
                     and producto.camposEspecificosEspecialID != None
                    )
                 or es_venta_rollos_c(producto)
                )
               ):
                for ldv in prods[producto]:
                    # prods es un diccionario que tiene como claves el producto 
                    # y como valores una lista de LDVs del albarán 
                    # pertenecientes a ese producto.
                    cantidad_anadida += ldv.cantidad
            total = sum([ldv.get_subtotal(iva = True) 
                         for ldv in prods[producto]])
            # cantidad_total = cantidad_anadida # WTF? ¿No sobra esta línea?
            try:
                # Calculándolo así soluciono el problema de varias líneas a 
                # diferentes precios, y me aseguro de que siempre cuadra (a 
                # no ser que haya precios muy pequeños, con muchos decimanes y
                # por cantidades muy altas, en cuyo caso *AL MOSTRAR EN 
                # IMPRESO* con dos decimales, se redondea. Internamente siguen 
                # siendo coherentes).
                precio_unitario = total / cantidad_anadida
            except ZeroDivisionError:
                precio_unitario = 0
            d = {'bulto': bultos,
                 'codigo': producto.codigo,
                 'descripcion': producto.descripcion,
                # 'cantidad': self.calcular_cantidad_ldvs(prods[p]),
                # 'cantidad': sum([ldv.cantidad for ldv in prods[p]]),
                 'cantidad': cantidad_anadida,
                 'numped': self.get_numpedidos_ldvs(prods[producto]), 
                 'precio unitario': utils.float2str_autoprecision(
                                                    precio_unitario, 
                                                    cantidad_anadida, 
                                                    total), 
                 'total': utils.float2str(total), 
                 'unidad': producto.get_str_unidad_de_venta()
                }
            lineas.append(d)
        ## SERVICIOS:  ##
        dde = pclases.DatosDeLaEmpresa.select()
        if dde.count() > 0:
            dde = dde[0]
            if not dde.esSociedad:
                for srv in albaran.servicios:
                    total = srv.get_subtotal(iva = True)
                    try:
                        precio_unitario = total / srv.cantidad
                    except ZeroDivisionError:
                        precio_unitario = 0
                    d = {'bulto': 0, 
                         'codigo': "", 
                         'descripcion': srv.concepto, 
                         'cantidad': srv.cantidad, 
                         'numped': srv.pedidoVenta 
                                    and srv.pedidoVenta.numpedido 
                                    or "", 
                         "precio unitario": utils.float2str_autoprecision(
                                    precio_unitario, 
                                    srv.cantidad, 
                                    total), 
                         "total": utils.float2str(total)
                        }
                    lineas.append(d)
        ## EOSERVICIOS ##
        observaciones = self.objeto.observaciones
        if (not cliente.provincia) and (not cliente.ciudad):
            destino = ''
        else:
            destino = "%s (%s)" % (cliente.ciudad, cliente.provincia)
        transporte = self.wids['e_agencia'].get_text()
        conformeT = {'nombre': self.wids['e_nombre'].get_text(),
                     'dni': self.wids['cbe_dni'].get_child().get_text(),
                     'telf': self.wids['e_telefono'].get_text(),
                     'matricula': self.wids['e_matricula'].get_text()
                    }  
        conformeD = {'nombre': '',
                     'dni': '',
                     'telf': '',
                     'matricula': ''}
        return composan, client, envio, general, lineas, observaciones, \
               destino, transporte, conformeT, conformeD

    def get_numpedidos_ldvs(self, ldvs):
        """
        Devuelve los número de pedidos como cadena,
        separados por coma, relacionados con las 
        LDVs de ldvs.
        """
        nps = []
        for ldv in ldvs:
            if isinstance(ldv, pclases.LineaDeVenta):
                if ldv.pedidoVenta != None and ldv.pedidoVenta.numpedido not in nps:
                    nps.append(ldv.pedidoVenta.numpedido)
        return ','.join([str(numpedido) for numpedido in nps])

    def calcular_cantidad_ldvs(self, lineas):
    #def calcular_cantidad_ldvs(self, albaran):
        """
        Recorre la lista de los artículos asociados al
        albarán y suma:
            - Si es una LDV de balas: pesobala
            - Si es un rollo: multiplicar longitud*ancho.
        """
        # OJO porque antes recibía una lista de LDVs y ahora recibe un albarán.
        # Primero determino si son LDVs de balas o rollos.
        try:
            if lineas[0].productoVenta.camposEspecificosRollo != None:
                return self.suma_cantidad_rollos(lineas)
            else:
                return self.suma_cantidad_balas(lineas)
        except IndexError:
            # No tiene artículos relacionados
            return 0

    def suma_cantidad_rollos(self, ars):
        articulos = len(ars) 
        ancho = ars[0].productoVenta.camposEspecificosRollo.ancho
        largo = ars[0].productoVenta.camposEspecificosRollo.metrosLineales
        metros_cuadrados = largo * ancho
        return articulos * metros_cuadrados

    def suma_cantidad_balas(self, ars):
        return sum([a.productoVenta.camposEspecificosBala.pesobala 
                    for a in ars])

    def ldvs_agrupadas_por_producto(self, albaran):
        """
        Devuelve un diccionario de LDVs.
        La clave es el código de producto y
        el valor es una lista de LDVs pertenecientes
        a ese producto.
        CWT: Y DE DEVOLUCIONES.
        """
        prods = {}
        for ldv in albaran.lineasDeVenta:
            producto = ldv.producto
            if producto not in prods.keys():
                prods[producto] = [ldv]
            else:
                prods[producto].append(ldv)
        return prods

    def imprimir(self, w):
        """
        Genera un albarán en PDF a partir de los datos
        del albarán actual.
        """
        if pclases.DEBUG:
            print "Llamando a self.preguntar_si_redistribuir..."
            antes = time.time()
        self.preguntar_si_redistribuir()
        if pclases.DEBUG:
            print "    --> Sin hueso mi ansiedad:", time.time() - antes
            print "Llamando a self.guardar..."
            antes = time.time()
        self.guardar(None, actualizar_ventana = False)  # Si se ha olvidado 
            # guardar, guardo yo.
        if pclases.DEBUG:
            print "    --> Sin hueso mi ansiedad:", time.time() - antes
            print "Comprobando self.wids['ch_debellevargastos']..."
            antes = time.time()
        albaran = self.objeto
        if (self.wids['ch_debellevargastos'].get_active() 
            and len(self.objeto.servicios) == 0):
            utils.dialogo_info(titulo = "ALBARÁN INCOMPLETO", 
                texto = "Se le ha indicado que el albarán debe incluir el "
                        "transporte.\n Sin embargo no ha incluido ninguno."
                        "\n Incluya uno o modifique el pedido original.", 
                padre = self.wids['ventana'])
            return
        if pclases.DEBUG:
            print "    --> Sin hueso mi ansiedad:", time.time() - antes
            print "Iterando bucle de cantidades de ldv "\
                  "(self.cantidad_anadida_a_ldv(ldv)..."
            antes = time.time()
        for ldv in albaran.lineasDeVenta:
            if ((ldv.productoVentaID and ldv.productoVenta.articulos) 
                and (self.usuario != None 
                     and self.usuario.nivel >= 1 
                     and not self.objeto.bloqueado)
                and not es_venta_rollos_c(ldv)):
                # DONE: Así consigo que se imprima la cantidad del pedido en 
                #       productos "especiales" (cables de fibra y cosas 
                #       así) que no tienen artículos en la BD porque nunca 
                #       se ha fabricado nada y no tienen existencias a 
                #       las que se le asignen códigos de bala o rollo.
                # CWT: Si el usuario tiene privilegios, que pueda imprimir 
                #      los albaranes con la cantidad que quieran.
                ldv.cantidad = self.cantidad_anadida_a_ldv(ldv)
                ldv.sync()
        if pclases.DEBUG:
            print "    --> Sin hueso mi ansiedad:", time.time() - antes
            print "Llamando a actualizar_ventana..."
            antes = time.time()
        self.actualizar_ventana()
            # Para refrescar los cambios en cantidades autoajustadas y tal.
        if pclases.DEBUG:
            print "    --> Sin hueso mi ansiedad:", time.time() - antes
            print "Llamando a preparar_llamada_imprimir..."
            antes = time.time()
        c, f, e, g, l, o, d, t, cT, cD=self.preparar_llamada_imprimir(albaran)
        if c == f == e == g == None:    # etc...
            return
        if pclases.DEBUG:
            print "    --> Sin hueso mi ansiedad:", time.time() - antes
            print "Comprobando configuración de albarán multipágina..."
            antes = time.time()
        if pclases.config.get_multipagina():
            from informes import albaran_multipag
            alb_mp = albaran_multipag.go_from_albaranSalida(self.objeto) 
            abrir_pdf(alb_mp)
        elif not pclases.config.get_valorar_albaranes():
            if c:
                nomarchivo = geninformes.albaran(False,f,e,g,l,o,d,t,cT,cD)
                self.abrir_albaran_imprimido(c, nomarchivo)
            nomarchivo_compo = geninformes.albaran(c,f,e,g,l,o,d,t,cT,cD)
            self.abrir_albaran_imprimido(c, nomarchivo_compo)
        else:
            nomarchivo = geninformes.albaranValorado(f, e, g, l, o, d, t, cT, 
                pclases.config.get_valorar_albaranes_con_iva())
            self.abrir_albaran_imprimido(c, nomarchivo)
            nomarchivo_compo = nomarchivo
        self.objeto.calcular_comisiones()
            # Hay que actualizar las comisiones antes de que se bloquee el 
            # albarán al generar la factura pero después de que se hayan 
            # redistribuido las cantidades de las LDV.
        if pclases.DEBUG:
            print "    --> Sin hueso mi ansiedad:", time.time() - antes
            print "Llamando a self.rellenar_comisiones..."
            antes = time.time()
        self.rellenar_comisiones()
        if pclases.DEBUG:
            print "    --> Sin hueso mi ansiedad:", time.time() - antes
            print "A partir de aquí ya son movidas de carta de portes, CMR, "\
                  "generación de factura y demás. No me interesa."
            antes = time.time()
        if pclases.config.get_carta_portes():
            from informes import albaran_porte
            try:
                kilos = sum([ldv.producto.calcular_kilos() * ldv.cantidad  
                             for ldv in self.objeto.lineasDeVenta])
            except (TypeError, ValueError):
                kilos = utils.dialogo_entrada(
                    titulo = "INTRODUZCA PESO TOTAL", 
                    texto = "Introduzca los kilogramos totales del albarán:", 
                    padre = self.wids['ventana'])
            recogida = utils.dialogo(titulo = "¿IMPRIMIR HOJA DE RECOGIDA?", 
                        texto = "Responda «Sí» para generar una hoja adicional de recogida de envases vacíos.", 
                        padre = self.wids['ventana'], 
                        defecto = gtk.RESPONSE_NO, 
                        tiempo = 10)
            alb_cp, envases = albaran_porte.go_from_albaranSalida(self.objeto, 
                                                                  kilos, 
                                                                  recogida)
            abrir_pdf(alb_cp)
            if envases:
                abrir_pdf(envases)
            # OJO: No se adjunta al correo.
        else:
            self.imprimir_cmr()
        if ((self.usuario == None or self.usuario.nivel <= 2) 
            and self.objeto.bloqueado):
            utils.dialogo_info(titulo = "NO SE GENERARÁ FACTURA",
                               texto = """
                El albarán se encuentra verificado y bloqueado.                 
                                                                                
                No se generará factura.                                         
                                                                                
                Si cree que debe generar una factura del presente               
                albarán (o de la parte que quede pendiente de                   
                facturar del mismo), desbloquee primero el albarán.             
                """, 
                                padre = self.wids['ventana'])
        if self.objeto and self.objeto.cliente:
            self.objeto.cliente.sync()
        if (self.objeto.facturable 
            and not self.objeto.bloqueado 
            and self.objeto.cliente and self.objeto.cliente.facturarConAlbaran
            and utils.dialogo(titulo = "¿GENERAR FACTURA?", 
                              texto = """
                        Compruebe minuciosamente el impreso generado. 
                        Si está seguro de que es correcto, responda 
                        sí para generar la factura.
                              """, 
                              padre = self.wids['ventana'])):
            # XXX: CWT (rparra): Si el albarán no tiene transporte, avisar 
            #                    antes de que se bloquee.
            if (not self.objeto.transportesACuenta
                and not utils.dialogo(titulo = "¿ESTÁ SEGURO?", 
                        texto = "El albarán no tiene transportes a cuenta.\n"
                                "Si genera la factura, no podrá agregarlos "
                                "más tarde. ¿Desea continuar?", 
                        padre = self.wids['ventana'])):
                    return
            # XXX
            ok, factura = self.generar_factura()
            if ok:
                self.objeto.bloqueado = factura.bloqueada = ok
                nomarchivo_factura = imprimir_factura(factura, self.usuario, 
                                                      albaran = self.objeto)
                for numcopia in range(self.objeto.cliente.copiasFactura):  # @UnusedVariable
                    imprimir_factura(factura, self.usuario, es_copia = True, 
                                     albaran = self.objeto)
                self.actualizar_ventana()
                from facturas_venta import debe_generar_recibo 
                from facturas_venta import generar_recibo 
                if debe_generar_recibo(factura, self.wids['ventana']):
                    generar_recibo(factura, 
                                   self.usuario, 
                                   self.logger, 
                                   self.wids['ventana'])
                # Finalmente, envío un correo al comercial. Es la mejor parte 
                # donde hacerlo para evitar que le llegue más de un correo por 
                # el mismo albarán.
                self.enviar_correo_notificacion_facturado(nomarchivo_factura)
        if self.objeto.cliente:
            correoe_cliente = self.objeto.cliente.email
            if self.objeto.cliente.cliente != None: 
                # Tiene intermediarios, añado sus correos a la lista de 
                # destinatarios; con los mismos adjuntos y demás que el 
                # cliente original, aunque no tenga marcadas las opciones de 
                # recibir copia en la ventana de clientes (eso se usaría para 
                # las ventas hechas directamente a él, no a sus clientes).
                correoe_cliente += " %s" % self.objeto.cliente.cliente.email
        else:
            correoe_cliente = ""
        correoe = utils.dialogo_entrada(
                    titulo = "¿ENVIAR ALBARÁN POR CORREO ELECTRÓNICO?", 
                    texto = """
                        Introduzca a continuación el correo electrónico del 
                        cliente si desea enviar una copia del albarán, 
                        "packing list" y/o factura en PDF. 
                        Cancele en caso contrario. 
                        Por defecto aparecerán las direcciones de correo del 
                        cliente, seguidas de las del comercial -si lo tuviera-.                    
                        """, 
                    valor_por_defecto = correoe_cliente, 
                    padre = self.wids['ventana'])
        if correoe != None and correoe != '':
            fichero_albaran = fichero_factura = ficheros_packing = None
            if self.objeto.cliente.enviarCorreoAlbaran:
                fichero_albaran = nomarchivo_compo  
                # Aunque parezca lo contrario, este no es el albarán 
                # de Composan.
            if self.objeto.cliente.enviarCorreoFactura:
                try:
                    fichero_factura = nomarchivo_factura
                except NameError:
                    utils.dialogo_info(titulo = "FACTURA NO GENERADA",
                        texto = "La factura no se ha generado correctamente "
                                "o fue creada con anterioridad.\nNo se "
                                "enviará por correo.\nSi la factura "
                                "existe y quiere enviar una copia por correo "
                                "electrónico, hágalo desde la ventana de "
                                "facturas de venta.",
                        padre = self.wids['ventana'])
            if self.objeto.cliente.enviarCorreoPacking:
                ficheros_packing = self.packinglist(None, abrir_pdf = False)
            self.enviar_por_correo(correoe, fichero_albaran, fichero_factura, 
                                   ficheros_packing) 
        #if self.objeto.cliente and self.objeto.cliente.cliente != None:     # Tiene comercial:
        #    txt = "El cliente tiene un comercial (%s).\n¿Desea que se genere la comisión automáticamente?" % (self.objeto.cliente.cliente.nombre)
        #    if utils.dialogo(titulo = "GENERAR COMISIÓN", 
        #                     texto = txt, 
        #                     padre = self.wids['ventana']):
        #        self.add_comision(None)

    def enviar_correo_notificacion_facturado(self, nomfich_pdf_factura):
        """
        Envía un correo de notificación de la factura al comercial implicado. 
        """
        if self.usuario and self.objeto:
            #comerciales = [c for c in self.usuario.get_comerciales() 
            #               if c != self.objeto.comercial]
            # Esto de aquí arriba no tiene sentido ninguno. ¿Lo tuvo alguna 
            # vez? Lo dejo comentado por interés arqueológico.
            comerciales=self.objeto.comercial and [self.objeto.comercial] or []
            servidor = self.usuario.smtpserver
            smtpuser = self.usuario.smtpuser
            smtppass = self.usuario.smtppassword
            rte = self.usuario.email
            # TODO: OJO: HARDCODED
            if self.usuario and self.usuario.id == 1:
                dests = ["informatica@geotexan.com"]
            else:
                dests = [comercial.correoe for comercial in comerciales]
            # Correo de riesgo de cliente
            texto = "%s ha generado la factura %s de la oferta %s "\
                    "para el cliente %s desde el albarán %s." % (
                        self.usuario and self.usuario.nombre or "Se", 
                        self.objeto.numalbaran, 
                        ", ".join([str(p.id) 
                            for p in self.objeto.get_presupuestos()]), 
                        self.objeto.cliente and self.objeto.nombre or "", 
                        self.objeto.numalbaran)
            utils.enviar_correoe(rte, 
                                 dests,
                                 "Factura %s de %s generada." % (
                                    ", ".join([f.numfactura 
                                        for f in self.objeto.get_facturas()]), 
                                    self.objeto.cliente 
                                        and self.objeto.cliente.nombre 
                                        or "cliente"), 
                                texto, 
                                adjuntos = [nomfich_pdf_factura], 
                                servidor = servidor, 
                                usuario = smtpuser, 
                                password = smtppass)
    
    def imprimir_cmr(self):
        lugar_entrega = utils.dialogo_entrada(titulo = "CMR", texto = "Lugar de entrega:", padre = self.wids['ventana'], textview = True, 
                                              valor_por_defecto = self.objeto.nombre + "\n" + self.objeto.direccion + "\n" + 
                                                                  self.objeto.cp + "\n" + self.objeto.ciudad + " " + self.objeto.pais)
        if lugar_entrega != None:
            transportista = utils.dialogo_entrada(titulo = "CMR", texto = "Transportista:", padre = self.wids['ventana'], textview = True)
            if transportista != None:
                porteadores = utils.dialogo_entrada(titulo = "CMR", texto = "Porteadores:", padre = self.wids['ventana'], textview = True)
                if porteadores != None:
                    abrir_pdf(geninformes.cmr(self.objeto, lugar_entrega, transportista, porteadores))
    
    def enviar_por_correo(self, email, fichero_albaran = None, fichero_factura = None, fichero_packing_list = None):
        """
        Crea un correo electrónico con fichero adjunto y 
        lo envía a la dirección "email".
        """
        texto_adjuntos = []
        adjuntos = []
        if fichero_albaran:
            adjuntos.append(fichero_albaran)
            texto_adjuntos.append("copia del albarán")
        if fichero_factura:
            adjuntos.append(fichero_factura)
            texto_adjuntos.append("copia de la factura")
        if fichero_packing_list:
            for fpl in fichero_packing_list:
                adjuntos.append(fpl)
            texto_adjuntos.append("copia de %d packing list%s" % (len(fichero_packing_list), len(fichero_packing_list) > 1 and "s" or ""))
        texto_adjuntos = ": " + ", ".join(texto_adjuntos) + "."
        correos = email.replace(",", " ").replace(";", "").strip().split()
        correos = utils.unificar([c.lower().strip() for c in correos])
        remitente = smtpuser = smtppass = server = ""
        if self.usuario != None:
            remitente = self.usuario.email
            smtpuser = self.usuario.smtpuser
            smtppass = self.usuario.smtppassword
            server = self.usuario.smtpserver
        if self.usuario == None or not remitente:
            remitente = utils.dialogo_entrada(
                    titulo = "DATO DE USUARIO NO ENCONTRADO", 
                    texto = "Introduzca remitente del correo electrónico:", 
                    padre = self.wids['ventana'])
            if remitente == None or remitente.strip() == '':
                return
        if self.usuario == None or not server:
            server = utils.dialogo_entrada(
                        titulo = "DATO DE USUARIO NO ENCONTRADO", 
                        texto = "Introduzca servidor SMTP de correo saliente:",
                        padre = self.wids['ventana'])
            if server == None or server.strip() == '':
                return
        if self.usuario == None or not smtpuser:
            smtpuser = utils.dialogo_entrada(
                            titulo = "DATO DE USUARIO NO ENCONTRADO", 
                            texto = "Introduzca usuario para autentificación"
                                    " en servidor SMTP de salida:", 
                            padre = self.wids['ventana'])
            if smtpuser == None:
                return
            if smtpuser.strip() == "":
                smtpuser = None
        if self.usuario == None or not smtppass:
            smtppass = utils.dialogo_entrada(
                        titulo = "DATO DE USUARIO NO ENCONTRADO", 
                        texto = "Introduzca contraseña para autentificación "
                                "en servidor SMTP de salida:", 
                        padre = self.wids['ventana'], 
                        pwd = True)
            if smtppass == None:
                return
            if smtppass.strip() == "":
                smtppass = None
        try:
            dde = pclases.DatosDeLaEmpresa.select()[0]
            empresa = " (%s)" % (dde.nombre)
        except:
            txt = "No hay empresa dada de alta en datos_de_la_empresa. Es "\
                  "necesario para que aparezca el nombre como remitenten en "\
                  "el asunto del correo electónico."
            self.logger.error(txt)
            print txt
            empresa = ""
        asunto = "Albarán %s%s" % (self.objeto.numalbaran, empresa)
        asunto = utils.dialogo_entrada(
            titulo = "ASUNTO DEL CORREO ELECTRÓNICO", 
            texto="Introduzca un texto para el asunto del correo electrónico:",
            padre = self.wids['ventana'],
            valor_por_defecto = asunto)
        if asunto == None:
            return 
        if adjuntos == []:
            texto = """Albarán %s generado e imprimido. Fecha de salida de la mercancía del almacén: %s.""" % (self.objeto.numalbaran, utils.str_fecha(mx.DateTime.localtime()))
        else:
            texto = """Adjunto la siguiente documentación en formato PDF correspondiente al albarán %s%s""" % (self.objeto.numalbaran, texto_adjuntos)
        texto = utils.dialogo_entrada(titulo = "TEXTO DEL CORREO ELECTRÓNICO",
                                      texto = "Introduzca un texto como "
                                              "contenido del correo "
                                              "electrónico:", 
                                      padre = self.wids['ventana'], 
                                      valor_por_defecto = texto)
        if texto == None:
            return
        try:
            dde = pclases.DatosDeLaEmpresa.select()[0]
            texto = texto + """
            
            %s
            %s
            %s - %s, %s
            %s
            """ % (dde.nombre, 
                   dde.direccion, 
                   dde.cp, 
                   dde.ciudad, 
                   dde.provincia, 
                   dde.pais)
        except:
            texto = texto + """
            
            Geotexan, S.A.
            Avda. Concha Espina, 5.
            21660 - Minas de Riotinto, Huelva.
            España.
            """
        correos.append(remitente)
        try:
            ok = utils.enviar_correoe(remitente, correos, asunto, texto, 
                                      adjuntos, server, smtpuser, smtppass)
        except Exception, msg:
            self.logger.error("%salbaranes_de_salida::enviar_por_correo -> "
                              "Error al enviar el albarán ID %d. Mensaje de "
                              "la excepción: %s" %  (
                                self.usuario 
                                    and self.usuario.usuario + ": " 
                                    or "", 
                                self.objeto and self.objeto.id or 0, 
                                msg))
            ok = False
        if not ok:
            utils.dialogo_info(titulo = "ERROR ENVÍO E-MAIL",
                               texto = "Ocurrió un error enviando el correo electrónico.\nGuarde los documentos e inténtelo más tarde desde su propio cliente de correo.", 
                               padre = self.wids['ventana'])
        else:
            utils.dialogo_info(titulo = "CORREO ELECTRÓNICO ENVIADO", 
                               texto = "Se envío el correo electrónico a los destinatarios y una copia al remitente.\nVerifique que lo recibe y vuelva a enviar la documentación en caso contrario.", 
                               padre = self.wids['ventana'])

    def abrir_albaran_imprimido(self, composan, nomarchivo):
        """
        Muestra el albarán generado en PDF.
        composan indica si hay que abrir también el de Composan.
        NOTA: La variable "composan" actualmente se ignora.
        """
        from formularios import reports
        reports.abrir_pdf(nomarchivo)

    def preguntar_si_redistribuir(self):
        """
        Comprueba cada línea de venta para ver si alguna no coincide 
        con las del pedido del que procede.
        Si es así, Y EL ALBARÁN ES NUEVO O 
        """
        # NOTA: No sé por qué no acabé la docstring, de todas formas me parece 
        # que este método, con la nueva forma de crear LDVs, no tiene ya mucho 
        # sentido. Tampoco creo que se cumpla la condición que hace saltar el 
        # dialogo y tal.
        # DONE: Repasar y quitar el diálogo de confirmación si es que 
        # realmente sobra (que para mí que sí).
        if self.nuevo or self.modificado:
            for idldv in self.__ldvs:
                if (round(self.__ldvs[idldv]['ldv'].cantidad, 3) 
                        != round(self.__ldvs[idldv]['cantidad'], 3)): 
                    if (self.__ldvs[idldv]['cantidad'] > 0
                        # CWT: Si son artículos clase C, como desde que se 
                        # pesaron hasta que se venden han podido variar de 
                        # peso (agua, plásticos, etc.), hay que respetar lo 
                        # que ha pesado el camión de verdad, que es lo que 
                        # ha tecleado el usuario como cantidad pedida y no lo 
                        # que dicen los pesos de los artículos. Pero los 
                        # artículos deben descontarse igualmente para que no 
                        # me descuadren los bultos en el almacén. Otra cosa 
                        # es que después las cantidades facturadas no 
                        # coincidan con las salidas de almacén. Pero eso ya 
                        # lo tienen contemplado y dicen que no les importa.
                        # UPDATE [20140306]: (rparra) Solo para geotextiles C. 
                        # La fibra C va a seguir saliendo con el peso que 
                        # marque su código de trazabilidad tanto en fra. como 
                        # en albarán.
                            and not es_venta_rollos_c(
                                self.__ldvs[idldv]['ldv'])):
                        # TODO: Si la cantidad AÑADIDA no es cero, ajusto las 
                        #       cantidades. Si es 0 prefiero dejar la cantidad 
                        #       de la LDV original porque es posible que sea 
                        #       una venta "especial" de cable de fibra o 
                        #       desechos que no tienen objetos artículos 
                        #       relacionados en almacén. Esto será así hasta 
                        #       que termine de definir cómo voy a almacenar 
                        #       este tipo de productos de venta en la BD.
                        model = self.wids['tv_ldvs'].get_model()
                        itr = model.get_iter_first()
                        self.redistribuir_ldv(model.get_path(itr))
                        itr = model.iter_next(itr)
                        while itr != None:
                            self.redistribuir_ldv(model.get_path(itr))
                            itr = model.iter_next(itr)
                        self.actualizar_ventana()
                    break

    def pre_salir(self, w):
        """
        Bueno, se ejecuta antes de salir de la ventana, ¿qué nombre esperabas?
        """
        self.preguntar_si_redistribuir()
        self.salir(w)

    def packinglist(self, boton, abrir_pdf = True):
        """
        Prepara e imprime (genera un PDF) los datos del Packing List de los
        artículos del albarán. Idealmente se usará solo para fibra, aunque
        también soporta geotextiles, geocompuestos y fibra de cemento.
        """
        pl = []
        albaran = self.objeto
        for ldv, linea_de_venta in [(self.__ldvs[ide], 
                                     pclases.LineaDeVenta.get(ide)) 
                        for ide in self.__ldvs 
                        if pclases.LineaDeVenta.get(ide).productoVenta != None]:
            # Diccionario de la LDV de la ventana y objeto LDV en sí
            if (not (linea_de_venta.productoVenta != None 
                and not linea_de_venta.productoVenta.es_especial())):
                continue
            producto = linea_de_venta.productoVenta.descripcion
            codigoproducto = linea_de_venta.productoVenta.codigo
            fecha = utils.str_fecha(albaran.fecha)
            try:
                datos_empresa = pclases.DatosDeLaEmpresa.select()[0]
                linea0 = datos_empresa.nombre.upper()
                linea1 = datos_empresa.direccion
                linea2 = "%s %s (%s)" % (datos_empresa.cp, 
                                         datos_empresa.ciudad, 
                                         datos_empresa.provincia)
                if datos_empresa.fax:
                    linea3 = "TEL %s - FAX %s" % (datos_empresa.telefono, 
                                                  datos_empresa.fax)
                else:
                    linea3 = "TEL %s" % (datos_empresa.telefono)
            except Exception, msg:
                utils.dialogo_info(titulo="ERROR BUSCANDO DATOS DE LA EMPRESA", 
                                texto = "Los datos de la cabecera "
                                        "(información de la propia empresa) "
                                        "no se encontraron.\n\nContacte con "
                                        "el administrador para solventar "
                                        "este error.\n\n\nInformación de "
                                        "depuración:\n%s" % msg, 
                                padre = self.wids['ventana'])
                return
            nombre = albaran.nombre
            direccion = albaran.direccion
            ciudad = albaran.ciudad
            cp = albaran.cp
            pais = albaran.pais
            lotes = self.get_lotes_o_partidas(ldv['articulos'])
            tipo = self.get_tipo(ldv)
            balas = self.get_balas_o_rollos(ldv['articulos'])
            total = "%d" % len(balas)
            peso = "%s" % utils.float2str(sum([b[2] for b in balas])) 
                # balas es una tupla de tuplas con 5 elementos: código, 
                # peso como cadena, peso, ide, código de trazabilidad (si es 
                # bala será el de Domenech) objeto articulo relacionado.
            modelo_pl_balas = False
            for i in range(len(balas)):
                articulo = balas[i][-1]
                if articulo.es_bala():
                    modelo_pl_balas = True
                    bala = articulo.bala
                    campos = articulo.productoVenta.camposEspecificosBala
                    baladic={'descripcion': articulo.productoVenta.descripcion,
                             'codigo': bala.codigo,
                             'color': str(campos.color),
                             'peso': utils.float2str(bala.pesobala),
                             'lote': bala.lote.codigo,
                             'tipo': campos.tipoMaterialBala and str(campos.tipoMaterialBala.descripcion) or "",
                             'longitud': str(campos.corte),
                             'nbala': str(bala.numbala),
                             'dtex': str(campos.dtex),
                             'dia': utils.str_fecha(bala.fechahora),
                             'acabado': campos.antiuv and 1 or 0,
                             'codigoBarra': articulo.productoVenta.codigo}
                    codigo_domher =  geninformes._build_codigo_domenech(baladic)
                    codigo_trazabilidad = codigo_domher
                else:
                    codigo_trazabilidad = articulo.codigo
                balas[i].insert(-1, codigo_trazabilidad)    # última posición 
                # siempre será el artículo. Código de trazabilidad penúltimo.
            balas = list(balas)
            # El orden que traía de la función solo es válido para 4 columnas, 
            # reordeno para que salgan de izquierda a derecha y de arriba a 
            # abajo.
            balas.sort(lambda b1, b2: int(b1[3] - b2[3]))
            balas = tuple(balas)
            pl.append({'producto': producto,
                       'codigo_producto': codigoproducto, 
                       'fecha': fecha,
                       'lote': lotes,
                       'tipo': tipo, 
                       'balas': balas,
                       'total': total,
                       'peso': peso,
                       'envio': {'nombre': nombre,
                                 'direccion': direccion, 
                                 'ciudad': ciudad,
                                 'cp': cp,
                                 'pais': pais}, 
                       'empresa': {'linea0': linea0,
                                   'linea1': linea1,
                                   'linea2': linea2,
                                   'linea3': linea3}
                       })
        return self.imprimir_packing_list(tuple(pl), abrir_pdf, 
                                          modelobalas = modelo_pl_balas)

    def imprimir_packing_list(self, packing_lists, abrir_pdf = True, 
                              modelobalas = True):
        """
        «modelobalas» define el modelo de packing list a imprimir. El de 
        balas (códigos más altos, una columna) o el antiguo.
        """
        self.guardar(None, actualizar_ventana = False)  # Si se ha olvidado 
            # guardar, guardo yo.
        packings_generados = []
        if self.objeto.cliente.packingListConCodigo:
            if modelobalas:
                func_packinglist = geninformes.packingListBalas
            else:
                func_packinglist = geninformes._packingListBalas
        else:
            func_packinglist = geninformes.oldPackingListBalas
        for i in xrange(len(packing_lists)):
            titulopackinglist = "Packing list. Albarán %s" % (
                    self.objeto.numalbaran) 
            if len(packing_lists) > 1:
                titulopackinglist += " (%d/%d)" % (i + 1, len(packing_lists))
            nomarchivo = func_packinglist(packing_lists[i], i+1, 
                                          titulo = titulopackinglist)
            if abrir_pdf:
                self.abrir_albaran_imprimido(False, nomarchivo)
            packings_generados.append(nomarchivo)
        return packings_generados

    def get_balas_o_rollos(self, articulos):
        balas = []
        pales_cemento_tratados = []
        for a in articulos:
            if a.es_bala():
                balas.append([a.bala.codigo, 
                              "%s kg" % utils.float2str(a.bala.pesobala), 
                              a.bala.pesobala, 
                              a.bala.numbala, 
                              a])
            elif a.es_caja():
                if a.caja.pale not in pales_cemento_tratados:
                    pale = a.caja.pale
                    lista = [pale.codigo, 
                             "%s kg" % utils.float2str(pale.calcular_peso()),
                             pale.calcular_peso(), 
                             pale.numpale, 
                             a]
                    balas.append(lista)
                    pales_cemento_tratados.append(pale)
            elif a.es_bala_cable():
                balas.append([a.balaCable.codigo, 
                              "%s kg" % utils.float2str(a.balaCable.peso), 
                              a.balaCable.peso, 
                              a.balaCable.numbala, 
                              a])
            elif a.es_rollo():
                try:
                    largo=a.productoVenta.camposEspecificosRollo.metrosLineales
                    ancho = a.productoVenta.camposEspecificosRollo.ancho
                    metros2 = largo * ancho
                except:
                    self.logger.error("albaranes_de_salida.py: get_balas_o_rollos: (packing list). El producto de venta del artículo no tiene campos específicos o el artículo no tiene producto de venta relacionado.")
                    metros2 = 0
                balas.append([a.rollo.codigo, 
                              "%s m2" % utils.float2str(metros2), 
                              metros2, 
                              a.rollo.numrollo, 
                              a])
            elif a.es_bigbag():
                balas.append([a.bigbag.codigo, 
                              "%s kg." % utils.float2str(a.bigbag.pesobigbag), 
                              a.bigbag.pesobigbag, 
                              a.bigbag.numbigbag, 
                              a])
            elif a.es_rollo_defectuoso():
                balas.append([a.codigo, 
                              "%s m2" % (utils.float2str(a.superficie)), 
                              a.superficie, 
                              a.rolloDefectuoso.numrollo, 
                              a])
            elif a.es_rolloC():
                balas.append([a.codigo, 
                              "%s kg" % utils.float2str(a.peso), 
                              a.peso, 
                              a.rolloC.numrollo, 
                              a])
            else:
                self.logger.error("El artículo ID %d no tiene asociado ni una bala, ni rollo [defectuoso] ni bigbag." % (a.id))
        balas_aux = []
        i = 0
        fcmp = lambda x,y:[(x[-1]<y[-1] and -1) or (x[-1]>y[-1] and 1) or 0][0]
        balas.sort(fcmp)
        while balas:
            numfilas = [(len(balas)/4.0) % 1 > 0 and int((len(balas)/4.0) + 1) or int(len(balas)/4.0)][0]
            balas_aux.append(balas.pop(i))
            i = [i+numfilas-1<len(balas) and i+numfilas-1 or 0][0]
            # Para que entren en orden descendente, de arriba a abajo y de 
            # izquierda a derecha en las 4 columnas del packing list.
        return tuple(balas_aux)

    def get_tipo(self, ldv):
        tipo = ""
        if len(ldv['articulos']):
            pv = ldv['articulos'][0].productoVenta
            if pv.es_rollo():
                tipo = "%.2fx%d" % (pv.camposEspecificosRollo.ancho, 
                                    pv.camposEspecificosRollo.metrosLineales)
            elif pv.es_bala() or pv.es_bigbag() or pv.es_caja():
                tipo = pv.camposEspecificosBala.color
            else:
                self.logger.error("El artículo %d no es bala, ni rollo, "
                                  "ni fibra de cemento en bigbag ni fibra "
                                  "de cemento embolsada." % (
                                    ldv['articulos'][0].id))
        return tipo

    def get_lotes_o_partidas(self, articulos):
        lotes = []
        for articulo in articulos:
            if articulo.productoVenta.es_bala():
                try:
                    #codlote = articulo.bala.lote.numlote
                    codlote = articulo.bala.lote.codigo
                except AttributeError:
                    self.logger.error("El artículo ID %d es fibra pero no tiene lote." % (articulo.id), exc_info = True)
                    codlote = None
                if codlote != None and codlote not in lotes:
                    lotes.append(codlote)
            elif articulo.productoVenta.es_rollo():
                try:
                    #codlote = articulo.rollo.partida.numpartida
                    codlote = articulo.rollo.partida.codigo
                except AttributeError:
                    self.logger.error("El artículo ID %d es geotextil pero no tiene partida." % (articulo.id), exc_info = True)
                    codlote = None
                if codlote != None and codlote not in lotes:
                    lotes.append(codlote)
            elif articulo.productoVenta.es_bigbag():
                try:
                    codlote = articulo.bigbag.loteCem.codigo
                except AttributeError:
                    self.logger.error("El artículo ID %d es geocem pero no tiene lote." % (articulo.id), exc_info = True)
                    codlote = None
                if codlote != None and codlote not in lotes:
                    lotes.append(codlote)
            elif articulo.productoVenta.es_caja():
                try:
                    codlote = articulo.caja.pale.partidaCem.codigo
                except AttributeError:
                    self.logger.error("El artículo ID %d es fibra embolsada pero no tiene partida." % (articulo.id), exc_info = True)
                    codlote = None
                if codlote != None and codlote not in lotes:
                    lotes.append(codlote)
            else:
                self.logger.error("El artículo ID %d no es ni fibra ni geotextil (ni geocompuesto/comercializado)." % (articulo.id))
        try:
            res = ', '.join(["%d" % (lote) for lote in lotes])
        except TypeError:
            res = ', '.join([lote for lote in lotes])
        return res 
        
    def cambiar_cantidad_srv(self, cell, path, texto):
        model = self.wids['tv_servicios'].get_model()
        idsrv = model[path][-1]
        #srv = pclases.Servicio.get(idsrv)
        srv = pclases.getObjetoPUID(idsrv)
        try:
            srv.cantidad = utils._float(texto)
            srv.syncUpdate()
            model[path][0] = srv.cantidad
            model[path][4] = srv.precio * (1.0 - srv.descuento) * srv.cantidad
            self.modificado = True
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                    texto = 'Formato numérico incorrecto', 
                    padre = self.wids['ventana'])

    def cambiar_precio_srv(self, cell, path, texto):
        model = self.wids['tv_servicios'].get_model()
        idsrv = model[path][-1]
        #srv = pclases.Servicio.get(idsrv)
        srv = pclases.getObjetoPUID(idsrv)
        try:
            srv.precio = utils._float(texto)
            self.modificado = True
            self.rellenar_servicios()
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                               texto = 'Formato numérico incorrecto', 
                               padre = self.wids['ventana'])

    def cambiar_descuento_srv(self, cell, path, texto):
        model = self.wids['tv_servicios'].get_model()
        idsrv = model[path][-1]
        #srv = pclases.Servicio.get(idsrv)
        srv = pclases.getObjetoPUID(idsrv)
        try:
            srv.descuento = utils.parse_porcentaje(texto)
            if srv.descuento > 1.0:
                srv.descuento /= 100.0
            self.rellenar_servicios()
            self.modificado = True
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                               texto = 'Formato numérico incorrecto', 
                               padre = self.wids['ventana'])

    def cambiar_concepto_srv(self, cell, path, texto):
        model = self.wids['tv_servicios'].get_model()
        idsrv = model[path][-1]
        #srv = pclases.Servicio.get(idsrv)
        srv = pclases.getObjetoPUID(idsrv)
        srv.concepto = texto
        self.modificado = True
        self.rellenar_servicios()

    def crear_servicio(self):
        # Datos a pedir: Concepto, descuento y precio... Bah, el descuento que lo cambie en el TreeView.
        concepto = utils.dialogo_entrada(titulo = "CONCEPTO",
                                         texto = 'Introduzca el concepto para el transporte:', 
                                         padre = self.wids['ventana'])
        if concepto != None:
            precio = utils.dialogo_entrada(titulo = "PRECIO", 
                                           texto = 'Introduzca el precio unitario sin IVA:', 
                                           padre = self.wids['ventana'])
            if precio != None:
                try:
                    precio = utils._float(precio)
                    servicio = pclases.Servicio(facturaVenta = None,
                                     albaranSalida = self.objeto,
                                     concepto = concepto,
                                     precio = precio,
                                     descuento = 0)
                    pclases.Auditoria.nuevo(servicio, self.usuario, __file__)
                    # Cantidad es 1 por defecto.
                    self.modificado = True
                except Exception, e:
                    utils.dialogo_info(titulo = "ERROR", 
                                       texto = """
                    Ocurrió un error al crear el servicio.                                      
                    Asegúrese de haber introducido correctamente los datos,                     
                    especialmente el precio (que no debe incluir símbolos                       
                    monetarios), y vuelva a intentarlo.

                    DEBUG: %s
                    """ % (e), 
                                       padre = self.wids['ventana'])
                    raise e
                    return
                self.rellenar_servicios()

    def add_srv(self, boton):
        if (self.objeto.cliente 
            and self.objeto.cliente.calcular_credito_disponible(
                base = self.objeto.calcular_total(iva_incluido = True)) <= 0):
            utils.dialogo_info(titulo = "CLIENTE SIN CRÉDITO", 
                               texto = "El cliente ha sobrepasado el "
                                       "crédito concedido.", 
                               padre = self.wids['ventana'])
            return
        if self.comprobar_cliente_deudor():
            self.to_log("[add_pedido] Cliente deudor.", 
                        {"cliente": self.objeto.cliente 
                                    and self.objeto.cliente.get_info()
                                    or "¿Sin self.objeto.cliente?", 
                         "albarán": self.objeto.numalbaran, 
                        })
            return
        self.crear_servicio()
        self.objeto.calcular_comisiones()
        self.rellenar_comisiones()

    def comprobar_cliente_deudor(self):
        """
        Comprueba si el cliente tiene facturas pendientes de recibir 
        documento de pago y devuelve True si no debe sacársele mercancía 
        o False si no tiene nada pendiente y vencido.
        Se considera una factura pendiente si no tiene doc. de pago o no 
        tiene cobro en absoluto. El documento de pago (pagaré, cheque o lo 
        que sea) puede estar pendiente de cobro, vencido o no, sin que afecte 
        a la factura como pendiente.
        Muestra una ventana de aviso si el cliente es deudor.
        Si el nivel del usuario es 1 ó 0 mostrará la opción de continuar 
        -devolviendo False en ese caso-.
        """
        cli = self.objeto.cliente
        if (cli 
            and cli.get_facturas_vencidas_sin_documento_de_cobro()):
            frasvenc = cli.get_facturas_vencidas_sin_documento_de_cobro()
            strfrasvenc = "; ".join([f.numfactura for f in frasvenc])
            if not self.usuario or self.usuario.nivel > 2:
                utils.dialogo_info(titulo = "CLIENTE DEUDOR", 
                                texto = "El cliente tiene %d facturas "
                                       "vencidas sin documento de pago:\n%s" 
                                        % (len(frasvenc), 
                                           strfrasvenc),
                                padre = self.wids['ventana'])
                return True
            else:
                continuar = utils.dialogo(titulo = "CLIENTE DEUDOR", 
                               texto = "El cliente tiene %d facturas "
                                       "vencidas sin documento de pago:\n%s\n"
                                       "¿Desea continuar?" 
                                        % (len(frasvenc), 
                                           strfrasvenc),
                               padre = self.wids['ventana'])
                self.to_log("[comprobar_cliente_deudor] "
                                "Cliente deudor pero usuario %s continúa." 
                                    % self.usuario, 
                            {"cliente": cli.get_info(), 
                             "albarán": self.objeto.numalbaran })
                return not continuar
        return False
    
    def drop_srv(self, boton):
        if self.wids['tv_servicios'].get_selection().count_selected_rows() != 0:
            model, itr = self.wids['tv_servicios'].get_selection().get_selected()
            idservicio = model[itr][-1]
            servicio = pclases.getObjetoPUID(idservicio)
            servicio.albaranSalida = None
            if (servicio.facturaVenta == None 
                and servicio.prefacturaID == None
                and servicio.pedidoVenta == None):
                servicio.destroy(ventana = __file__)  
                    # No debería saltar ninguna excepción. 
            self.rellenar_servicios()
            self.modificado = True
            self.objeto.calcular_comisiones()
            self.rellenar_comisiones()

    def drop_transporte_a_cuenta(self, boton):
        """
        Elimina el transporte a cuenta seleccionado en el treeview.
        """
        tv = self.wids['tv_transportesACuenta']
        if tv.get_selection().count_selected_rows() > 0: 
            model, paths = tv.get_selection().get_selected_rows()
            for path in paths:
                idtac = model[path][-1]
                #tac = pclases.TransporteACuenta.get(idtac)
                tac = pclases.getObjetoPUID(idtac)
                tac.destroy(ventana = __file__)
            self.rellenar_transportes_a_cuenta()

    def add_transporte_a_cuenta(self, boton):
        """
        Añade un nuevo transporte a cuenta al albarán actual.
        """
        if (self.objeto 
                and self.usuario and self.usuario.nivel >= 2 
                and self.objeto.get_facturas()):
            utils.dialogo_info(titulo = "ALBARÁN FACTURADO", 
                    texto = "El albarán se encuentra facturado.\n"
                            "No puede agregar más transportes.", 
                    padre = self.wids['ventana'])
        else:
            t = pclases.TransporteACuenta(concepto = "Transporte pagado.", 
                    precio = 0, 
                    proveedor = None,
                    observaciones="Introduzca el precio y empresa transportista.", 
                    fecha = mx.DateTime.localtime(), 
                    albaranSalidaID = self.objeto.id)
            pclases.Auditoria.nuevo(t, self.usuario, __file__)
            self.rellenar_transportes_a_cuenta()

    def cambiar_concepto_tac(self, cell, path, texto):
        model = self.wids['tv_transportesACuenta'].get_model()
        idtac = model[path][-1]
        #tac = pclases.TransporteACuenta.get(idtac)
        tac = pclases.getObjetoPUID(idtac)
        tac.concepto = texto
        self.modificado = True
        model[path][0] = tac.concepto

    def cambiar_precio_tac(self, cell, path, texto):
        if (self.objeto 
                and self.usuario and self.usuario.nivel >= 2 
                and self.objeto.get_facturas()):
            utils.dialogo_info(titulo = "ALBARÁN FACTURADO", 
                    texto = "El albarán se encuentra facturado.\n"
                            "No puede modificar el precio del transporte.", 
                    padre = self.wids['ventana'])
        else:
            try:
                precio = utils._float(texto)
            except ValueError:
                utils.dialogo_info(titulo = "PRECIO INCORRECTO", 
                    texto = "El texto introducido %s no es una cantidad "\
                            "correcta." % (texto), 
                    padre = self.wids['ventana'])
            else:
                model = self.wids['tv_transportesACuenta'].get_model()
                idtac = model[path][-1]
                #tac = pclases.TransporteACuenta.get(idtac)
                tac = pclases.getObjetoPUID(idtac)
                tac.precio = precio
                tac.syncUpdate()
                # BUGFIX: GINN-75
                for st in tac.serviciosTomados:
                    st.precio = precio / len(tac.serviciosTomados)
                    st.syncUpdate()
                self.modificado = True
                model[path][1] = utils.float2str(tac.precio)

    def cambiar_observaciones_tac(self, cell, path, texto):
        model = self.wids['tv_transportesACuenta'].get_model()
        idtac = model[path][-1]
        #tac = pclases.TransporteACuenta.get(idtac)
        tac = pclases.getObjetoPUID(idtac)
        tac.observaciones = texto
        tac.syncUpdate()
        self.modificado = True
        model[path][3] = tac.observaciones

    def cambiar_fecha_tac(self, cell, path, texto):
        model = self.wids['tv_transportesACuenta'].get_model()
        idtac = model[path][-1]
        #tac = pclases.TransporteACuenta.get(idtac)
        tac = pclases.getObjetoPUID(idtac)
        try:
            fecha = utils.parse_fecha(texto)
        except (ValueError, mx.DateTime.RangeError):
            utils.dialogo_info(titulo = "FECHA INCORRECTA", 
                               texto = "La fecha %s no es correcta." % (texto), 
                               padre = self.wids['ventana'])
        else:
            tac.fecha = fecha
            tac.syncUpdate()
            self.modificado = True
            model[path][4] = utils.str_fecha(tac.fecha)

    def cambiar_proveedor_tac(self, cell, path, texto):
        model = self.wids['tv_transportesACuenta'].get_model()
        idtac = model[path][-1]
        #tac = pclases.TransporteACuenta.get(idtac)
        tac = pclases.getObjetoPUID(idtac)
        if texto.strip() == "":
            tac.proveedor = None
            model[path][2] = ""
        else:
            proveedor = buscar_proveedor(texto, self.wids['ventana'])
            if proveedor != None:
                tac.proveedor = proveedor
                tac.syncUpdate()
                self.modificado = True
                model[path][2] = tac.proveedor.nombre
            # else:
            #     utils.dialogo_info(titulo = "PROVEEDOR NO ENCONTRADO", 
            #                        texto = "El proveedor del servicio o transporte debe estar dado de alta.\nCierre esta ventana, cree el proveedor y vuelva a intentarlo.", 
            #                        padre = self.wids['ventana'])

    def rellenar_transportes_a_cuenta(self):
        model = self.wids['tv_transportesACuenta'].get_model()
        model.clear()
        for tac in self.objeto.transportesACuenta:
            precio = utils.float2str(tac.precio)
            proveedor = tac.proveedor and tac.proveedor.nombre or ""
            try:
                numfactura = tac.serviciosTomados[0].facturaCompra.numfactura
            except (IndexError, AttributeError):
                numfactura = ""
            model.append((tac.concepto, 
                          precio, 
                          proveedor, 
                          tac.observaciones, 
                          utils.str_fecha(tac.fecha), 
                          numfactura, 
                          tac.get_puid()))

    def cambiar_concepto_comision(self, cell, path, texto):
        model = self.wids['tv_comisiones'].get_model()
        idcomision = model[path][-1]
        #comision = pclases.Comision.get(idcomision)
        comision = pclases.getObjetoPUID(idcomision)
        comision.concepto = texto
        self.modificado = True
        model[path][0] = comision.concepto

    def rellenar_comisiones(self):
        model = self.wids['tv_comisiones'].get_model()
        model.clear()
        for comision in self.objeto.comisiones:
            precio = utils.float2str(comision.precio)
            cliente = comision.cliente and comision.cliente.nombre or ""
            try:
                numfactura = comision.serviciosTomados[0].facturaCompra.numfactura
            except (IndexError, AttributeError):
                numfactura = ""
            model.append((comision.concepto, 
                          utils.float2str(precio), 
                          comision.observaciones, 
                          cliente, 
                          "%s %%" % (utils.float2str(100*comision.porcentaje)),
                          numfactura, 
                          comision.get_puid()))

    def cambiar_precio_comision(self, cell, path, texto):
        try:
            precio = utils._float(texto)
        except ValueError:
            utils.dialogo_info(titulo = "PRECIO INCORRECTO", 
                               texto = "El texto introducido %s no es una cantidad correcta." % (texto), 
                               padre = self.wids['ventana'])
        else:
            model = self.wids['tv_comisiones'].get_model()
            idcomision = model[path][-1]
            #comision = pclases.Comision.get(idcomision)
            comision = pclases.getObjetoPUID(idcomision)
            comision.precio = precio
            self.modificado = True
            model[path][1] = utils.float2str(comision.precio)
            total = self.objeto.calcular_total()
            porcentaje = precio / total
            comision.porcentaje = porcentaje
            model[path][4] = "%s %%" % (utils.float2str(100 * porcentaje))

    def cambiar_observaciones_comision(self, cell, path, texto):
        model = self.wids['tv_comisiones'].get_model()
        idcomision = model[path][-1]
        #comision = pclases.Comision.get(idcomision)
        comision = pclases.getObjetoPUID(idcomision)
        comision.observaciones = texto
        self.modificado = True
        model[path][2] = comision.observaciones
    
    def cambiar_comercial_comision(self, cell, path, texto):
        model = self.wids['tv_comisiones'].get_model()
        idcomision = model[path][-1]
        #comision = pclases.Comision.get(idcomision)
        comision = pclases.getObjetoPUID(idcomision)
        if texto.strip() == "":
            comision.cliente = None
            model[path][3] = ""
        else:
            cliente = buscar_cliente(texto, self.wids['ventana'])
            if cliente != None:
                comision.cliente = cliente
                self.modificado = True
                model[path][3] = comision.cliente.nombre
    
    def cambiar_porcentaje_comision(self, cell, path, texto):
        try:
            porcentaje = utils.parse_porcentaje(texto, fraccion = True)
        except ValueError:
            utils.dialogo_info(titulo = "PORCENTAJE INCORRECTO", 
                               texto = "El texto introducido (%s) no es una cantidad correcta." % (texto), 
                               padre = self.wids['ventana'])
        else:
            model = self.wids['tv_comisiones'].get_model()
            idcomision = model[path][-1]
            #comision = pclases.Comision.get(idcomision)
            comision = pclases.getObjetoPUID(idcomision)
            comision.porcentaje = porcentaje
            model[path][4] = "%s %%" % (utils.float2str(100 * porcentaje))
            self.modificado = True
            total = self.objeto.calcular_total()
            precio = total * comision.porcentaje
            comision.precio = precio
            model[path][1] = utils.float2str(comision.precio)

    def add_comision(self, boton):
        """
        Añade una comisión al albarán.
        """
        cliente = self.objeto.cliente
        if cliente == None:
            utils.dialogo_info(titulo = "ALBARÁN SIN CLIENTE", 
                               texto = "Seleccione primero el cliente del albarán.", 
                               padre = self.wids['ventana'])
        else:
            c = pclases.Comision(cliente = cliente.cliente, 
                    porcentaje = cliente.porcentaje, 
                    precio = self.objeto.calcular_total() * cliente.porcentaje, 
                    fecha = mx.DateTime.localtime(), 
                    concepto = "Comisión por ventas. Albarán %s." % (
                                                self.objeto.numalbaran), 
                    observaciones = "", 
                    albaranSalida = self.objeto)
            pclases.Auditoria.nuevo(c, self.usuario, __file__)
            self.rellenar_comisiones()

    def drop_comision(self, boton):
        """
        Elimina la comisión seleccionada en el TreeView del albarán.
        """
        if self.wids['tv_comisiones'].get_selection().count_selected_rows() > 0: 
            model, paths = self.wids['tv_comisiones'].get_selection().get_selected_rows()
            for path in paths:
                idcomision = model[path][-1]
                comision = pclases.getObjetoPUID(idcomision)
                comision.destroy(ventana = __file__)
            self.rellenar_comisiones()

# XXX Parte de facturación automática: 
    def get_siguiente_numfactura(self, cliente):
        """
        Consulta el registro contador del cliente.
        Si no tiene, devuelve None.
        En otro caso, devuelve el número compuesto 
        por el contador+1 más el prefijo y sufijo
        que indique el registro.
        """
        # NOTA: Calcado de facturas_venta.py. Si cambio algo aquí, cambiar allí y viceversa.
        numfactura = None
        if cliente.contador != None:
            cliente.contador.sync()
            numfactura = "%s%04d%s" % (cliente.contador.prefijo, cliente.contador.contador, cliente.contador.sufijo)
            # El número entre prefijo y sufijo pasa a tener 4 dígitos como mínimo
        return numfactura
        
    def generar_factura(self):
        """
        Crea una factura de venta con el contenido del albarán.
        1.- Se comprueba que no se hayan facturado ya las LDVs.
        2.- Las que no han sido facturadas, se facturan. 
        3.- Se relacionan las comisiones (si las tuviera) con la factura. 
            OJO: La relación principal a tener en cuenta es la de las 
            comisiones con el albarán. Una comisión puede cambiar de factura 
            si el albarán se factura en dos veces.
        """
        factura = None
        (fras, ldvs_facturadas, srvs_facturados, ldvs_facturables, 
         srvs_facturables) = self.init_structs_factura()
        if fras != []:
            ldvs_facturadas = "\n".join(["Venta de %s en factura %s." % 
                (ldv.producto.descripcion, 
                 ((ldv.facturaVenta and ldv.facturaVenta.numfactura) or 
                  (ldv.prefactura and ldv.prefactura.numfactura) or "")
                ) for ldv in ldvs_facturadas])
            srvs_facturados = "\n".join(["%s en factura %s." % 
                (srv.concepto, 
                 ((srv.facturaVenta and srv.facturaVenta.numfactura) or 
                  (srv.prefactura and srv.prefactura.numfactura) or "")
                ) for srv in srvs_facturados])
            utils.dialogo_info(titulo = "VENTAS FACTURADAS", 
                texto = "Algunas salidas ya han sido facturadas:\n%s\n%s" % (
                    ldvs_facturadas, srvs_facturados), 
                padre = self.wids['ventana'])
        
        if ldvs_facturables == [] and srvs_facturables == []:
            utils.dialogo_info(titulo = "NO SE PUEDE GENERAR FACTURA", 
                texto="Todas las salidas del albarán han sido ya facturadas.",
                padre = self.wids['ventana'])
            ok = False
        else: 
            cliente = self.objeto.cliente
            if cliente == None:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Albarán sin cliente.", 
                                   padre = self.wids['ventana'])
                ok = False
                return ok, None
            numfactura = self.get_siguiente_numfactura(cliente)
            if numfactura == None:
                utils.dialogo_info(titulo = "ERROR",
                                   texto = "Cliente sin contador.", 
                                   padre = self.wids['ventana'])
                ok = False
                return ok, None
            #fecha = self.objeto.fecha  # Había empezado a dar problemas de 
            # secuencialidad en los números de serie porque a veces se dejan 
            # albaranes sin facturar o con fechas posteriores para 
            # completarlos en Toledo. Al facturarlos desde la ventana de 
            # albaranes días más tarde, salían las facturas con la fecha del 
            # albarán, que era anterior al de las facturas anteriores. CWT: Si 
            # usamos siempre la fecha actual, no debería haber problemas.
            fecha = mx.DateTime.localtime()
            ultima_factura, ok = chequear_restricciones_nueva_factura(cliente,  # @UnusedVariable
                                                                   numfactura,
                                                                        fecha)
            if ok:
                contador = self.objeto.cliente.contador
                numfactura2 = contador.get_and_commit_numfactura()
                try:
                    assert numfactura == numfactura2, "Número de factura precalculado y obtenido al actualizar el contador difieren: %s != %s." % (numfactura, numfactura2)
                except AssertionError, msg:
                    self.logger.error("%salbaranes_salida::generar_factura -> Error al actualizar contador (probablemente debido a concurrencia): %s" % (self.usuario and self.usuario.usuario or "", msg))
                    utils.dialogo_info(titulo = "ERROR", 
                        texto = "Error al calcular el número de factura. Vuel"
                                "va a intentarlo o contacte con el administra"
                                "dor.", 
                        padre = self.wids['ventana'])
                    return False, None
            else:
                try:
                    contador = self.objeto.cliente.contador
                    numfactura = probar_siguientes(contador, cliente, fecha)
                except:
                    numfactura = None
                if numfactura is None:
                    utils.dialogo_info(titulo = "ERROR", 
                        texto = "Número y fecha no satisfacen restricciones "
                                "de secuencialidad o número de factura ya ex"
                                "iste. Compruebe contadores.", 
                        padre = self.wids['ventana'])
                    ok = False
                    return ok, None
            iva = cliente.get_iva_norm()
            if len(ldvs_facturables) > 0:
                try:
                    descuento = ldvs_facturables[0].pedidoVenta.descuento
                        # El descuento de la factura es el del pedido de la 
                        # primera de las líneas de venta. Si tiene varias, 
                        # es de esperar que todas sean del mismo pedido y 
                        # con el mismo descuento.
                except AttributeError:  # PedidoVenta es None.
                    self.logger.warning("albaranes_de_salida.py: "
                        "Línea de venta con ID %d no tiene pedido de venta."
                        " ¿De dónde viene entonces?" % (
                            ldvs_facturables[0].id))
                    descuento = 0
            else:
                descuento = 0
            try:
                irpf = pclases.DatosDeLaEmpresa.select()[0].irpf
            except (IndexError, AttributeError), msg:
                self.logger.error("albaranes_de_salida::generar_factura ->"
                                  " No se encontraron los datos de la empresa."
                                  " Excepción: %s" % (msg))
                irpf = 0.0
            obra_albaran = self.objeto.determinar_obra()
            factura = pclases.FacturaVenta(fecha = fecha, 
                                           numfactura = numfactura,
                                           cliente = cliente,
                                           iva = iva,
                                           cargo = 0,
                                           bloqueada = False, 
                                           descuento = descuento, 
                                           irpf = irpf, 
                                           obra = obra_albaran)
            pclases.Auditoria.nuevo(factura, self.usuario, __file__)
            for ldv in ldvs_facturables:
                ldv.facturaVenta = factura
            for srv in srvs_facturables:
                srv.facturaVenta = factura
            for comision in self.objeto.comisiones:
                comision.facturaVenta = factura
            utils.dialogo_info(titulo = "FACTURA GENERADA", 
                               texto = "Factura %s generada correctamente.\n"
                                       "A continuación se van a intentar "
                                       "crear los vencimientos." % (
                                            factura.numfactura), 
                               padre = self.wids['ventana'])
            ok = self.crear_vencimientos_por_defecto(factura)
            ok = ok and factura.cliente.cif and factura.cliente.cif.strip()!=""
        return ok, factura

    def init_structs_factura(self):
        fras = []
        ldvs_facturables = [ldv for ldv in self.objeto.lineasDeVenta if ldv.facturaVentaID == None and ldv.prefacturaID == None]
        srvs_facturables = [srv for srv in self.objeto.servicios if srv.facturaVentaID == None and srv.prefactura == None]
        ldvs = [ldv for ldv in self.objeto.lineasDeVenta]
        srvs = [srv for srv in self.objeto.servicios]
        ldvs_facturadas = [ldv for ldv in self.objeto.lineasDeVenta if ldv.facturaVentaID != None or ldv.prefacturaID != None]
        srvs_facturados = [srv for srv in self.objeto.servicios if srv.facturaVentaID != None or srv.prefacturaID != None]
        
        for ldv in ldvs:
            if ldv.facturaVentaID != None and ldv.facturaVenta not in fras:
                fras.append(ldv.facturaVenta)
            if ldv.prefacturaID != None and ldv.prefactura not in fras:
                fras.append(ldv.prefactura)
        for srv in srvs:
            if srv.facturaVentaID != None and srv.facturaVenta not in fras:
                fras.append(srv.facturaVenta)
            if srv.prefacturaID != None and srv.prefactura not in fras:
                fras.append(srv.prefactura)
        return fras, ldvs_facturadas, srvs_facturados, ldvs_facturables, srvs_facturables

 
    def borrar_vencimientos_y_estimaciones(self, factura):
        for vto in factura.vencimientosCobro:
            vto.factura = None
            vto.destroy(ventana = __file__)
        for est in factura.estimacionesCobro:
            est.factura = None
            est.destroy(ventana = __file__)
    
    def rellenar_totales(self, factura):
        """
        Calcula los totales de la factura a partir de 
        las LDVs, servicios, cargo, descuento y abonos.
        """
        subtotal = self.total_ldvs(factura) + self.total_srvs(factura)
        tot_dto = ffloat(-1 * (subtotal + factura.cargo) * factura.descuento)
        abonos = sum([pa.importe for pa in factura.pagosDeAbono])
        tot_iva = self.total_iva(factura.iva, subtotal, tot_dto, factura.cargo, abonos)
        irpf = factura.calcular_total_irpf()
        return self.total(subtotal, factura.cargo, tot_dto, tot_iva, abonos, irpf)

    def total(self, subtotal, cargo, dto, iva, abonos, irpf):
        return ffloat(subtotal + cargo + dto + iva + abonos - irpf)

    def total_iva(self, iva, subtotal, tot_dto, cargo, abonos):
        return ffloat(subtotal + tot_dto + cargo + abonos) * iva

    def total_ldvs(self, factura):
        """
        Total de las líneas de venta. Sin IVA.
        """
        return sum([ffloat((l.cantidad * l.precio) * (1 - l.descuento)) for l in factura.lineasDeVenta])
        
    def total_srvs(self, factura):
        """
        Total de servicios. Sin IVA.
        """
        return sum([ffloat((s.precio * s.cantidad) * (1 - s.descuento)) for s in factura.servicios])


    def crear_vencimientos_por_defecto(self, factura):
        """
        Crea e inserta los vencimientos por defecto
        definidos por el cliente en la factura
        actual y en función de las LDV que tenga
        en ese momento (concretamente del valor
        del total de la ventana calculado a partir
        de las LDV.)
        """
        ok = False
        # NOTA: Casi-casi igual al de facturas_venta.py. Si cambia algo importante aquí, cambiar también allí y viceversa.
        cliente = factura.cliente
        try:
            pedido = self.objeto.get_pedidos()[0]
        except IndexError:
            vtos = None
        else:
            try:
                vtos = [pedido.formaDePago.plazo]
            except AttributeError:
                vtos = None
        if not vtos:
            if cliente.vencimientos != None and cliente.vencimientos != '':
                try:
                    vtos = cliente.get_vencimientos(factura.fecha)
                except:
                    utils.dialogo_info(titulo = 'ERROR VENCIMIENTOS POR DEFECTO', 
                                       texto = 'Los vencimientos por defecto del cliente no se pudieron procesar correctamente.\nVerifique que están bien escritos y el formato es correcto en la ventana de clientes.', 
                                       padre = self.wids['ventana'])
                    return ok    # Los vencimientos no son válidos o no tiene.
        if vtos:
            self.borrar_vencimientos_y_estimaciones(factura)
            total = self.rellenar_totales(factura)
            numvtos = len(vtos)
            try:
                cantidad = total/numvtos
            except ZeroDivisionError:
                cantidad = total
            if not factura.fecha:
                factura.fecha = mx.DateTime.localtime()
            if cliente.diadepago != None and cliente.diadepago != '':
                diaest = cliente.get_dias_de_pago()
            else:
                diaest = False
            if factura.get_pedidos():
                try:
                    pedido = factura.get_pedidos()[0]
                    str_formapago = pedido.formaDePago.toString(cliente)
                except (AttributeError, IndexError):
                    str_formapago = factura.cliente and factura.cliente.textoformacobro or ""
            else:   # Albarán sin pedidos. No debería, pero puede pasar.
                str_formapago = factura.cliente.get_texto_forma_cobro()
            for incr in vtos:
                fechavto = mx.DateTime.DateFrom(factura.fecha) + (incr * mx.DateTime.oneDay)
                vto = pclases.VencimientoCobro(fecha = fechavto,
                        importe = float(cantidad),
                        facturaVenta = factura, 
                        observaciones = str_formapago, 
                        cuentaOrigen = factura.cliente 
                            and factura.cliente.cuentaOrigen or None)
                pclases.Auditoria.nuevo(vto, self.usuario, __file__)
                if diaest:
# XXX 24/05/06
                    # Esto es más complicado de lo que pueda parecer a simple 
                    # vista. Ante poca inspiración... ¡FUERZA BRUTA!
                    fechas_est = []
                    for dia_estimado in diaest:
                        while True:
                            try:
                                fechaest = mx.DateTime.DateTimeFrom(day = dia_estimado, month = fechavto.month, year = fechavto.year)
                                break
                            except:
                                dia_estimado -= 1
                                if dia_estimado <= 0:
                                    dia_estimado = 31
                        if fechaest < fechavto:     # El día estimado cae ANTES del día del vencimiento. 
                                                    # No es lógico, la estimación debe ser posterior.
                                                    # Cae en el mes siguiente, pues.
                            mes = fechaest.month + 1
                            anno = fechaest.year
                            if mes > 12:
                                mes = 1
                                anno += 1
                            try:
                                fechaest = mx.DateTime.DateTimeFrom(day = dia_estimado, month = mes, year = anno)
                            except mx.DateTime.RangeError:
                                # La ley de comercio dice que se pasa al último día del mes:
                                fechaest = mx.DateTime.DateTimeFrom(day = -1, month = mes, year = anno)
                        fechas_est.append(fechaest)
                    fechas_est.sort(utils.cmp_mxDateTime)
                    fechaest = fechas_est[0]
                    vto.fecha = fechaest 
            ok = True
        else:
            utils.dialogo_info(titulo = "SIN DATOS", 
                               texto = "El cliente no tiene datos suficientes para crear vencimientos por defecto.", 
                               padre = self.wids['ventana'])
        return ok

    def descargar_de_terminal(self, boton):
        """
        Lee los códigos almacenados en el terminal de códigos de barras 
        y los introduce en el albarán actual (siempre que los datos del 
        lector no incluyan número de albarán o éste sea igual al del 
        albarán actual) de la misma forma que si se teclearan manualmente.
        """
        self.logger.warning("%salbaranes_de_salida -> Iniciando descargar_de_terminal (salida de artículos automática)" % (self.usuario and self.usuario.usuario + ": " or ""))
        # TODO: Hay que meter una ventana de progreso o algo, porque en 
        # descargar 130 rollos se ha tirado por lo menos un minuto la ventana 
        # en blanco.
        datos = None
        cancelar = False
        while datos == None and not cancelar:
            datos = utils.descargar_phaser(logger = self.logger)
            if datos == None:
                cancelar = not utils.dialogo(titulo = "¿VOLVER A INTENTAR?", 
                                             texto = "Se ha superado el tiempo de espera.\n¿Desea continuar?\n\n(Pulse SÍ para volver a intentar o NO para cancelar la operación.)", 
                                             padre = self.wids['ventana'])
            elif isinstance(datos, (type([]), type(()))):
                self.descargar_y_meter_articulos_en_albaran_actual(datos)
            elif isinstance(datos, type({})):
                for albaran in datos:
                    if albaran == self.objeto:
                        self.descargar_y_meter_articulos_en_albaran_actual(datos[albaran])
                    else:
                        self.logger.warning("Albarán actual: %s. Albarán descargado: %s. IGNORO ALBARÁN." % (self.objeto.numalbaran, albaran.numalbaran))
                        utils.dialogo_info(titulo = "ALBARÁN INCORRECTO", 
                                           texto = "El albarán descargado (%s) no coincide con el albarán actual en ventana (%s).\nSe ignorará.\n\nNo borre la memoria del terminal y realice la descarga en el albarán correcto.\n\n\nSi ha leído más de un albarán en el terminal, a continuación se intentarán descargar también.", 
                                           padre = self.wids['ventana'])

    def descargar_y_meter_articulos_en_albaran_actual(self, datos):
        """
        Datos es una lista de objetos bala, bigbag o rollo.
        Los lee e introduce en el albarán actual
        """
        articulos = []
        articulos_baja_calidad = []
        for bala_o_rollo_o_bb in datos:
            articulo = bala_o_rollo_o_bb.articulo
            if articulo.es_de_baja_calidad():
                articulos_baja_calidad.append(articulo)
            articulos.append(articulo)
        texto = """
        Los siguientes artículos se han considerado que son         
        de baja calidad. ¿Continuar?                                
                                                                    
        %s  
        """ % ("\n".join([a.codigo for a in articulos_baja_calidad]))
        if articulos_baja_calidad == [] or utils.dialogo(titulo = "ARTÍCULOS DE BAJA CALIDAD", texto = texto, padre = self.wids['ventana']):
            self.crear_ldv(articulos)   # FLIPA: En realidad no crea, asocia 
                                        # artículos al albarán
            self.objeto.calcular_comisiones()
            self.actualizar_ventana()

def get_str_pedidos_albaranes(factura):
    """
    Devuelve una cadena con los pedidos y albaranes entre paréntesis de las 
    LDV de la factura.
    """
    peds = {'-': []}
    for ldv in factura.lineasDeVenta:
        if ldv.pedidoVenta == None and ldv.albaranSalida != None:
            peds['-'].append(ldv.albaranSalida.numalbaran)
        elif ldv.pedidoVenta != None:
            if ldv.pedidoVenta.numpedido not in peds:
                peds[ldv.pedidoVenta.numpedido] = []
            if ldv.albaranSalida != None:
                if not ldv.albaranSalida.numalbaran in peds[ldv.pedidoVenta.numpedido]:
                    peds[ldv.pedidoVenta.numpedido].append(ldv.albaranSalida.numalbaran)
    pedsalbs = ""
    for p in peds:
        if p == '-' and peds[p] == []:
            continue
        pedsalbs += "%s(%s) " % (p, ','.join(peds[p]))
    return pedsalbs

def imprimir_factura(factura, usuario = None, abrir = True, es_copia = False, 
                     albaran = None):
    """
    Imprime una factura generando el PDF tal y como se hace 
    desde la ventana facturas_venta.py.
    NOTA: usuario se pasaba con intención de abrir la ventana 
    de facturas desde aquí. Actualmente ya no se usa.
    Si "abrir" es True, después de generar el PDF lo abre con 
    el visor predeterminado.
    """
    # CWT: Si las observaciones están en blanco, copio "Ref.: nombre_obra"
    if (not factura.observaciones.strip() 
        and factura.obra and not factura.obra.generica):
        factura.observaciones = "Ref. obra: %s" % factura.obra.nombre
        factura.syncUpdate()
        factura.sync()
    # EOCWT
    # GTX4: Uso dirección de envío del albarán. Si no me llega albarán, 
    # entonces la de la obra. Si no hay obra, pues la del cliente.
    obra = factura.obra
    # CWT: Nombre de envío, el del cliente otra vez.
    #try:
    #    nomenv = obra.nombre
    #except AttributeError:
    #    try:
    #        nomenv = albaran.nombre
    #    except AttributeError:
    #        nomenv = factura.cliente.nombre
    nomenv = factura.cliente.nombre
    try:
        direnv = obra.direccion
    except AttributeError:
        try:
            direnv = albaran.direccion
        except AttributeError:
            direnv = factura.cliente.direccion
    try:
        cpenv = obra.cp
    except AttributeError:
        try:
            cpenv = albaran.cp
        except AttributeError:
            cpenv = factura.cliente.cp
    try:
        ciuenv = obra.ciudad
    except AttributeError:
        try:
            ciuenv = albaran.ciudad
        except AttributeError:
            ciuenv = factura.cliente.ciudad
    try:
        proenv = obra.provincia
    except AttributeError:
        try:
            proenv = albaran.provincia
        except AttributeError:
            proenv = factura.cliente.provincia
    try:
        paisenv = obra.pais
    except AttributeError:
        try:
            paisenv = albaran.pais
        except AttributeError:
            paisenv = factura.cliente.pais
    cliente = {'numcli': str(factura.cliente.id),
               'nombre': nomenv,
               'nombref': factura.cliente.nombref,
               'cif': factura.cliente.cif,
               'direccion': direnv,
               'cp': cpenv,
               'localidad': ciuenv,
               'provincia': proenv,
               'pais': paisenv,
               'telf': factura.cliente.telefono,
               'fax':'',
               'direccionf': factura.cliente.direccionfacturacion,
               'cpf': factura.cliente.cpfacturacion,
               'localidadf': factura.cliente.ciudadfacturacion,
               'provinciaf': factura.cliente.provinciafacturacion,
               'paisf': factura.cliente.paisfacturacion}
    numpeds = get_str_pedidos_albaranes(factura)
    
    facdata = {'facnum': factura.numfactura,
               'fecha': utils.str_fecha(factura.fecha),
               'pedido': numpeds,
               'albaranes':'',
               'observaciones': factura.observaciones}
    lineas = []
    lineasdeventa = [ldv for ldv in factura.lineasDeVenta]
    lineasdeventa.sort(utils.f_sort_id)
    for l in lineasdeventa:
        linea = {'codigo': l.producto.codigo,
                 'cantidad': l.cantidad,
                 'descripcion': l.producto.descripcion,
                 'precio': l.precio,
                 'descuento': str(l.descuento), 
                 'unidad': l.producto.get_str_unidad_de_venta()}
        lineas.append(linea)
    if factura.cliente.pais.upper().replace(' ','') != 'ESPAÑA':
        arancel_lista = [ldv.productoVenta.arancel 
                         for ldv in factura.lineasDeVenta 
                         if ldv.productoVenta 
                             and ldv.productoVenta.arancel != "" 
                             and ldv.productoVenta.arancel != None]
        # OJO: NOTA: El arancel es siempre el mismo. Muestro el del primer 
        # articulo que encuentre con arancel != "".
        if arancel_lista != []:
            arancel = arancel_lista[0]
        else:
            arancel = None
    else:
        arancel = None
    for l in factura.servicios:
        descripcion = l.concepto
        linea = {'codigo': "",
                 'cantidad': l.cantidad,
                 'descripcion': descripcion,
                 'precio': l.precio,
                 'descuento': str(l.descuento), 
                 "unidad": ""}
        lineas.append(linea)
    vtos = factura.vencimientosCobro[:]
    vtos.sort(utils.cmp_fecha_id)
    fechasVencimiento = []
    documentosDePago = []
    for vto in vtos:
        fechasVencimiento.append(utils.str_fecha(vto.fecha))
        if vto.cuentaOrigen:
            cuenta = "a %s %s" % (vto.cuentaOrigen.banco, vto.cuentaOrigen.ccc)
        else:
            cuenta = ""
        documentosDePago.append("%s %s" % (vto.observaciones, cuenta))
    vencimiento = {'fecha': "; ".join(fechasVencimiento),
                   # 'pago': factura.cliente.vencimientos,
                   'pago': str(factura.get_plazo_pago(default = "")),
                   'documento': "; ".join(documentosDePago)}
    from formularios import numerals
    totalfra = factura.calcular_total()
    totales = {}
    totales['subtotal'] = "%s €" % (
        utils.float2str(factura.calcular_subtotal(), 2))
    cargo = factura.cargo 
    if not cargo:   # Si es 0, 0.0, None o cualquier cosa de estas...
        cargo = None
    totales['cargo'] = cargo
    descuento = factura.calcular_total_descuento()
    if not descuento: 
        descuento = None
    else:
        descuento = "%s (%s %%)" % (utils.float2str(descuento), 
                                    utils.float2str(factura.descuento*100, 0))
    totales['descuento'] = descuento
    totales['iva'] = "%s %%" % (utils.float2str(factura.iva * 100, 0))
    totales['totaliva'] = "%s €"%utils.float2str(factura.calcular_total_iva())
    totales['total'] = "%s €" % (utils.float2str(totalfra, 2))
    totales['irpf'] = "%s %%" % (utils.float2str(factura.irpf * 100, 0))
    totales['totirpf'] = "%s €"%utils.float2str(factura.calcular_total_irpf())
    texto = numerals.numerals(totalfra, moneda = "euros", 
                              fraccion = "céntimos").upper()
    if pclases.config.get_multipagina() == 1:
        from informes import factura_multipag
        nomarchivo = factura_multipag.go_from_facturaVenta(factura)
    else:
        nomarchivo = geninformes.factura(cliente,
                                         facdata,
                                         lineas,
                                         arancel,
                                         vencimiento,
                                         texto, 
                                         totales, 
                                         es_copia = es_copia)
    if abrir:
        from formularios import reports
        reports.abrir_pdf(nomarchivo)
    return nomarchivo
    
def buscar_proveedor(nombre, ventana_padre = None, 
                     incluir_inhabilitados = False):
    """
    Busca un proveedor por su nombre. Si no lo encuentra solo con el 
    parámetro recibido o si encuentra más de uno, muestra una ventana 
    con los resultados para que el usuario elija uno de ellos.
    Devuelve el proveedor seleccionado o None.
    """
    proveedor = None
    if incluir_inhabilitados:
        proveedores = pclases.Proveedor.select(
                pclases.Proveedor.q.nombre.contains(nombre))
    else:
        proveedores = pclases.Proveedor.select(pclases.AND(
            pclases.Proveedor.q.inhabilitado == False, 
            pclases.Proveedor.q.nombre.contains(nombre)))
    numresultados = proveedores.count()
    if numresultados == 0:
        proveedores = pclases.Proveedor.select()
    if numresultados != 1:
        filas_res = [(p.id, p.nombre, p.cif) for p in proveedores]
        idproveedor = utils.dialogo_resultado(filas_res,
                                              titulo = 'Seleccione proveedor',
                                              cabeceras = ('ID', 'Nombre', 'C.I.F.'),  
                                              padre = ventana_padre) 
        if idproveedor > 0:
            proveedor = pclases.Proveedor.get(idproveedor)
    elif numresultados == 1:
        proveedor = proveedores[0]
    return proveedor
    
def buscar_cliente(nombre, ventana_padre = None):
    """
    Busca un cliente por su nombre. Si no lo encuentra solo con el 
    parámetro recibido o si encuentra más de uno, muestra una ventana 
    con los resultados para que el usuario elija uno de ellos.
    Devuelve el cliente seleccionado o None.
    """
    cliente = None
    clientes = pclases.Cliente.select(pclases.Cliente.q.nombre.contains(nombre))
    numresultados = clientes.count()
    if numresultados == 0:
        clientes = pclases.Cliente.select()
    if numresultados != 1:
        filas_res = [(p.id, p.nombre, p.cif) for p in clientes]
        idcliente = utils.dialogo_resultado(filas_res,
                                              titulo = 'Seleccione cliente',
                                              cabeceras = ('ID', 'Nombre', 'C.I.F.'),  
                                              padre = ventana_padre) 
        if idcliente > 0:
            cliente = pclases.Cliente.get(idcliente)
    elif numresultados == 1:
        cliente = clientes[0]
    return cliente
    
def ajustar_existencias(ldv, cantidad_anterior = None):
    """
    Si la LDV es de un producto de compra o de un producto especial, 
    ajusta las existencias del mismo y le resta la cantidad que 
    sale del almacén en la LDV.
    Si el parámetro opcional cantidad_anterior es distinto de None (se 
    usa al cambiar la cantidad de la LDV con posterioridad) la cantidad 
    a restar a las existencias es la cantidad actual menos la cantidad_anterior.
    Siempre ajusta las existencias aunque el campo controlExistencias esté 
    a False y el producto es un producto de compra, solo que en ese caso 
    se ignoran las existencias en el resto del programa; pero ajustarlas las 
    ajusta.
    """
    producto = ldv.get_producto()
    cantidad = ldv.cantidad
    if cantidad_anterior != None:
        cantidad = cantidad - cantidad_anterior
    if cantidad != 0:   # Para evitar tráfico innecesario. Si no hay cambios 
                        # en las existencias de los productos, no los toco.
        producto.sync()
        if isinstance(producto, pclases.ProductoCompra):
            producto.existencias -= cantidad
            # Ajusto también las existencias del almacén origen.
            try:
                almacenorigen = ldv.albaranSalida.almacenOrigen
            except AttributeError:
                # OJO: Si la LDV viene de una factura que descuenta 
                # existencias sin que haya albarán de por medio, siempre se 
                # usará el principal como almacén origen.
                almacenorigen = pclases.Almacen.get_almacen_principal()
            producto.add_existencias(-cantidad, almacenorigen)
            if ldv.albaranSalida and ldv.albaranSalida.almacenDestino:
                producto.add_existencias(cantidad, 
                                         ldv.albaranSalida.almacenDestino)
        elif (isinstance(producto, pclases.ProductoVenta) 
              and producto.es_especial()):
            producto.camposEspecificosEspecial.sync()
            try:
                cantidad_por_bulto = producto.stock / producto.existencias
                bultos = cantidad / cantidad_por_bulto
            except ZeroDivisionError:
                bultos = 0
            #print producto.camposEspecificosEspecial.stock, cantidad
            #print producto.camposEspecificosEspecial.existencias, bultos
            # TODO: No hay rastro de las existencias por almacén 
            # en los productos de venta especiales. FUUUUUUUUUUUUUUUU
            producto.camposEspecificosEspecial.stock -= cantidad
            producto.camposEspecificosEspecial.existencias -= int(bultos)
            # DONE: ¿Qué pasa con los bultos en los almacenes?
            #       Nada. Se guardan las existencias. Se mira la razón 
            #       existencias/bultos y se multiplica por las existencias del 
            #       stock_especial para que nos dé el número de bultos 
            #       correspondiente a esas existencias.
            producto.camposEspecificosEspecial.sync()
        producto.sync()

def chequear_restricciones_nueva_factura(cliente, numfactura, fecha):
    """
    Devuelve la última factura de la serie del cliente recibido y un booleano
    que valdrá True si pasa las restricciones o False si no las cumple.
    Las restricciones son:
        1.- El número de factura no puede ser inferior al de la última
            factura existente de la serie (que debería ser el contador -1)
        2.- El número de factura no puede estar repetido.
        3.- La fecha no debe ser inferior a la de la última factura 
            existente de la serie.
    """
    # NOTA: Calcado (casi) de facturas_venta.py. Si cambio 
    # algo *significativo* aquí, cambiar allí y viceversa.
    ultima_factura = None
    ok = False
    FV = pclases.FacturaVenta
    if (FV.select(FV.q.numfactura == numfactura).count() == 0
        and cliente.contador != None):
        clientes = [str(c.id) for c in cliente.contador.clientes]
        clientes = ','.join(clientes)
        facturas = pclases.FacturaVenta.select("cliente_id IN (%s)"%clientes)
        ok = True
        # Any better?
        facturas = [f for f in facturas 
                    if f.numfactura.startswith(cliente.contador.prefijo) 
                       and f.numfactura.endswith(cliente.contador.sufijo)]
        facturas.sort(lambda f1, f2: f1.get_numero_numfactura() \
                                     - f2.get_numero_numfactura())
        if facturas:
            ultima_factura = facturas[-1]
            try:
                numero = int(numfactura.replace(cliente.contador.prefijo, \
                                  '').replace(cliente.contador.sufijo, ''))
            except:
                ok = False
            ok = ok and numero > ultima_factura.get_numero_numfactura()
            numero_repetido = pclases.FacturaVenta.select(\
                   pclases.FacturaVenta.q.numfactura == numfactura).count()
            ok = ok and not numero_repetido
            ok = ok and mx.DateTime.DateTimeFrom(fecha) \
                         >= ultima_factura.fecha
        else:
            ultima_factura = None
    return ultima_factura, ok

def probar_siguientes(c, cliente, fecha, rango = 5):
    """
    Recibe un contador y devuelve un número de factura válido
    dentro de los siguientes 5 números (por defecto).
    Si se encuentra, actualiza el contador y lo devuelve.
    En caso de que no se encuentre, devuelve None.
    """
    numfactura = None
    for i in range(1, rango):
        tmpnumfactura = c.get_next_numfactura(inc = i)
        ok, ult_factura = chequear_restricciones_nueva_factura(cliente,  # @UnusedVariable
                                                               tmpnumfactura, 
                                                               fecha)
        if ok:
            numfactura = c.get_next_numfactura(commit = True, inc = i)
            break
    return numfactura


def comprobar_existencias_producto(ldp, ventana_padre, cantidad, almacen):
    """
    Comprueba que para el producto que se va a servir en la línea de pedido 
    hay existencias mayores o iguales que «cantidad». Si hay menos, pregunta 
    al usuario y devuelve la cantidad elegida finalmente, que debe ser igual 
    o menor que el mínimo entre la cantidad recibida y la cantidad 
    disponible del producto.
    Si cancela devuelve None.
    """
    producto = ldp.producto
    hay = producto.get_stock(almacen = almacen)
    if hay < cantidad:
        a_servir = utils.dialogo_entrada(titulo = "EXISTENCIAS INSUFICIENTES",
            texto="No hay existencias sufucientes para servir %s %s de %s.\n"
                  "Introduzca la nueva cantidad a servir:\n\n"
                  "Máximo en stock en %s: %s" % (
                    utils.float2str(cantidad, autodec = True), 
                    producto.unidad, 
                    producto.descripcion, 
                    almacen.nombre, 
                    utils.float2str(hay, autodec = True)), 
            padre = ventana_padre, 
            valor_por_defecto = utils.float2str(hay))
        if a_servir != None:
            try:
                a_servir = utils._float(a_servir)
                    # Aquí me aseguro de que, aunque me intente
                    # hacer el gato metiendo más cantidad de la 
                    # que hay, no va a salir de aquí con una cant. superior
                    # a la que se puede servir.
                a_servir = min(hay, a_servir) 
            except (ValueError, TypeError):
                utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                    texto = "El texto introducido (%s) no es un número válido"
                        % a_servir, 
                    padre = ventana_padre)
                a_servir = None
    else:
        a_servir = cantidad
    return a_servir
 
def es_venta_rollos_c(ldv_o_producto):
    """
    Comprueba si la línea de venta es de un producto C con artículos rollos C. 
    Porque en ese caso no debería ajustarse la cantidad de la línea con el peso
    real de sus artículos.
    """
    if isinstance(ldv_o_producto, pclases.LineaDeVenta):
        producto = ldv_o_producto.productoVenta
    else:
        producto = ldv_o_producto
    try:
        # CWT: Solo para rollos C. Nada de balas de cable. 
        #res = (producto.es_bala_cable() 
        #        or producto.es_rollo_c())
        res = producto.es_rollo_c()
    except AttributeError:
        res = False
    if pclases.DEBUG:
        print "albaranes_de_salida::es_venta_rollos_c ->", res
    return res

def select_lineas_pedido(pedido, padre = None):
    """
    Muestra las líneas del pedido pendientes de servir y permite al usuario 
    seleccionar las que realmente va a incluir en el albarán.
    Devuelve dos listas: una de líneas de pedido y otra de servicios.
    Si cancela devuelve las listas vacías.
    """
    ops = []
    default = []
    for ldp in pedido.lineasDePedido:
        ops.append((ldp.puid, ldp.get_info()))
        if ldp.get_cantidad_pendiente():
            default.append(ldp.puid)
    for srv in pedido.servicios:
        ops.append((srv.puid, srv.get_info()))
    res = utils.dialogo_checks(titulo = "SELECCIONE LÍNEAS DEL PEDIDO", 
            texto = "Selecciones las líneas del pedido %s a servir en\n"
                    "el presente albarán. Las líneas no seleccionadas\n"
                    "quedarán pendientes de servir." % pedido.numpedido, 
            ops = ops, 
            padre = padre, 
            valor_por_defecto = default) # Marcadas las líneas pendientes.
    ldps = []
    srvs = []
    if res == False:
        return None     # Ha cancelado y res no son dos listas. Es False.
    else:
        for puid in res:
            obj = pclases.getObjetoPUID(puid)
            if isinstance(obj, pclases.LineaDePedido):
                ldps.append(obj)
            elif isinstance(obj, pclases.Servicio):
                srvs.append(obj)
        return ldps, srvs

if __name__=='__main__':
    a = AlbaranesDeSalida()

