#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ajusta las existencias de rollos y balas según inventario de final de septiembre de 2006.

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


def build_inventario(drollos, dbalas):
    """
    Construye el diccionario con el inventario real.
    rollos y balas es diccionario con los productos y 
    una tupla con los NÚMEROS de rollo o bala en cada 
    producto
    """
    inventario = {}
    no_existen = []

    try:
        partida = pclases.Partida.select(pclases.Partida.q.numpartida == -1)[0]
    except IndexError:
        partida = pclases.Partida(numpartida = -1, codigo = "PARTIDA_AJUSTE_10_10_2006")
    for strproducto in drollos:
        for rangorollo in drollos[strproducto]:
            if isinstance(rangorollo, str) and '-' in rangorollo:
                ini, fin = [int(i) for i in rangorollo.split('-')]
#                for nuevo_numrollo in xrange(ini, fin+1):
#                    drollos[strproducto].append(nuevo_numrollo)
            else:
                ini = fin = int(rangorollo)
            for numrollo in xrange(ini, fin+1):
                prod, fam, ancho, largo = strproducto.split(" ")
                prod = "%s %s" % (prod, fam)
                try:
                    producto_se_supone = pclases.ProductoVenta.select(pclases.AND(pclases.ProductoVenta.q.descripcion.contains(prod),
                                                                                  pclases.ProductoVenta.q.descripcion.contains(" %s " % (fam)),
                                                                                  pclases.ProductoVenta.q.descripcion.contains(ancho),
                                                                                  pclases.ProductoVenta.q.descripcion.contains("X%s" % (largo))))
                    if producto_se_supone.count() > 1:
                        print "Hay más de un producto que coincide con %s. Corrige y a empezar de nuevo." % (strproducto)
                        print " --> ", prod, fam, ancho, largo
                        sys.stdout.flush()
                        for p in producto_se_supone:
                            print p.descripcion
                            sys.stdout.flush()
                        sys.exit(1)
                    producto_se_supone = producto_se_supone[0]
                except IndexError:
                    print "%s NO ENCONTRADO. A empezar de nuevo." % (strproducto)
                    sys.stdout.flush()
                    sys.exit(1)

                numrollo = "R%s" % (numrollo)
                try:
                    rollo = pclases.Rollo.select(pclases.Rollo.q.codigo == numrollo)[0]
                except IndexError:
                    print "¡Rollo %s no existe!" % (numrollo),
                    sys.stdout.flush()
#                    sys.exit(0)    # Creo el rollo en el almacén:
                    densidad = producto_se_supone.camposEspecificosRollo.gramos
                    metros_cuadrados = producto_se_supone.camposEspecificosRollo.metros_cuadrados
                    rollo = pclases.Rollo(numrollo = int(numrollo.replace("R", "")), 
                                          codigo = numrollo, 
                                          fechahora = mx.DateTime.localtime(),
                                          observaciones = "Rollo sin parte de producción. Proviene de ajuste existencias 10/10/2006", 
                                          muestra = False, 
                                          peso = (densidad * metros_cuadrados) / 1000.0, 
                                          densidad = densidad,
                                          partida = partida)
                    articulo = pclases.Articulo(productoVenta = producto_se_supone, 
                                                rollo = rollo, 
                                                bala = None,
                                                bigbag = None,
                                                parteDeProduccion = None,
                                                albaranSalida = None)
