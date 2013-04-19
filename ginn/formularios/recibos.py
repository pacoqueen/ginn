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
## recibos.py - Gestión de recibos emitidos. 
###################################################################
## NOTAS:
##  
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 29 de mayo de 2007 -> Inicio
## 
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
from informes import geninformes
import mx.DateTime
from framework.seeker import VentanaGenerica 
from numerals import numerals

class Recibos(Ventana, VentanaGenerica):

    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.clase = pclases.Recibo
        self.dic_campos = {"numrecibo": "e_numrecibo", 
                           "anno": "sp_anno", 
                           "lugarLibramiento": "e_lugar_libramiento", 
                           "fechaLibramiento": "e_fecha_libramiento", 
                           "fechaVencimiento": "e_fecha_vencimiento", 
                           "personaPago": "e_persona_pago", 
                           "domicilioPago": "e_domicilio_pago", 
                           "cuentaOrigenID": "cbe_cuenta_origen", 
                           "cuentaBancariaClienteID": 
                                "cbe_cuenta_bancaria_cliente", 
                           "nombreLibrado": "e_nombre_librado", 
                           "direccionLibrado": "e_direccion_librado", 
                           "observaciones": "txt_observaciones", 
                           }
        Ventana.__init__(self, 'recibos.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar,
                       'b_cliente/clicked': self.set_cliente, 
                       'b_factura/clicked': self.set_factura, 
                       'b_imprimir/clicked': self.imprimir, 
                       'b_drop_factura/clicked': self.drop_factura, 
                       "b_siguiente/clicked": self.ir_a_sig_ant, 
                       "b_anterior/clicked": self.ir_a_sig_ant, 
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        self.cliente = None
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def ir_a_sig_ant(self, boton):
        if self.objeto:
            id_actual = self.objeto.id
            if boton.name == "b_anterior":
                r = pclases.Recibo.select(pclases.Recibo.q.id < id_actual, 
                                          orderBy = "-id")
            elif boton.name == "b_siguiente":
                r = pclases.Recibo.select(pclases.Recibo.q.id > id_actual, 
                                          orderBy = "id")
            else:
                r = None
            if r != None and r.count() > 0:
                recibo = r[0]
                self.ir_a(recibo)
            else:
                utils.dialogo_info(titulo = "NO HAY MÁS RECIBOS", 
                                   texto = "No hay más recibos.", 
                                   padre = self.wids['ventana'])

    def borrar(self, boton):
        """
        Borra el registro activo.
        """
        if utils.dialogo(titulo = "¿BORRAR?", texto = "¿Desea eliminar el recibo en pantalla?", padre = self.wids['ventana']):
            try:
                for vto in self.objeto.vencimientosCobro:
                    vto.recibo = None
                    txtrcbo = "Recibo bancario número %d con fecha de emisión %s." % (self.objeto.numrecibo, 
                                                                                          utils.str_fecha(self.objeto.fechaLibramiento))
                    if txtrcbo in vto.observaciones:
                        vto.observaciones = vto.observaciones.replace(txtrcbo, "")
                    else:   # Se ha cambiado la fecha o el número del recibo 
                            # después de haber incluido el vencimiento
                        if "Recibo bancario" in vto.observaciones:
                            vto.observaciones = vto.observaciones[:vto.observaciones.index("Recibo bancario")]
                        else:   # No sé lo que habrá hecho el usuario con las observaciones, reinicio al texto de forma de pago original:
                            try:
                                vto.observaciones = vto.get_factura_o_prefactura().cliente.textoformacobro
                            except AttributeError, msg:  # No tiene factura, o la factura no tiene cliente. Dejo las observaciones que tuviera.
                                txterror = "%srecibos::drop_factura -> El vencimientoCobro ID %d no tiene factura, o su factura no tiene cliente. Mensaje de la excepción: %s" % (self.usuario and self.usuario.usuario + ": " or "", vto.id, msg)
                                self.logger.warning(txterror)
                self.objeto.destroy(ventana = __file__)
            except Exception, msg:
                utils.dialogo_info(titulo = "ERROR", texto = "El registro no se pudo eliminar", padre = self.wids['ventana'])
                self.logger.error("%srecibos::borrar -> No se pudo eliminar el recibo ID %d. Excepcion: %s" % 
                    (self.usuario and self.usuario.usuario + ": " or "", self.objeto and self.objeto.id or 0, msg))
            else:
                self.ir_a_primero()

    def drop_factura(self, boton = None):
        """
        Elimina la relación entre una factura (en realidad un 
        vencimiento) y el recibo actual.
        """
        if self.objeto != None:
            ops = [(v.id, "%s: %s € (%s))" % (v.get_factura_o_prefactura() and v.get_factura_o_prefactura().numfactura or "?", 
                                              utils.float2str(v.importe), 
                                              utils.str_fecha(v.fecha))) for v in self.objeto.vencimientosCobro]
            ide = utils.dialogo_combo(titulo = "QUITAR FACTURA", 
                                     texto = "Seleccione un vencimiento a eliminar del recibo.", 
                                     padre = self.wids['ventana'], 
                                     ops = ops)
            if ide != None:
                vto = pclases.VencimientoCobro.get(ide)
                vto.recibo = None
                txtrcbo = "Recibo bancario número %d con fecha de emisión %s." % (self.objeto.numrecibo, 
                                                                                      utils.str_fecha(self.objeto.fechaLibramiento))
                if txtrcbo in vto.observaciones:
                    vto.observaciones = vto.observaciones.replace(txtrcbo, "")
                else:   # Se ha cambiado la fecha o el número del recibo después de haber incluido el vencimiento
                    if "Recibo bancario" in vto.observaciones:
                        vto.observaciones = vto.observaciones[:vto.observaciones.index("Recibo bancario")]
                    else:   # No sé lo que habrá hecho el usuario con las observaciones, reinicio al texto de forma de pago original:
                        try:
                            vto.observaciones = vto.get_factura_o_prefactura().cliente.textoformacobro
                        except AttributeError:  # No tiene factura, o la factura no tiene cliente. Dejo las observaciones que tuviera.
                            self.logger.warning("%srecibos::drop_factura -> El vencimientoCobro ID %d no tiene factura, o su factura no tiene cliente." % (self.usuario and self.usuario.usuario + ": " or "", vto.id))
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
            filas_res.append((r.id, 
                              r.numrecibo, 
                              r.anno, 
                              r.get_cliente() and r.get_cliente().nombre or "", 
                              ", ".join([f.numfactura for f 
                                         in r.get_facturas()]), 
                              utils.float2str(r.calcular_importe()), 
                              utils.str_fecha(r.fechaLibramiento), 
                              utils.str_fecha(r.fechaVencimiento)
                             ))
        idrecibo = utils.dialogo_resultado(filas_res,
                                           titulo = 'SELECCIONE RECIBO',
                                           cabeceras = ('ID', 
                                                        'Número', 
                                                        'Año', 
                                                        'Cliente', 
                                                        'Facturas', 
                                                        'Importe', 
                                                        'Libramiento', 
                                                        'Vencimiento'), 
                                           padre = self.wids['ventana'])
        if idrecibo < 0:
            return None
        else:
            return idrecibo
    
    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        recibo = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR RECIBO", 
                                         texto = "Introduzca número de recibo o nombre del cliente:", 
                                         padre = self.wids['ventana']) 
        if a_buscar != None:
            try:
                numrecibo = int(a_buscar)
                nombrecliente = None  # @UnusedVariable
            except ValueError:
                nombrecliente = a_buscar  # @UnusedVariable
                numrecibo = None
            if numrecibo != None:
                criterio = pclases.Recibo.q.numrecibo == numrecibo
                resultados = [r for r 
                              in pclases.Recibo.select(criterio,orderBy = "id")]
            else:
                resultados = [r for r in pclases.Recibo.select(orderBy = "id") 
                              if (r.get_cliente() != None 
                                  and a_buscar.upper() 
                                        in r.get_cliente().nombre.upper())
                                  or (r.get_cliente() == None 
                                      and a_buscar == "")]
            if len(resultados) > 1:
                ## Refinar los resultados
                idrecibo = self.refinar_resultados_busqueda(resultados)
                if idrecibo == None:
                    return
                resultados = [pclases.Recibo.get(idrecibo)]
                # Me quedo con una lista de resultados de un único objeto 
                # ocupando la primera posición.
                # (Más abajo será cuando se cambie realmente el objeto actual 
                # por este resultado.)
            elif len(resultados) < 1:
                    ## Sin resultados de búsqueda
                    utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)',
                                       padre = self.wids['ventana'])
                    return
            ## Un único resultado
            # Primero anulo la función de actualización
            if recibo != None:
                recibo.notificador.desactivar()
            # Pongo el objeto como actual
            try:
                recibo = resultados[0]
            except IndexError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Se produjo un error al recuperar la información.\nCierre y vuelva a abrir la ventana antes de volver a intentarlo.", 
                                   padre = self.wids['texto'])
                return
            # Y activo la función de notificación:
            recibo.notificador.activar(self.aviso_actualizacion)
            self.activar_widgets(True)
        self.objeto = recibo
        self.actualizar_ventana()

    def set_cliente(self, boton):
        """
        Busca un cliente y lo hace activo solo si el recibo 
        actual no tiene ya uno.
        Si tiene uno, pregunta si desea eliminarlo antes (junto 
        con los vencimientos).
        """
        if self.objeto:
            if ((self.objeto.get_cliente() != None and
                 utils.dialogo(titulo = "¿ELIMINAR CLIENTE ACTUAL?", 
                               texto = "El recibo ya tiene cliente y vencimientos relacionados.\nSi cambia el cliente, se eliminará esta información.\n¿Desea continuar?", 
                               padre = self.wids['ventana'])) 
                 or (self.objeto.get_cliente() == None)):
                idcliente = self.buscar_cliente()
                if idcliente != None:
                    self.objeto.nombreLibrado = ""
                    self.objeto.direccionLibrado = ""
                    self.cliente = pclases.Cliente.get(idcliente)
                    self.actualizar_ventana()
    
    def buscar_cliente(self):
        """
        Busca un cliente y devuelve su ID o None.
        """
        idcliente = None
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR CLIENTE", texto = "Introduzca nombre o CIF del cliente:", padre = self.wids['ventana']) 
        if a_buscar != None:
            criterio = pclases.OR(pclases.Cliente.q.nombre.contains(a_buscar),
                                  pclases.Cliente.q.cif.contains(a_buscar))
            resultados = pclases.Cliente.select(criterio) 
            if resultados.count() > 1:
                ## Refinar los resultados
                idcliente = self.refinar_resultados_busqueda_cliente(resultados)
                if idcliente == None:
                    return None
                resultados = [pclases.Cliente.get(idcliente)]
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 
                                   'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)', 
                                   padre = self.wids['ventana'])
                return None
            ## Un único resultado
            idcliente = resultados[0].id
        return idcliente
    
    def refinar_resultados_busqueda_cliente(self, resultados):
        """
        Muestra en una ventana de resultados todos los
        registros de "resultados".
        Devuelve el id (primera columna de la ventana
        de resultados) de la fila seleccionada o None
        si se canceló.
        """
        filas_res = []
        for r in resultados:
            filas_res.append((r.id, r.nombre, r.cif))
        idcliente = utils.dialogo_resultado(filas_res,
                                            titulo = 'Seleccione Cliente',
                                            cabeceras = ('ID Interno', 'Nombre', 'CIF'), 
                                            padre = self.wids['ventana'])
        if idcliente < 0:
            return None
        else:
            return idcliente
    
    def buscar_factura(self, cliente, filtrar_pagadas = True):
        """
        Si filtrar_pagadas == True solo busca entre las facturas que tengan 
        algún pendiente de cobro.
        """
        fras = None
        numfra = utils.dialogo_entrada(titulo = "NÚMERO DE FACTURA", 
                                       texto = "Introduzca el número de factura", 
                                       padre = self.wids['ventana'])
        if numfra != None:
            fras = [((isinstance(f, pclases.FacturaVenta) and "FV:%d" % f.id) or \
                     (isinstance(f, pclases.Prefactura) and "PF:%d" % f.id) or "-1", 
                     f.numfactura, 
                     utils.str_fecha(f.fecha), 
                     "%s €" % (utils.float2str(f.importeTotal)), 
                     "%s €" % (utils.float2str(f.calcular_pendiente_cobro())), 
                     f) 
                     for f in cliente.facturasVenta + cliente.prefacturas if numfra.upper() in f.numfactura.upper()]
            if filtrar_pagadas:
                fras = [tupla for tupla in fras if tupla[-1].calcular_pendiente_cobro() > 0]
            if len(fras) > 1:
                idsfra = utils.dialogo_resultado([f[:-1] for f in fras],
                                                 titulo = "SELECCIONE FACTURA",
                                                 cabeceras = ('ID', 'Número de factura', 'Fecha', 'Importe total', 'Pendiente de cobro'),
                                                 padre = self.wids['ventana'], 
                                                 multi = True)
            elif len(fras) == 1:
                idsfra = [fras[0][0]]
            else:
                utils.dialogo_info(titulo = "FACTURA NO ENCONTRADA", 
                                   texto = "No se encontró ninguna factura.", 
                                   padre = self.wids['ventana'])
                idsfra = []
            fras = []
            if len(idsfra) > 0 and idsfra[0] != -1 and idsfra[0] != -2:
                for tipo, ide in [e.split(":") for e in idsfra]:
                    idfra = int(ide)
                    if tipo == "FV":
                        fras.append(pclases.FacturaVenta.get(idfra))
                    elif tipo == "PF":
                        fras.append(pclases.Prefactura.get(idfra))
        else:
            fras = None
        return fras
    
    def preparar_vencimientos(self, factura):
        """
        A partir de los vencimientos y pagos asociados a la 
        factura construye una lista de listas de la forma:
        [[vencimiento, vencimiento_estimado, pago],
         [vencimiento, vencimiento_estimado, pago],
         ...]
        Cualquiera de los tres objetos puede ser None en
        alguna fila donde no haya, por ejemplo, una estimación
        o un pago para un vencimiento.
        La lista se construye emparejando por proximidad de
        fechas entre los tres grupos (vto., vto. estimado y
        pago) y no se tiene en cuenta ningún otro criterio.
        """
        res = []
        vtos = [v for v in factura.vencimientosCobro]
        ests = [v for v in factura.estimacionesCobro]
        pags = factura.cobros
        mas_larga = [l for l in (vtos, ests, pags) if len(l)==max(len(vtos), len(ests), len(pags))][0]
        if len(mas_larga) == 0: return []
        for i in xrange(len(mas_larga)):  # @UnusedVariable
            res.append([None, None, None])
        def comp(v1, v2):
            if v1.fecha < v2.fecha: return -1
            if v1.fecha > v2.fecha: return 1
            return 0
        def distancia(v1, v2):
            return abs(v1.fecha - v2.fecha)
        def lugar(v):
            if isinstance(v, pclases.VencimientoCobro):
                return 0
            elif isinstance(v, pclases.EstimacionCobro):
                return 1
            else:
                return 2
        resto = [vtos, ests, pags]
        resto.remove(mas_larga)
        mas_larga.sort(comp)
        pos = 0
        for item in mas_larga:
            res [pos][lugar(item)] = item
            pos += 1
        for lista in resto:
            mlc = mas_larga[:]
            lista.sort(comp)
            while lista:
                item2 = lista.pop()
                mindist = distancia(item2, mlc[0])
                sol = mlc[0]
                for item1 in mlc:
                    if distancia(item1, item2) < mindist:
                        sol = item1
                        mindist = distancia(item1, item2)
                res[mas_larga.index(sol)][lugar(item2)] = item2 
                mlc.remove(sol)
        return res
    
    def buscar_vencimiento(self, factura):
        vtos_full = self.preparar_vencimientos(factura)
        if len(vtos_full) == 0:
            utils.dialogo_info(titulo = "FACTURA SIN VENCIMIENTOS", 
                               texto = "La factura %s no tiene vencimientos."
                                       "\nPara evitar incoherencias, todo co"
                                       "bro, pagaré o recibo bancario debe c"
                                       "orresponderse con un vencimiento.\nC"
                                       "ree los vencimientos antes de relaci"
                                       "onar la factura con un recibo." % (
                                            factura.numfactura), 
                               padre = self.wids['ventana'])
            return None
        vtos = [(v[0].id, 
                 utils.str_fecha(v[0].fecha), 
                 "%s €" % (utils.float2str(v[0].importe)), 
                 v[0].observaciones, 
                 v[2] != None and v[2].pagareCobroID != None 
                            and v[2].pagareCobro.codigo or "") 
                for v in vtos_full if v[0] != None #] #\
                # if v[2] == None] # El vencimiento no tiene cobro "asociado".
                                    and v[2] == None]
        if len(vtos) > 1:
            idvto = utils.dialogo_resultado(vtos,
                        titulo = "SELECCIONE VENCIMIENTO",
                        cabeceras = ('ID', 'Fecha', 'Importe', 
                                     'Observaciones', 'Cubierto en pagaré'),
                        padre = self.wids['ventana'])
        elif len(vtos) == 1:
            idvto = vtos[0][0]
        else:
            utils.dialogo_info(titulo = "FACTURA SIN VENCIMIENTOS", 
                               texto = "La factura no tiene vencimientos o ya han sido cubiertos en otro pagaré.", 
                               padre = self.wids['ventana'])
            idvto = -1
        if idvto > 0:
            vto = pclases.VencimientoCobro.get(idvto)
        else:
            vto = None
        return vto

    def set_factura(self, boton):
        """
        Busca un vencimiento de una factura y lo agrega al recibo actual.
        """
        recibo = self.objeto
        if self.cliente == None:
            idcliente = self.buscar_cliente()
            if idcliente == None:
                return
            self.cliente = pclases.Cliente.get(idcliente)
        cliente = self.cliente
        facturas = self.buscar_factura(cliente)
        if facturas == None:
            return
        if len(facturas) == 0:
            if utils.dialogo(titulo = "¿BUSCAR EN FACTURAS PAGADAS?", 
                             texto = "No se han encontrado facturas pendient"
                                     "es de cobro que satisfagan el criterio"
                                     " de búsqueda.\n¿Desea volver a buscar "
                                     "incluyendo facturas pagadas?", 
                             padre = self.wids['ventana']):
                facturas = self.buscar_factura(cliente, filtrar_pagadas = False)
        for factura in facturas:
            vencimiento = self.buscar_vencimiento(factura)
            if vencimiento == None:
                continue
            recibo.fechaVencimiento = vencimiento.fecha
            recibo.fechaLibramiento = factura.fecha
            observaciones = "Recibo bancario número %d con fecha de emisión %s." % (self.objeto.numrecibo, utils.str_fecha(self.objeto.fechaLibramiento))
            vencimiento.observaciones += observaciones
            vencimiento.recibo = recibo
            self.actualizar_ventana()

    def inicializar_ventana(self):
        """
        Inicialización de controles de la ventana.
        """
        self.wids['frame_observaciones'].set_property("visible", False)
        try:
            dde = pclases.DatosDeLaEmpresa.select()[0]
            if "Bogado" in dde.nombre:
                self.wids['frame_observaciones'].set_property("visible", True)
        except:
            pass
        self.activar_widgets(False)
        utils.rellenar_lista(self.wids['cbe_cuenta_origen'], 
                             [(c.id, "%s%s" % (c.ccc, c.nombre and " (%s)" % c.nombre or "")) for c in pclases.CuentaOrigen.select(orderBy = "nombre")])
        utils.rellenar_lista(self.wids['cbe_cuenta_bancaria_cliente'], 
                                [(c.id, "%s%s%s%s (%s)" % (
                                    c.cuenta, 
                                    c.iban and " | IBAN: " + c.iban or "", 
                                    c.swif and " | SWIF: " + c.swif or "", 
                                    c.banco and " (%s)" % c.banco or "", 
                                    c.cliente and c.cliente.nombre 
                                        or "SIN CLIENTE")) 
                                 for c in pclases.CuentaBancariaCliente.select(orderBy = "id")])
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
    
    def mostrar_info_cliente(self):
        """
        Introduce el código del cliente y la información relativa en los 
        widgets.
        Si el nombre y domicilio del librado están en blanco, escribe también 
        ahí los datos del cliente.
        """
        if self.cliente == None:
            self.wids['e_codcliente'].set_text("")
            utils.rellenar_lista(self.wids['cbe_cuenta_bancaria_cliente'], 
                [(c.id, "%s%s%s%s" % (c.cuenta, 
                                      c.iban and " | IBAN: " + c.iban or "", 
                                      c.swif and " | SWIF: " + c.swif or "", 
                                      c.banco and " (%s)" % c.banco or "")) 
                 for c in pclases.CuentaBancariaCliente.select(orderBy = "id")])
        else:
            self.wids['e_codcliente'].set_text(`self.cliente.id`)
            cuentas_cliente = pclases.CuentaBancariaCliente.select(
                    pclases.CuentaBancariaCliente.q.clienteID==self.cliente.id,
                    orderBy = "id")
            utils.rellenar_lista(self.wids['cbe_cuenta_bancaria_cliente'], 
                [(c.id, "%s%s%s%s" % (c.cuenta, 
                                      c.iban and " | IBAN: " + c.iban or "", 
                                      c.swif and " | SWIF: " + c.swif or "", 
                                      c.banco and " (%s)" % c.banco or "")) 
                 for c in cuentas_cliente])
            if cuentas_cliente.count():
                utils.combo_set_from_db(
                    self.wids['cbe_cuenta_bancaria_cliente'], 
                    cuentas_cliente[-1].id)
                self.objeto.cuentaBancariaCliente = cuentas_cliente[-1]
                self.objeto.syncUpdate()
            if self.objeto.nombreLibrado == "":
                self.objeto.nombreLibrado = self.cliente.nombre
            if self.objeto.direccionLibrado == "":
                self.objeto.direccionLibrado = ", ".join(
                                                    (self.cliente.direccion, 
                                                     self.cliente.cp, 
                                                     self.cliente.ciudad))

    def mostrar_info_facturas(self):
        """
        Muestra los números de factura y fecha de factura del último
        vencimiento de todos los relacionados con el recibo.
        """
        txtfacturas = ", ".join([v.get_factura_o_prefactura().numfactura 
                                 for v in self.objeto.vencimientosCobro])
        try:
            fechasfras = [v.get_factura_o_prefactura().fecha 
                          for v in self.objeto.vencimientosCobro]
            def distintitems(l):
                aux = []
                for i in l: 
                    if i not in aux: aux.append(i)
                return aux
            fechasfras = distintitems(fechasfras)
            txtfechafra = ", ".join([utils.str_fecha(f) for f in fechasfras])
        except (IndexError, ValueError):
            txtfechafra = ""
        self.wids['e_numfactura'].set_text(txtfacturas)
        self.wids['e_fecha_factura'].set_text(txtfechafra)

    def rellenar_widgets(self):
        """
        Introduce la información del recibo actual
        en los widgets.
        """
        recibo = self.objeto
        if recibo.get_cliente() != None:
            self.cliente = recibo.get_cliente()
        self.mostrar_info_cliente()
        self.mostrar_info_facturas()
        txtimporte = numerals(recibo.importe).upper()
        self.wids['txt_importe'].get_buffer().set_text(txtimporte)
        self.wids['e_importe'].set_text(
            "%s €" % (utils.float2str(recibo.importe)))
        if recibo != None:
            for nombre_col in self.dic_campos:
                self.escribir_valor(recibo._SO_columnDict[nombre_col], 
                                    getattr(recibo, nombre_col), 
                                    self.dic_campos[nombre_col])
            self.objeto.make_swap()
        else:
            self.activar_widgets(False)
    
    def es_diferente(self):
        """
        Devuelve True si algún valor en ventana difiere de 
        los del objeto.
        """
        if self.objeto == None:
            igual = True
        else:
            igual = self.objeto != None
            for colname in self.dic_campos:
                col = self.clase._SO_columnDict[colname]
                try:
                    valor_ventana = self.leer_valor(col, 
                                                    self.dic_campos[colname])
                except (ValueError, mx.DateTime.RangeError, TypeError):
                    igual = False
                valor_objeto = getattr(self.objeto, col.name)
                if isinstance(col, pclases.SODateCol):
                    valor_objeto = utils.abs_mxfecha(valor_objeto)
                igual = igual and (valor_ventana == valor_objeto)
                if not igual:
                    break
        return not igual

    def verificar_numrecibo_unico(self):
        """
        Comprueba que el número de recibo no existe en el año 
        de la ventana (a no ser que sea el propio recibo en pantalla).
        """
        r = self.objeto
        numrecibo = self.wids['e_numrecibo'].get_text()
        anno = self.wids['sp_anno'].get_value()
        try:
            numrecibo = int(numrecibo)
            anno = int(anno)
        except ValueError:
            self.logger.error("%srecibos::verificar_numrecibo_unico -> Error convirtiendo año o número de recibo a entero." % (self.usuario and self.usuario.usuario + ": " or ""))
            res = False
        else:
            cons_recibos = pclases.Recibo.select(pclases.AND(
                                    pclases.Recibo.q.anno == anno, 
                                    pclases.Recibo.q.numrecibo == numrecibo))
            recibos = cons_recibos.count()
            if r.numrecibo == numrecibo and r.anno == anno:
                res = recibos == 1
            else:
                res = recibos == 0
        return res

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        if not self.verificar_numrecibo_unico():
            utils.dialogo_info(titulo = "RECIBO DUPLICADO", 
                    texto = "El número de recibo %s ya existe en el año %d." % (
                                self.wids['e_numrecibo'].get_text(), 
                                self.wids['sp_anno'].get_value()), 
                    padre = self.wids['ventana'])
        else:
            # Desactivo el notificador momentáneamente
            self.objeto.notificador.activar(lambda: None)
            # Actualizo los datos del objeto
            for colname in self.dic_campos:
                col = self.clase._SO_columnDict[colname]
                try:
                    valor_ventana = self.leer_valor(col, 
                                                    self.dic_campos[colname])
                    setattr(self.objeto, colname, valor_ventana)
                except (ValueError, mx.DateTime.RangeError, TypeError):
                    pass    # TODO: Avisar al usuario o algo. El problema es que no hay una forma "limpia" de obtener el valor que ha fallado.
            # Fuerzo la actualización de la BD y no espero a que SQLObject lo haga por mí:
            self.objeto.syncUpdate()
            self.objeto.sync()
            # Vuelvo a activar el notificador
            self.objeto.notificador.activar(self.aviso_actualizacion)
            self.actualizar_ventana()
            self.wids['b_guardar'].set_sensitive(False)

    def nuevo(self, boton):
        """
        Crea un nuevo recibo en blanco.
        """
        try:
            dde = pclases.DatosDeLaEmpresa.select()[0]
            lugarLibramiento = dde.ciudad
        except:
            txt = "No hay empresa dada de alta en datos_de_la_empresa."
            self.logger.error(txt)
            print txt
            lugarLibramiento = ""
        try:
            cuentaOrigen = pclases.CuentaOrigen.select()[0]
        except IndexError:
            cuentaOrigen = None
        anno = mx.DateTime.localtime().year
        numrecibo = pclases.Recibo.get_next_numrecibo(anno)
        try:
            recibo = pclases.Recibo(numrecibo = numrecibo, 
                                    anno = anno, 
                                    fechaLibramiento = mx.DateTime.localtime(), 
                                    fechaVencimiento = mx.DateTime.localtime(), 
                                    lugarLibramiento = lugarLibramiento, 
                                    cuentaOrigen = cuentaOrigen, 
                                    nombreLibrado = "", 
                                    direccionLibrado = "")
            pclases.Auditoria.nuevo(recibo, self.usuario, __file__)
            # CWT:
            self.cliente = None
        except Exception, msg:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = "Ocurrió un error al crear el nuevo recibo.\nVuelva a intentarlo y reinice la aplicación si fuera necesario.", 
                               padre = self.wids['ventana'])
            self.logger.error("%srecibos::nuevo -> Error al crear nuevo recibo. Mensaje de la excepción: %s" % (self.usuario and self.usuario.usuario or "", msg))
        else:
            self.objeto = recibo
            self.actualizar_ventana()

    def imprimir(self, boton):
        """
        Genera y muestra el PDF del recibo bancario.
        """
        from formularios import reports
        numrecibo = self.wids['e_numrecibo'].get_text()
        lugar_libramiento = self.wids['e_lugar_libramiento'].get_text()
        importe = self.wids['e_importe'].get_text()
        fecha_libramiento = self.wids['e_fecha_libramiento'].get_text()
        vencimiento = self.wids['e_fecha_vencimiento'].get_text()
        codigo_cliente = self.wids['e_codcliente'].get_text()
        numfactura = self.wids['e_numfactura'].get_text()
        fechafactura = self.wids['e_fecha_factura'].get_text()
        persona_pago = self.wids['e_persona_pago'].get_text()
        domicilio_pago = self.wids['e_domicilio_pago'].get_text()
        # cuenta_pago = self.wids['cbe_cuenta_origen'].child.get_text()
        cuenta_pago = self.wids['cbe_cuenta_bancaria_cliente'].child.get_text()
        nombre_librado = self.wids['e_nombre_librado'].get_text()
        direccion_librado = self.wids['e_direccion_librado'].get_text()
        pdf = geninformes.recibo(numrecibo, 
                                 lugar_libramiento, 
                                 importe, 
                                 fecha_libramiento, 
                                 vencimiento, 
                                 codigo_cliente, 
                                 numfactura, 
                                 fechafactura, 
                                 persona_pago, 
                                 domicilio_pago, 
                                 cuenta_pago, 
                                 nombre_librado, 
                                 direccion_librado)        
        reports.abrir_pdf(pdf)

    def activar_widgets(self, s, chequear_permisos = True):
        if self.objeto == None:
            s = False
        ws = tuple(["b_borrar", "b_cliente", "b_factura", "b_drop_factura"] + [self.dic_campos[k] for k in self.dic_campos.keys()])
        for w in ws:
            try:
                self.wids[w].set_sensitive(s)
            except Exception, msg:
                print "Widget problemático:", w, "Excepción:", msg
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "recibos.py")


if __name__ == '__main__':
    v = Recibos()

