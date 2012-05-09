#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ajusta las existencias de balas según inventario de final de septiembre de 2006.

Para ello:
    Recorre todos los rollos y balas fabricados que no tengan albarán de salida (es decir, que 
    estén en almacén).

    Si el rollo/bala NO ESTÁ en la lista de los que se suponen que deben estar, se anotan 
    para agregar a un albarán "ficticio" de ajuste para sacarlo del almacén y lo elimina del 
    listado del inventario.

    Una vez ha finalizado la primera fase, examina los artículos que han quedado en la lista 
    del inventario "real". Para cada uno de ellos se mira la fecha del albarán de salida.
    Si es posterior al 30 de septiembre, se eliminan también de la lista, puesto que han salido
    del almacén.

    Finalmente imprime los rollos que se suponen que están en almacén pero no lo están según 
    el inventario y los que están en el inventario real pero que en el programa dice que han 
    salido.

"""

import sys, os
sys.path.append('../framework')

import pclases
import mx, mx.DateTime
sys.path.append('../formularios')
import utils

uno_octubre = mx.DateTime.DateTimeFrom(day = 1, month = 10, year = 2006)

def leer_fichero_balas(fichero):
    """
    Lee los números de bala y producto del fichero indicado.
    """
    balas = []
    import re
    reprod = re.compile("^1.*[A-C]\d\d")
    f = open(fichero)
    lote_actual = None
    for linea in f.readlines():
        stuffs = linea.split()
        if len(stuffs) == 0:
            continue
        if len(stuffs) == 1:    # Producto.
            # solo por asegurarme
            strproducto = stuffs[0]
#            print strproducto, stuffs
            strproducto = reprod.findall(strproducto)[0]
            if len(strproducto) != 8:
                print "PRODUCTO IRRECONOCIBLE."
                sys.exit(1)
            material = strproducto[0]
            dtex = strproducto[1:3]
            corte = strproducto[3:5]
            calidad = strproducto[5]
            color = strproducto[6]
            antiuvi = strproducto[7]
            producto = buscar_producto(material, dtex, corte, calidad, color, antiuvi)
            peso_producto = 0.0
            balas_producto = 0
#            balas[producto] = []
            lote_actual = None
            continue
        elif len(stuffs) == 2:    # Nº Bala y peso.
            try:
                numbala = int(stuffs[0])
                peso = utils._float(stuffs[1])
            except ValueError, msg:
                print msg, stuffs, linea
                sys.exit(-1)
            if numbala < 10000:     # Es suma de comprobación
                if numbala == balas_producto:
                    print "%d balas de %s (%s), OK" % (balas_producto, strproducto, producto.descripcion)
                else:
                    print "%d != %d balas de %s (%s), KO" % (numbala, balas_producto, strproducto, producto.descripcion)
                if numbala == balas_producto:
                    print "%d kilos de %s (%s), OK" % (peso_producto, strproducto, producto.descripcion)
                else:
                    print "%d != %d kilos de %s (%s), KO" % (peso, peso_producto, strproducto, producto.descripcion)
                peso_producto = 0.0
                balas_producto = 0
            else:
                bala = comprobar_bala(numbala, peso, producto, calidad, lote_actual)
                if bala != None:
                    print "... Añadiendo bala %s a lista de balas de inventario." % (bala.codigo)
                    balas.append(bala)      # No la cuento para el albarán ficticio, PERO SÍ PARA LA SUMA DE COMPROBACIÓN.
                peso_producto += peso
                balas_producto += 1
        elif len(stuffs) == 4:    # Nº Bala, peso, "Lote" y numlote.
            numbala = int(stuffs[0])
            peso = utils._float(stuffs[1])
            lote = int(stuffs[3])
#            print "        --------------- lote: ", lote
            bala = comprobar_bala(numbala, peso, producto, calidad, lote)
            if bala != None:
                print "... Añadiendo bala %s a lista de balas de inventario." % (bala.codigo)
            balas.append(bala)      # No la cuento para el albarán ficticio, PERO SÍ PARA LA SUMA DE COMPROBACIÓN.
            peso_producto += peso
            balas_producto += 1
        else:
            print "ERROR PARSEANDO:\n%s" % (" ".join(stuffs))
            sys.exit(2)
    f.close()
    return balas

def comprobar_bala(numbala, peso, producto, calidad, lote = None):
    """
    Comprueba si la bala existe en almacén y coincide el peso, 
    producto.
    Si no coincide, muestra un error y cancela la actualización.
    Si coincide, y está en almacén (esto es, no albarán salida y 
    no usada en partida para fabricar rollos), se pasa a chequear el lote.
    Si coincide pero no está en almacén (ya se ha usado para vender 
    o para fabricar), se duplica la bala, a la usada se le marca como
    duplicada y a la nueva se le asigna el numbala y fecha fabricación 
    el localtime().
    Si no existe, se crea la bala y:
        - Si lote == None, se busca o se crea un lote de esas caracaterísticas que 
          contenga la palabra "AJUSTE_OCT06" en el código y un número 
          negativo de lote (el menor disponible).
        - Si lote != None, se busca ese lote en la BD.
            * Si el lote no se encuentra, se crea.
            * Si se encuentra pero no es de ese producto, se cancela todo y se sale del programa.
            * Si se encuentra y es de ese producto, se comprueba que el lote 
              coincide con la calidad especificada.
    """
    bala_none = False
    B = pclases.Bala
    balas = B.select(B.q.numbala == numbala)
    if calidad == "C": 
        calidad = "B"
        marcar_b = True
    else:
        marcar_b = False
    if balas.count() > 1:
        print "ERROR. %d balas duplicadas:" % (balas.count())
        for b in balas:
            print b.id, b.numbala, b.codigo
        sys.exit(5)
    elif balas.count() == 1:        # La bala existe.
        bala = balas[0]
        print "Comprobando bala %s..." % (bala.codigo)
        if bala.pesobala != peso:
            print "WARNING: Peso %f no coincide con el peso de la bala %d: %f. Machaco a peso EXCEL." % (peso, bala.numbala, bala.pesobala)
            bala.pesobala = peso
        if (bala.articulos[0].albaranSalidaID != None and bala.articulos[0].albaranSalida.fecha < uno_octubre) \
            or (bala.partidaID != None \
               and (bala.partida.rollos[0].articulos[0].parteDeProduccion and bala.partida.rollos[0].articulos[0].parteDeProduccion.fecha < uno_octubre or bala.partida.numpartida < 1177)):
            print "La bala %d no está en almacén y se empleó antes del 1 de octubre: albarán %s, partida %s. Se duplica." \
                % (bala.numbala, bala.articulos[0].albaranSalida and bala.articulos[0].albaranSalida.numalbaran or "-", bala.partida and bala.partida.numpartida or "-")
            bala = duplicar_bala(bala)
        else:
            "La bala está en almacén o se empleó después del 1 de octubre."
            if bala.articulos[0].albaranSalidaID != None:
                print "Bala %s no está en almacén, pero se vendió en albarán %s con fecha %s. OK" % (bala.codigo, bala.articulos[0].albaranSalida.numalbaran, utils.str_fecha(bala.articulos[0].albaranSalida.fecha))
            if bala.partidaID != None:
                if bala.partida.rollos[0].articulos[0].parteDeProduccion:
                    print "Bala %s no está en almacén, pero se empleó en la partida %s con producción en fecha %s (parte de producción ID %d). OK" % (bala.codigo, bala.partida.codigo, utils.str_fecha(bala.partida.rollos[0].articulos[0].parteDeProduccion.fecha), bala.partida.rollos[0].articulos[0].parteDeProduccion.id)
                else:
                    print "Bala %s no está en almacén, pero se empleó en la partida %s. (La 1º de octubre es la 1177.) OK" % (bala.codigo, bala.partida.codigo)
#            bala_none = True   # Hay que meterla siempre en el inventario Excel porque ya se ha tratado, tanto si se duplica (está en Excel y no en Ginn) como si no, (está en Excel y no en Ginn pero gastada después del 1 de octubre O está en Excel y en Ginn y es correcto -no hay que meterla en el albarán ficticio-).
#        print lote
        if lote == None:    # Si en EXCEL no tiene lote, uso el lote de la bala de la base de datos.
            lote = bala.lote.numlote
        lotebd = comprobar_lote(lote, calidad, producto)
#        print lote, lotebd.numlote
        if bala.claseb and not marcar_b:
            print "WARNING: La bala %d (ID %d) es clase B: %s. En EXCEL dice que es clase B: %s..." % (bala.numbala, bala.id, bala.claseb, marcar_b),
            if marcar_b:
                print "Marco como BAJA CALIDAD."
                bala.claseb = True
                bala.motivo = "Marcada como baja calidad por ajuste existencias Octubre 06"
            else:
                print "Dejo como está."
        if lote == None:    # No tenía lote. Asigno la bala al lote de la BD (que estará recién creado)
            bala.lote = lotebd
            bala.sync()
        elif lote != bala.lote.numlote:
            print "ERROR: El lote de la BD %d de la bala %d no coincide con %d. ¿Ahora qué?" % (lotebd.numlote, bala.numbala, lote)
            sys.exit(6)
        if bala_none:
            bala = None     # La bala es del inventario de septiembre, pero no está en el almacén. No la cuento como que debería estar
                            # a la hora de hacer el albarán ficticio. La pongo a None una vez he chequeado el lote y tal.
    else:
        print "BALA %d NO EXISTE. LA CREO." % (numbala)
        nueva_bala = pclases.Bala(partida = None, 
                                  lote = None, 
                                  numbala = numbala, 
                                  codigo = "B%d" % (numbala),
                                  pesobala = peso,
                                  fechahora = mx.DateTime.localtime(),
                                  muestra = None, 
                                  claseb = marcar_b, 
                                  motivo = marcar_b and "Creada como baja calidad en ajuste existencias Oct06.")
        articulo = pclases.Articulo(productoVenta = producto,
                                    bigbag = None,
                                    bala = nueva_bala,
                                    rollo = None,
                                    parteDeProduccion = None,
                                    albaranSalida = None)
        lotebd = comprobar_lote(lote, calidad, producto)
        nueva_bala.lote = lotebd
        print "WARNING: Bala %s creada en lote %s." % (nueva_bala.codigo, lotebd.codigo)
        bala = nueva_bala
    return bala

def duplicar_bala(bala):
    """
    Duplica la bala recibida. La nueva (que constará 
    en almacén) conservará el número.
    La antigua se marcará con número de bala negativo (*-1)
    y "-D" en el código.
    """
    numbala = bala.numbala
    bala.numbala = -bala.numbala
    bala.codigo += "-D"
    bala.observaciones = "Rectificado por ajuste de existencias 19/10/2006."
    nueva_bala = pclases.Bala(partida = None, 
                              lote = bala.lote, 
                              numbala = numbala, 
                              codigo = "B%d" % (numbala),
                              pesobala = bala.pesobala,
                              fechahora = mx.DateTime.localtime(),
                              muestra = bala.muestra, 
                              claseb = bala.claseb, 
                              motivo = bala.motivo)
    articulo = pclases.Articulo(productoVenta = bala.articulos[0].productoVenta,
                                bigbag = None,
                                bala = nueva_bala,
                                rollo = None,
                                parteDeProduccion = None,
                                albaranSalida = None)
    print "Bala %d duplicada: %s (%d) y %s (%d)." % (numbala, bala.codigo, bala.id, nueva_bala.codigo, nueva_bala.id)
    return nueva_bala       # La nueva es la que pertenece al inventario. La antigua es la que se queda albaraneada.

def comprobar_lote(lote, calidad, producto):
    """
    Comprueba que el lote recibido existe en la BD
    con la calidad y el producto recibido.
    Si no existe, lo crea.
    Si existe pero algo no coincide, avisa y sale 
    del script (de momento).
    """
    L = pclases.Lote
    if lote != None:
        lotes = L.select(L.q.numlote == lote)
        if lotes.count() > 1:
            print "ERROR. %d lotes duplicados:" % (lotes.count())
            for l in lotes:
                print l.id, l.numlote, l.codigo
            sys.exit(5)
        elif lotes.count() == 1:
            lote = lotes[0]
            if lote.numlote > 0 and lote.balas[0].articulos[0].productoVenta != producto:
                # Si es un lote < 0, es especial (de ajuste y recién creado, seguramente).
                print "WARNING: Producto del lote %d (%s) no coincide con %s." % (lote.numlote, lote.balas[0].articulos[0].productoVenta.descripcion, producto.descripcion)
                if calidad == "B":
                    print "         Falsa alarma. La bala es de baja calidad y en Excel se mezclan colores."
                else:
                    print "         BALA QUEDARÁ MARCADA EN UN PRODUCTO INCORRECTO. REPASAR A MANO (probablemente haya que cambiarla de parte de producción)."
#                    sys.exit(5)
            else:
                if calidad != lote.tenacidad:
                    print "WARNING: La tenacidad no coincide. ID Lote: %d, numlote %d, tenacidad %s, calidad %s" % (lote.id, lote.numlote, lote.tenacidad, calidad)
                    lote.tenacidad = calidad.upper()
                    print "Machaco tenacidad a %s." % (lote.tenacidad)
        else:
            print "ERROR. Lote %d no existe. Lo creo." % (lote)
            lote = L(numlote = lote, codigo = "LOTE_AJUSTE_OCT06(%s)" % (lote), tenacidad = calidad, elongacion = calidad, rizo = 6, encogimiento = calidad, grasa = 0.0, tolerancia = 0.2, mediatitulo = 0.0)
    else:   # No sabemos el lote.
        print "\tNo sabemos el lote. Hay que crear uno con número negativo o buscar uno de ajuste, con calidad %s. Todas las balas que compartan calidad compartirán lote, da igual del producto que sean." % (calidad)
        lotes = pclases.Lote.select(pclases.AND(pclases.Lote.q.numlote < 0, 
                                                pclases.Lote.q.tenacidad == calidad, 
                                                pclases.Lote.q.codigo.contains("OCT06")))
        if lotes.count() == 0:
            minlote = pclases.Lote._connection.queryOne(""" SELECT MIN(numlote) FROM lote """)[0]
            if minlote < 0:
                numlote = minlote - 1
            else:
                numlote = -1
            lote = L(numlote = numlote, codigo = "LOTE_AJUSTE_OCT06(%s)" % (numlote), tenacidad = calidad, elongacion = calidad, rizo = 6, encogimiento = calidad, grasa = 0.0, tolerancia = 0.2, mediatitulo = 0.0)
            print "\t --> Lote %d creado." % (lote.numlote)
        else:
            lote = lotes[0]
            print "\t --> Lote %d encontrado." % (lote.numlote)
    return lote


def buscar_producto(material, dtex, corte, calidad, color, antiuvi):
    """
    Busca un producto que reúna las 
    características recibidas.
    """
    dtex = "%s.%s" % (dtex[0], dtex[1])
    descripcion = "%s/%s" % (dtex, corte)
    if color == "3":
        producto = pclases.ProductoVenta.select(pclases.AND(pclases.ProductoVenta.q.descripcion.contains(descripcion),
                                                            pclases.OR(pclases.ProductoVenta.q.descripcion.contains("EGR"), 
                                                                       pclases.ProductoVenta.q.descripcion.contains("egr")),
                                                            pclases.NOT(pclases.ProductoVenta.q.descripcion.contains("BONAR"))
                                                           )
                                               )
    elif color == "1" or color == "2":
        producto = pclases.ProductoVenta.select(pclases.AND(pclases.ProductoVenta.q.descripcion.contains(descripcion), 
                                                            pclases.NOT (pclases.OR(pclases.ProductoVenta.q.descripcion.contains("EGR"), 
                                                                                    pclases.ProductoVenta.q.descripcion.contains("egr"),
                                                                                   ) 
                                                                        ),
                                                            pclases.NOT(pclases.ProductoVenta.q.descripcion.contains("BONAR"))
                                                           )
                                               )
    else:
        print "ERROR COLOR %s." % (color)
        sys.exit(3)
    if producto.count() > 1:
        print "Más de uno. Refinar material: %s; dtex: %s; corte: %s; calidad: %s; color: %s; antiuvi: %s" % (material, dtex, corte, calidad, color, antiuvi)
        for p in producto:
            print p.id, p.descripcion
        sys.exit(4)
    else:
        return producto[0]

def calcular_producido(producto):
    """
    Devuelve una tupla con la cantidad en kilos como cadena, bultos como cadena,
    cantidad en kilos como flotante y bultos como entero de material producido 
    a partir del 1 de octubre del producto recibido.
    """
    # DA IGUAL LOS LOTES O SI SON BALAS B. Tener en cuenta después para comparar con el Excel y ver si cuadra, que allí sí se separan las "C".
    uno_oct = mx.DateTime.DateTimeFrom(day = 1, month = 10, year = 2006)
    PDPs = pclases.ParteDeProduccion.select(pclases.ParteDeProduccion.q.fecha >= uno_oct)
    # No estamos para florituras. Ya habrá tiempo de optimizar (no creo, se va a usar una vez únicamente, da igual que tarde 2 horas).
    PDPs = [p for p in PDPs if p.es_de_balas() and p.articulos!=[] and p.articulos[0].productoVenta == producto]
    peso = 0
    balas = 0
    for parte in PDPs:
        balas += len(parte.articulos)
        for a in parte.articulos:
            try:
                peso += a.bala.pesobala
            except AttributeError, msg:
                print "EXCEPCIÓN con bala %d: %s" % (bala.id, msg)
    return ("%s kg" % (utils.float2str(peso)), "%d balas" % (balas), peso, balas)

def calcular_vendido(producto):
    """
    Devuelve una tupla con la cantidad en kilos como cadena, bultos como cadena,
    cantidad en kilos como flotante y bultos como entero de material vendido 
    a partir del 1 de octubre del producto recibido.
    """
    uno_oct = mx.DateTime.DateTimeFrom(day = 1, month = 10, year = 2006)
    albs = pclases.AlbaranSalida.select(pclases.AND(pclases.AlbaranSalida.q.fecha >= uno_oct, 
                                                    pclases.NOT(pclases.AlbaranSalida.q.numalbaran.contains("AJUSTE"))
                                                    ))
    peso = 0
    balas = 0
    for a in albs:
        for bala in [articulo.bala for articulo in a.articulos if articulo.productoVenta == producto]:
            try:
                peso += bala.pesobala
                balas += 1
            except AttributeError, msg:
                print "EXCEPCIÓN con bala %d: %s" % (bala.id, msg)
    return ("%s kg" % (utils.float2str(peso)), "%d balas" % (balas), peso, balas)
            
def calcular_consumido(producto):
    """
    Devuelve una tupla con la cantidad en kilos como cadena, bultos como cadena,
    cantidad en kilos como flotante y bultos como entero de material consumido 
    a partir del 1 de octubre del producto recibido.
    """
    uno_oct = mx.DateTime.DateTimeFrom(day = 1, month = 10, year = 2006)
    PDPs = pclases.ParteDeProduccion.select(pclases.ParteDeProduccion.q.fecha >= uno_oct)
    # No estamos para florituras. Ya habrá tiempo de optimizar (no creo, se va a usar una vez únicamente, da igual que tarde 2 horas).
    PDPs = [p for p in PDPs if p.es_de_rollos()]
    partidas = []
    for pdp in PDPs:
        if pdp.articulos != []:
            if pdp.articulos[0].rollo.partida not in partidas:
                partidas.append(pdp.articulos[0].rollo.partida)
    for partida in pclases.Partida.select(pclases.Partida.q.numpartida >= 1177):
        if partida not in partidas:
            partidas.append(partida)
    peso = 0
    balas = 0
    for partida in partidas:
        for bala in [bala for bala in partida.balas if bala.articulos[0].productoVenta == producto]:
            try:
                peso += bala.pesobala
                balas += 1
            except AttributeError, msg:
                print "EXCEPCIÓN con bala %d: %s" % (bala.id, msg)
    return ("%s kg" % (utils.float2str(peso)), "%d balas" % (balas), peso, balas)

def calcular_almacen_30sept(producto, producido, vendido, consumido):
    """
    Devuelve una tupla con la cantidad en kilos y bultos como cadena 
    de producto en almacén menos lo consumido, menos lo vendido y 
    más lo producido.
    """
    uno_oct = mx.DateTime.DateTimeFrom(day = 1, month = 10, year = 2006)
    peso = producto.get_stock() - producido[2] + vendido[2] + consumido[2]
    balas = producto.get_existencias() - producido[3] + vendido[3] + consumido[3]
    return ("%s kg" % (utils.float2str(peso)), "%d balas" % (balas), peso, balas)


if __name__=="__main__":
    print "Se va a proceder a ajustar las existencias de balas en almacén.\n¿Está seguro? (S/N)"
    if raw_input() == "S":
        print "A partir de ahora, la salida se puede ver con tail -f /tmp/ajuste_existencias_balas.log"
        sys.stdout = open("/tmp/ajuste_existencias_balas.log", "w")
        print "-" * 80
        balas = leer_fichero_balas('inventario_fibra.txt')
        print "-" * 80
        print "COMPROBANDO BALAS QUE ESTÁN EN GINN PERO NO EN EXCEL."
        # ¡PEDAZO DE CAZURRO! ¡ANIMAL! SE TE HABÍA OLVIDADO FILTRAR LAS QUE SE FABRICARON DESPUÉS DEL 1 DE OCTUBRE
        albaran = pclases.AlbaranSalida.select(pclases.AlbaranSalida.q.numalbaran == 'A_AJUSTE')[0]
        print balas, len(balas)
        print pclases.Bala.select(""" bala.id IN (SELECT bala_id FROM articulo WHERE bala_id IS NOT NULL AND albaran_salida_id IS NULL)
                                            AND bala.partida_id IS NULL """).count()
        for bala in pclases.Bala.select(""" bala.id IN (SELECT bala_id FROM articulo WHERE bala_id IS NOT NULL AND albaran_salida_id IS NULL)
                                            AND bala.partida_id IS NULL """):
            if bala not in balas:
                print "Añadiendo bala %s (%d) a albarán de ajuste." % (bala.codigo, bala.id)
                producto = bala.articulos[0].productoVenta
                if producto not in [ldv.productoVenta for ldv in albaran.lineasDeVenta]:
                    ldv = pclases.LineaDeVenta(pedidoVenta = None,
                                               facturaVenta = None,
                                               productoVenta = producto,
                                               albaranSalida = albaran,
                                               fechahora = mx.DateTime.localtime(),
                                               cantidad = 0,
                                               precio = 0,
                                               descuento = 0)
                ldv = [ldv for ldv in albaran.lineasDeVenta if ldv.productoVenta == producto][0]
                ldv.cantidad += bala.pesobala
                bala.articulos[0].albaranSalida = albaran
        for producto in [p for p in pclases.ProductoVenta.select(pclases.ProductoVenta.q.camposEspecificosBalaID != None) if p.es_bala()]:
            producido = calcular_producido(producto)
            vendido = calcular_vendido(producto)
            consumido = calcular_consumido(producto)
            almacen_30sept = calcular_almacen_30sept(producto, producido, vendido, consumido)
            print
            print
            print "RESUMEN PRODUCTO %s:" % (producto.descripcion)
            print "\tEn almacén ahora mismo: %s %s" % (producto.get_str_stock(), producto.get_str_existencias())
            print "\tProducido a partir del 1 de octubre: %s %s" % (producido[:2])
            print "\tVendido a partir del 1 de octubre: %s %s" % (vendido[:2])
            print "\tConsumido a partir del 1 de octubre: %s %s" % (consumido[:2])
            print "\tEn almacén al 30 de septiembre: %s %s" % (almacen_30sept[:2])

    print "EOF"