#                    no_existen.append((numrollo, producto_se_supone))
#                    rollo = None
                    print "... rollo ID %d creado." % (rollo.id)
                    sys.stdout.flush()
                if rollo != None:
                    producto = rollo.articulos[0].productoVenta
                    if producto != producto_se_supone:
                        print "¡%s no coincide con el producto %s del número de rollo %s! A empezar de nuevo." % (strproducto, producto.descripcion, rollo.codigo)
                        sys.stdout.flush()
                        sys.exit(1)
                
                    if producto not in inventario:
                        inventario[producto] = []
                    inventario[producto].append(rollo)
                
    for strproducto in dbalas:
        for numbala in dbalas[strproducto]:
            if isinstance(numbala, str) and '-' in numbala:
                dbalas[strproducto].remove(numbala)
                ini, fin = [int(i) for i in numbala.split('-')]
                for nuevo_numbala in xrange(ini, fin+1):
                    dbalas[strproducto].append(nuevo_numbala)
            else:
                prod, fam, ancho, largo = strproducto.split(" ")
                prod = "%s %s" % (prod, fam)
                # Todo esto, cambiar:
                try:
                    producto_se_supone = pclases.ProductoVenta.select(pclases.AND(pclases.ProductoVenta.q.descripcion.contains(prod),
                                                                                  pclases.ProductoVenta.q.descripcion.contains(" %s " % (fam)),
                                                                                  pclases.ProductoVenta.q.descripcion.contains(ancho),
                                                                                  pclases.ProductoVenta.q.descripcion.contains("X%s" % (largo))))
                    if producto_se_supone.count() > 1:
                        print "Hay más de un producto que coincide con %s. Corrige y a empezar de nuevo." % (strproducto)
                        print " --> ", prod, fam, ancho, largo
                        sys.stdout.flush()
                        for p in producto_se_supone:
                            print p.descripcion
                            sys.stdout.flush()
                        sys.exit(1)
                    producto_se_supone = producto_se_supone[0]
                except IndexError:
                    print "%s NO ENCONTRADO. A empezar de nuevo." % (strproducto)
                    sys.stdout.flush()
                    sys.exit(1)

            numbala = "B%s" % (numbala)
            bala = pclases.Bala.select(pclases.Bala.q.codigo == numbala)[0]
            
            producto = bala.articulos[0].productoVenta
            
            if producto not in inventario:
                inventario[producto] = []
            inventario.append(bala)
            
    return inventario

def duplicar_rollo(rollo):
    # 1.- Cambiar información rollo albaraneado para no crear dos exactamente iguales.
    numrollo = rollo.numrollo
    rollo.numrollo = -rollo.numrollo
    rollo.codigo += "-D"
    rollo.observaciones = "Rectificado por ajuste de existencias 11/10/2006."
    # 2.- Crear nuevo rollo porque debe constar en almacén según EXCEL.
    nuevo_rollo = pclases.Rollo(partida = rollo.partida, numrollo = numrollo, codigo = "R%d" % (numrollo), fechahora = mx.DateTime.localtime(), observaciones = "Creado por ajuste de existencias 11/10/2006 a partir de uno existente y albaraneado antes del 1/10/2006.", muestra = False, peso = rollo.peso, densidad = rollo.densidad)
    # 3.- Crear artículo que relaciona rollo con producto de venta.
    articulo = pclases.Articulo(productoVenta = rollo.articulos[0].productoVenta, bigbag = None, bala = None, rollo = nuevo_rollo, parteDeProduccion = None, albaranSalida = None)


