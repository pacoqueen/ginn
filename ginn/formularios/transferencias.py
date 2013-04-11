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
## transferencias.py -- Hacer, editar o borrar transferencias
###################################################################
## NOTAS:
##  La clase base es Pagos, pero sólo tiene en cuenta aquellos
##  que sean transferencia.
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 22 de febrero de 2007 -> Inicio
## 
###################################################################


import sys, os
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, mx, mx.DateTime
try:
    from framework import pclases
    from seeker import VentanaGenerica 
except ImportError:
    sys.path.append(os.path.join('..', 'framework'))
    from framework import pclases
    from seeker import VentanaGenerica 
from utils import _float as float


class Transferencias(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.clase = pclases.Pago
        self.dic_campos = {"importe": "e_importe", 
                           "proveedorID": "cbe_proveedor", 
                           "cuentaOrigenID": "cbe_origen", 
                           "cuentaDestinoID": "cbe_destino", 
                           "fecha": "e_fecha", 
                           "conceptoLibre": "e_concepto", 
                          }
        Ventana.__init__(self, 'transferencias.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar, 
                       'b_fecha/clicked': self.set_fecha, 
                       'b_factura/clicked': self.set_factura, 
                       'b_imprimir/clicked': self.imprimir, 
                       'b_nuevo_destino/clicked': self.crear_nueva_cuenta_destino
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def imprimir(self, boton):
        """
        Imprime un fax con la información de la transferencia.
        Solicita un firmante al usuario. El resto de los datos 
        se obtienen de la BD.
        """
        sys.path.append(os.path.join("..", "informes"))
        from geninformes import fax_transferencia
        from informes import abrir_pdf
        firmantes = {1: "Otro (texto libre)", 
                     2: "D. Enrique Román Corzo", 
                     3: "D. Enrique Figueroa Yáñez", 
                     4: "D. Enrique Mozo del Río", 
                     5: "D. Fernando Guijarro Lozano"}    # TODO: HARCODED
        claves = firmantes.keys()
        claves.sort()
        firmado = utils.dialogo_combo(titulo = "FIRMANTE", 
                                      texto = 'Seleccione un firmante o elija "otro" y pulse\n«Aceptar» para escribir uno distinto:', 
                                      ops = ([(k, firmantes[k]) for k in claves]), 
                                      padre = self.wids['ventana'])
        if firmado == 1:
            firmado = utils.dialogo_entrada(titulo = "FIRMANTE", 
                                            texto = "Introduzca el nombre que aparecerá en la firma:", 
                                            padre = self.wids['ventana'])
        elif firmado != None:
            firmado = firmantes[firmado]
        if firmado != None:
            try:
                e = pclases.DatosDeLaEmpresa.select()[0]
                t = self.objeto
                o = t.cuentaOrigen
                d = t.cuentaDestino
                p = t.proveedor
                empresa = o.banco
                contacto = o.contacto
                fax = o.fax
                telefono = o.telefono
                de = e.nombreContacto 
                asunto = "Transferencia"
                fecha = utils.str_fecha(t.fecha)
                beneficiario = p.nombre
                banco = d.banco
                #if p.es_extranjero():
                #    cuenta = "%s %s" % (d.iban, d.swif)
                #else:
                #    cuenta = d.cuenta
                cuenta = d.cuenta
                porcuenta = e.nombre
                ccc = o.ccc
                concepto = t.concepto
                importe = "%s €" % (utils.float2str(t.importe))
                swift = d.swif
                iban = d.iban
                observaciones = d.observaciones
                conceptoLibre = t.conceptoLibre
            except AttributeError, msg:
                utils.dialogo_info(titulo = "ERROR AL GENERAR FAX", texto = "No se encontraron algunos datos.\n\nVerifique la información y vuelva a intentarlo.", padre = self.wids['ventana'])
                self.logger.error("transferencias.py::imprimir -> AttributeError: %s" % msg)
            except IndexError, msg:
                utils.dialogo_info(titulo = "ERROR AL RECUPERAR DATOS DE LA EMPRESA", texto = "No se encontraron los datos de la empresa.\n\nCompruebe que existe una empresa en la tabla «datos_de_la_empresa».\n\n\n(Contacte con el administrador en caso de duda.)", padre = self.wids['ventana'])
                self.logger.error("transferencias.py::imprimir -> IndexError: %s" % msg)
            else:
                abrir_pdf(fax_transferencia(empresa, 
                                            contacto, 
                                            fax, 
                                            telefono, 
                                            de, 
                                            asunto, 
                                            fecha, 
                                            beneficiario, 
                                            banco, 
                                            cuenta, 
                                            porcuenta, 
                                            ccc, 
                                            concepto, 
                                            importe, 
                                            firmado, 
                                            swift, 
                                            iban, 
                                            observaciones, 
                                            conceptoLibre))
    
    def ir_a_primero(self):
        """
        Sobeescribe el método de seeker.
        Va a la última transferencia de la BD.
        """
        anterior = self.objeto
        objeto = None
        ts = pclases.Pago.select(orderBy = "-id")
        for t in ts:
            if t.es_transferencia():
                objeto = t
                break
        if objeto != None:
            if self.objeto != None:
                self.objeto.notificador.desactivar()
            self.objeto = objeto
            self.objeto.notificador.activar(self.aviso_actualizacion)
        self.actualizar_ventana(objeto_anterior = anterior)
        self.activar_widgets(False)     # Por defecto lo inhabilito, no sea que se confunda y lo machaque con una transferencia nueva.

    def crear_nueva_cuenta_destino(self, boton):
        """
        Crea una nueva cuenta destino a través de la ventana de cuentas destino 
        y la introduce en el ComboBoxEntry.
        """
        if self.objeto != None:
            import cuentas_destino
            nueva_cuenta_destino = pclases.CuentaDestino(proveedor = self.objeto.proveedor, 
                                                         nombre = "Nueva cuenta de %s" % (self.objeto.proveedor and self.objeto.proveedor.nombre or "?"))
            pclases.Auditoria.nuevo(nueva_cuenta_destino, self.usuario, 
                                    __file__)
            utils.dialogo_info(titulo = "NUEVA CUENTA CREADA", 
                               texto = """
                A continuación complete la información de la nueva cuenta del proveedor                 
                y cierre la ventana que aparecerá.                                                      
                Después podrá seleccionarla en la ventana de transferencias.                            
                               """, 
                               padre = self.wids['ventana'])
            v = cuentas_destino.CuentasDestino(objeto = nueva_cuenta_destino, usuario = self.usuario)
            self.actualizar_ventana()

    def set_factura(self, boton):
        """
        Busca una factura de compra de la BD y la 
        guarda en el objeto activo antes de recargar 
        la ventana.
        """
        factura = self.buscar_factura()     # Si lo que va a pagar es un LOGIC, que lo haga desde la ventana de vencimientos_pendientes.
        if factura != None:
            self.objeto.importe = factura.get_importe_primer_vencimiento_pendiente()
            self.objeto.facturaCompra = factura
            self.objeto.proveedor = factura.proveedor
            self.actualizar_ventana()

    def set_fecha(self, boton):
        """
        Introduce la fecha seleccionada de un diálogo calendario en el entry.
        """
        self.wids['e_fecha'].set_text(utils.str_fecha(utils.mostrar_calendario(fecha_defecto = self.objeto and self.objeto.fecha or None, padre = self.wids['ventana'])))

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
                    valor_ventana = self.leer_valor(col, self.dic_campos[colname])
                except (ValueError, mx.DateTime.RangeError, TypeError):
                    igual = False
                valor_objeto = getattr(self.objeto, col.name)
                if isinstance(col, pclases.SODateCol):
                    valor_objeto = utils.abs_mxfecha(valor_objeto)
                igual = igual and (valor_ventana == valor_objeto)
                if not igual:
                    break
        return not igual
    
    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        # Inicialización del resto de widgets:
        utils.rellenar_lista(self.wids['cbe_proveedor'], [(p.id, p.nombre) for p in pclases.Proveedor.select(orderBy = "nombre")])
        utils.rellenar_lista(self.wids['cbe_origen'], [(p.id, p.nombre) for p in pclases.CuentaOrigen.select(orderBy = "nombre")])
        utils.rellenar_lista(self.wids['cbe_destino'], [(p.id, p.nombre + " " + p.cuenta) for p in pclases.CuentaDestino.select(orderBy = "nombre")])

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        ws = tuple(["b_factura", "b_fecha", "b_nuevo_destino", "b_borrar", "e_factura"] + [self.dic_campos[k] for k in self.dic_campos.keys()])
        for w in ws:
            try:
                self.wids[w].set_sensitive(s)
            except:
                print w

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
            if r.es_transferencia():
                filas_res.append((r.id, 
                                  utils.str_fecha(r.fecha), 
                                  r.proveedor and r.proveedor.nombre or "-", 
                                  r.cuentaOrigen and r.cuentaOrigen.nombre or "-", 
                                  r.cuentaDestino and r.cuentaDestino.nombre or "-", 
                                  utils.float2str(r.importe)))
        idcuenta = utils.dialogo_resultado(filas_res,
                                           titulo = 'SELECCIONE TRANSFERENCIA',
                                           cabeceras = ('ID', 'Fecha', 'Proveedor', 'Cuenta', 'Destino', "Importe"), 
                                           padre = self.wids['ventana'])
        if idcuenta < 0:
            return None
        else:
            return idcuenta

    def rellenar_widgets(self):
        """
        Introduce la información del cuenta actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        if self.objeto.facturaCompra and self.objeto.facturaCompra.proveedor != self.objeto.proveedor: # Cuando hay que recurrir a estas cosas, es que el diseño no es bueno.
            self.objeto.facturaCompra = None
        if self.objeto.proveedorID != None:     # Meto en las cuentas sólo las del proveedor de la transferencia.
            utils.rellenar_lista(self.wids['cbe_destino'], 
                                 [(p.id, p.nombre + " " + p.cuenta) for p in pclases.CuentaDestino.select(pclases.CuentaDestino.q.proveedorID == self.objeto.proveedor.id, orderBy = "nombre")])
        else:
            utils.rellenar_lista(self.wids['cbe_destino'], [(p.id, p.nombre + " " + p.cuenta) for p in pclases.CuentaDestino.select(orderBy = "nombre")])
        for nombre_col in self.dic_campos:
            self.escribir_valor(self.objeto._SO_columnDict[nombre_col], getattr(self.objeto, nombre_col), self.dic_campos[nombre_col])
        self.wids['e_factura'].set_text(self.objeto.concepto)
        self.objeto.make_swap()

    def buscar_factura(self):
        """
        Ventana de búsqueda de facturas de compra
        """
        res = None
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR FACTURA",  
                                         texto = "Introduzca número de factura a buscar:", 
                                         padre = self.wids['ventana'])
        if a_buscar != None:
            facturas = pclases.FacturaCompra.select(pclases.FacturaCompra.q.numfactura.contains(a_buscar))
            if facturas.count() >= 1:
                id = utils.dialogo_resultado(filas = [(f.id, f.numfactura, f.proveedor and f.proveedor.nombre or "") for f in facturas], 
                                             titulo = "SELECCIONE FACTURA", 
                                             padre = self.wids['ventana'], 
                                             cabeceras = ("ID", "Número de factura", "Proveedor"))
                if id > 0:
                    res = pclases.FacturaCompra.get(id)
            else:
                utils.dialogo_info(titulo = "SIN RESULTADOS", 
                                   texto = "La búsqueda del texto %s no produjo resultados." % (a_buscar), 
                                   padre = self.wids['ventana'])
        return res

    def nuevo(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        anterior = self.objeto
        if anterior != None:
            anterior.notificador.desactivar()
        factura = self.buscar_factura()     # Si lo que va a pagar es un LOGIC, que lo haga desde la ventana de vencimientos_pendientes.
        if factura != None:
            importe = factura.get_importe_primer_vencimiento_pendiente()    # Devuelve 0 si no quedan.
            try:
                nuevo = pclases.Pago(cuentaOrigen = pclases.CuentaOrigen.select(orderBy = "-id")[0], 
                                     fecha = mx.DateTime.localtime(), 
                                     facturaCompra = factura, 
                                     proveedor = factura.proveedor, 
                                     importe = importe)
                pclases.Auditoria.nuevo(nuevo, self.usuario, __file__)
            except IndexError:
                utils.dialogo_info(titulo = "ERROR CREANDO TRANSFERENCIA", 
                                   texto = "Se produjo un error al crear una nueva transferencia.\nProbablemente no existan cuentas en la aplicación desde donde realizar transferencias.", 
                                   padre = self.wids['ventana'])
            else:
                utils.dialogo_info('NUEVA TRANSFERENCIA CREADA', 
                                   'Se ha creado una transferencia nueva.\nA continuación complete la información de la misma y guarde los cambios.', 
                                   padre = self.wids['ventana'])
            self.objeto = nuevo
            self.objeto.notificador.activar(self.aviso_actualizacion)
            self.activar_widgets(True)
            self.actualizar_ventana(objeto_anterior = anterior)
    
    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        transferencia = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR TRANSFERENCIA", 
                                         texto = "Introduzca identificador, importe o pulse «Aceptar» para verlas todas:", 
                                         padre = self.wids['ventana']) 
        if a_buscar != None:
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            try:
                a_buscar = float(a_buscar)
            except ValueError:
                if ida_buscar != -1:
                    criterio = pclases.Pago.q.id == ida_buscar
                else:
                    criterio = None
            else:
                criterio = pclases.OR(pclases.Pago.q.importe == a_buscar,
                                      pclases.Pago.q.id == ida_buscar)
            resultados = pclases.Pago.select(criterio)
            resultados = [r for r in resultados if r.es_transferencia()]
            if len(resultados) > 1:
                    ## Refinar los resultados
                    idtransferencia = self.refinar_resultados_busqueda(resultados)
                    if idtransferencia == None:
                        return
                    resultados = [pclases.Pago.get(idtransferencia)]
            elif len(resultados) < 1:
                    ## Sin resultados de búsqueda
                    utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)',
                                       padre = self.wids['ventana'])
                    return
            ## Un único resultado
            # Primero anulo la función de actualización
            if transferencia != None:
                transferencia.notificador.desactivar()
            # Pongo el objeto como actual
            try:
                transferencia = resultados[0]
            except IndexError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Se produjo un error al recuperar la información.\nCierre y vuelva a abrir la ventana antes de volver a intentarlo.", 
                                   padre = self.wids['texto'])
                return
            # Y activo la función de notificación:
            transferencia.notificador.activar(self.aviso_actualizacion)
            self.activar_widgets(True)
        self.objeto = transferencia
        self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        # Desactivo el notificador momentáneamente
        self.objeto.notificador.activar(lambda: None)
        # Actualizo los datos del objeto
        for colname in self.dic_campos:
            col = self.clase._SO_columnDict[colname]
            try:
                valor_ventana = self.leer_valor(col, self.dic_campos[colname])
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

    def borrar(self, widget):
        """
        Elimina el pago de la tabla pero NO
        intenta eliminar ninguna de sus relaciones,
        de forma que si se incumple alguna 
        restricción de la BD, cancelará la eliminación
        y avisará al usuario.
        """
        transferencia = self.objeto
        if not utils.dialogo('¿Eliminar la transferencia?', 'BORRAR', padre = self.wids['ventana']):
            return
        else:
            transferencia.notificador.desactivar()
            try:
                transferencia.destroy(ventana = __file__)
            except Exception, e:
                self.logger.error("transferencias::borrar -> Pago ID %d no se pudo eliminar. Excepción: %s." % (transferencia.id, e))
                utils.dialogo_info(titulo = "TRANSFERENCIA NO BORRADA", 
                                   texto = "La transferencia no se pudo eliminar.\n\nSe generó un informe de error en el «log» de la aplicación.",
                                   padre = self.wids['ventana'])
                self.actualizar_ventana()
                return
            self.objeto = None
            self.ir_a_primero()

if __name__ == "__main__":
    #p = Transferencias()
    p = Transferencias(usuario = pclases.Usuario.selectBy(usuario = "admin")[0])

