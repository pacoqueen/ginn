#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import * 

class FacturaVenta(SQLObject, PRPCTOO, SuperFacturaVenta):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- clienteID = ForeignKey('Cliente')
    servicios = MultipleJoin('Servicio')
    lineasDeVenta = MultipleJoin('LineaDeVenta')
    vencimientosCobro = MultipleJoin('VencimientoCobro')
    cobros = MultipleJoin('Cobro')
    estimacionesCobro = MultipleJoin('EstimacionCobro')
    pagosDeAbono = MultipleJoin('PagoDeAbono')
    comisiones = MultipleJoin('Comision')
    documentos = MultipleJoin('Documento')
    #------------------------------- obraID = ForeignKey('Obra', default = None)
    notas = MultipleJoin("Nota")
    alarmas = MultipleJoin("Alarma")
    tareas = MultipleJoin("Tarea")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        res = "%s - %s; %s" % (self.numfactura, 
                self.cliente and self.cliente.nombre or "", 
                utils.str_fecha(self.fecha))
        return res

    def old_get_str_estado(self):
        """
        Devuelve el estado de la factura como cadena: 
        Vacía: No tiene líneas de venta ni servicios.
        Sin vencimientos: No tiene vencimientos creados.
        No vencida: Si alguna fecha de vencimiento < actual.
        Vencida: Si todas las fechas de vencimiento >= actual.
        Cobrada: Si cobros == importe total.
        """
        ESTADOS = ("Vacía", "Sin vencimientos", "No vencida", "Vencida", 
                   "Cobrada")
        if len(self.lineasDeVenta) + len(self.servicios) == 0:
            return ESTADOS[0]
        if len(self.vencimientosCobro) == 0:
            return ESTADOS[1]
        ultima_fecha_vto = self.vencimientosCobro[0].fecha
        for v in self.vencimientosCobro:
            if v.fecha > ultima_fecha_vto:
                ultima_fecha_vto = v.fecha
        vencido = sum([v.importe for v in self.vencimientosCobro])
        cobrado = sum([c.importe for c in self.cobros
                    if c.pagareCobro == None or not c.pagareCobro.pendiente])
        if cobrado and cobrado >= vencido:
            return ESTADOS[4]
        else:
            if ultima_fecha_vto < mx.DateTime.today():
                return ESTADOS[3]
            else:
                return ESTADOS[2]

    def get_contador(self):
        """
        Devuelve el contador de la factura aunque el cliente ya haya 
        cambiado de contador (por cierre de año, por ejemplo).
        Si no se puede determinar, devuelve None.
        """
        res = None
        numfactura = self.numfactura
        contadores = Contador.select()
        for c in contadores:
            if (numfactura.startswith(c.prefijo) 
               and numfactura.endswith(c.sufijo)):
                tmpnumfactura = numfactura.replace(c.prefijo, "", 1)
                tmpnumfactura=tmpnumfactura[::-1].replace(c.sufijo[::-1], "", 1)
                # Para que solo sustituya el sufijo del final. Útil si el 
                # sufijo es numérico (por ejemplo, un año) y se encuentra por 
                # casualidad también en el propio número.
                if tmpnumfactura.isdigit():
                    res = c
                    break
        return res

    def get_numero_numfactura_contador(self):
        """
        Devuelve el número de la factura como entero sin tener en cuenta 
        el contador del cliente. En lugar de eso, determina el contador de 
        la factura mediante el método «get_contador».
        Si el contador no se puede determinar, intentará usar el del cliente 
        mediante el método «get_numero_numfactura».
        """
        contador = self.get_contador()
        numero = self.numfactura.replace(contador.prefijo, "", 1)
        numero = numero[::-1].replace(contador.prefijo[::-1], "", 1)[::-1]
        try:
            res = int(numero)
        except (ValueError, TypeError):
            res = self.get_numero_numfactura()
        return res

    def get_numero_numfactura(self):
        """
        Devuelve el número de factura sin prefijo ni 
        sufijo y como entero.
        Salta una excepción si no se pudo determinar
        la parte numérica del número de factura.
        """
        ## import re
        ## expresion = re.compile('[0-9]+')
        ## numero = expresion.findall(self.numfactura)
        # NOTA: Esto de arriba está bien, pero no vale cuando tiene prefijos y sufijos numéricos.
        try:
            prefijo = self.cliente.contador.prefijo     # DEBE tener cliente y contador. Es precondición al crear una fra.
            sufijo = self.cliente.contador.sufijo
            # TODO: OJO: Hay un problema. Si se le ha cambiado el contador 
            #            al cliente... la cagaste Burt Lancaster.
        except AttributeError:
            self.cliente.sync()
            try:
                prefijo = self.cliente.contador.prefijo     # DEBE tener cliente y contador. Es precondición al crear una fra.
                sufijo = self.cliente.contador.sufijo
            except Exception, msg:
                txt = "pclases::get_numero_numfactura -> Excepción: %s" % (msg)
                print txt
                prefijo = sufijo = ""
        numero = self.numfactura.replace(prefijo, '')
        numero = numero.replace(sufijo, '')
        # print self.cliente.contador.prefijo, self.cliente.contador.sufijo, numero
        # return int(numero)   # Prefiero que salte la excepción si no se encuentra el número.
        # Ok. El cliente no está, así que voy a intentar primero sacar el número de la factura errónea 
        # (es errónea porque no coincide con el formato del contador de su cliente) y si no puedo, la
        # ignoro.
        try:
            numero = int(numero)
        except ValueError:
            expr_entero = re.compile('[0-9]+')
            try:
                numero = int(expr_entero.findall(numero)[-1])
            except ValueError:
                numero = 0  # Esto NO debería ocurrir.
            except IndexError:
                numero = 0  # Algo hay que hacer. Y se tiene que devolver un 
                            # número sí o sí, así que...
                            # Como supongo que esto no se usa más que para 
                            # ordenar facturas por número, las facturas 
                            # inválidas (número no encaja en contador) no 
                            # influirán en la actualización del contador.
        return numero

    def calcular_total_irpf(self, subtotal = None, tot_dto = None, cargo = None, abonos = None):
        """
        Calcula el importe total de retención de IRPF (se resta al total)
        de la factura. Se devuelve en positivo (aunque en realidad sea una 
        cantidad negativa a sumar al total).
        """
        if self.irpf != 0:
            if subtotal == None:
                subtotal = self.calcular_subtotal()
            if tot_dto == None: 
                tot_dto = self.calcular_total_descuento(subtotal)
            if cargo == None:
                cargo = self.cargo
            if abonos == None:
                abonos = sum([pa.importe for pa in self.pagosDeAbono])
            total_irpf = utils.ffloat(subtotal + tot_dto + self.cargo + abonos) * self.irpf
        else:
            total_irpf = 0.0
        return total_irpf

    def enviar_por_correoe_a_comercial_relacionado(self, asunto = None):
        """
        Envia un correo electrónico al (o a los) comercial relacionado con la 
        factura con dos PDF adjuntos: una factura con la marca de agua "copia" 
        y el histórico del CRM.
        También crea una tarea automática para identificar que ya se ha 
        enviado la factura.
        Si no tiene comercial relacionado, envia el correo electrónico a todos 
        los usuarios con permisos sobre la ventana de crm de seguimiento de 
        impagos.
        """
        # No estoy muy seguro de que esta sea el sitio indicado para meter 
        # esta rutina.
        from informes.geninformes import crm_generar_pdf_detalles_factura
        from formularios.albaranes_de_salida import imprimir_factura as generar_factura
        copiafra = generar_factura(self, abrir = False, es_copia = True)
        historial = crm_generar_pdf_detalles_factura(self) 
        comerciales = self.get_comerciales()
        destinatarios = [c.correoe.strip() for c in comerciales 
                         if c.correoe and c.correoe.strip()]
        if not destinatarios:
            # OJO: Ventana HARDCODED.
            try:
                ventana = Ventana.selectBy(
                    fichero = "crm_seguimiento_impagos.py")[0]
            except IndexError:
                pass    # La ventana no existe por lo que sea. 
                        # Weird, but... pasando.
            else:
                for permiso in ventana.permisos:
                    u = permiso.usuario
                    if u.email and u.email.strip():
                        destinatarios.append(u.email.strip())
        if DEBUG:
            destinatarios.append("rodriguez.bogado@gmail.com")
            destinatarios.append("frbogado@novaweb.es")
        if destinatarios:
            # TODO: FIXME: Datos de correo HARCODED e incorrectos, para colmo.
            remitente = ("comercialgeotexan@gea21.es", 
                         "comercialgeotexan@gea21.es", "comgeo98")
            if asunto is None:
                asunto = "Factura %s" % self.numfactura
            texto = "Se adjunta copia de la factura en PDF e historial de "\
                    "la misma."
            servidor = "gea21.es"
            ok = utils.enviar_correoe(remitente[0],  
                    destinatarios, 
                    asunto, 
                    texto, 
                    [copiafra, historial], 
                    servidor, 
                    remitente[1], 
                    remitente[2])
            if ok:
                t = Tarea(facturaVenta = self,  # @UnusedVariable
                          categoria = 
                            Categoria.get_categoria_tareas_automaticas(), 
                          texto = "Factura emitida hace más de 45 días."
                                  "No se ha recibido documento de cobro."
                                  "Enviar correo a comercial.", 
                          pendiente = False, 
                          fecha = mx.DateTime.today(), 
                          observaciones = "Tarea creada automáticamente.", 
                          fechadone = mx.DateTime.today())

    def calcular_subtotal(self, incluir_descuento = False, precision = None):
        """
        Devuelve el subtotal de la factura: líneas de venta + servicios.
        No cuenta abonos, descuento global ni IVA.
        Si precision es != None, redondea los subtotales de línea a esa 
        cantidad de decimales ANTES de hacer la suma total. Debe ser 
        un entero o None.
        """
        #import time
        #antes = time.time()
        # OPTIMIZACIÓN:
        asserterror = "Precision debe ser None o un número entero postivo."
        assert precision == None or (isinstance(precision, int) 
                                     and precision >= 0), asserterror
        try:
            if precision == None:
                total_ldvs = FacturaVenta._connection.queryOne(""" 
                    SELECT SUM(
                        CAST(cantidad * precio * (1-descuento) AS NUMERIC))
                      FROM linea_de_venta
                      WHERE factura_venta_id = %d
                    ;""" % self.id)[0]
            else:
                total_ldvs = FacturaVenta._connection.queryOne(""" 
                    SELECT SUM(ROUND(
                            CAST(cantidad * precio * (1-descuento) AS NUMERIC), 
                            %d))
                      FROM linea_de_venta
                      WHERE factura_venta_id = %d
                    ;""" % (precision, self.id))[0]
            if total_ldvs == None:
                total_ldvs = 0.0
        except IndexError:
            total_ldvs = 0.0
        try:
            if precision == None:
                total_srvs = FacturaVenta._connection.queryOne(""" 
                    SELECT SUM(
                        CAST(cantidad * precio * (1-descuento) AS NUMERIC))
                      FROM servicio      
                      WHERE factura_venta_id = %d
                    ;""" % self.id)[0]
            else:
                total_srvs = FacturaVenta._connection.queryOne(""" 
                    SELECT SUM(ROUND(
                            CAST(cantidad * precio * (1-descuento) AS NUMERIC), 
                            %d)) 
                      FROM servicio      
                      WHERE factura_venta_id = %d
                    ;""" % (precision, self.id))[0]
            if total_srvs == None:
                total_srvs = 0.0
        except IndexError:
            total_srvs = 0.0
        subtotal = float(total_ldvs) + float(total_srvs)
        if incluir_descuento: 
            subtotal += self.calcular_total_descuento(subtotal)
        #_subtotal = subtotal
        #tuno = time.time() - antes
        #print "1.-", tuno 
        #antes = time.time()
        # Código original:
        #total_ldvs = sum([utils.ffloat((l.cantidad * l.precio) * (1 - l.descuento)) for l in self.lineasDeVenta])
        #total_srvs = sum([utils.ffloat((s.precio * s.cantidad) * (1 - s.descuento)) for s in self.servicios])
        #subtotal = total_ldvs + total_srvs
        #if incluir_descuento:
        #    subtotal += self.calcular_total_descuento(subtotal)
        #tdos = time.time() - antes
        #print "2.-", tdos 
        # En las siguientes líneas de venta, la optimización da el resultado 
        # correcto, era el código original el que bailaba un decimal, así que 
        # no comparo
        #if self.id not in (236, 264, 344, 618, 695, 704, 750):
        #    assert _subtotal == subtotal, "\n_subtotal: %s\nsubtotal: %s\nid: %s (%s)" % (_subtotal, subtotal, self.id, self.numfactura)
        #print tuno <= tdos and "                    ---> OK <---" or "                    ---> :( <---"
        return subtotal

    def calcular_base_imponible(self):
        """
        Devuelve la base imponible (subtotal + descuento global + abonos) 
        de la factura.
        """
        base_imponible = self.calcular_subtotal(incluir_descuento = True)
        abonos = sum([pa.importe for pa in self.pagosDeAbono])
        base_imponible += abonos
        return base_imponible

    def get_last_evento(self):
        """
        Devuelve la última nota (por fecha) relacionada con la factura.
        """
        notas = Nota.select(Nota.q.facturaVentaID == self.id, 
                            orderBy = "-fechahora")
        try:
            return notas[0]
        except IndexError:
            return None
 