# ROLLOS -------------------------------------------------
global rollos
rollos = {'NT 11 2.75 100': ['82413-82492', '83486-83641'],
          'NT 11 5.5 100': ['34555-34558', '34570-34584', 34589, 34599, 34600, 34610, '75281-75303', '77915-77919',
                            '80646-80691'],
          'NT 12 2.75 100': ['85325-85486', ],
          'NT 12 5.5 100': [30688, 30698, 30700, 30701, 30704, 30710, 30711, 30712, 30715, 35515, 35516, 35519, '64113-64115', 
                            '64117-64146', '78024-78067', '78079-78085', 78090, 78091, 78093, 78095, 78096],
          'NT 13 2.75 100': ['73137-73174', 73180, 73181], 
          'NT 13 5.5 100': ['79746-79755', ],
          'NT 13B 2.3 900': ['80908-80933', 75219, 75220], 
          'NT 14 2.2 600': [63947, ],
          'NT 15 2.75 100': [78262, '78277-78280', '82619-82726', '85173-85235'],
          'NT 15 5.5 100': ['44266-44272', '82770-82814', '85129-85172'],
          'NT 15 2.1 100': ['85062-85099'],
          'NT 17 2.75 100': [80270, 80271, '85547-85786'], 
          'NT 17 5.5 100': ['78445-78536', '78576-78577', '79390-79420', '79483-79511', '79549-79626'],
          'NT 17 4.0 100': [69016, '69024-69052', '81243-81298'], 
          'NT 18 2.75 100': [42227, '84081-84192'], 
          'NT 18 5.5 100': ['63065-63071', '71140-71177', 71191, 71195, '72755-72762', '81964-82040', '82077-82101'], 
          'NT 18 4.0 100': ['44863-44882', '44907-44910', '44926-44927'], 
          'NT 18 2.5 500': [3552, 3554, 3556, 3564, 3566, 3568, 3570], 
          'NT 18 3.0 500': ['3559-3563'], 
          'NT 18 2.1 600': ['27411-27432'], 
          'NT 21 5.5 100': [4238, 4291, '81462-81492'], 
          'NT 22 5.5 100': [25292, 25293], 
          'NT 23 5.5 100': ['44779-44784', '45319-45327', '45329-45335', '45337-45342', '45344-45353', '45355-45357', '45359-45360', 45362, '45589-45608', '60876-60877', '61575-61620', '61939-61941', 62074, 
                            62088, 62194, 62195, 62200, 62201, 62220, 62743, '62876-62878', '62880-62882', '65350-65357', 
                            65360, 65362, 65363, 65364, 65367, 65368, 65369, 65370, 65372, 65373, 65377, 65378, 65379, 65382, 
                            69755, 69756, 71047, '71092-71137', '76245-76251', '76256-76265', '79345-79370', '79380-79382', 
                            '79387-79389', '79958-79994', '79998-80019', '80402-80407', '80415-80416', 80424, '80426-80430', 80442, '82300-82339', 
                            82342, 82345, 82346, 82348, '82353-82370', '82727-82763', '82830-82917', '82919-83006'], 
          
          'NT 200 5.30 350': [70262, '72127-70133', '72136-72137', 75037, 75066, 75072, 75073, '75075-75077', '75081-75087', 
                              '76859-76861', '76863-76865', 76885, 76896, 80843, 80844, 80848, 80853, 80854, 80855, 80856, 80857, 
                              '80868-80881', 80934, 80935, 80938, 80939, 80948, 80949, 80950, 80970, 80973, '83340-83459'],
          'NT 23 2.75 100': ['83007-83036'], 
          'NT 24 5.5 100': ['74106-74111', '74114-74121'],
          'NT 25 5.5 90': [71857, '81196-81228'], 
          'NT 30 5.5 90': ['69353-69376', '70571-70593', '77417-77494', 78952, 78953, '80120-80150', '83136-83173', '83642-83666', 83682, 
                           '84041-84080'], 
          'NT 30 2.75 90': ['43251-43257'], 
          'NT 35 4.2 80': ['84952-85041'], 
          'NT 35 5.5 80': [62553, 62554, '72497-72525', 74219, '76357-76360', '77565-77567', '77662-77680', '79227-79261', '80195-80232', 
                           '84275-84306', 84329, '84801-84951'], 
          'NT 40 5.5 70': [76432, 76433, 76562, 80692, '81512-81583', 81598, '81620-81656', '84687-84800'], 
          'NT 46 5.5 60': ['61438-61450', '68039-68055', '77761-77771', '77775-77781', 77787, '77789-77791', '77793-77827'], 
          'NT 46 2.75 60': ['38598-38602'], 
          'NT 58 5.5 50': [30955, 81744, 81748, 81749, '81751-81754', '84330-84365', '84364-84381'], 
          'NT 90 5.5 20': ['14861-14868'], 
          'NT 80 5.5 50': [14844, '14858-14860', '14845-14851'], 
          'NT 80 5.5 20': ['84576-84686', '74865-74900', 76614, 76615, 81788, 81789, 81790], 
          'NT 69 5.5 40': [74359, '84402-84420', '84536-84575'], 
          'NT 300 5.5 60': ['40459-40478']
         }

# ¡TIENE QUE QUEDAR TAL Y COMO EL INVENTARIO (QUITANDO LO QUE SE HAYA PRODUCIDO Y VENDIDO CON POSTERIORIDAD AL 30/09/2006)!

# BALAS --------------------------------------------------
global balas
balas = {}


if __name__=="__main__":
    print "Se va a proceder a ajustar las existencias de rollos y balas en almacén.\n¿Está seguro? (S/N)"
    if raw_input() == "S":
        print "A partir de ahora, la salida se puede ver con tail -f /tmp/ajuste_existencias.log"
        sys.stdout = open("/tmp/ajuste_existencias.log", "w")
#        print rollos, balas
        inventario = build_inventario(rollos, balas)
#        print inventario
        print "Construyendo inventario..."
        sys.stdout.flush()
        print " --> Total rollos en inventario: %d" % (sum([len(inventario[p]) for p in inventario]))
        sys.stdout.flush()
        en_almacen_en_excel_pero_en_albaran_en_programa = []
        for producto in inventario:
            print producto.descripcion, len(inventario[producto]) 
            sys.stdout.flush()
            if producto.es_rollo():
                for rollo in inventario[producto]:
                    if rollo.articulos[0].albaranSalida == None:
                        print "Rollo %s en almacén excel y en almacén ginn. [OK]" % (rollo.codigo)
                        sys.stdout.flush()
                    elif rollo.articulos[0].albaranSalida.fecha > mx.DateTime.DateTimeFrom(day = 30, month = 9, year = 2006):
                        print "Rollo %s en almacén excel y en albarán posterior a 30 de septiembre en ginn. [OK]" % (rollo.codigo)
                        sys.stdout.flush()
                    else:
                        print "Rollo %s en almacén excel pero en albarán anterior a 30 de septiembre en ginn. [KO]" % (rollo.codigo)
                        sys.stdout.flush()
                        en_almacen_en_excel_pero_en_albaran_en_programa.append(rollo)
            elif producto.es_bala():
                pass

        
        # Buscar los que están en almacén pero no en la hoja para asignarlos a un albarán ficticio, a no ser que la 
        # fecha de fabricación sea superior al 30 de septiembre de 2006.
        print "ROLLOS EN ALMACÉN EN GINN PERO ALBARANEADOS EN EXCEL"
        sys.stdout.flush()
        rollos_en_almacen = pclases.Rollo.select(""" rollo.id IN (SELECT rollo_id FROM articulo WHERE rollo_id IS NOT NULL and albaran_salida_id IS NULL) """)
        if rollos_en_almacen.count() > 0:
            cliente = pclases.Cliente.select(pclases.Cliente.q.nombre.contains('texan'))[0]
            albaran = pclases.AlbaranSalida(cliente = cliente, 
                                            transportista = None, 
                                            numalbaran = 'A_AJUSTE', 
                                            fecha = mx.DateTime.localtime(), 
                                            observaciones = 'Albarán "ficticio" de ajuste de existencias.',
                                            facturable = False, 
                                            motivo = "Albarán de ajuste.", 
                                            bloqueado = True)
        for rollo in rollos_en_almacen:
            producto = rollo.articulos[0].productoVenta
            # Si el rollo no tiene parte de producción (porque se acaba de añadir o procede del ajuste de febrero) pero la fecha de 
            # fabricación es anterior al 1 de octubre;
            # o bien, tiene parte de producción, es anterior al 1 de octubre y no está en el inventario.
            fecha_inventario = mx.DateTime.DateTimeFrom(day = 1, month = 10, year = 2006)
            if (not rollo.articulos[0].parteDeProduccion and rollo.articulos[0].fechahora < fecha_inventario) \
               or ((rollo.articulos[0].parteDeProduccion and rollo.articulos[0].parteDeProduccion.fecha < fecha_inventario) \
               and (producto not in inventario or rollo not in inventario[producto])):
                print "Añado a albarán ficticio: %s->rollo %s" % (producto.descripcion, rollo.codigo)
                sys.stdout.flush()
                # Creo LDV si no existe e incremento la cantidad en los m² del rollo.
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
                ldv.cantidad += producto.camposEspecificosRollo.metros_cuadrados
                # Relaciono el rollo con el albarán.
                rollo.articulos[0].albaranSalida = albaran
        print "ROLLOS EN ALMACÉN EN EXCEL PERO ALBARANEADOS EN GINN:"
        sys.stdout.flush()
        for rollo in en_almacen_en_excel_pero_en_albaran_en_programa:
            print "Rollo %s; Albarán %s" % (rollo.numrollo, rollo.articulos[0].albaranSalida.numalbaran),
            fecha_inventario = mx.DateTime.DateTimeFrom(day = 1, month = 10, year = 2006)
            if rollo.articulos[0].albaranSalida.fecha >= fecha_inventario:
                print "El albarán es posterior. [OK]"
            else:
                duplicar_rollo(rollo)
                print "Rollo %s duplicado con éxito [OK]" % (rollo.codigo)
            sys.stdout.flush()

        sys.stdout.close()

